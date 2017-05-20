from _animation import Animation
import time
import utils
from random import randint

class AnimationSquares(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self, leds):
        """ Initializes running state """
        self.leds = leds
        self.distance = 0
        self.pingCount = 0

    def run(self):      

        """ Maps color range to distance and applies results to bisected strip """

        self._stop = False
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance
            self.count = int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), 30, 5))
            self.size = int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), 3, 10))
            self.rMax = int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), 0, 255))
            self.bMax = int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), 255, 0))
        
        #animation
        self.startTime = time.time()  
        
        self.pingCount += 1 

        while not self.waitForPing():
            self.randomizeSquares()


    def stop(self):
        self._stop = True
        self.distance = 0
        self.pingCount = 0

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05

    def randomizeSquares(self):
        self.setCoordinates()
        for j in range(self.count):

            color = (0,0,0) if j%5 == 0 else (randint(0, self.rMax), randint(0, 255), randint(0, self.bMax))

            for i in range(1, self.size):
                self.drawSquareAtCenter(self.coordinates[j][0], self.coordinates[j][1], i, color)
                self.leds.show()

    def setCoordinates(self):
        self.coordinates = []
        for i in range(self.count):
            self.coordinates.append((randint(0,7), randint(0,self.leds.getRowCount()-1)))


    def drawSquareAtCenter(self, x, y, size, color):
        midpoint = int(size/2)
        for w in range(size):
            for h in range(size):
                self.leds.setPixelColorXY(utils.clamp(x+w-midpoint, 0, 7), utils.clamp(y-h+midpoint, 0, self.leds.getRowCount()-1), color[0], color[1], color[2])

