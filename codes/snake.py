import copy
import math
import random
import sys
import tkinter.messagebox
from tkinter import Tk, Canvas
from time import sleep


class Program:

    def __init__(self):

        self.HEIGHT = 720
        self.WIDTH = 1080
        self.X_BLOCKS_COUNT = 32
        self.BLOCK_SIZE = self.WIDTH / self.X_BLOCKS_COUNT
        self.Y_BLOCKS_COUNT = math.floor(self.HEIGHT / self.BLOCK_SIZE)
        self.TICK = 0.01666
        self.SPEED = self.BLOCK_SIZE * 0.3 * self.TICK

        self.COLORS = {
            "candy": "#f88",
            "body": "#8f8",
            "head": "#0a0"
        }

        self.running = True

        self.setup()

        self.master = Tk()
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.resizable(False, False)
        self.master.bind("<Button-1>", self.change_direction)

        self.canvas = Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg="#000")
        self.canvas.pack()

    def setup(self):

        self.direction = [1, 0]
        self.body_parts = [[self.X_BLOCKS_COUNT//2, self.Y_BLOCKS_COUNT // 2]]
        self.left_distance = [0, 0]

        self.map = []
        for y in range(self.Y_BLOCKS_COUNT):
            self.map.append([])
            for x in range(self.X_BLOCKS_COUNT):
                self.map[-1].append([])

        self.spawn_candy()
    def change_direction(self, event):

        if -1 in self.direction:
            if self.direction[0] == -1:
                self.direction = [0, -1]
            else: self.direction = [1, 0]
        else:
            if self.direction[0] == 1:
                self.direction = [0, 1]
            else: self.direction = [-1, 0]

    def spawn_candy(self):

        map_copy = copy.deepcopy(self.map)
        for body_part in self.body_parts:
            map_copy[body_part[1]][body_part[0]] = 1

        possible_places = []
        for y in range(len(map_copy)):
            for x in range(len(map_copy[y])):
                if map_copy[y][x] != 1:
                    possible_places.append([x,y])

        result_place = random.choice(possible_places)
        self.map[result_place[1]][result_place[0]] = "candy"

    def update_window(self):
        self.master.update()
        self.master.update_idletasks()

    def move(self):

        self.body_parts.append([self.body_parts[-1][0]+self.direction[0], self.body_parts[-1][1]+self.direction[1]])

        if self.body_parts[-1][1] >= len(self.map):
            self.body_parts[-1][1] = 0
        elif self.body_parts[-1][1] < 0:
            self.body_parts[-1][1] = len(self.map)-1

        if self.body_parts[-1][0] >= len(self.map[-1]):
            self.body_parts[-1][0] = 0
        elif self.body_parts[-1][0] < 0 :
            self.body_parts[-1][0] = len(self.map[-1])-1

        next_step = self.map[self.body_parts[-1][1]][self.body_parts[-1][0]]

        if next_step != "candy":
            self.body_parts.pop(0)
        else:
            self.map[self.body_parts[-1][1]][self.body_parts[-1][0]] = []
            self.spawn_candy()

        if [self.body_parts[-1][0], self.body_parts[-1][1]] in self.body_parts[:len(self.body_parts)-1]:
            tkinter.messagebox.showinfo("Oh no!", "You lose :(")
            self.setup()


    def calc_snake(self):

        if abs(sum(self.left_distance)) >= 1:
            for i in range(int(abs(sum(self.left_distance))//1)):
                self.move()
            self.left_distance = [0, 0]

    def draw_block(self, pos, fill):
        self.canvas.create_polygon(pos[0], pos[1]+self.BLOCK_SIZE, pos[0]+self.BLOCK_SIZE, pos[1]+self.BLOCK_SIZE,
                                   pos[0]+self.BLOCK_SIZE, pos[1], pos[0], pos[1], fill=fill)

    def render(self):

        for y, line in enumerate(self.map):
            for x, block in enumerate(line):
                if block == "candy":
                    self.draw_block([x*self.BLOCK_SIZE, y*self.BLOCK_SIZE], self.COLORS["candy"])

        for body_part in self.body_parts[:len(self.body_parts)-1]:
            self.draw_block([body_part[0]*self.BLOCK_SIZE, body_part[1]*self.BLOCK_SIZE], self.COLORS["body"])
        self.draw_block([self.body_parts[-1][0]*self.BLOCK_SIZE, self.body_parts[-1][1]*self.BLOCK_SIZE], self.COLORS["head"])

    def next_iteration(self):

        self.canvas.delete("all")
        self.left_distance = [self.left_distance[0] + self.direction[0] * self.SPEED, self.left_distance[1] + self.direction[1] * self.SPEED]
        self.calc_snake()
        self.render()


if __name__ == "__main__":

    program = Program()

    while program.running:

        program.update_window()
        program.next_iteration()
        sleep(program.TICK)

    sys.exit()
