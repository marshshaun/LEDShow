from _animation import Animation
import time
import utils

class AnimationPulse(Animation):

    def __init__(self, leds):
        self.leds = leds
        self.distance = 0

        #temp
        leds.setGridColor(0,0,255)
        leds.show()

    def run(self):    
        
        self._stop = False          

        #distance change
        if not utils.withinAccuracyRange(self.distance, self.leds.distance):
            self.distance = self.leds.distance   
            self.steps = int(utils.mapRange(self.distance, 80.0, 312.0, 10, 30))
            self.hold = int(utils.mapRange(self.distance, 80.0, 312.0, 0, 0.2))            

        self.pulse()

    def pulse(self):
        b = self.leds.getBrightness()
        utils.transitionBrightness(b, 0, self.fade, self.steps)
        time.sleep(self.hold)
        utils.transitionBrightness(0, 130, self.fade, self.steps)
        time.sleep(self.hold)

            
    def fade(self, brightness):
        self.leds.setBrightness(brightness)
        self.leds.show()

    def stop(self):
        self._stop = True
        self.distance = 0
        self.leds.setBrightness(130)

    def pingInterval(self):
        return 1

    def waitForPing(self):
        if self._stop:
            return True
        elapsed = time.time() - self.startTime
        return elapsed >= self.pingInterval() - 0.05
    