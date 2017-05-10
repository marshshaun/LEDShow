from _animation import Animation
import time
import utils
from random import randint

class AnimationPulse(Animation):

    def __init__(self, leds):
        self.leds = leds
        self.distance = 0
        self.pingCount = 0
        self.blue = self.randomBlue()

    def run(self):    
        
        self._stop = False  
        self.max = self.leds.getBrightness()      

        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance   
            self.steps = int(utils.mapRange(self.distance, 80.0, 312.0, 10, 30))
            self.hold = int(utils.mapRange(self.distance, 80.0, 312.0, 0, 0.2))            

        #switch to random blue color on every 4th ping
        if self.pingCount % 4 == 0:
            self.blue = self.randomBlue()
        self.pingCount += 1

        #run pulse animation
        self.pulse()

    def pulse(self):
        b = self.leds.getBrightness()
        utils.transitionBrightness(b, 0, self.fade, self.steps)
        time.sleep(self.hold)
        self.leds.setGridColor(self.blue[0], self.blue[1], self.blue[2])
        utils.transitionBrightness(0, self.max, self.fade, self.steps)
        time.sleep(self.hold)

            
    def fade(self, brightness):
        self.leds.setBrightness(brightness)
        self.leds.show()


    def randomBlue(self):
        return (randint(0, 5), randint(0, 200), randint(20,255))

    def stop(self):
        self._stop = True
        self.distance = 0
        self.pingCount = 0
        self.leds.setBrightness(self.max)

    def pingInterval(self):
        return 1

    def waitForPing(self):
        pass
    