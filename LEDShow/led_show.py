import time
from ping_sensor import PingSensor
import RPi.GPIO as GPIO
from neopixel import *
import utils
from repeat_timer import RepeatTimer
from random import randint

from animation_wipe import AnimationWipe
from animation_pulse import AnimationPulse
from animation_leap import AnimationLeap
from animation_mirror import AnimationMirror
from animation_duel import AnimationDuel
from animation_wave import AnimationWave
from animation_squares import AnimationSquares

class LEDShow(object):
    """ LEDShow manages the ultrasonic sensor readings and the LED animation sequence. """

    # LED strip configuration:
    LED_COUNT      = 1536        # Number of LED pixels.
    LED_PIN        = 18         # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5          # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 100        # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)

    #Sensor configuration
    ANIMATION_DURATION = 300     # The collective inactive (non animating) time from animation start to finish(trigger next animation)
    MAX_DISTANCE = 300.0         # The maximum distance accepted from the ultrasonic sensor (cm)
    MIN_DISTANCE = 80.0          # The minimum distance accepted from the ultrasonic sensor (cm)
    RANDOMIZE = True             # Next animation is selected randomly


    def __init__(self):
        """ Initialize sensor readings and led animations """
        
        #initialize ping sensor and register callback
        self.sensor = PingSensor(self.setDistance)
        
        #initialize neopixel object
        self.strip = Adafruit_NeoPixel(LEDShow.LED_COUNT, LEDShow.LED_PIN, LEDShow.LED_FREQ_HZ, LEDShow.LED_DMA, LEDShow.LED_INVERT, LEDShow.LED_BRIGHTNESS)
        self.strip.begin()	   
        
        #grid conversion
        self.grid = utils.stripToGrid(LEDShow.LED_COUNT, 8)
        
        ###SHUFFLE THESE!!!
        #list of animations to cycle through
        self.animations = [
            AnimationWipe(self),
            AnimationPulse(self),
            AnimationLeap(self),                        
            AnimationMirror(self), 
            AnimationDuel(self),
            AnimationWave(self), 
            AnimationSquares(self)
            ]   

        #initialized animation index
        self.animationIndex = -1     
        
        #animation duration timer
        if len(self.animations) > 1:  
            self.timer = RepeatTimer()
            self.timer.start(LEDShow.ANIMATION_DURATION, self.nextAnimation)

        #initialize animations
        self.currentAnimation = None
        self.nextAnimation()
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
        self.startPingInterval = time.time()
        
        #only update animation when new distance is less than MAX_DISTANCE
        #and current animation is valid
        distance = int(d)
        if not self.currentAnimation == None:
            self.distance = distance
            self.currentAnimation.run()

    def nextAnimation(self):
        """ Queues the next animation in the list and updates the sensor interval.
            If the current animation is at the end of the list, the sequence starts over.
        """
        #next index
        if LEDShow.RANDOMIZE:
            index = self.animationIndex
            while index == self.animationIndex:
                index = randint(0, len(self.animations)-1)
            self.animationIndex = index
        else:
            self.animationIndex = 0 if (self.animationIndex == len(self.animations)-1) else (self.animationIndex + 1)

        if not self.currentAnimation == None:
            self.currentAnimation.stop()

        self.currentAnimation = self.animations[self.animationIndex]
        print(self.currentAnimation)

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


    def getPixelColorXY(self, x, y):
        return self.getPixelColor(self.grid[x][y])


    def setRowColor(self, row, red, green, blue):
        """ Set entire a row to the provided color """
        if row < len(self.grid[0]):
            for x in range(len(self.grid)):
                self.setPixelColorXY(x, row, red, green, blue)


    def getRowCount(self):
        return len(self.grid[0])


    def getColumnCount(self):
        return len(self.grid)


    def setColumnColor(self, column, red, green, blue):
        """ Set entire column to the provided color """
        if column < len(self.grid):
            for y in range(len(self.grid[0])):
                self.setPixelColorXY(column, y, red, green, blue)

    def setGridColor(self, red, green, blue):
        for i in range(self.numPixels()):
            self.setPixelColor(i, red, green, blue)

    def drawSquare(self, x, y, width, height, red, green, blue):
        for w in range(width):
            for h in range(height):
                self.setPixelColorXY(x+w, y-h, red, green, blue)


    def show(self):
        """ Refresh LEDs """
        self.strip.show()

    def numPixels(self):
        """ The strips LED count """
        return self.strip.numPixels()

    def setBrightness(self, brightness):
        LEDShow.LED_BRIGHTNESS = brightness 
        self.strip.setBrightness(LEDShow.LED_BRIGHTNESS)

    def getBrightness(self):
        return LEDShow.LED_BRIGHTNESS

    def getMaxDistance(self):
        return LEDShow.MAX_DISTANCE

    def getMinDistance(self):
        return LEDShow.MIN_DISTANCE



