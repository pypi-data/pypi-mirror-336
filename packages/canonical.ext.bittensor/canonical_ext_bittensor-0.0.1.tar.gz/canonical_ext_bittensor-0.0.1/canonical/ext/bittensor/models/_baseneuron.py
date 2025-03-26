# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import ClassVar
from typing import TypeAlias
from typing import TypeVar
from typing import Union
from typing import TYPE_CHECKING

import pydantic
from libcanonical.bases import StateLogger

if TYPE_CHECKING:
    from ._minerneuron import MinerNeuron
    from ._validatorneuron import ValidatorNeuron


S = TypeVar('S', bound='BaseNeuron')
T = TypeVar('T', bound=Union['MinerNeuron', 'ValidatorNeuron'])
NeuronType: TypeAlias = Union['MinerNeuron', 'ValidatorNeuron']


class BaseNeuron(pydantic.BaseModel, StateLogger):
    logger: ClassVar[logging.Logger] = logging.getLogger(__name__)
    active: bool = False
    coldkey: str
    consensus: float = 0.0
    dividends: float = 0.0
    emission: float = 0.0
    host: str = '0.0.0.0'
    hotkey: str
    incentive: float = 0.0
    port: int = 0
    rank: float = 0.0
    stake: float = 0.0
    trust: float = 0.0
    uid: int = -1
    updated: int = 0

    def is_miner(self) -> bool:
        raise NotImplementedError

    def is_validator(self) -> bool:
        raise NotImplementedError

    def is_registered(self):
        return self.uid >= 0

    def diff(self, neuron: Union['MinerNeuron', 'ValidatorNeuron']) -> set[str]:
        changed: set[str] = set()
        for attname in self.model_fields.keys():
            if getattr(self, attname) == getattr(neuron, attname):
                continue
            changed.add(attname)
        return changed

    def update(self, neuron: NeuronType) -> tuple[NeuronType, NeuronType, tuple[str, ...]]:
        adapter: pydantic.TypeAdapter[NeuronType] = pydantic.TypeAdapter(type(neuron) | type(self))
        changed = self.diff(neuron)
        old = adapter.validate_python(self.model_dump())
        for k in changed:
            new = getattr(neuron, k)
            setattr(self, k, new)
        return old, neuron, tuple(changed)

    def __hash__(self) -> int:
        return hash(self.hotkey)