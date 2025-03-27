# Copyright (C) 2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Generic
from typing import TypeVar

import bittensor
import fastapi
import fastapi.routing
import starlette
import starlette.requests

from ._request import SynapseRequest


S = TypeVar('S', bound=bittensor.Synapse)


class SynapseRouteHandler(fastapi.routing.APIRoute, Generic[S]):
    logger: logging.Logger = logging.getLogger(__name__)
    synapse_class: type[S]

    @classmethod
    def build(
        cls,
        synapse_class: type[Any]
    ) -> type['SynapseRouteHandler[Any]']:
        return type(f'{synapse_class.__name__}', (cls, ), {
            'synapse_class': synapse_class
        })

    def get_route_handler(self) -> Callable[[starlette.requests.Request], Coroutine[Any, Any, fastapi.Response]]:
        handler = super().get_route_handler()

        async def f(request: starlette.requests.Request) -> fastapi.Response:
            request = SynapseRequest(
                model=self.synapse_class,
                scope=request.scope,
                receive=request.receive
            )
            return await handler(request)
        return f