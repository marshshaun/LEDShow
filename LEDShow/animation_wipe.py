from _animation import Animation
import time

class AnimationWipe(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self):
        """ Initializes running state """
        self._running = False

    def run(self, leds):      
        """ Maps color range to distance and applies results to bisected strip """
       self._running = True

       #color range
       x = int(self.controlrange(leds.distance, 1.0, 350, 0.0, 255.0))

       #bottom section
       for i in range(x):
           leds.setPixelColor(i, 24, x, 0)
           leds.show()
           time.sleep(21/500.0)

       #top section
       for i in range(256-x):
           leds.setPixelColor(i+x, 80, 0, x*2)
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
	    NewValue = ( (OldValue - OldMin) / (OldMax - OldMin) ) * (NewMax - NewMin) + NewMin

	    if clamp == True:
		    if NewValue < NewMin:
			    NewValue = NewMin
		    if NewValue > NewMax:
			    NewValue = NewMax
	    return NewValue