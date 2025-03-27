import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin


class Thread:
    def __init__(self, name: str):
        self.name = name


class Session:
    def __init__(self, name: str, externalUserId: Optional[str] = None):
        self.name = name
        self.externalUserId = externalUserId


class Agent:
    def __init__(self, name: str):
        self.name = name


class Server:
    def __init__(self, apiKey: str, projectId: str, host: str):
        self.apiKey = apiKey
        self.projectId = projectId
        self.host = host

    def _doReq(self, config: Dict[str, Any]) -> Any:
        headers = config.get('headers', {})
        headers.update({
            'Content-Type': 'application/json',
            'x-observa-api-key': self.apiKey,
            'x-observa-project-id': self.projectId
        })
        try:
            response = requests.request(
                method=config['method'],
                url=config['url'],
                json=config.get('data'),
                headers=headers
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            raise Exception(error.response.json().get('message', '未知错误'))

    def createThread(self, thread: Thread) -> str:
        res = self._doReq({
            'url': urljoin(self.host, 'api/v1/thread'),
            'method': 'POST',
            'data': thread.__dict__
        })
        return res.json()['id']

    def createSession(self, session: Session) -> str:
        res = self._doReq({
            'url': urljoin(self.host, 'api/v1/session'),
            'method': 'POST',
            'data': session.__dict__
        })
        return res.json()['id']

    def createAgent(self, agent: Agent) -> str:
        res = self._doReq({
            'url': urljoin(self.host, 'api/v1/agent'),
            'method': 'POST',
            'data': agent.__dict__
        })
        return res.json()['id']

    def createEvent(self, event: Dict[str, Any]) -> None:
        self._doReq({
            'url': urljoin(self.host, 'api/v1/event'),
            'method': 'POST',
            'data': event
        })
