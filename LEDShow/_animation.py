from abc import ABCMeta, abstractmethod

class Animation(object):
    """ Animation base class defining common attributes and settings """
        
    __metaclass__ = ABCMeta

    def __init__(self, leds):
        pass

    @abstractmethod
    def run(self):
        """ Executes animations on the provided *leds* instance """
        pass

    @abstractmethod
    def stop(self):
        """ Stop and reset animation """
        pass

    @abstractmethod
    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 1

    @abstractmethod
    def waitForPing(self):
        """ Intended to trigger just before ping to allow interruption of animation loops 
        so they aren't locking the main thread """
        return False

    
