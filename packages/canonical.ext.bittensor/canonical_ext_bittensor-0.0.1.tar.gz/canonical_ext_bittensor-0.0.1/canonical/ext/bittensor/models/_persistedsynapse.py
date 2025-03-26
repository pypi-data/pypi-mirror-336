# Copyright (C) Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import pydantic


class PersistedSynapse(pydantic.BaseModel):
    request_id: int = pydantic.Field(
        default=...
    )

    received: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    netuid: int = pydantic.Field(
        default=...
    )

    uid: int | None = pydantic.Field(
        default=None
    )

    kind: str = pydantic.Field(
        default=...
    )

    host: str = pydantic.Field(
        default=...
    )

    method: str = pydantic.Field(
        default=...
    )

    path: str = pydantic.Field(
        default=...
    )

    headers: dict[str, str] = pydantic.Field(
        default=...
    )

    payload: str | None = pydantic.Field(
        default=None
    )