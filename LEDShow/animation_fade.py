from _animation import Animation
import time
from random import randint
import utils

class AnimationFade(Animation):
    """PLACEHOLDER ANIMATION"""

    """
    Pulse alternate colors every four pulses
    *Seperate animation - brightness based on distance (randome color)
    """

    def __init__(self):
        self._running = False

    def run(self, leds):
        self._running = True

        brightness = 100

        leds.setBrightness(brightness)
        leds.setGridColor(0, 0, 255)
        leds.show()

        direction = -1
        while True: 
            brightness += direction
            leds.setBrightness(brightness)
            leds.show()
            time.sleep(0.1)
            if brightness <= 0:
                direction = 1
            elif brightness >= 100:
                direction = -1

        self._running = False

    def running(self):
        return self._running

    def stop(self):
        self._running = False

    def pingInterval(self):
        return 1

    def pingLoop(self):
        return True


   