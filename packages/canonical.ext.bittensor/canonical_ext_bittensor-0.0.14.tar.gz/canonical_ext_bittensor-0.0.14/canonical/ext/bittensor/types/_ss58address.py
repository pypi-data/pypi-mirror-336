# Copyright (C) 2023-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import TypeVar

from substrateinterface.utils.ss58 import ss58_decode
from substrateinterface.utils.ss58 import is_valid_ss58_address
from substrateinterface import Keypair
from pydantic_core import CoreSchema
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import GetJsonSchemaHandler


__all__: list[str] = [
    'SS58Address'
]

T = TypeVar('T', bound='SS58Address')


class SS58Address(str):
    __module__: str = 'canonical.ext.bittensor'

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.chain_schema([
                core_schema.is_instance_schema(str),
                core_schema.no_info_plain_validator_function(cls.validate)
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(cls.serialize)
        )

    @functools.cached_property
    def public_bytes(self):
        return bytes.fromhex(ss58_decode(self))

    @functools.cached_property
    def keypair(self):
        return Keypair(ss58_address=self)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

    @classmethod
    def validate(cls: type[T], instance: T | str) -> T:
        if not is_valid_ss58_address(instance):
            raise ValueError("not a valid SS58 address")
        return cls(instance)

    def serialize(self) -> str:
        return self

    def verify(
        self,
        data: str | bytes,
        signature: str | bytes
    ):
        return self.keypair.verify(data, signature)

    def __repr__(self):
        return f'<SS58Address: {str(self)}>'