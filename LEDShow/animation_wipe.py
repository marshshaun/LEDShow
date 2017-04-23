from animation import Animation
import time

class AnimationWipe(Animation):
    """description of class"""

    def __init__(self):
        self.show = False

    def run(self, leds):        
       for i in range(leds.numPixels()):
            leds.setPixelColor(i, 0, 255, 0)
            leds.show()
            time.sleep(21/500)

    def pingInterval(self):
        return 5

