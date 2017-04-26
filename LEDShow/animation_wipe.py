from _animation import Animation
import time
import utils

class AnimationWipe(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self):
        """ Initializes running state """
        self._running = False

    def run(self, leds):      

        """ Maps color range to distance and applies results to bisected strip """
        self._running = True

        #color range
        x = int(utils.mapRange(leds.distance, 1.0, 350, 0.0, 255.0))

        #bottom section
        for i in range(x):
           leds.setPixelColor(i, x, 24, 0)
           leds.show()
           time.sleep(21/500.0)

        #top section
        for i in range(256-x):
           leds.setPixelColor(i+x, 0, 80, x*2)
           leds.show()
           time.sleep(21/600.0)

        self._running = False

    def running(self):
        """ Returns the running state of the animation """
        return self._running

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3

    def	controlrange(self, OldValue, OldMin, OldMax, NewMin, NewMax, clamp = True):
        """ Maps color range to distance """
        newValue = ((OldValue - OldMin) /(OldMax - OldMin)) * (NewMax - NewMin) + NewMin

        if clamp:
            if(newValue < NewMin):
                newValue = NewMin
            if(newValue > NewMax):
                newValue = NewMax

        return newValue