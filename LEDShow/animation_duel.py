from _animation import Animation
import time
import utils

class AnimationDuel(Animation):

    def __init__(self, leds):
        self.leds = leds
        self.pixels = leds.numPixels()
        self.stop() 
        self.half = 0
        self.steps = 50
        self.colors = [
            (255, 163, 0),
            (0, 255, 255), 
            (238, 130, 238), 
            (154, 255, 50), 
            (255, 69, 0), 
            (5, 60, 73),
            (0, 125, 255), 
            (125, 255, 0)
            ]

    def run(self):      

        self._stop = False
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance
            index = int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), len(self.colors)-1, 0))
            self.color = self.colors[index]
        
        #animation
        self.startTime = time.time()
        if not self._started:
            self.startAnimation()
        else:
            self.alternate()

    def stop(self):
        self._stop = True
        self._started = False
        self.distance = 0
        self.half = 0

    def pingInterval(self):
        return 1

    def waitForPing(self):
        pass
    
    def startAnimation(self):
        c1 = self.colors[0]
        c2 = self.colors[1]

        for i in range(self.pixels/2 + 1):
            self.leds.setPixelColor(i, c1[0], c1[1], c1[2])
            self.leds.setPixelColor(self.pixels-i, c2[0], c2[1], c2[2])
            self.leds.show()
            if self._stop:
                return
        self._started = True

    def alternate(self):
        pixel = 0 if self.half == 0 else self.pixels-1
        current = self.leds.getPixelColor(pixel)
        if not utils.colorsAreEqual(self.color, current):
            utils.crossFade(current, self.color, self.fade, self.half, self.steps)
            self.half = 0 if self.half == 1 else 1

    def fade(self, color, context):
        if context == 0:
            for i in range(self.pixels/2 + 1):
                self.leds.setPixelColor(i, color[0], color[1], color[2])
        else:
            for i in range(self.pixels/2):
                self.leds.setPixelColor(self.pixels-i, color[0], color[1], color[2])
        self.leds.show()

