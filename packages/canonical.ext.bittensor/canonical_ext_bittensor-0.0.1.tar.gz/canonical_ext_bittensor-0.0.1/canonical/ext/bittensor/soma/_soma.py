# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import inspect
import ipaddress
import os
from typing import Any
from typing import AsyncGenerator
from typing import Awaitable
from typing import Callable
from typing import TypeAlias
from typing import TypeVar
from typing import ParamSpec
from typing import Union

import bittensor
from bittensor.core.settings import DEFAULT_NETWORK
from libcanonical.runtime import MainProcess
from libcanonical.types import FatalException
from libcanonical.utils import deephash

from canonical.ext.bittensor.bases import BaseSoma
from canonical.ext.bittensor.models import Hotkey
from canonical.ext.bittensor.models import SynapseEnvelope
from ..axon import Axon
from ..axon import SynapseResponse
from .._environment import BittensorEnvironment
from .._metagraph import Metagraph
from ._axontransport import AxonTransport
from ._taskrunner import TaskRunner


F = TypeVar('F')
P = ParamSpec('P')
S = TypeVar('S', bound=bittensor.Synapse)

Self = TypeVar('Self', bound='Soma[Any]')

SynapseHandlerType: TypeAlias = Union[
    Callable[..., AsyncGenerator[None | Exception | SynapseResponse, bittensor.Synapse | None]],
    Callable[..., Awaitable[None | SynapseResponse]]
]

SynapseTask: TypeAlias = AsyncGenerator[None | SynapseResponse, bittensor.Synapse | None]


class Soma(MainProcess, BaseSoma[S]):
    """The base class for the :class:`~canonical.ext.bittensor.Validator`
    and :class:`canonical.ext.bittensor.Miner` classes.
    """
    axon_class: type[Axon] = Axon
    config_class: type[BittensorEnvironment] = BittensorEnvironment
    interval = 1
    synapse_classes: list[type[bittensor.Synapse]]
    synapse_handlers: dict[str, SynapseHandlerType]
    task_identifier_exclude: set[str] = {'axon', 'dendrite'}

    @classmethod
    def fromenv(cls, name: str, **kwargs: Any):
        env = cls.config_class.model_validate_env({
            **os.environ,
            **{k: v for k, v in kwargs.items() if v is not None}
        })
        if env.netuid is None:
            raise FatalException(
                "Unable to infer netuid from the environment. Set "
                "the BT_SUBNET_UID environment variable to specify "
                "the subnet."
            )
        return cls(
            name=name,
            network=env.network,
            netuid=env.netuid,
            axon_ip=env.axon_ip,
            axon_port=env.axon_port,
            disable_axon=env.axon_disabled,
            hotkeys=list(env.enabled_hotkeys)
        )

    @classmethod
    def register(cls, synapse_class: Any) -> Any:
        def decorator(func: Any):
            func.synapse_class = synapse_class
            return func

        return decorator

    def __init__(
        self,
        name: str,
        netuid: int,
        hotkeys: list[Hotkey] | None = None,
        network: str = DEFAULT_NETWORK,
        axon_ip: ipaddress.IPv4Address = ipaddress.IPv4Address('0.0.0.0'),
        axon_port: int = 8091,
        disable_axon: bool = False
    ):
        super().__init__(name=name)
        self.axon_ip = axon_ip
        self.axon_port = axon_port
        self.disable_axon = disable_axon
        self.hotkeys = hotkeys or []
        self.metagraph = Metagraph(
            netuid=netuid,
            network=network
        )
        self.netuid = netuid
        self.network = network
        self.synapse_classes = []
        self.synapse_handlers = {}

    def generate_task_id(self, synapse: S) -> str:
        """Generates a task identifier for an incoming synapse. Task identifiers
        are used to identify similar tasks so that the scheduler can optimize
        execution.
        """
        if not synapse.dendrite:
            raise TypeError("The synapse.dendrite attribute can not be None.")
        return deephash(
            (
                synapse.dendrite.hotkey,
                synapse.model_dump(exclude=self.task_identifier_exclude)
             ),
            encode='hex',
            using='sha256'
        )

    def log_status(self):
        if not self.metagraph.wait(timeout=0.1):
            self.logger.critical("Metagraph is not up-to-date (age: %.02fs)", self.metagraph.age)
        self.logger.info(
            'Running on subnet %s (metagraph-age: %.02fs)',
            self.netuid,
            self.metagraph.age,
        )

    def must_report(self):
        return all([
            self.runtime > 1,
            self.interval >= 1.0,
            int(self.runtime) % 15 == 0
        ])

    def submit(
        self,
        envelope: SynapseEnvelope[Any],
        future: asyncio.Future[SynapseResponse]
    ) -> None:
        self.tasks.schedule(envelope, future)

    async def configure(self, reloading: bool = False):
        if not reloading:
            self.logger.info("Booting %s", self.name)

            # Ensure that all components have access to the
            # handlers.
            self._register_handlers()

            # Start the metagraph and ensure that the main event loop
            # starts with an up-to-date set of neurons.
            self.metagraph.start()
            self.logger.info(
                "Starting metagraph and awaiting initial update."
            )
            self.metagraph.wait()
            self.logger.info(
                "Commencing main event loop after successful metagraph update."
            )

            # Task runner needs to be available before the transport
            # starts.
            self.tasks = TaskRunner(
                soma=self,
                loop=self.loop,
                handlers=self.synapse_handlers
            )

            # Start transport to receive synapses. For now this is an
            # HTTP server, but other protocols might be considered.
            if self.disable_axon:
                self.transport = AxonTransport(
                    soma=self,
                    synapse_classes=self.synapse_classes
                )
            else:
                self.transport = self.axon_class(
                    soma=self,
                    metagraph=self.metagraph,
                    host=str(self.axon_ip),
                    port=self.axon_port,
                    hotkeys=self.hotkeys,
                    synapse_types=self.synapse_classes
                )
            self.transport.start()
            self.transport.wait()
            self.logger.info(
                "Bound axon transport to %s:%s",
                self.transport.host,
                self.transport.port
            )

    async def main_event(self) -> None:
        if not self.transport.is_running():
            self.logger.critical("Transport exited unexpectedly.")
            self.stop()
            return
        if self.must_report():
            self.log_status()
        await self.tasks.run_all()

    async def run_axon(self) -> None:
        raise NotImplementedError

    def _register_handlers(self):
        for _, value in inspect.getmembers(self):
            if not hasattr(value, 'synapse_class'):
                continue
            cls: type[bittensor.Synapse] = getattr(value, 'synapse_class')
            qualname = cls.__name__
            self.synapse_classes.append(cls)
            self.synapse_handlers[qualname] = value
            self.logger.info(
                "Initialized %s handler function.",
                qualname
            )