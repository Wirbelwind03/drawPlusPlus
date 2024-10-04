from abc import ABC, abstractmethod

class BaseCommand(ABC):

    @abstractmethod
    def prepare(self, tokens, line_number):
        pass

    @abstractmethod
    def execute(self, cursors, canvas):
        pass