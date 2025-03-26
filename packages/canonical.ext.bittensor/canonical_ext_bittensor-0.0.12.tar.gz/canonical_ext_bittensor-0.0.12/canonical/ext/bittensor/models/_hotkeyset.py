# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pathlib
from typing import Literal

import pydantic

from ._hotkey import Hotkey


class HotkeySet(pydantic.BaseModel):
    model_config = {'populate_by_name': True}

    items: dict[str, Hotkey] = pydantic.Field(
        default_factory=dict
    )

    def load(
        self,
        path: pathlib.Path,
        mode: Literal['public', 'private', 'phrase']
    ):
        for hotkey in self.items.values():
            hotkey.load(path, mode=mode)