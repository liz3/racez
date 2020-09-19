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
def is_included(last, x,y):
    for entry in last:
        if entry[0] == x and entry[1] == y:
            return True
    return False
def get_next(pix, last, x,y, start, info_points):
   # print(x,y)
    if x == start[0] and y == start[1]:
        if start[2] == "-x":
             xStart = x-1
             for yTarget in range(-1,1):
                 pixelData = pix[xStart, y+yTarget]
                 if pixelData[2] < 30:
                     return (xStart, y+yTarget, [(start[0], start[1]), (xStart, yTarget), (xStart, yTarget)], None, info_points)
    else:
        flag = None
        coords = None
        for xTarget in range(x-2,x+2):
            for yTarget in range(y-2,y+2):
                pixelData = pix[xTarget, yTarget]
                if pixelData[2] < 30 and coords == None:
                    if not is_included(last, xTarget, yTarget):
                        coords = (xTarget, yTarget)
                elif pixelData[1] > 244 and pixelData[0] < 240 and not is_included(info_points, xTarget, yTarget):
                    flag = "accelerator"    
                    info_points.append((xTarget, yTarget)) 
                elif pixelData[0] > 244 and pixelData[1] < 240 and not is_included(info_points, xTarget, yTarget):
                    flag = "break"
                    info_points.append((xTarget, yTarget)) 
                    print(xTarget, yTarget)
        return (coords[0], coords[1], [(coords[0], coords[1])] + last[0:5], flag, info_points)


def main():
    sdl2.ext.init()
    raw_img = Image.open("assets/monza-graphic.png")
    pix = raw_img.load()
    print(pix[1100, 655])
    window = sdl2.ext.Window("Hello World!", size=(raw_img.size[0], raw_img.size[1]))
    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(renderer=renderer) # Creating Sprite Factory
    texture = factory.from_image("assets/monza-graphic.png")
    last = []
    info_points = []
    start = (1079, 657, "-x")
    x = start[0]
    y = start[1]
    accelerator = True
    brake = False
    window.show()
    running = True
    while running:
        renderer.clear()
        result = get_next(pix, last, x,y,start, info_points)
        x = result[0]
        y = result[1]
        last = result[2]
        flag = result[3]
        info_points = result[4]
        if flag != None:
            if flag == "break":
                brake = not brake
                if brake:
                    accelerator = False
            elif flag == "accelerator":
                accelerator = True
            print(brake, accelerator)
        if x == start[0] and y == start[1]:
            info_points = []
            print("LAP")
        renderer.copy(texture)
        render_point(x, y, 3, renderer)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
      #  sdl2.SDL_Delay(200)
        renderer.present()
    return 0

if __name__ == "__main__":
    main()