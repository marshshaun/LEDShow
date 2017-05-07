from _animation import Animation
import time
import utils

class AnimationSunset(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self.sunState = -1
        self.skyState = -1
        self.min = 6.0
        self._running = False

        self.colors = [
            [(255,163,0),(229,148,0),(0,255,255),(0,89,89)],
            [(204,40,40),(255,255,0),(0,229,229),(101,101,204)],
            [(255,165,0),(255,182,47),(137,207,240),(0,0,255)],
            [(50,50,255),(0,0,255),(0,0,255),(0,0,128)]
            ]

    def run(self, leds):
       self._running = True
       leds.setBrightness(130)
       self.max = leds.getRowCount() - 2
       #self.sun(leds)
       self.sky(leds)
       self._running = False

    def stop(self):
        self.sunState = -1
        self.skyState = -1
        self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 2000

    def pingLoop(self):
        return False

    """
    *10 colors from color wheel
    *intro top bottom meet in the middle fill
    *alternate fade sections between top and bottom
    *assign fixed color order to distance
    """
    def sky(self, leds):
        state = int(utils.mapRange(leds.distance, 80.0, 312.0, 3, 0))
        pixels = leds.numPixels()
        for i in range(pixels/2):
            leds.setPixelColor(i, 255, 163, 0)
            leds.setPixelColor(pixels-i, 0, 255, 255)
            leds.show()

        time.sleep(5)
        self.animateToColor(leds, 255, 0, 0, 0, 0, 255, 1)

    def sun(self, leds):
        y = int(utils.mapRange(leds.distance, 80.0, 312.0, self.max, self.min))
        if(self.sunState == y):
            return
        if(self.sunState == -1):
            self.sunState = y
            leds.drawSquare(0, self.sunState, 8, 12, 0, 255, 255)
            leds.show()
        else:
            direction = 1 if y > self.sunState else -1
            for i in range(self.sunState, y, direction):
                self.clearSquare(leds, 1, i, direction)
                leds.drawSquare(0, i+direction, 8, 12, 0, 255, 255)
                leds.show()
                time.sleep(0.05)
            self.sunState = y

    def clearSquare(self, leds, x, y, direction):
        pixel = y - 5 if direction > 0 else y 
        c = leds.getPixelColorXY(0,pixel)
        for w in range(6):
            for h in range(6):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])

    def animateToColor(self, leds, r1, g1, b1, r2, g2, b2, increment=4):
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
        current1 = leds.getPixelColor(0)
        current2 = leds.getPixelColor(leds.numPixels()-1)

        # current rgb values
        red1 = current1[0]
        green1 = current1[1]
        blue1 = current1[2]

        red2 = current2[0]
        green2 = current2[1]
        blue2 = current2[2]

        # rgb deltas
        rDelta1 = r1 - red1
        gDelta1 = g1 - green1
        bDelta1 = b1 - blue1

        rDelta2 = r2 - red2
        gDelta2 = g2 - green2
        bDelta2 = b2 - blue2

        #delta directions
        rDirection1 = increment if rDelta1 > 0 else -increment
        gDirection1 = increment if gDelta1 > 0 else -increment
        bDirection1 = increment if bDelta1 > 0 else -increment

        rDirection2 = increment if rDelta2 > 0 else -increment
        gDirection2 = increment if gDelta2 > 0 else -increment
        bDirection2 = increment if bDelta2 > 0 else -increment

        #maximim delta
        spread1 = int(max(abs(rDelta1), abs(gDelta1), abs(bDelta1)) /increment)      
        spread2 = int(max(abs(rDelta2), abs(gDelta2), abs(bDelta2)) /increment)      

        spread = int(max(spread1, spread2))

        #animate current color to new color
        while spread > 0:
            
            if not r1 == red1:
                red1 += rDirection1  
            if not g1 == green1:
                green1 += gDirection1
            if not b1 == blue1:
                blue1 += bDirection1                                                        

            if not r2 == red2:
                red2 += rDirection2  
            if not g2 == green2:
                green2 += gDirection2
            if not b2 == blue2:
                blue2 += bDirection2

            rows = leds.getRowCount()
            for row in range(rows/2):
                leds.setRowColor(row, red1, green1, blue1)
                leds.setRowColor(rows-row, red2, green2, blue2)
            leds.show()
            time.sleep(0.05)

            spread -= 1