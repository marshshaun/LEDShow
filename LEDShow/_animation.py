from abc import ABCMeta, abstractmethod

class Animation(object):
    """ Animation base class defining common attributes and settings """
        
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, leds):
        """ Executes animations on the provided *leds* instance """
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def running():
        """ Returns the running state of the animation """
        return False

    @abstractmethod
    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 1

    @abstractmethod
    def pingLoop(self):
        return False

    
