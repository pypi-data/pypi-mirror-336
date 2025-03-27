# Copyright (C) 2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generic
from typing import TypeVar

import bittensor
import fastapi

from ._apiroute import SynapseRouteHandler


S = TypeVar('S', bound=bittensor.Synapse)


class SynapseRouter(fastapi.APIRouter, Generic[S]):
    """A :class:`fastapi.APIRouter` implementation that provided additional
    interfaces to register synapse routes.
    """
    __module__: str = 'tensorshield.ext.axon.routing'
    route_class: type[SynapseRouteHandler[S]]