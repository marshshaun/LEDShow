from _animation import Animation
import time
import utils

class AnimationPulse(Animation):
    """ A bottom-to-top wiping animation that dynamically changeds colors based on sensor distance """

    def __init__(self):
        """ Initializes running state """
        self.reset()

    def run(self, leds):      

        """ Maps color range to distance and applies results to bisected strip """
        
        #distance change
        if not utils.withinAccuracyRange(self.distance, leds.distance):
            self.distance = leds.distance
            self.leds = leds

            fromColor = (0, 0, 0)
            toColor = (0, 0, 255)

            leds.setGridColor(fromColor[0], fromColor[1], fromColor[2])
            leds.show()
            time.sleep(1)
            utils.crossFade(fromColor, toColor, 20, self.fade)
            
    def fade(self, color):
        self.leds.setGridColor(color[0], color[1], color[2])
        self.leds.show()

    def reset(self):
        self.distance = 0

    def pingInterval(self):
        """ The perferred freqeuncy of distance updates from the sensor """
        return 3000

    def waitForPing(self):
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05
    