from _animation import Animation
import time

class AnimationBlue(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self._running = False

    def run(self, leds):
        self._running = True
        for i in range(leds.numPixels()):
            leds.setPixelColor(i, 0, 0, 255)
            leds.show()
            time.sleep(21/500)
        self._running = False

    def running(self):
        return self._running

    def pingInterval(self):
        return 1