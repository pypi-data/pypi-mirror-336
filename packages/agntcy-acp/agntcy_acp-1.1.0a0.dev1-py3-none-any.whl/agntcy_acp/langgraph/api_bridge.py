# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
from pydantic import BaseModel, Field

from typing import Any
from langchain_core.runnables import RunnableConfig
from langgraph.utils.runnable import RunnableCallable
from agntcy_acp import ACPClient, ApiClient, AsyncACPClient, AsyncApiClient, Configuration
from agntcy_acp.models import RunCreate, Run, RunResult, AgentACPDescriptor
import requests
from agntcy_acp.langgraph import acp_node


class APIBridgeInput(BaseModel):
   query: str = Field(..., description="Query for the API bridge agent in natural language")

class APIBridgeOutput(BaseModel):
    result: str = Field(..., description="API response from API bridge agent")

class APIBridgeAgentNode(acp_node.ACPNode):
    def __init__(self, name: str, hostname: str, service_name: str, input_path: str, output_path: str, service_api_key: str, input_type = None, output_type=None, apikey: str = None):
        self.__name__ = name
        self.hostname = hostname
        self.apikey = apikey
        self.service_name = service_name
        self.inputType = input_type if input_type else APIBridgeInput
        self.outputType = output_type if output_type else APIBridgeOutput
        self.inputPath = input_path
        self.outputPath = output_path
        self.service_api_key = service_api_key




    def invoke(self, state: Any, config: RunnableConfig) -> Any:
        api_bridge_input = self._extract_input(state)

        api_bridge_input.query = "Please use content-type application/json." + api_bridge_input.query

        print(f"*************\n{api_bridge_input.query}\n**********")


        # TODO: Merge config with runnable config
        headers = {
            "Accept": None,
            "Authorization": f"Bearer {self.service_api_key}",
            "Accept-Encoding": None,
            "Content-Type": "text/plain",
            "X-Nl-Query-Enabled": "yes"
        }
        r = requests.post(f"{self.hostname}/{self.service_name}", headers=headers, data=api_bridge_input.query)
        r.raise_for_status()
        response = r.text
        if not response: response = f"Operation performed: {r.url} Result{r.status_code}"
        output = APIBridgeOutput(result=response)
        self._set_output(state, self.outputType.model_validate(output.model_dump()))

        return state

    async def ainvoke(self, state: Any, config: RunnableConfig) -> Any:
        # TODO: Add proper support for ainvoke.
        self.invoke(state, config)

        return state


