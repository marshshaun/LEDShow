from animation import Animation
import time

class AnimationWipe(Animation):
    """description of class"""

    def __init__(self):
        self.show = False

    def run(self, strip):        
       for i in range(strip.numPixels()):
            strip.setPixelColorRGB(i, 0, 255, 0)
            strip.show()
            time.sleep(21/500)

