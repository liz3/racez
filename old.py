import ctypes
import os
import sdl2
import sdl2.ext
import time
import sdl2.sdlimage
from PIL import Image
from random import randint


RESOURCES = sdl2.ext.Resources(__file__, "assets")
# This is an attempt to follow C++ Syntax on my conversion

def render_point(x,y,size,renderer):
    for targetX in range(x-size, x+size+1):
         for targetY in range(y-size, y+size+1):
             renderer.draw_point([targetX,targetY], sdl2.ext.Color(255,0,0))
    return

def get_direction(last, pix, x,y, step, checkval1, checkval2):
    next = None
    forbidden = None
    value = None
    nextDir = last
    try_set = -3
    try_set2 = -3
    if last == "-x":
        next = pix[x-checkval2, y]
        forbidden = "x"
    if last == "x":
        next = pix[x+checkval2, y]
        forbidden = "-x"
    if last == "-y":
        next = pix[x, y-checkval2]
        forbidden = "y"
    if last == "y":
        next = pix[x, y+checkval2]
        forbidden = "-y"
    tested = 0
    while next[2] != 0 or nextDir == forbidden:
        if tested > 4 and try_set <= 3:
            try_set +=1
            if try_set +1 % 2 ==0:
                value = None
            if try_set % 3 == 0 and try_set2 % 3 != 0:
                try_set+=1
            else:
                try_set2+=1
            xtt = nextDir
            if last == "-x":
                if value == None:
                    next = pix[x-checkval1+try_set, y+checkval1+try_set2]
                    value = (x-checkval1+try_set,y+checkval1+try_set)
                    nextDir = "y"
                else:
                    next = pix[x-checkval1+try_set, y-checkval1+try_set2]
                    value = (x-checkval1+try_set,y-checkval1+try_set2)
                    nextDir = "-y"
            if last == "x":
                if value == None:
                    next = pix[x+checkval1+try_set, y+checkval1+try_set2]
                    value = (x+checkval1+try_set,y+checkval1+try_set2)
                    nextDir = "y"
                else:
                    next = pix[x+checkval1+try_set, y-checkval1+try_set2]
                    value = (x+checkval1+try_set,y-checkval1+try_set2)
                    nextDir = "-y"
            if last == "y":
                if value == None:
                    next = pix[x+checkval1+try_set, y+checkval1+try_set2]
                    value = (x+checkval1+try_set,y+checkval1+try_set2)
                    nextDir = "x"
                else:
                    next = pix[x-checkval1+try_set, y+checkval1+try_set2]
                    value = (x-checkval1+try_set,y+checkval1+try_set2) 
                    nextDir = "-x"
            if last == "-y":
                if value == None:
                    next = pix[x+checkval1+try_set, y-checkval1+try_set2]
                    value = (x+checkval1+try_set,y-checkval1+try_set2)
                    nextDir = "x"
                else:
                    next = pix[x-checkval1+try_set, y-checkval1+try_set2]
                    value = (x-checkval1+try_set,y-checkval1+try_set2)
                    nextDir = "-x"
            if next[2] == 0:
                break
            else:
                nextDir = xtt
        tested+=1          
        if nextDir == "-x":
            nextDir = "-y"
            next = pix[x, y-checkval2]
        elif nextDir == "x":
            nextDir = "y"
            next = pix[x, y+checkval2]
        elif nextDir == "y":
            nextDir = "-x"
            next = pix[x-checkval2, y]
        elif nextDir == "-y":
            nextDir = "x"
            next = pix[x+checkval2, y]
    if value != None:
        x = value[0]
        y = value[1]
        if nextDir == "-x":
            corrected = calc_adjustment("y", "-y", pix, x,y)
            return (nextDir, x, y+corrected[0]-corrected[1])
        if nextDir == "x":
            corrected = calc_adjustment("-y", "y", pix, x,y)
            return (nextDir, x, y+corrected[1]-corrected[0])
        if nextDir == "y":
            corrected = calc_adjustment("x", "-x", pix, x,y)
            return (nextDir, x-corrected[1]+corrected[0], y)
        if nextDir == "-y":
            corrected = calc_adjustment("-x", "x", pix, x,y)
            return (nextDir, x-corrected[0]+corrected[1], y)
    if nextDir == "-x":
        corrected = calc_adjustment("y", "-y", pix, x,y)
        return (nextDir, x-step, y+corrected[0]-corrected[1])
    if nextDir == "x":
        corrected = calc_adjustment("-y", "y", pix, x,y)
        return (nextDir, x+step, y+corrected[1]-corrected[0])
    if nextDir == "y":
        corrected = calc_adjustment("x", "-x", pix, x,y)
        return (nextDir, x-corrected[1]+corrected[0], y+step)
    if nextDir == "-y":
        corrected = calc_adjustment("-x", "x", pix, x,y)
        return (nextDir, x-corrected[0]+corrected[1], y-step)
def calc_adjustment(left,right, pix, x,y):
    distRight = 0
    distLeft = 0
    while True:
        next = None
        if right == "x":
            next = pix[x+distRight+1,y]
        if right == "-x":
            next = pix[x-distRight-1,y]
        if right == "-y":
            next = pix[x,y-distRight-1]
        if right == "y":
            next = pix[x,y+distRight+1]
        if next[2] != 0:
            break
        distRight+=1
    while True:
        next = None
        if left == "x":
            next = pix[x+distLeft+1,y]
        if left == "-x":
            next = pix[x-distLeft-1,y]
        if left == "-y":
            next = pix[x,y-distLeft-1]
        if left == "y":
            next = pix[x,y+distLeft+1]
        if next[2] != 0:
            break
        distLeft+=1
    correctLeft = 0
    correctRight = 0    
    if distLeft - distRight >= distLeft-1:
        if distLeft > 10:
            correctLeft = 0
        elif distLeft >= 1:
            correctLeft = 1
        else:
            correctLeft = distLeft
    if distRight - distLeft >= distRight-1:
        if distRight > 10:
            correctRight = 0
        elif distRight >= 1:
            correctRight =1
        else:
            correctRight = distRight    
    return (correctLeft, correctRight)


def main():
    sdl2.ext.init()
    raw_img = Image.open("assets/monza-graphic.png")
    pix = raw_img.load()
    print(pix[1100, 655])
    window = sdl2.ext.Window("Hello World!", size=(raw_img.size[0], raw_img.size[1]))
    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(renderer=renderer) # Creating Sprite Factory
    texture = factory.from_image("assets/monza-graphic.jpg")
    x = 1100
    y = 655
    direction = "-x"
    window.show()
    running = True
    while running:
        renderer.clear()
        result = get_direction(direction, pix,x,y,2, 2,2)
        direction = result[0]
        x = result[1]
        y = result[2]
        renderer.copy(texture)
        render_point(x, y, 3, renderer)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        renderer.present()
        sdl2.timer.SDL_Delay(25)
    return 0

if __name__ == "__main__":
    main()