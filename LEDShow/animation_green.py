from animation import Animation
import time

class AnimationGreen(Animation):
    """description of class"""

    def __init__(self):
        pass

    def run(self, strip):
       for i in range(strip.numPixels()):
            strip.setPixelColorRGB(i, 255, 0, 0)
            strip.show()
            time.sleep(21/500)


