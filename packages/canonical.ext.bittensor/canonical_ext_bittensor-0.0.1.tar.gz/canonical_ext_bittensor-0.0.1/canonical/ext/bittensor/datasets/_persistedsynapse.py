# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import TypedDict

from datasets import Sequence
from datasets import Value

from canonical.ext.datasets import Dataset



class PersistedSynapseDict(TypedDict):
    headers: dict[str, str]
    host: str
    kind: str
    method: str
    netuid: int
    path: str
    payload: str
    received: datetime.datetime


class PersistedSynapseDataset(Dataset[PersistedSynapseDict]):

    @classmethod
    def column_values(cls) -> dict[str, Sequence | Value]:
        return {
            'headers': Sequence(Sequence(Value('string'))),
            'host': Value('string'),
            'kind': Value('string'),
            'method': Value('string'),
            'netuid': Value('int32'),
            'path': Value('string'),
            'payload': Value('string'),
            'received': Value('timestamp[us]')
        }