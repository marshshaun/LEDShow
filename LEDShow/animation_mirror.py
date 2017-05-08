from _animation import Animation
import time
import utils

"""
*Add ping interrupt
*Slow background crossfade every set interval 20s or so
"""
class AnimationMirror(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self, leds):
        self.background = (0,0,0)
        self.color1 = utils.randomColor()
        self.color2 = utils.randomColor()
        self.y1 = -1
        self.min = 6.0
        self.count = 0
        self.leds = leds

    def run(self):
       self.count += 1
       if self.count == 5:
           self.count = 0
           self.y1 = -1     
       self.max = self.leds.getRowCount() - 2
       self.squares(self.leds)

    def stop(self):
        self.y1 = -1       

    def pingInterval(self):
        return 1000

    def waitForPing(self):
        pass

    def squares(self, leds):
        y = int(utils.mapRange(leds.distance, 80.0, 312.0, self.max, self.min))
        if(self.y1 == y):
            return
        if(self.y1 == -1):
            self.y1 = y
            self.background = utils.randomColor()
            leds.setGridColor(self.background[0], self.background[1], self.background[2])      
            self.drawSquare(leds, 0, self.y1, self.color1)    
            self.drawSquare(leds, 0, self.mirror(self.y1), self.color2)                                    
            leds.show()
        else:
            direction = 1 if y > self.y1 else -1
            for i in range(self.y1, y, direction): 
                self.clearSquare(leds, 1, i)
                self.clearSquare(leds, 1, self.mirror(i))
                self.drawSquare(leds, 1, i+direction, self.color1)
                self.drawSquare(leds, 1, self.mirror(i+direction), self.color2)
                leds.show()
                time.sleep(0.05)
            self.y1 = y

    def mirror(self, y):
        return int(self.max - (y - self.min))

    def drawSquare(self, leds, x, y, c):
        for w in range(8):
            for h in range(20):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])                                 

    def clearSquare(self, leds, x, y):
        for w in range(8):
            for h in range(20):
                leds.setPixelColorXY(x+w, y-h, self.background[0], self.background[1], self.background[2])