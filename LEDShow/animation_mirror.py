from _animation import Animation
import time
import utils

class AnimationMirror(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self.background = (0, 0, 0)
        self.color1 = (0, 255, 0)
        self.color2 = (255, 0, 255)
        self.y1 = -1
        self.min = 6.0
        self._running = False

    def run(self, leds):
       self._running = True
       self.max = leds.getRowCount() - 2
       self.squares(leds)
       self._running = False

    def stop(self):
        self.y1 = -1
        self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 1

    def pingLoop(self):
        return False

    def squares(self, leds):
        y = int(utils.mapRange(leds.distance, 80.0, 312.0, self.max, self.min))
        if(self.y1 == y):
            return
        if(self.y1 == -1):
            self.y1 = y
            leds.setGridColor(self.background[0], self.background[1], self.background[2])      
            self.drawSquare(leds, 1, self.y1, self.color1)    
            self.drawSquare(leds, 1, self.mirror(self.y1), self.color2)                                    
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
        for w in range(6):
            for h in range(6):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])                                 

    def clearSquare(self, leds, x, y):
        for w in range(6):
            for h in range(6):
                leds.setPixelColorXY(x+w, y-h, self.background[0], self.background[1], self.background[2])