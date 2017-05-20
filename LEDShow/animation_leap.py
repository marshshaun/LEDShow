from _animation import Animation
import time
import utils
from random import randint
from math import floor

class AnimationLeap(Animation):

    def __init__(self, leds):
        self.leds = leds
        self.distance = 0
        self.pingCount = 0
        self.position = 0 
        self.destination = 0

        self.sections = 6
        rowCount = leds.getRowCount() 
        self.interval = int(floor(rowCount/self.sections))

        self.background = (0,0,0)

    def run(self):

        self._stop = False

        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance   
            self.destination = int(utils.mapRange(self.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), self.sections-1, 0))              

        #change colors every set interval 
        if self.pingCount % 60 == 0:      
            self.fillSections()  
        self.pingCount += 1

        #leap animation
        self.leap()      

    def stop(self):
        self._stop = True
        self.distance = 0
        self.pingCount = 0
        self.position = 0
        self.destination = 0

    def pingInterval(self):
        return 1

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05

    def fillSections(self):
        self.rows = []
        self.row = -1
        self.randomizeColors()

        for i in range(self.sections):
            self.row += self.interval
            self.rows.append(self.row)

            fromColor = self.leds.getPixelColorXY(0, self.row)
            utils.crossFade(fromColor, self.colors[i], self.fade, 0)          

        #fade remaining to black
        self.excess = []
        for i in range(self.rows[self.sections-1]+1, self.leds.getRowCount()):
            self.excess.append(i)
            fromColor = self.leds.getPixelColorXY(0, i)
            utils.crossFade(fromColor, self.background, self.fade, 1)
    
    def randomizeColors(self):
        self.colors = [
        self.randomRG(), 
        self.randomRG(),
        self.randomRG(),
        self.randomRG(),
        self.randomRG(),
        self.randomRG()]

    def randomRG(self):
        return (randint(10,255), randint(0,255), randint(0,0))

    def drawSquare(self, x, y, c):
        for w in range(8):
            for h in range(self.interval):
                self.leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])                                 

    def clearSquare(self, x, y, c):
        for w in range(8):
            for h in range(self.interval):
                self.leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])

    def leap(self):
        self.startTime = time.time()
        if not self.position  == self.destination: 
            direction = 1 if self.destination > self.position else -1
            for i in range(self.position, self.destination, direction):
                self.position = i+direction
                self.swap(i, self.position)    
                if self.waitForPing():
                    return        
            

    def swap(self, a, b):
        r1 = self.rows[a] 
        r2 = self.rows[b] 
        direction = 1 if r2 > r1 else -1

        for i in range(r1, r2, direction):
            self.clearSquare(0, r1, self.background) 
            self.drawSquare(0, i+direction, self.colors[a])           
            self.leds.show()       

        self.row = r2 
        fromColor = self.leds.getPixelColorXY(0, self.row)
        toColor = self.colors[b]          
        utils.crossFade(fromColor, toColor, self.fade)

        for j in range(r2, r1, -direction):
            self.clearSquare(0, r2, self.colors[a])
            self.drawSquare(0, j-direction, self.colors[b])
            self.leds.show()     

        tmp = self.colors[a]
        self.colors[a] = self.colors[b]
        self.colors[b] = tmp


    def fade(self, color, context):
        if context == 0:
            self.drawSquare(0, self.row, color)
        elif context == 1:
            for i in range(len(self.excess)):
                self.leds.setRowColor(self.excess[i], color[0], color[1], color[2])
        self.leds.show()
    