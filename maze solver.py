from PIL import Image
import numpy as np
# from time import sleep
import sys
import os
import Tkinter as tk
import tkFileDialog
from time import sleep

import pygame as pg






#legend
wall = 0
path = 1
visited = 2
solution = 3

black = (0,0,0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)



# encapsulating maze class
class Maze():
    def __init__(self, img):
        self.img = img
        self.maze = np.asarray(img)
        self.maze.flags.writeable = True

        #find coords of start and end
        whites = np.where(self.maze == 1)
        self.start = (whites[1][0], whites[0][0])
        self.end = (whites[1][-1], whites[0][-1])


        print self.start, self.end

        
        
        

    def __repr__(self):
        block = u"\u2588".encode("utf-8")
        star = u"\u2605".encode("utf-8")
        space = u"\u2591".encode("utf-8")
        return "\n".join(["".join([("X", " ", " ", "*")[cell] for cell in row]) for row in self.maze])

    
    def solve(self, x=None, y=None):
        if x == None:
            x, y = self.start

        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
            color = [black, blue, blue, red][self.maze[y][x]]
            pg.draw.rect(self.screen, color, pg.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size), 0)
            pg.display.update()
        except:
            pass

        if y >= len(self.maze) or x >= len(self.maze[0]):
            return False

        # print x, y
        # print self
        # print "\n"
        # sleep(0.01)

        if self.maze[y][x] == path or (x, y) == self.start:
            self.maze[y][x] = visited
            if (self.solve(x+1, y) or self.solve(x-1, y) or
                self.solve(x, y+1) or self.solve(x, y-1)):
                    self.maze[y][x] = solution
                    try:
                        color = [black, white, blue, red][self.maze[y][x]]
                        pg.draw.rect(self.screen, color, pg.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size), 0)
                        pg.display.update()
                    except:
                        pass
                    return True
            
        if (x, y) == self.end:
            self.maze[y][x] = solution
            return True

        return False


    def get_output_img(self):
        img_array_rgb = np.asarray(self.img.convert("RGB"))
        img_array_rgb.flags.writeable = True
        for y in range(len(self.maze) - 1):
            for x in range(len(self.maze[0]) - 1):
                img_array_rgb[y][x] = (black, white, white, red)[self.maze[y][x]]
        img_array_rgb[self.end[1]][self.end[0]] = red
        img = Image.fromarray(img_array_rgb)
        return img





# define func to get image filename through GUI
def getFilename():
    root = tk.Tk()
    # name = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

    name = tkFileDialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
    root.destroy()
    return name[name.index("Solver/") + 7:]






def display(screen, maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = [black, white, white, red][maze[y][x]]
            pg.draw.rect(screen, color, pg.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size), 0)
            # screen.set_at((x, y), color)
    pg.display.update()





if __name__ == "__main__":

    name = getFilename()
    # name = "maze1"  + ".png"          #uncomment this line to override TK gui file selection

    # print name
    source = Image.open(name)

    sys.setrecursionlimit(100000)

    pixel_size = int(round(800.0 / max(source.width, source.height)))
    print(pixel_size)
    screen = pg.display.set_mode((source.width * pixel_size, source.height * pixel_size))

    maze = Maze(source)
    maze.screen = screen
    display(screen, maze.maze)
    maze.solve()
    # print maze


    output = maze.get_output_img()
    output_name = name[:-4] + "_solution.png"
    output.save(output_name)
    os.system(output_name)

    alive = True
    while alive:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                alive = False
                pg.display.quit()

                
