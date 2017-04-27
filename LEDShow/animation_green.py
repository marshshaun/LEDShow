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
       self.colorRow(leds, row)
       self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 1

    def colorRow(self, leds, row):
        if(self.row == row):
            return
        if(self.row == -1):
            self.row = row
            leds.setRowColor(self.row, 0, 255, 0)
            leds.show()
        else:
            direction = 1 if row > self.row else -1
            for i in range(self.row, row, direction):
                leds.setRowColor(i, 0, 0, 0)
                leds.setRowColor(i+direction, 0, 255, 0)
                leds.show()
                time.sleep(0.05)
            self.row = row
            



