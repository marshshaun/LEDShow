from _animation import Animation
import time
import utils

class AnimationWipe(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self, leds):
        """ Initializes running state """
        self.leds = leds
        self.wipeCount = 6  #number of rows to wipe at a time
        self.stop() 
        self.temp = 0

    def run(self):      

        """ Maps color range to distance and applies results to bisected strip """

        self._stop = False
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance
            self.pixel = int(utils.mapRange(self.distance, 0.0, self.leds.getMaxDistance(), 50.0, self.leds.numPixels()-1))            
        
        #animation
        self.startTime = time.time()

        self.bottomSection(self.pixel)
        self.topSection(self.pixel)


        #self.bottomSectionOriginal(self.pixel)
        #self.topSectionOriginal(self.pixel)

    def stop(self):
        self._stop = True
        self.bottomIndex = 0
        self.topIndex = 0
        self.distance = 0
        self.top = True

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        interval = self.pingInterval() - 0.05
        wait = elapsed >= interval
        return wait
    
    #def bottomSectionOriginal(self, pixel):
    #    for i in range(self.bottomIndex, pixel):
    #        self.leds.setPixelColor(i, pixel, 24, 0)
    #        self.leds.show()
    #        if self.waitForPing():
    #            self.bottomIndex = i
    #            return

    #def topSectionOriginal(self, pixel):
    #    for i in range(self.topIndex, self.leds.numPixels()-pixel):
    #        self.leds.setPixelColor(i+pixel, 0, 80, pixel*2)
    #        self.leds.show()
    #        if self.waitForPing():
    #            self.topIndex = i
    #            return

    def bottomSection(self, pixel):
        row = int(pixel/self.leds.getColumnCount()) 
        direction = 1
        for i in range(self.bottomIndex, row, self.wipeCount):
            self.wipeRows(i, self.wipeCount, direction, pixel%256, 24, 0)
            direction = 1 if direction < 0 else -1
            if self.waitForPing():
                self.bottomIndex = i
                return
            self.bottomIndex = row
        self.top = True

    def topSection(self, pixel):
        row = int(pixel/self.leds.getColumnCount()) 
        direction = 1
        for i in range(self.topIndex, self.leds.getRowCount()-1, self.wipeCount):
            self.wipeRows(i, self.wipeCount, direction, 0, 80, (pixel%256)*2)
            direction = 1 if direction < 0 else -1
            if self.waitForPing():
                self.topIndex = i + self.wipeCount
                return  
            self.topIndex = row
        self.topIndex = 0
        self.bottomIndex = 0
        self.top = False
            

    def wipeRows(self, start, count, direction, r, g, b):
        x1 = self.leds.getColumnCount() if direction < 0 else 0
        x2 = self.leds.getColumnCount() if x1 == 0 else -1
        for x in range(x1, x2, direction):
            for y in range(start, start+count):
                self.leds.setPixelColorXY(x, y, r, g, b)
            self.leds.show()

