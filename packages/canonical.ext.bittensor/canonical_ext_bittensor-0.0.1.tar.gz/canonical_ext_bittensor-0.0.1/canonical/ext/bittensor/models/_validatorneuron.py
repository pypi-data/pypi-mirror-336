# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic

from ._baseneuron import BaseNeuron


class ValidatorNeuron(BaseNeuron):
    validator_permit: Literal[True] = pydantic.Field(
        default=...
    )

    vtrust: float = pydantic.Field(
        default=...
    )

    def is_miner(self) -> bool:
        return self.trust > 0.0

    def is_validator(self) -> bool:
        return True