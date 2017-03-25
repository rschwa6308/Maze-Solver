from PIL import Image
import numpy as np
# from time import sleep
import sys
import os
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import time



#legend
wall = 0
path = 1
visited = 2
solution = 3

black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0,0, 255)



# encapsulating maze class
class Maze():
    def __init__(self, img):
        img.convert("1")
        self.solvable = False

        self.img = img
        self.maze = np.asarray(img).astype(int)
        self.maze.flags.writeable = True


        #find coords of start and end
        whites = np.where(self.maze == 1)
        self.start = (whites[1][0], whites[0][0])
        self.end = (whites[1][-1], whites[0][-1])


        print self.start, self.end

        
        
        

    def __repr__(self):
        # block = u"\u2588".encode("utf-8")
        # star = u"\u2605".encode("utf-8")
        # space = u"\u2591".encode("utf-8")
        return "\n".join(["".join([("X", " ", " ", "*")[cell] for cell in row]) for row in self.maze])

    
    def solve(self, x=None, y=None):
        if x == None:
            x, y = self.start

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
                return True
            
        if (x, y) == self.end:
            self.maze[y][x] = solution
            self.solvable = True
            return True

        return False


    def get_output_img(self):
        wall_color = black
        path_color = white
        visited_color = white
        solution_color = red


        img_array_rgb = np.asarray(self.img.convert("RGB"))
        img_array_rgb.flags.writeable = True
        for y in range(len(self.maze) - 1):
            for x in range(len(self.maze[0]) - 1):
                img_array_rgb[y][x] = (wall_color, path_color, visited_color, solution_color)[self.maze[y][x]]
        img_array_rgb[self.end[1]][self.end[0]] = solution_color
        img = Image.fromarray(img_array_rgb)
        return img





# define func to get image filename through GUI
def getFilename():
    root = tk.Tk()

    name = tkFileDialog.askopenfilename(filetypes = (("png files","*.png"), ("bmp files", "*.bmp"), ("all files","*.*")))
    root.destroy()
    return name[name.index("Solver/") + 7:]




if __name__ == "__main__":
    np.set_printoptions(threshold="nan")

    name = getFilename()
    # name = "maze1"  + ".png"          #uncomment this line to override TK gui file selection

    # print name
    start_time = time.clock()
    
    source = Image.open(name)

    sys.setrecursionlimit(100000000)

    maze = Maze(source)
    maze.solve()
    # print maze.maze


    end_time = time.clock()
    print start_time, end_time
    print end_time - start_time

    if (maze.solvable):
        output = maze.get_output_img()
        output_name = name[:-4] + "_solution.png"
        output.save(output_name)
        
        os.system(output_name)
    else:
        end_time = time.clock()
        top = tk.Tk()
        top.wm_withdraw()
        tkMessageBox.showinfo("Result", "The maze, '" + name + "', is not solvable.")


    
    

