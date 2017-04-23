from animation import Animation
import time

class AnimationGreen(Animation):
    """description of class"""

    def __init__(self):
        pass

    def run(self, leds):
       for i in range(leds.numPixels()):
            leds.setPixelColor(i, 255, 0, 0)
            leds.show()
            time.sleep(21/500)

    def pingInterval(self):
        return super().pingInterval()


