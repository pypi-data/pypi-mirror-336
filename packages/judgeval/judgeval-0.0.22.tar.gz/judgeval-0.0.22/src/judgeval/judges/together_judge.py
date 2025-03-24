"""
Implementation of using TogetherAI inference for judges.
"""

from pydantic import BaseModel
from typing import List, Union, Mapping
from judgeval.common.logger import debug, error

from judgeval.judges import JudgevalJudge
from judgeval.common.utils import fetch_together_api_response, afetch_together_api_response

BASE_CONVERSATION = [
    {"role": "system", "content": "You are a helpful assistant."},
]

class TogetherJudge(JudgevalJudge):
    def __init__(self, model: str = "Qwen/Qwen2.5-72B-Instruct-Turbo", **kwargs):
        debug(f"Initializing TogetherJudge with model={model}")
        self.model = model
        self.kwargs = kwargs
        super().__init__(model_name=model)

    # TODO: Fix cost for generate and a_generate
    def generate(self, input: Union[str, List[Mapping[str, str]]], schema: BaseModel = None) -> str:
        debug(f"Generating response for input type: {type(input)}")
        if isinstance(input, str):
            convo = BASE_CONVERSATION + [{"role": "user", "content": input}]
            return fetch_together_api_response(self.model, convo, response_format=schema)
        elif isinstance(input, list):
            convo = input
            return fetch_together_api_response(self.model, convo, response_format=schema)
        else:
            error(f"Invalid input type received: {type(input)}")
            raise TypeError("Input must be a string or a list of dictionaries.")

    async def a_generate(self, input: Union[str, List[dict]], schema: BaseModel = None) -> str:
        debug(f"Async generating response for input type: {type(input)}")
        if isinstance(input, str):
            convo = BASE_CONVERSATION + [{"role": "user", "content": input}]
            res = await afetch_together_api_response(self.model, convo, response_format=schema)
            return res
        elif isinstance(input, list):
            convo = input
            res = await afetch_together_api_response(self.model, convo, response_format=schema)
            return res
        else:
            error(f"Invalid input type received: {type(input)}")
            raise TypeError("Input must be a string or a list of dictionaries.")

    def load_model(self) -> str:
        return self.model

    def get_model_name(self) -> str:
        return self.model
    