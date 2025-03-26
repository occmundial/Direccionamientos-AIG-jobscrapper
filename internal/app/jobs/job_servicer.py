from abc import ABC, abstractmethod


class JobServicer(ABC):
    @abstractmethod
    def Start(self):
        pass