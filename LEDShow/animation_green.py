from _animation import Animation
import time
import utils

class AnimationGreen(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self.row = -1
        self._running = False

    def run(self, leds):
       self._running = True
       row = int(utils.mapRange(leds.distance, 80.0, 312.0, 31.0, 0.0))
       if not(self.row == row):
           leds.setRowColor(self.row, 0, 0, 0)
           self.row = row
           leds.setRowColor(self.row, 0, 255, 0)
           leds.show()
       self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 0.5


