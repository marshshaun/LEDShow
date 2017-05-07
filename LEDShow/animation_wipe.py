from _animation import Animation
import time
import utils

class AnimationWipe(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self):
        """ Initializes running state """
        self.reset()

    def run(self, leds):      

        """ Maps color range to distance and applies results to bisected strip """
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, leds.distance):
            self.distance = leds.distance
            self.bottomIndex = 0    
            self.topIndex = 0
            self.pixel = int(utils.mapRange(self.distance, 1.0, 350, 0.0, leds.numPixels()-1))        
        
        #animation
        self.startTime = time.time()
        self.bottomSection(leds, self.pixel)
        self.topSection(leds, self.pixel)

    def reset(self):
        self.bottomIndex = 0
        self.topIndex = 0
        self.distance = 0

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3

    def waitForPing(self):
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05
    
    def bottomSection(self, leds, pixel):
        for i in range(self.bottomIndex, pixel):
            leds.setPixelColor(i, pixel, 24, 0)
            leds.show()
            if self.waitForPing():
                self.bottomIndex = i
                return

    def topSection(self, leds, pixel):
        for i in range(self.topIndex, leds.numPixels()-pixel):
            leds.setPixelColor(i+pixel, 0, 80, pixel*2)
            leds.show()
            if self.waitForPing():
                self.topIndex = i
                return
