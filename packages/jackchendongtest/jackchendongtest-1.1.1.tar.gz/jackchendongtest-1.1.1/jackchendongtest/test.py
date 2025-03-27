# from langchain_community.llms import OpenAI
# if not os.environ.get("OPENAI_API_KEY"):
#   os.environ["OPENAI_API_KEY"] = "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"
# if not os.environ.get("GEMINI_API_KEY"):
#     os.environ["GEMINI_API_KEY"] = "AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y"
# from langchain.chat_models import init_chat_model
#
# # llm = init_chat_model("gpt-3.5-turbo-instruct", model_provider="openai",api_key="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")
# llm = init_chat_model("gemini-2.0-flash-exp", model_provider="google_vertexai",api_key="AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y")
# json_schema = {
#     "title": "joke",
#     "description": "Joke to tell user.",
#     "type": "object",
#     "properties": {
#         "setup": {
#             "type": "string",
#             "description": "The setup of the joke",
#         },
#         "punchline": {
#             "type": "string",
#             "description": "The punchline to the joke",
#         },
#         "rating": {
#             "type": "integer",
#             "description": "How funny the joke is, from 1 to 10",
#             "default": None,
#         },
#     },
#     "required": ["setup", "punchline"],
# }
# structured_llm = llm.with_structured_output(json_schema)
#
# structured_llm.invoke("Tell me a joke about cats")


# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.runnables import RunnableGenerator
# from typing import Iterator

# if not os.environ.get("GOOGLE_API_KEY"):
#   os.environ["GOOGLE_API_KEY"] = "AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y"

# def _generate(input: Iterator) -> Iterator[str]:
#     print(1111)
#     yield from "foo bar"
#
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-exp",
#
#     google_api_key="AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y"
# ).with_fallbacks([RunnableGenerator(_generate)])
# print(llm.invoke("给我讲一个笑话"))


from jackchendongtest.observer import  LangChainObserver, ObserverConfig, SessionConfig,TracerConfig
from langchain_google_genai import ChatGoogleGenerativeAI

ObserverConfig = ObserverConfig(projectId="4723b7100da6a05a4c68fe43c0f7a83f", threadId="test",
                                apiHost="http://39.104.13.226:8088", apiKey="osk-JnSwDBQakTZeNiMYn1UknmArIHzNUxiY")
client = LangChainObserver(ObserverConfig)
client.startSession(SessionConfig(sessionName="eat"))
tracer = client.createTracer(TracerConfig(agentName="agent"))
mode = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key="AIzaSyDzj2f8kaoEBFbjY3T0UTtnwTlHRwtvR1Y")
res = mode.invoke("给我讲一个笑话", {"callbacks": [tracer]})

print(res)
