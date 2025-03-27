from abc import abstractmethod
from igbot_base.igbot_base.llmmemory import LlmMemory


class PersistableMemory(LlmMemory):

    @abstractmethod
    def save(self):
        pass
