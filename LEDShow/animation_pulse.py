from _animation import Animation
import time

class AnimationPulse(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self._running = False

    def run(self, leds):
        self._running = True
        self.leds = leds
        self.pulseColor(0, 255, 233, leds.distance)
        self._running = False

    def running(self):
        return self._running

    def pingInterval(self):
        return 1

    def pingLoop(self):
        return True

    def pulseColor(self, r, g, b, distance):
        #center
        self.setColumns(3, 4, r, g, b, False)
        
        #on
        self.setColumns(2, 5, r, g, b)
        self.setColumns(1, 6, r, g, b)
        self.setColumns(0, 7, r, g, b)

        #off
        self.setColumns(0, 7, 0, 0, 0)
        if distance > 120:
            self.setColumns(1, 6, 0, 0, 0)
        if distance > 300:
            self.setColumns(2, 5, 0, 0, 0)

    def setColumns(self, column1, column2, r, g, b, animate=True):
        if animate:
            self.animateColumnsToColor(column1, column2, r, g, b)
        else:
            self.leds.setColumnColor(column1, r, g, b)
            self.leds.setColumnColor(column2, r, g, b)
            self.leds.show()

    def animateColumnsToColor(self, column1, column2, r, g, b, increment=3):

        # current pixel color of column
        current = self.leds.getPixelColor(column1)

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

            self.leds.setColumnColor(column1, red, green, blue)
            self.leds.setColumnColor(column2, red, green, blue)
            self.leds.show()

            spread -= 1