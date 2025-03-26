# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any
from typing import Generic
from typing import TypeVar

from canonical.ext.bittensor.models import SynapseEnvelope


S = TypeVar('S')


class BaseSoma(Generic[S]):
    """Specifies the base interface to a :class:`~canonical.ext.bittensor.Soma`
    implementation.
    """

    async def discover(self) -> None:
        raise NotImplementedError

    def submit(
        self,
        envelope: SynapseEnvelope[Any],
        future: asyncio.Future[Any]
    ) -> None:
        raise NotImplementedError