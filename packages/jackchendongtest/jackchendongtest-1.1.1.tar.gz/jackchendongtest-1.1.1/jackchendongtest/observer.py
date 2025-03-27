import time
from typing import Optional, Dict, Any, List

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from jackchendongtest.config import API_KEY, API_HOST, OUTPUT_LOG_SWITCH
from jackchendongtest.event import EventManager, Event, EventType
from jackchendongtest.server import Server, Session, Agent, Thread


class ObserverConfig:
    def __init__(self, projectId: str, apiKey: Optional[str] = None, apiHost: Optional[str] = None,
                 threadId: Optional[str] = None):
        self.projectId = projectId
        self.apiKey = apiKey
        self.apiHost = apiHost
        self.threadId = threadId


class SessionConfig:
    def __init__(self, sessionName: str, externalUserId: Optional[str] = None):
        self.sessionName = sessionName
        self.externalUserId = externalUserId


class TracerConfig:
    def __init__(self, agentName: Optional[str]):
        self.agentName = agentName


class LangChainObserver:
    def __init__(self, observerConfig: ObserverConfig):
        self.observaSession = None
        self.observaAgent = None
        self.observaThread = None
        self.projectId = observerConfig.projectId
        apiKey = observerConfig.apiKey or API_KEY
        host = observerConfig.apiHost or API_HOST

        if observerConfig.threadId:
            self.observaThread = {'threadId': observerConfig.threadId}
        self.apiServer = Server(apiKey, self.projectId, host)

    def createTracer(self, traceConfig: Optional[TracerConfig]):
        self.createThread()
        if traceConfig and traceConfig.agentName:
            self.observaAgent = {
                "agentName": traceConfig.agentName
            }
            self.createAgent()
        return TracerObserver(self)

    def createThread(self):
        if self.observaThread and not self.observaThread.get("observaThreadId"):
            self.observaThread['observaThreadId'] = self.apiServer.createThread(
                Thread(self.observaThread.get("threadId")))

    def createAgent(self):
        if self.observaAgent and not self.observaAgent.get('id'):
            self.observaAgent['id'] = self.apiServer.createAgent(Agent(self.observaAgent.get('agentName') or ""))

    def startSession(self, sessionConfig: SessionConfig):
        session = Session(sessionConfig.sessionName, sessionConfig.externalUserId)
        sessionId = self.apiServer.createSession(session)
        self.observaSession = {
            "sessionName": sessionConfig.sessionName,
            "externalUserId": sessionConfig.externalUserId,
            "id": sessionId
        }
        return self

    def getProjectId(self):
        return self.projectId


