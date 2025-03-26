# Copyright (C) 2022-2025 Cochise Ruhulessin
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
import pydantic

from ._synapseheader import SynapseHeader


S = TypeVar('S', bound=bittensor.Synapse)


class SynapseEnvelope(pydantic.BaseModel, Generic[S]):
    remote_host: str
    remote_port: int | None = None
    headers: SynapseHeader
    synapse: S

    @classmethod
    def annotate(cls, synapse_class: type[S]) -> type['SynapseEnvelope[S]']:
        return SynapseEnvelope[synapse_class]