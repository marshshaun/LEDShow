from _animation import Animation
import time
import utils
from random import randint

class AnimationLeap(Animation):

    def __init__(self):
        self._running = False
        self.colors = [
            (randint(0,255), randint(0,255), randint(0,0)), 
            (randint(0,255), randint(0,255), randint(0,0)),
            (randint(0,255), randint(0,255), randint(0,0)),
            (randint(0,255), randint(0,255), randint(0,0)),
            (randint(0,255), randint(0,255), randint(0,0)),
            (randint(0,255), randint(0,255), randint(0,0))]
        self.background = (0,0,0)#utils.randomColor()

    def run(self, leds):
       self._running = True

       rowCount = leds.getRowCount() 
       self.interval = int(rowCount/6)
       
       c = 0
       self.rows = []
       #for row in range(0, rowCount, self.interval):
       #    self.rows.append(row)
       #    if c < len(self.colors)-1:
       #       self.drawSquare(leds, 0, row, self.colors[c])
       #    c += 1
       #    leds.show()

       row = self.interval
       self.rows.append(row)
       self.drawSquare(leds, 0, row, self.colors[0])
       row += self.interval
       self.rows.append(row)
       self.drawSquare(leds, 0, row, self.colors[1])
       row += self.interval
       self.rows.append(row)
       self.drawSquare(leds, 0, row, self.colors[2])
       row += self.interval
       self.rows.append(row)
       self.drawSquare(leds, 0, row, self.colors[3])
       row += self.interval
       self.rows.append(row)
       self.drawSquare(leds, 0, row, self.colors[4])
       row += self.interval
       self.rows.append(row)
       self.drawSquare(leds, 0, row, self.colors[5])
       leds.show()

       self.swap(leds, 0, 1)
       self.swap(leds, 1, 2)
       self.swap(leds, 2, 3)
       self.swap(leds, 3, 4)
       self.swap(leds, 4, 5)

       self.swap(leds, 5, 4)
       self.swap(leds, 4, 3)
       self.swap(leds, 3, 2)
       self.swap(leds, 2, 1)
       self.swap(leds, 1, 0)

       self._running = False

    def stop(self):
        self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 1

    def pingLoop(self):
        return False

    def drawSquare(self, leds, x, y, c):
        for w in range(8):
            for h in range(self.interval):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])                                 

    def clearSquare(self, leds, x, y, c):
        for w in range(8):
            for h in range(self.interval):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])

    def swap(self, leds, a, b):
        r1 = self.rows[a]
        r2 = self.rows[b]
        direction = 1 if r2 > r1 else -1

        for i in range(r1, r2+direction, direction):
            self.clearSquare(leds, 0, r1, self.background) 
            self.drawSquare(leds, 0, i+direction, self.colors[a])           
            leds.show()
        
        c = self.colors[b]  
        self.animateToColor(leds, r2-1, c[0], c[1], c[2], 4)      

        for j in range(r2, r1-direction, -direction):
            self.clearSquare(leds, 0, r2, self.colors[a])
            self.drawSquare(leds, 0, j-direction, self.colors[b])
            leds.show()
            

        tmp = self.colors[a]
        self.colors[a] = self.colors[b]
        self.colors[b] = tmp

    def animateToColor(self, leds, row, r, g, b, increment=4):
        """
        Linearly transitions from current color to target color

        Attributes:
            leds: Reference to LED instance
            r: Target red value
            g: Target green value
            b: Target blue value
            increment: The value to incremeent by (the higher the value the quicker the animation)
        """

        # current pixel color of column
        current = leds.getPixelColorXY(0, row)

        # current rgb values
        red = current[0]
        green = current[1]
        blue = current[2]

        # rgb deltas
        rDelta = r - red
        gDelta = g - green
        bDelta = b - blue

        #delta directions
        rDirection = increment if rDelta > 0 else -increment
        gDirection = increment if gDelta > 0 else -increment
        bDirection = increment if bDelta > 0 else -increment

        #maximim delta
        spread = int(max(abs(rDelta), abs(gDelta), abs(bDelta)) /increment)      

        #animate current color to new color
        while spread > 0:
            
            if not r == red:
                red += rDirection  
            if not g == green:
                green += gDirection
            if not b == blue:
                blue += bDirection  

            red = utils.clamp(red, 0, 255)                
            green = utils.clamp(green, 0, 255)
            blue = utils.clamp(blue, 0, 255)
            
            self.drawSquare(leds, 0, row, (red, green, blue))
            leds.show()

            spread -= 1
    