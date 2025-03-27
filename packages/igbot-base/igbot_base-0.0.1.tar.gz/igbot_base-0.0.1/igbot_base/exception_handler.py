from abc import ABC, abstractmethod


class ExceptionHandler(ABC):

    @abstractmethod
    def handle(self, e: Exception):
        pass


class NoopExceptionHandler(ExceptionHandler):

    def handle(self, e: Exception):
        pass


class PrintingExceptionHandler(ExceptionHandler):

    def handle(self, e: Exception):
        print(e)
