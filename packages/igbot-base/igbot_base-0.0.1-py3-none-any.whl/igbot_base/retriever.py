from abc import ABC, abstractmethod


class Retriever(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_relevant_data(self, query: str):
        pass
