import pygame
import random
import time
import sys

from threading import Thread
from pprint import pprint
from pygame import key, freetype

pygame.init()


class Game:
    def __init__(self, width=1024, height=620, cell=30):
        """constructor for Game
        
        Keyword Arguments:
            width {number} -- window width in pixels (default: {1024})
            height {number} -- window eight in pixels (default: {620})
            cell {number} -- cell count (default: {30})
        """
        pygame.display.set_caption("python))))")
        pygame.display.set_icon(pygame.image.load("face.jpg"))
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.cell_size = width//cell
        self.grid = [width//self.cell_size, height//self.cell_size]
        print(self.grid)
        self.snake = Snake(self.grid)
        self.grid = [[0 for i in range(self.grid[1])] for j in range(self.grid[0])]

        self.face = pygame.image.load("face.jpg")
        self.tits = pygame.image.load("tits.jpg")
        self.ass = pygame.image.load("ass.jpg")

        self.face = pygame.transform.scale(self.face, (self.cell_size, self.cell_size))
        self.tits = pygame.transform.scale(self.tits, (self.cell_size, self.cell_size))
        self.ass = pygame.transform.scale(self.ass, (self.cell_size, self.cell_size))

        self.font = freetype.SysFont("OpenSans", 12)

    def start(self):
        """start game
        """
        while True:
            self.clock.tick(120)
            self.draw()
            self.handle_events()
            pygame.display.update()

    def draw(self):
        """draw snake, fps and food
        """
        self.screen.fill((255, 255, 255, 255))
        for i in self.snake.body:
            self.screen.blit(self.tits, (self.cell_size*i[0], self.cell_size*i[1]))
        self.screen.blit(self.ass, (self.snake.food[0]*self.cell_size, self.snake.food[1]*self.cell_size))
        self.screen.blit(self.face, (self.cell_size*self.snake.body[0][0], self.cell_size*self.snake.body[0][1]))

        fps = self.font.render("FPS: %d" % self.clock.get_fps(), (0, 0, 0, 255), (255, 255, 255, 255))[0]
        fps.set_colorkey((255, 255, 255, 255))
        self.screen.blit(fps, (5, 5))

        score = self.font.render("Score: %d" % len(self.snake.body), (0, 0, 0, 255), (255, 255, 255, 255))[0]
        score.set_colorkey((255, 255, 255, 255))
        self.screen.blit(score, (5, 25))

    def handle_events(self):
        """handle keyboard events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.snake.is_run = 0
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if chr(event.key) in "wasd":
                    self.snake.direction = chr(event.key)


class Snake:
    max_length = 100
    
    def __init__(self, grid):
        """Snake constructor
        
        Arguments:
            grid {list} -- cell size
        """
        self.body = [[grid[0]//2, grid[1]//2]]
        self.food = [grid[0]//2, grid[1]//5]
        self.grid = grid
        self.direction = ""
        self.is_run = 1
        Thread_(self.go).start()

    def add(self):
        self.body.append(self.body[-1][:])
        self.body[-1][1] -= 1
        Snake.max_length += 1

    def go(self):
        while self.is_run:
            if self.direction:
                eval("self.%s()" % self.direction)
                if self.body[0][:] == self.food[:]:
                    self.add()
                    self.food = [random.randint(0, self.grid[0]-1), random.randint(0, self.grid[1]-1)]
                time.sleep(0.004*(Snake.max_length-len(self.body)))

    def w(self):
        for i in range(len(self.body)-1, -1, -1):
            if i > 0:
                self.body[i] = self.body[i-1][:]
            else:
                if self.body[i][1] > 0:
                    self.body[i][1] -= 1
                else:
                    self.body[i][1] = self.grid[1]-1

    def a(self):
        for i in range(len(self.body)-1, -1, -1):
            if i > 0:
                self.body[i] = self.body[i-1][:]
            else:
                if self.body[i][0] > 0:
                    self.body[i][0] -= 1
                else:
                    self.body[i][0] = self.grid[0]-1

    def s(self):
        for i in range(len(self.body)-1, -1, -1):
            if i > 0:
                self.body[i] = self.body[i-1][:]
            else:
                if self.body[i][1] < self.grid[1]-1:
                    self.body[i][1] += 1
                else:
                    self.body[i][1] = 0

    def d(self):
        for i in range(len(self.body)-1, -1, -1):
            if i > 0:
                self.body[i] = self.body[i-1][:]
            else:
                if self.body[i][0] < self.grid[0]-1:
                    self.body[i][0] += 1
                else:
                    self.body[i][0] = 0

class Thread_(Thread):
    def __init__(self, f):
        Thread.__init__(self)
        self.f = f
    def run(self):
        self.f()


if __name__ == '__main__':
    game = Game(1024, 620)
    game.start()
