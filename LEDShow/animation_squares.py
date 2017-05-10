from _animation import Animation
import time
import utils
import math

class AnimationSquares(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self, leds):
        """ Initializes running state """
        self.leds = leds
        self.distance = 0

    def run(self):      

        """ Maps color range to distance and applies results to bisected strip """

        self._stop = False
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance
        
        #animation
        self.startTime = time.time()   

        for i in range(6, 1, -1):
            self.drawSquareAtCenter(4, 10, i, utils.randomColor())                 
            self.leds.show()


    def stop(self):
        self._stop = True
        self.distance = 0

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 1

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05


    def drawSquareAtCenter(self, x, y, size, color):
        midpoint = int(size/2)
        for w in range(size):
            for h in range(size):
                self.leds.setPixelColorXY(x+w-midpoint, y-h+midpoint, color[0], color[1], color[2])