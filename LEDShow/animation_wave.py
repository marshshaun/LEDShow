from _animation import Animation
import time
import utils
import math

class AnimationWave(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self, leds):
        """ Initializes running state """
        self.leds = leds
        self.distance = 0
        self.init = True
        self.y = 0.0
        self.x = 3
        self.xDirection = -1
        self.yIncrement = 2
        self.colorPairs = [
            [(0,0,255),(0,255,0)],
            [(0,0,255), (255, 165, 0)],
            [(0,255,255), (255, 255, 0)],
            [(255,0,0), (0, 0, 255)],
            ]

    def run(self):      

        """ Maps color range to distance and applies results to bisected strip """

        self._stop = False

        #fade to back on init
        if self.init:
            self.brightness = self.leds.getBrightness()
            self.init = False
            b = self.leds.getBrightness()
            utils.transitionBrightness(b, 0, self.fade)
        self.leds.setBrightness(self.brightness)
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance
            self.colors = self.colorPairs[int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), 3, 0))]
        
        #animation
        self.startTime = time.time()   

        #animation
        while not self.waitForPing():
            self.wave()

    def fade(self, brightness):
        self.leds.setBrightness(brightness)
        if(brightness == 0):
            self.leds.setGridColor(0,0,0)
        self.leds.show()

    def stop(self):
        self._stop = True
        self.distance = 0
        self.y = 0.0
        self.x = 3
        self.xDirection = -1
        self.init = True

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 1

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05

    def wave(self):

        #altrenating colors
        for column in range(5):
            color = self.colors[column % 2] 
            xVal = utils.clamp(self.x - (column-3), 0, 7)
            self.leds.setPixelColorXY(xVal, int(self.y), color[0], color[1], color[2])

        #horizontal direction
        if self.x == 7:
            self.xDirection = -1
        elif self.x == 0:
            self.xDirection = 1        
        self.x += self.xDirection

        #vertical offset
        self.y = self.y + self.yIncrement if self.y + self.yIncrement < self.leds.getRowCount() else 0.0

        #reset animation and swap colors
        if self.y == 0.0:
            self.x = 3
            tmp = self.colors[0]
            self.colors[0] = self.colors[1]
            self.colors[1] = tmp


        #display
        self.leds.show()