
from typing import Any, Dict
from uuid import UUID
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.outputs import LLMResult, ChatGeneration
from pydantic.v1.typing import NoneType


def recursive_to_dict(obj: Any) -> Dict:
    if isinstance(obj, dict):
        return {key: recursive_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [recursive_to_dict(item) for item in obj]
    elif isinstance(obj, UUID):
        return str(obj)  # 将 UUID 转换为字符串
    elif isinstance(obj, int):
        return obj  # 将 datetime 转换为 ISO 格式字符串
    elif isinstance(obj, LLMResult):
        return obj.model_dump()
        # return obj.__dict__
    elif isinstance(obj, HumanMessage):
        return obj.model_dump()
    elif isinstance(obj, ChatGeneration):
        return obj.model_dump()
    elif isinstance(obj, AIMessage):
        return obj.model_dump()
    elif isinstance(obj, NoneType):
        return None

    return obj
