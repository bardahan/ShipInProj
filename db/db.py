from abc import ABC, abstractmethod


class DB(ABC):

    @abstractmethod
    def select(self, query, params=None):
        pass

    @abstractmethod
    def insert(self, query, params):
        pass
