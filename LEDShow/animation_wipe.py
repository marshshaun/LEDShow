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
        self._running = False

        #color range
        x = int(utils.mapRange(leds.distance, 1.0, 350, 0.0, leds.numPixels()-1))

        #bottom section
        for i in range(x):
           leds.setPixelColor(i, x, 24, 0)
           leds.show()
           time.sleep(42/1000)

        #top section
        for i in range(256-x):
           leds.setPixelColor(i+x, 0, 80, x*2)
           leds.show()
           time.sleep(35/1000.0)

        self._running = False

    def running(self):
        """ Returns the running state of the animation """
        return self._running

    def stop(self):
        self._running = False

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3

    def pingLoop(self):
        return False