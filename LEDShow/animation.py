from abc import ABCMeta, abstractmethod

class Animation(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, strip):
        pass


