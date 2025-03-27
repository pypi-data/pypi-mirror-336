# Copyright (C) 2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import bittensor
import fastapi


class SynapseResponse(fastapi.responses.JSONResponse):

    def __init__(
        self,
        synapse: bittensor.Synapse,
        status_code: int = 200
    ):
        if synapse.axon is not None:
            synapse.axon.status_code = status_code
            synapse.axon.status_message = "Success"
            if status_code >= 400:
                synapse.axon.status_message = "Error"
        super().__init__(
            status_code=status_code,
            content=synapse.model_dump(mode='json')
        )
        self.headers.update(synapse.to_headers()) # type: ignore
        self.headers['Content-Type'] = "application/json"