from abc import ABCMeta, abstractmethod

class Animation(object):
    """ Animation base class defining common attributes and settings """
        
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, leds):
        """ Executes animations on the provided *leds* instance """
        pass

    @abstractmethod
    def reset(self):
        """ Restore initial state """
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

    
