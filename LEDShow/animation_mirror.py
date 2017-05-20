from _animation import Animation
import time
import utils

class AnimationMirror(Animation):

    def __init__(self, leds):
        self.distance = 0
        self.pingCount = 0
        self.background = (0, 0, 0)
        self.height = 8 if leds.numPixels() <= 256 else 16
        self.min = float(self.height - 1)
        self.max = leds.getRowCount() -1
        self.leds = leds
        self.position = int(self.min)

    def run(self):
       self._stop = False

        #distance change
       if not utils.withinAccuracyRange(self.distance, self.leds.distance):
           self.distance = self.leds.distance   
           self.destination = int(utils.mapRange(self.leds.distance, self.leds.getMinDistance(), self.leds.getMaxDistance(), self.max, self.min))

       #change colors onse
       if self.pingCount % 60 == 0:
           self.randomizeColors()
       self.pingCount += 1
            
       #animate squares
       self.squares()

    def stop(self):
        self._stop = True
        self.position = int(self.min)
        self.distance = 0
        self.pingCount = 0  
        self.background = (0,0,0)

    def pingInterval(self):
        return 1

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05

    def randomizeColors(self):
        self.color1 = utils.randomColor()
        self.color2 = utils.randomColor()

        utils.crossFade(self.background, utils.randomColor(), self.fade, 0)

        fromColor1 = self.leds.getPixelColorXY(0, self.position)
        utils.crossFade(fromColor1, self.color1, self.fade, 1)
   
        fromColor2 = self.leds.getPixelColorXY(0, self.mirror(self.position))
        utils.crossFade(fromColor2, self.color2, self.fade, 2)

    def fade(self, color, context):
        if context == 0:
            self.leds.setGridColor(color[0], color[1], color[2])
            self.background = color
        elif context == 1:
            self.drawSquare(0, self.position, color)
        else:
            self.drawSquare(0, self.mirror(self.position), color)
        self.leds.show()

    def squares(self):
        self.startTime = time.time()
        if not self.position == self.destination:
            direction = 1 if self.destination > self.position else -1
            for i in range(self.position, self.destination, direction): 
                self.clearSquare(0, i)
                self.clearSquare(0, self.mirror(i))

                self.position = i+direction
                self.drawSquare(0, self.position, self.color1)
                self.drawSquare(0, self.mirror(self.position), self.color2)

                self.leds.show()
                if self.waitForPing():
                    return

    def mirror(self, y):
        return int(self.max - (y - self.min))

    def drawSquare(self, x, y, c):
        for w in range(8):
            for h in range(self.height):
                self.leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])                                 

    def clearSquare(self, x, y):
        for w in range(8):
            for h in range(self.height):
                self.leds.setPixelColorXY(x+w, y-h, self.background[0], self.background[1], self.background[2])