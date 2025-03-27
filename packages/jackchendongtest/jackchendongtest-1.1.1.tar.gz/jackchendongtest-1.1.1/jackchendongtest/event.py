from enum import Enum
from typing import List, Optional, Dict, Any, Union
import time
from langchain_core.outputs import LLMResult
from pydantic import BaseModel


class EventType(str, Enum):
    LLM = 'LLM'
    TOOL = 'TOOL'
    CHAIN = 'CHAIN'
    RETRIEVAL = 'RETRIEVAL'


class Event(BaseModel):
    eventId: str
    eventType: EventType
    eventName: str
    parentId: Optional[str] = None
    children: Optional[List['Event']] = None
    metadata: Optional[Dict] = None
    input: Any = None
    output: Optional[Union[LLMResult, str, int, List[str], Dict[str, Any]]] = None
    startTime: Optional[int] = None
    endTime: Optional[int] = None
    error: Optional[Dict] = None
    tags: Optional[List[str]] = None
    duration: Optional[int] = None
    tokenCount: Optional[int] = None
    extraParams: Optional[Dict] = None
    model: Optional[str] = None


class EventManager:

    def __init__(self, project: str):
        self.project = project
        self.eventMap: Dict[str, Event] = {}
        self.rootEvents: List[Event] = []

    def createEventAndTrace(self, event: Event) -> Event:
        if not event.startTime:
            event.startTime = int(time.time() * 1000)
        if event.tokenCount is None:
            event.tokenCount = 0
        self.addEventToParent(event)
        return event

    def addEventToParent(self, event: Event) -> None:
        if event.parentId:
            parentEvent = self.eventMap.get(event.parentId)
            if parentEvent:
                parentEvent.children.append(event)
        else:
            self.rootEvents.append(event)
        self.eventMap[event.eventId] = event

    def getRootEvents(self) -> List[Dict]:
        return list(map(lambda x: x.model_dump(), self.rootEvents))

    def getEventById(self, eventId: str) -> Optional[Event]:
        return self.eventMap.get(eventId)

    def clear(self) -> None:
        self.rootEvents.clear()
        self.eventMap.clear()
