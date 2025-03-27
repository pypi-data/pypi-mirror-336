from abc import ABC, abstractmethod

from igbot_base.igbot_base.retriever import Retriever


class Metadata:

    def __init__(self):
        self.metadata = {}

    def append(self, key, value):
        if key not in self.metadata:
            self.metadata[key] = set()

        self.metadata[key].add(value)

    def get(self):
        return self.metadata.copy()


class Vectorstore(ABC):

    @abstractmethod
    def remove_db(self):
        pass

    @abstractmethod
    def get_dimensions_number(self):
        pass

    @abstractmethod
    def get_retriever(self, load_number_of_chunks) -> Retriever:
        pass

    @abstractmethod
    def get_legacy_retriever(self, load_number_of_chunks):
        pass

    @abstractmethod
    def append(self, chunks):
        pass

    @abstractmethod
    def get_metadata(self) -> Metadata:
        pass
