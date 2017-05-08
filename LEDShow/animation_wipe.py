from _animation import Animation
import time
import utils

class AnimationWipe(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self, leds):
        """ Initializes running state """
        self.leds = leds
        self.stop() 

    def run(self):      

        """ Maps color range to distance and applies results to bisected strip """

        self._stop = False
        self.leds.setBrightness(30)
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance
            self.bottomIndex = 0    
            self.topIndex = 0
            self.pixel = int(utils.mapRange(self.distance, 1.0, 350, 0.0, self.leds.numPixels()-1))        
        
        #animation
        self.startTime = time.time()
        self.bottomSection(self.pixel)
        self.topSection(self.pixel)

    def stop(self):
        self._stop = True
        self.bottomIndex = 0
        self.topIndex = 0
        self.distance = 0

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05
    
    def bottomSection(self, pixel):
        for i in range(self.bottomIndex, pixel):
            self.leds.setPixelColor(i, pixel, 24, 0)
            self.leds.show()
            if self.waitForPing():
                self.bottomIndex = i
                return

    def topSection(self, pixel):
        for i in range(self.topIndex, self.leds.numPixels()-pixel):
            self.leds.setPixelColor(i+pixel, 0, 80, pixel*2)
            self.leds.show()
            if self.waitForPing():
                self.topIndex = i
                return
