import time
from ping_sensor import PingSensor
import RPi.GPIO as GPIO
from neopixel import *
import utils

from animation_blue import AnimationBlue
from animation_green import AnimationGreen
from animation_wipe import AnimationWipe
from animation_warmer import AnimationWarmer
from animation_pulse import AnimationPulse

class LEDShow(object):
    """ LEDShow manages the ultrasonic sensor readings and the LED animation sequence. """

    # LED strip configuration:
    LED_COUNT      = 256        # Number of LED pixels.
    LED_PIN        = 18         # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5          # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 10         # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)

    #Sensor configuration
    ANIMATION_DURATION = 30     # The collective inactive (non animating) time from animation start to finish(trigger next animation)
    MAX_DISTANCE = 350          # The maximum distance accepted from the ultrasonic sensor (cm)
    ACCURACY = 5                # The difference in distance between readings needs to be greater than this value to trigger an update.


    def __init__(self):
        """ Initialize sensor readings and led animations """
        
        #initialize ping sensor and register callback
        self.sensor = PingSensor(self.setDistance)
        
        #initialize neopixel object
        self.strip = Adafruit_NeoPixel(LEDShow.LED_COUNT, LEDShow.LED_PIN, LEDShow.LED_FREQ_HZ, LEDShow.LED_DMA, LEDShow.LED_INVERT, LEDShow.LED_BRIGHTNESS)
        self.strip.begin()	   
        
        #grid conversion
        self.grid = utils.stripToGrid(LEDShow.LED_COUNT, 8)
        
        #list of animations to cycle through
        self.animations = [
            AnimationPulse()
            #AnimationWipe(), 
            #AnimationGreen(), 
            #AnimationBlue(),
            #AnimationWarmer()
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
        """ The sensor callback evaluates the reported distance then sends it to the current
            animation when a change is detected. Also queues the next animation when the 
            *ANIMATION_DURATION* has expired.
        """

        #increment animation time
        self.animationTime += self.pingInterval
        self.startPingInterval = time.time()
        
        #only update animation when new distance is less than MAX_DISTANCE,
        #differs(within the ACCURACY range) from the previous,
        #and the animation is inactive (not currently running)
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
        """ Returns True if the provided distance is within a certain number 
            of centimeters of the current distance. 
        """
        return d > self.distance - LEDShow.ACCURACY and d < self.distance + LEDShow.ACCURACY


    def nextAnimation(self):
        """ Queues the next animation in the list and updates the sensor interval.
            If the current animation is at the end of the list, the sequence starts over.
        """
        self.currentAnimation = self.animations[self.animationIndex]
        self.animationIndex = 0 if (self.animationIndex == len(self.animations)-1) else (self.animationIndex + 1)
        self.animationTime = 0
        self.distance = 0
        self.pingInterval = self.currentAnimation.pingInterval()        


    def clearPixels(self):
        """ Clears all pixels in the strip """
        for i in range(self.numPixels()):
            self.setPixelColor(i, 0, 0, 0)
        self.show()


    def setPixelColor(self, pixel, red, green, blue):
        """ Set specified LED to RGB value """
        if pixel < LEDShow.LED_COUNT:
            red = utils.clamp(red, 0, 255)
            green = utils.clamp(green, 0, 255)
            blue = utils.clamp(blue, 0, 255)
            self.strip.setPixelColorRGB(pixel, green, red, blue)  #GRB to RGB


    def getPixelColor(self, pixel):
        """ Return RGB value of specified pixel """
        return utils.intToRGB(self.strip.getPixelColor(pixel))

    
    def setPixelColorXY(self, x, y, red, green, blue):
        """ Set color of pixel at specified grid location """
        if x < len(self.grid) and y < len(self.grid[0]):
            self.setPixelColor(self.grid[x][y], red, green, blue)


    def setRowColor(self, row, red, green, blue):
        """ Set entire a row to the provided color """
        if row < len(self.grid[0]):
            for x in range(len(self.grid)):
                self.setPixelColorXY(x, row, red, green, blue)


    def setColumnColor(self, column, red, green, blue):
        """ Set entire column to the provided color """
        if column < len(self.grid):
            for y in range(len(self.grid[0])):
                self.setPixelColorXY(column, y, red, green, blue)

    def setGridColor(self, red, green, blue):
        for i in range(self.numPixels()):
            self.setPixelColor(i, red, green, blue)


    def show(self):
        """ Refresh LEDs """
        self.strip.show()


    def numPixels(self):
        """ The strips LED count """
        return self.strip.numPixels()

