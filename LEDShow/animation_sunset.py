from _animation import Animation
import time
import utils

class AnimationSunset(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self.sunState = -1
        self.skyState = -1
        self.min = 6.0
        self._running = False

        self.colors = [
            [(255,163,0),(229,148,0),(0,255,255),(0,89,89)],
            [(204,40,40),(255,255,0),(0,229,229),(101,101,204)],
            [(255,165,0),(255,182,47),(137,207,240),(0,0,255)],
            [(50,50,255),(0,0,255),(0,0,255),(0,0,128)]
            ]

    def run(self, leds):
       self._running = True
       self.max = leds.getRowCount() - 2
       #self.sun(leds)
       self.sky(leds)
       self._running = False

    def stop(self):
        self.sunState = -1
        self.skyState = -1
        self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 2

    def pingLoop(self):
        return False

    def sky(self, leds):
        state = int(utils.mapRange(leds.distance, 80.0, 312.0, 3, 0))
        pixels = leds.numPixels()
        for i in range(pixels/2):
            leds.setPixelColor(i, 255, 163, 0)
            leds.setPixelColor(pixels-i, 0, 255, 255)
            leds.show()

    def sun(self, leds):
        y = int(utils.mapRange(leds.distance, 80.0, 312.0, self.max, self.min))
        if(self.sunState == y):
            return
        if(self.sunState == -1):
            self.sunState = y
            leds.drawSquare(0, self.sunState, 8, 12, 0, 255, 255)
            leds.show()
        else:
            direction = 1 if y > self.sunState else -1
            for i in range(self.sunState, y, direction):
                self.clearSquare(leds, 1, i, direction)
                leds.drawSquare(0, i+direction, 8, 12, 0, 255, 255)
                leds.show()
                time.sleep(0.05)
            self.sunState = y

    def clearSquare(self, leds, x, y, direction):
        pixel = y - 5 if direction > 0 else y 
        c = leds.getPixelColorXY(0,pixel)
        for w in range(6):
            for h in range(6):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])