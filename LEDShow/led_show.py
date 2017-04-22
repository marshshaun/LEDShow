import time
from ping_sensor import PingSensor
from repeat_timer import RepeatTimer
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

    #current ping sensor distance(cm)
    distance = 0
    animations = []
    animationIndex = 0
    currentAnimation = None

    def __init__(self):

        #initialize ping sensor
        sensor = PingSensor(self.setDistance)
        
        #initialize neopixel object
        strip = Adafruit_NeoPixel(LEDShow.LED_COUNT, LEDShow.LED_PIN, LEDShow.LED_FREQ_HZ, LEDShow.LED_DMA, LEDShow.LED_INVERT, LEDShow.LED_BRIGHTNESS)
        strip.begin()	    

        strip.setPixelColorRGB(0, 0, 0, 0)
        strip.setPixelColor(8, Color(0, 0, 0))
        strip.setPixelColor(16, Color(0,0,0))
        strip.show()
        
        LEDShow.animations = [AnimationWipe(), AnimationGreen(), AnimationBlue()]   
        self.nextAnimation()                     
            

    def setDistance(self, d):
        distance = d
        print("distance: "+str(distance))

    def nextAnimation(self):
        if not(LEDShow.currentAnimation == None):
            LEDShow.currentAnimation.stop()
        LEDShow.currentAnimation = LEDShow.animations[LEDShow.animationIndex]
        LEDShow.currentAnimation.start()
        LEDShow.animationIndex = 0 if (LEDShow.animationIndex == len(LEDShow.animations)-1) else (LEDShow.animationIndex + 1)

