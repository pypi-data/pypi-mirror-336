from abc import ABC, abstractmethod

from igbot_base.igbot_base.agent_response import AgentResponse


class Agent(ABC):

    @abstractmethod
    def invoke(self, query) -> AgentResponse:
        pass