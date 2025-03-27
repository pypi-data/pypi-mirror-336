from langchain_core.callbacks import BaseCallbackHandler, StdOutCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Dict, Any, List
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class LoggingHandler(BaseCallbackHandler):
    def on_chat_model_start(
            self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        print(kwargs.get("run_id"))
        print("Chat model started")

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""

        print("llm model started")

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        print(f"Chat model ended, response: {response}")

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs
    ) -> None:
        print(f"Chain {serialized.get('name')} started")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        print(f"Chain ended, outputs: {outputs}")


# callbacks = [LoggingHandler()]
#
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-exp",
#     google_api_key="AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y"
# )
# llm.with_config(callbacks=callbacks)
# res = llm.invoke("给我讲一个笑话")
# print(222, res)

handler = LoggingHandler()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key="AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y"
)
res = llm.invoke("给我讲一个笑话", {"callbacks": [handler]})
print(222, res)
