from animation import Animation
import time

class AnimationBlue(Animation):
    """description of class"""

    def __init__(self):
        pass

    def run(self, strip):
        for i in range(strip.numPixels()):
            strip.setPixelColorRGB(i, 0, 0, 255)
            strip.show()
            time.sleep(21/500)


