# Copyright (C) 2022-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from cryptography.hazmat.primitives.asymmetric import ed25519
from libcanonical.types import HexEncoded

from ._hotkeypublickey import HotkeyPublicKey


class HotkeyPrivateKey(HotkeyPublicKey):
    private_key: HexEncoded = pydantic.Field(
        default=...,
        alias='privateKey'
    )

    @property
    def private(self):
        return ed25519.Ed25519PrivateKey.from_private_bytes(self.private_key)