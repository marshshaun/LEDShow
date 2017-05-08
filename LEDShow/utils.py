from random import randint
import time

def mapRange(num, min1, max1, min2, max2, clamp=True):
    """
    Linearly maps and incoming value from one range to another

    Attributes:
        num:    Incoming value to be mapped
        min1:   Incoming minimum range value
        max1:   Incoming maximum range value
        min2:   Outgoing minimum range value
        max2:   Outgoing maximum range value
        clamp:  Whether the returned value is constrained to the min and max values

    Return:     Mapped value
            
    """
    if(clamp and num < min1):
        return min2
    if(clamp and num > max1):
        return max2

    num1 = (num - min1) / (max1 - min1)
    num2 = (num1 * (max2 - min2)) + min2
    return num2


def clamp(num, min, max):
    """
    Constrain number to specified range
    
    Attributes:
        num: The number to clamp
        min: Minimum range value
        max: Maximum range value     
    """ 
    if num < min:
        num = min
    elif num > max:
        num = max
    return num



def stripToGrid(pixelCount, columnCount):
    """
    Converts neopixel linear strip positions to row/column grid coordinates (bottom left origin)
    
    Attributes:
        pixelCount:  Number of pixels 
        columnCount: Number of columns          

    Return: A 2 dimensional array with linear positions mapped to grid 

    """
    rowCount = int(pixelCount/columnCount)
    grid = [[0 for x in range(rowCount)] for y in range(columnCount)]

    pixel = 0
    for y in range(rowCount):
        for x in range(columnCount):  
            column = x if y%2 == 0 else columnCount-1-x
            grid[column][y] = pixel            
            pixel += 1            

    return grid


def intToRGB(RGBInt):
    """
    Converts 24-bit RGB color value to RGB

    Attributes:
        RGBInt: Color value to convert
    """
    b = RGBInt & 255
    r = (RGBInt >> 8) & 255
    g = (RGBInt >> 16) & 255
    return (r,g,b)

def colorsAreEqual(color1, color2):
    return color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]

def randomColor():
    return (randint(0,255), randint(0,255), randint(0,255))

def withinAccuracyRange(oldDistance, newDistance, range = 5):
    return newDistance > oldDistance - range and newDistance < oldDistance + range

def crossFade(fromColor, toColor, onStep, context = None, steps=20):

    fRed = fromColor[0]
    fGreen = fromColor[1]
    fBlue = fromColor[2]

    tRed = toColor[0]
    tGreen = toColor[1]
    tBlue = toColor[2]

    stepRed = (float(tRed) - float(fRed)) / steps
    stepGreen = (float(tGreen) - float(fGreen)) / steps
    stepBlue = (float(tBlue) - float(fBlue)) / steps

    for i in range(steps):
        fRed += stepRed
        fGreen += stepGreen
        fBlue += stepBlue

        if not onStep == None:
            onStep((int(fRed), int(fGreen), int(fBlue)), context)

def transitionBrightness(fromBrightness, toBrightness, onStep, steps=10):
    step = (float(toBrightness) - float(fromBrightness)) / steps
    for i in range(steps):
        fromBrightness += step
        onStep(int(fromBrightness))


            