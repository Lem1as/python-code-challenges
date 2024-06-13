import math
import random
from tkinter import Tk, Canvas
from time import sleep


class Program:

    def __init__(self):

        self.HEIGHT = 720
        self.WIDTH = 1080
        self.CENTER = [self.WIDTH/2, self.HEIGHT/2]
        self.TICK = 0.01666
        self.MAX_DISTANCE = max(self.WIDTH, self.HEIGHT)
        self.MAX_STARS_COUNT = 500
        self.MAX_SPEED = self.MAX_DISTANCE / 2.5
        self.MIN_SPEED = self.MAX_SPEED / 2.5
        self.RAINBOW_MODE = True

        self.running = True
        self.stars = []

        self.master = Tk()
        self.master.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.master.resizable(False, False)

        self.canvas = Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg="#000")
        self.canvas.pack()


    def update_window(self):
        self.master.update()
        self.master.update_idletasks()

    # def create_circle(self, radius, position, fill="#fff", **kwargs):
    #     self.canvas.create_arc(position[0]-radius, position[1]-radius,
    #       position[0]+radius, position[1]+radius, fill=fill, **kwargs)

    def create_trail(self, star, **kwargs):

        end_x, end_y = (self.CENTER[0]-star["pos"][0])/star["pos"][2]+self.CENTER[0], (self.CENTER[1]-star["pos"][1])/star["pos"][2]+self.CENTER[1]
        self.canvas.create_line(star["lastpos"][0], star["lastpos"][1], end_x, end_y, fill=star["color"], width=abs(end_x/self.WIDTH/2)*7, **kwargs)
        return [end_x, end_y]

    def calc_stars(self):

        stars_to_add = 0
        for id, star in enumerate(self.stars):

            star["pos"][2] -= star["speed"] * (star["pos"][2]/self.MAX_DISTANCE) * self.TICK*10

            if star["pos"][2] <= 0.3:
                self.stars.pop(id)
                stars_to_add += 1
                continue

            self.stars[id]["lastpos"] = self.create_trail(star)

        for i in range(stars_to_add):
            self.create_star()


    def create_star(self):

        color = "#fff"
        if self.RAINBOW_MODE:
            color = random.choice(["#f88", "#8f8", "#88f", "#f8f", "#ff8", "#8ff", "#fff"])

        self.stars.append({"pos": [random.randint(10, self.WIDTH), random.randint(10, self.HEIGHT), self.MAX_DISTANCE],
                           "lastpos": [self.CENTER[0],self.CENTER[1]],
                           "speed": random.randint(math.floor(self.MIN_SPEED), math.ceil(self.MAX_SPEED)),
                           "color": color})

    def next_iteration(self):

        if len(self.stars) == 0:
            for i in range(random.randint(self.MAX_STARS_COUNT//2, self.MAX_STARS_COUNT)):
                self.create_star()

        self.canvas.delete("all")
        self.calc_stars()




if __name__ == "__main__":

    program = Program()

    while program.running:

        program.update_window()
        program.next_iteration()
        sleep(program.TICK)
