# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
import pathlib
from typing import Literal

import pydantic

from ._hotkeyref import HotkeyRef
from ._hotkeyprivatekey import HotkeyPrivateKey
from ._hotkeypublickey import HotkeyPublicKey


class Hotkey(pydantic.RootModel[HotkeyRef|HotkeyPublicKey]):

    @property
    def public_bytes(self):
        if not isinstance(self.root, (HotkeyPublicKey, HotkeyPrivateKey)):
            raise TypeError("Hotkey is not loaded.")
        return self.root.public_key

    @property
    def hotkey(self):
        return self.root.hotkey

    @property
    def name(self):
        return self.root.name

    @property
    def ss58_address(self):
        if not isinstance(self.root, (HotkeyPublicKey, HotkeyPrivateKey)):
            raise TypeError("Hotkey is not loaded.")
        return self.root.ss58_address

    @property
    def qualname(self):
        return f'{self.root.name}/{self.root.hotkey}'

    def load(
        self,
        path: pathlib.Path,
        mode: Literal['public', 'private', 'phrase']
    ):
        p = path.joinpath(self.root.name, 'hotkeys', self.root.hotkey)
        with open(p, 'r') as f:
            data: dict[str, str] = {
                **json.loads(f.read()),
                'name': self.root.name,
                'hotkey': self.root.hotkey
            }
        match mode:
            case 'public': self.root = HotkeyPublicKey.model_validate(data)
            case 'private': self.root = HotkeyPrivateKey.model_validate(data)
            case 'phrase': raise NotImplementedError

        # TODO: Use stringwipe instead of garbage collect.
        del data

    def unload(self):
        self.root = HotkeyRef.model_validate(self.root.model_dump())

    def __hash__(self):
        return hash(self.root)