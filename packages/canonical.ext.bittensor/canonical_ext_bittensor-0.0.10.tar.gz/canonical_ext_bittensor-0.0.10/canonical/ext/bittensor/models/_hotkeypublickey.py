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

from canonical.ext.bittensor.types import SS58Address
from ._hotkeyref import HotkeyRef


class HotkeyPublicKey(HotkeyRef):
    public_key: HexEncoded = pydantic.Field(
        default=...,
        alias='publicKey'
    )

    ss58_address: SS58Address = pydantic.Field(
        default=...,
        alias='ss58Address'
    )

    @property
    def public(self):
        return ed25519.Ed25519PublicKey.from_public_bytes(self.public_key)