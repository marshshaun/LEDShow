from _animation import Animation
import time
import utils

class AnimationWarmer(Animation):
    """PLACEHOLDER ANIMATION"""

    def __init__(self):
        self._running = False
        self.colors = (255, 65535, 16711680, 16776960, 65280)

    def run(self, leds):
        self._running = True
        color = int(utils.mapRange(leds.distance, 50.0, 350.0, 4.0, 0.0))
        rgb = utils.intToRGB(self.colors[color])
        self.animateToColor(leds, rgb[0], rgb[1], rgb[2])
        self._running = False

    def running(self):
        return self._running

    def pingInterval(self):
        return 1

    def animateToColor(self, leds, r, g, b, increment=4):
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
        current = leds.getPixelColor(0)

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

            leds.setGridColor(red, green, blue)
            leds.show()

            spread -= 1

