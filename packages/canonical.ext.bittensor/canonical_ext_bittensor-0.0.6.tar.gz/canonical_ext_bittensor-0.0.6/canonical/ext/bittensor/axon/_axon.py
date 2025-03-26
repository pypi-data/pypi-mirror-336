# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import threading
import os
from typing import cast
from typing import Any
from typing import Iterable
from typing import Literal
from typing import TYPE_CHECKING

import bittensor
import fastapi
from libcanonical.bases import StateLogger
from uvicorn import Server
from uvicorn import Config

from canonical.ext.bittensor.bases import BaseSoma
from canonical.ext.bittensor.models import Hotkey
from canonical.ext.bittensor.models import HotkeySet
from canonical.ext.bittensor.models import SynapseEnvelope
from ._apiroute import SynapseRouteHandler
from ._request import SynapseRequest
from ._router import SynapseRouter
if TYPE_CHECKING:
    from .._metagraph import Metagraph


AuthorizationFailureReason = Literal[
    'SIGNATURE_INVALID',
    'UNREGISTERED_NEURON',
    'INSUFFICIENT_STAKE'
]



class Axon(threading.Thread, StateLogger):
    __module__: str = 'canonical.ext.bittensor'
    allow_unregistered: bool = False
    force_validator_permit: bool = True
    min_stake: float = 4096.0
    soma: 'BaseSoma[Any]'

    def __init__(
        self,
        soma: 'BaseSoma[Any]',
        metagraph: 'Metagraph',
        hotkeys: list[Hotkey],
        host: str,
        port: int,
        synapse_types: Iterable[type[bittensor.Synapse]] | None = None,
        allow_unregistered: bool = False,
        force_validator_permit: bool = True,
        min_stake: float = 4096.0,
    ):
        super().__init__(
            daemon=True,
            target=self.main_event_loop
        )
        self.app = fastapi.FastAPI()
        self.allow_unregistered = allow_unregistered
        self.force_validator_permit  = force_validator_permit
        self.host = host
        self.port = port
        self.metagraph = metagraph
        self.hotkeys = HotkeySet(items={h.ss58_address: h for h in hotkeys})
        self.min_stake = min_stake
        self.running = threading.Event()
        self.soma = soma
        self.synapse_types = list(synapse_types or [])
        for synapse_class in self.synapse_types:
            self.attach(synapse_class)

    async def authorize(self, request: fastapi.Request, fatal: bool = True) -> bool:
        """Authorizes a :class:`~canonical.ext.bittensor.axon.SynapseRequest`."""
        request = cast(SynapseRequest[Any], request)
        conditions: list[AuthorizationFailureReason] = []

        # Verify the signature first.
        if not request.verify():
            conditions.append('SIGNATURE_INVALID')

        validator = self.metagraph.neuron(
            request.validator_hotkey,
            validator_permit=self.force_validator_permit
        )
        if not validator.is_registered() and not self.allow_unregistered:
            conditions.append('UNREGISTERED_NEURON')

        if (validator.stake < self.min_stake) and not self.allow_unregistered:
            # Unregistered neurons are assumed to never have stake in a
            # subnet.
            conditions.append('INSUFFICIENT_STAKE')

        for condition in conditions:
            match condition:
                case 'SIGNATURE_INVALID':
                    request.log(
                        'CRITICAL', "Signature did not validate (hotkey: %s)",
                        request.validator_hotkey
                    )
                case 'UNREGISTERED_NEURON':
                    request.log(
                        'CRITICAL', "Signer is not registered as a validator (hotkey: %s)",
                        request.validator_hotkey
                    )
                case 'INSUFFICIENT_STAKE':
                    request.log(
                        'CRITICAL', "Validator does not have sufficient stake (uid: %s)",
                        validator.uid
                    )

        if bool(conditions) and fatal:
            raise fastapi.HTTPException(
                status_code=403
            )

        return not bool(conditions)

    def attach(self, synapse_class: type[bittensor.Synapse]):
        """Exposes an endpoint to handle a synapse of the given class."""
        self.logger.info(
            "Accepting %s at http://%s:%s/%s",
            synapse_class.__name__,
            self.host,
            self.port,
            synapse_class.__name__
        )
        router: SynapseRouter[Any] = SynapseRouter(
            route_class=SynapseRouteHandler.build(synapse_class)
        )
        router.add_api_route(
            path=f'/{synapse_class.__name__}',
            endpoint=self.default_handler,
            methods=['POST'],
            response_model=synapse_class,
            response_description=(
                "The provided synapse updated with the results from the "
                "neuron."
            )
        )
        self.app.include_router(
            router=router,
            include_in_schema=True,
            dependencies=[
                fastapi.Depends(self.authorize)
            ]
        )

    async def default_handler(
        self,
        request: fastapi.Request
    ) -> fastapi.Response:
        return await self.submit(await cast(SynapseRequest[Any], request).envelope())

    def is_running(self):
        return self.running.is_set()

    def main_event_loop(self):
        self.config = Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level='debug',
            access_log=True,
        )
        self.server = Server(config=self.config)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        for synapse_class in self.synapse_types:
            self.attach(synapse_class)
        try:
            self.running.set()
            self.loop.run_until_complete(
                self.server.serve(sockets=[self.config.bind_socket()])
            )
        finally:
            self.running.clear()
            if self.config.uds and os.path.exists(self.config.uds):
                os.remove(self.config.uds)  # pragma: py-win32

    def submit(
        self,
        envelope: SynapseEnvelope[Any]
    ) -> asyncio.Future[fastapi.Response]:
        future = self.loop.create_future()
        self.soma.submit(envelope, future)
        return future

    def wait(self):
        return self.running.wait()