class TracerObserver(BaseCallbackHandler):

    def __init__(self, client: LangChainObserver):
        super()
        self.name = "TracerObserver"
        self.outputLogSwitch = OUTPUT_LOG_SWITCH
        self.client = client
        self.eventManager = EventManager(self.client.projectId)
        self.observaAgent = None
        self.observaThread = None

    def outputLog(self, fName: str, data: Any):
        if self.outputLogSwitch:
            print(fName, data)

    def getAgentId(self):
        return (self.observaAgent and self.observaAgent.get('id')) or self.client.observaAgent.get('id', '')

    def getThreadId(self):
        return (self.observaThread and self.observaThread.id) or self.client.observaThread.get('observaThreadId', '')

    def getSessionId(self):
        return self.client.observaSession.get('id', '')

    def createThread(self, threadId: str):
        if not self.observaThread:
            self.observaThread = {
                "threadId": threadId
            }
        if self.observaThread and not self.observaThread.threadId:
            self.observaThread.observaThreadId = self.client.apiServer.createThread(
                Thread(self.observaThread.threadId or ''))

    def createAgent(self, agentName: str):
        if not self.observaAgent:
            self.observaAgent = {
                "agentName": agentName
            }
        if self.observaAgent and not self.observaAgent.get('id'):
            self.observaAgent["id"] = self.client.apiServer.createAgent(Agent(agentName or ""))

    def on_chat_model_start(
            self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        self.outputLog("on_chat_model_start", {**kwargs, "serialized": serialized, "messages": messages})
        metadata = kwargs.get("metadata")
        if metadata and metadata.get('agentName'):
            self.createAgent(metadata.get('agentName'))
        if metadata and metadata.get('threadId'):
            self.createThread(metadata.get('threadId'))
        extraParams = kwargs.get('extra_params', {})
        self.eventManager.createEventAndTrace(Event(
            eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
            parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
            eventType=EventType.LLM,
            eventName=serialized.get('id')[len(serialized.get('id')) - 1],
            metadata=metadata,
            tags=kwargs.get('tags'),
            input=messages,
            startTime=int(time.time() * 1000),
            extraParams=extraParams,
            model=extraParams.get('invocation_params', {}).get('model') or \
                  extraParams.get('invocation_params', {}).get('modelName') or \
                  metadata.get('ls_model_name')
        ))

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        self.outputLog("on_llm_start", {**kwargs, "serialized": serialized, "prompts": prompts})
        metadata = kwargs.get("metadata")
        if metadata and metadata.get('agentName'):
            self.createAgent(metadata.get('agentName'))
        if metadata and metadata.get('threadId'):
            self.createThread(metadata.get('threadId'))
        extraParams = kwargs.get('extra_params', {})
        self.eventManager.createEventAndTrace(Event(
            eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
            parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
            eventType=EventType.LLM,
            eventName=serialized.get('id')[len(serialized.get('id')) - 1],
            metadata=metadata,
            tags=kwargs.get('tags'),
            input=prompts,
            startTime=int(time.time() * 1000),
            extraParams=extraParams,
            model=extraParams.get('invocation_params', {}).get('model') or \
                  extraParams.get('invocation_params', {}).get('modelName') or \
                  metadata.get('ls_model_name')
        ))

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        self.outputLog("on_llm_end", {**kwargs, "response": response})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.output = response
            event.tokenCount = event.output and event.output.llm_output and event.output.llm_output.get(
                'token_usage') and event.output.llm_output.get('token_usage').get("total_tokens") or 0
        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_llm_error(
            self,
            error: BaseException,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_llm_error", {**kwargs, "error": error})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.error = error
        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs
    ) -> None:
        self.outputLog("on_chain_start", {**kwargs, "serialized": serialized, "inputs": inputs})
        metadata = kwargs.get("metadata")
        if metadata and metadata.get('agentName'):
            self.createAgent(metadata.get('agentName'))
        if metadata and metadata.get('threadId'):
            self.createThread(metadata.get('threadId'))

        self.eventManager.createEventAndTrace(Event(
            eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
            parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
            eventType=EventType.CHAIN,
            eventName=serialized.get('id')[len(serialized.get('id')) - 1],
            tags=kwargs.get('tags'),
            input=inputs,
            startTime=int(time.time() * 1000),
        ))

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        self.outputLog("on_chain_end", {**kwargs, "outputs": outputs})

        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(kwargs.get('run_id'))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.output = outputs

        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_chain_error(
            self,
            error: BaseException,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_chain_error", {**kwargs, "error": error})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.error = error

        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_agent_action(
            self,
            action: AgentAction,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_agent_action", {**kwargs, "action": action})
        event = self.eventManager.createEventAndTrace(Event(
            eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
            parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
            eventType=EventType.TOOL,
            eventName="Agent Action",
            tags=kwargs.get('tags'),
            input=action.tool_input,
            startTime=int(time.time() * 1000),
        ))
        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_agent_finish(
            self,
            finish: AgentFinish,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_agent_finish", {**kwargs, "finish": finish})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.output = finish.return_values
            if event and not event.parentId:
                self.client.apiServer.createEvent({
                    "sessionId": self.getSessionId(),
                    "threadId": self.getThreadId(),
                    "agentId": self.getAgentId(),
                    "logList": self.eventManager.getRootEvents()
                })
        else:
            event = self.eventManager.createEventAndTrace(Event(
                eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
                parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
                eventType=EventType.TOOL,
                eventName="Agent Finish",
                tags=kwargs.get('tags'),
                output=finish.return_values,
                startTime=endTime,
                endTime=endTime
            ))
            if event and not event.parentId:
                self.client.apiServer.createEvent({
                    "sessionId": self.getSessionId(),
                    "threadId": self.getThreadId(),
                    "agentId": self.getAgentId(),
                    "logList": self.eventManager.getRootEvents()
                })

    def on_tool_start(
            self,
            serialized: dict[str, Any],
            input_str: str,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_tool_start", {**kwargs, "serialized": serialized, "input_str": input_str})
        metadata = kwargs.get("metadata")
        if metadata and metadata.get('agentName'):
            self.createAgent(metadata.get('agentName'))
        if metadata and metadata.get('threadId'):
            self.createThread(metadata.get('threadId'))
        self.eventManager.createEventAndTrace(Event(
            eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
            parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
            eventType=EventType.TOOL,
            eventName=serialized.get('id')[len(serialized.get('id')) - 1],
            tags=kwargs.get('tags'),
            input=input_str,
            startTime=int(time.time() * 1000),
        ))

    def on_tool_end(
            self,
            output: Any,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_tool_end", {**kwargs, "output": output})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.output = output
        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_tool_error(
            self,
            error: BaseException,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_tool_error", {**kwargs, "error": error})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.error = error

        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_retriever_start(
            self,
            serialized: dict[str, Any],
            query: str,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_retriever_start", {**kwargs, "query": query, "serialized": serialized})
        metadata = kwargs.get("metadata")
        if metadata and metadata.get('agentName'):
            self.createAgent(metadata.get('agentName'))
        if metadata and metadata.get('threadId'):
            self.createThread(metadata.get('threadId'))
        self.eventManager.createEventAndTrace(Event(
            eventId=kwargs.get("run_id") and str(kwargs.get("run_id")),
            parentId=kwargs.get("parent_run_id") and str(kwargs.get("parent_run_id")),
            eventType=EventType.RETRIEVAL,
            eventName=serialized.get('id')[len(serialized.get('id')) - 1],
            tags=kwargs.get('tags'),
            input=query,
            startTime=int(time.time() * 1000),
        ))

    def on_retriever_end(
            self,
            documents: Any,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_retriever_end", {**kwargs, "documents": documents})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.output = documents

        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })

    def on_retriever_error(
            self,
            error: BaseException,
            **kwargs: Any,
    ) -> Any:
        self.outputLog("on_retriever_error", {**kwargs, "error": error})
        endTime = int(time.time() * 1000)
        event = self.eventManager.getEventById(str(kwargs.get('run_id')))
        if event:
            event.endTime = endTime
            if event.startTime:
                event.duration = endTime - event.startTime
            event.error = error
        if event and not event.parentId:
            self.client.apiServer.createEvent({
                "sessionId": self.getSessionId(),
                "threadId": self.getThreadId(),
                "agentId": self.getAgentId(),
                "logList": self.eventManager.getRootEvents()
            })
