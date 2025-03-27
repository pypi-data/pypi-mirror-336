import pytest
from pydantic import BaseModel

from packages.freeflock_contraptions.configuration import collect_from_config
from packages.freeflock_contraptions.inference import OpenaiInference

OPENAI_API_KEY = collect_from_config("OPENAI_API_KEY")


@pytest.mark.asyncio
async def test_infer():
    inference_client = OpenaiInference(OPENAI_API_KEY)
    model_name = "o3-mini"
    system_prompt = "You are a helpful assistant."
    user_prompt = "What is the capital of France?"
    reasoning_effort = "low"
    result = await inference_client.infer(model_name, system_prompt, user_prompt, reasoning_effort)
    assert "paris" in result.lower()
    print(result)


@pytest.mark.asyncio
async def test_infer_json():
    inference_client = OpenaiInference(OPENAI_API_KEY)
    model_name = "o3-mini"
    system_prompt = "You are a helpful assistant."
    user_prompt = "What is the capital of France?"
    reasoning_effort = "low"
    result = await inference_client.infer_json(model_name, system_prompt, user_prompt, reasoning_effort, Capital)
    assert "paris" in result.capital.lower()
    print(result)


class Capital(BaseModel):
    capital: str
