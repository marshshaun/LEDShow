import time
from ping_sensor import PingSensor
import RPi.GPIO as GPIO
from neopixel import *
from animation_blue import AnimationBlue
from animation_green import AnimationGreen
from animation_wipe import AnimationWipe

class LEDShow(object):

    # LED strip configuration:
    LED_COUNT      = 256        # Number of LED pixels.
    LED_PIN        = 18         # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5          # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 10         # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)

    ANIMATION_DURATION = 60     # The collective inactive (non animating) time from animation start to finish(trigger next animation)
    MAX_DISTANCE = 350          
    ACCURACY = 5                

    def __init__(self):

        #initialize ping sensor
        self.sensor = PingSensor(self.setDistance)
        
        #initialize neopixel object
        self.strip = Adafruit_NeoPixel(LEDShow.LED_COUNT, LEDShow.LED_PIN, LEDShow.LED_FREQ_HZ, LEDShow.LED_DMA, LEDShow.LED_INVERT, LEDShow.LED_BRIGHTNESS)
        self.strip.begin()	    
        
        #list of animations to cycle through
        self.animations = [
            AnimationWipe(), 
            AnimationGreen(), 
            AnimationBlue()
            ]   

        #index of current animation
        self.animationIndex = 0       

        #initialize animations
        self.nextAnimation()
        self.pingInterval = self.currentAnimation.pingInterval()
        self.startPingInterval = time.time()

        #ping loop
        try:
            GPIO.setmode(GPIO.BOARD)
            self.sensor.ping()

            #emit ping every interval defined by the animation
            while(True):
                self.endPingInterval = time.time() - self.startPingInterval
                if(self.endPingInterval >= self.pingInterval):
                    self.sensor.ping()

        #cleanup
        finally: 
            GPIO.cleanup()
            self.clearPixels()


    def setDistance(self, d):

        #increment animation time
        self.animationTime += self.pingInterval
        self.startPingInterval = time.time()
        print("distance: "+str(d)+" "+str(self.animationTime)+" "+str(self.currentAnimation.running()))  
        
        #only update animation when new distance is less than MAX_DISTANCE
        #and differs(within the ACCURACY range) from the previous 
        distance = int(d)
        if(distance < LEDShow.MAX_DISTANCE 
           and not self.withinAccuracyRange(distance)
           and not self.currentAnimation.running()):
            self.distance = distance
            self.currentAnimation.run(self)

        #bypass cycling if less than 2 animations
        if(len(self.animations) < 2):
            return

        #trigger next animation
        if(self.animationTime >= LEDShow.ANIMATION_DURATION):
            self.nextAnimation()


    def withinAccuracyRange(self, d):
        return d > self.distance - 5 and d < self.distance + 5


    def nextAnimation(self):
        self.currentAnimation = self.animations[self.animationIndex]
        self.animationIndex = 0 if (self.animationIndex == len(self.animations)-1) else (self.animationIndex + 1)
        self.animationTime = 0
        self.distance = 0
        self.pingInterval = self.currentAnimation.pingInterval()        

    def clearPixels(self):
        for i in range(self.numPixels()):
            self.setPixelColor(i, 0, 0, 0)
        self.show()

    def setPixelColor(self, pixel, red, green, blue):
        self.strip.setPixelColorRGB(pixel, red, green, blue)

    def show(self):
        self.strip.show()

    def numPixels(self):
        return self.strip.numPixels()

