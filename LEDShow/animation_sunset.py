from _animation import Animation
import time
import utils

class AnimationSunset(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self.y1 = -1
        self.min = 6.0
        self._running = False

    def run(self, leds):
       self._running = True
       self.sun(leds)
       self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 1

    def pingLoop(self):
        return False

    def sun(self, leds):
        self.max = leds.getRowCount() - 2
        y = int(utils.mapRange(leds.distance, 80.0, 312.0, self.max, self.min))
        if(self.y1 == y):
            return
        if(self.y1 == -1):
            self.y1 = y
            for i in range(leds.getRowCount()):
                c = (255, 0, 0) if i < leds.getRowCount()/2 else (0, 0, 255)
                leds.setRowColor(i, c[0], c[1], c[2])
            leds.drawSquare(1, self.y1, 6, 6, 255, 255, 255)
            leds.show()
        else:
            direction = 1 if y > self.y1 else -1
            for i in range(self.y1, y, direction):
                self.clearSquare(leds, 1, i, direction)
                leds.drawSquare(1, i+direction, 6, 6, 255, 255, 255)
                leds.show()
                time.sleep(0.05)
            self.y1 = y

    def clearSquare(self, leds, x, y, direction):
        pixel = y - 5 if direction > 0 else y 
        c = leds.getPixelColorXY(0,pixel)
        for w in range(6):
            for h in range(6):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])