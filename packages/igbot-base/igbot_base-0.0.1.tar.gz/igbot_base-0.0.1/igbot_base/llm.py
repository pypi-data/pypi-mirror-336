from abc import ABC, abstractmethod
from builtins import dict
from typing import Optional

from igbot_base.igbot_base.exception_handler import ExceptionHandler, NoopExceptionHandler
from igbot_base.igbot_base.llmmemory import LlmMemory
from igbot_base.igbot_base.models import Model


class Llm(ABC):

    def __init__(
            self,
            name: str,
            model: Model,
            temperature: float,
            response_format: Optional[dict],
            llm_exception_handler: ExceptionHandler = NoopExceptionHandler()):
        self._name = name
        self._model = model
        self._temperature = temperature
        self._format = response_format
        self._exception_handler = llm_exception_handler

    @abstractmethod
    def _call(self, user_query: str, history: LlmMemory, params: dict) -> str:
        pass

    def _revert_memory(self, history: LlmMemory):
        history.revert_to_snapshot()

    def call(self, user_query: str, history: LlmMemory, params: dict) -> str:
        history.set_snapshot()
        try:
            return self._call(user_query, history, params)
        except Exception as e:
            self._revert_memory(history)
            self._exception_handler.handle(e)

    def get_additional_llm_args(self):
        args = {}
        if self._temperature is not None:
            args["temperature"] = self._temperature
        if self._format is not None:
            args["response_format"] = self._format

        return args
