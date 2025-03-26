# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class HotkeyRef(pydantic.BaseModel):
    model_config = {'populate_by_name': True}

    name: str = pydantic.Field(
        default=...
    )

    hotkey: str = pydantic.Field(
        default=...
    )

    @property
    def qualname(self):
        return f'{self.name}/{self.hotkey}'

    def __hash__(self):
        return hash(f'{self.name}/{self.hotkey}')