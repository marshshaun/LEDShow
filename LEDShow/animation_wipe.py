from animation import Animation
import time

class AnimationWipe(Animation):
    """description of class"""

    def __init__(self):
        self._running = False

    def run(self, leds):      
       self._running = True

       x = int(self.controlrange(leds.distance, 1.0, 350, 0.0, 255.0))
       print(x)

       for i in range(x):
           leds.setPixelColor(i, 24, x, 0)
           leds.show()
           time.sleep(21/500.0)

       for i in range(256-x):
           leds.setPixelColor(i+x, 80, 0, x*2)
           leds.show()
           time.sleep(21/600.0)

       self._running = False

    def running(self):
        return self._running

    def pingInterval(self):
        return 3

    def	controlrange(self, OldValue, OldMin, OldMax, NewMin, NewMax, clamp = True):
	    NewValue = ( (OldValue - OldMin) / (OldMax - OldMin) ) * (NewMax - NewMin) + NewMin

	    if clamp == True:
		    if NewValue < NewMin:
			    NewValue = NewMin
		    if NewValue > NewMax:
			    NewValue = NewMax
	    return NewValue