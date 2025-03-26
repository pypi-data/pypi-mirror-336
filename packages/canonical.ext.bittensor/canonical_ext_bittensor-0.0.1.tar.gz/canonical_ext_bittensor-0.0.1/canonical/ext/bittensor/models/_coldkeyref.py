# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pathlib

import pydantic

from ._hotkey import Hotkey


class ColdkeyRef(pydantic.BaseModel):
    name: str = pydantic.Field(
        default=...
    )

    def hotkeys(
        self,
        wallet_path: pathlib.Path,
        refs_only: bool = True
    ):
        if not refs_only:
            raise NotImplementedError
        hotkeys: list[Hotkey] = []
        for p in sorted(wallet_path.joinpath(self.name).glob('hotkeys/*')):
            hotkeys.append(
                Hotkey.model_validate({
                    'name': self.name,
                    'hotkey': p.stem
                })
            )
        return hotkeys

    def __hash__(self):
        return hash(self.name)