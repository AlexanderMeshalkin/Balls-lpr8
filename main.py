#Проект еще не закончен, планируется добавить прыгающий счетчик, абсолютно упругие соударения шаров и возможность менять вектор гравитации

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = (x ** 2 + y ** 2) ** 0.5

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.length = (self.x ** 2 + self.y ** 2) ** 0.5

    def multiplyByNumber(self, k):
        self.x *= k
        self.y *= k
        self.length *= k

    def scalarProduct(self, vector):
        return self.x * vector.x + self.y * vector.y



class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def addVector(self, vector):
        self.x += vector.x
        self.y += vector.y

    def distance(self, pos):
        return ((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2) ** 0.5


class Ball:

    def __init__(self, pos, r, color, velocity):
        global g
        self.pos = pos
        self.r = r
        self.color = color
        self.velocity = velocity
        self.mass = r ** 3
        self.isDestroyed = False

    def draw(self):
        circle(screen, self.color, (self.pos.x, self.pos.y), self.r)

    def update(self):
        global g
        if not self.isDestroyed:

            circle(screen, BLACK, (self.pos.x, self.pos.y), self.r)

            #Collision processing

            isCollision = False
            if self.checkHorizontalWallCollision():
                isCollision = True
                self.horizontalWallCollision()
            if self.checkVerticalWallCollision():
                isCollision = True
                self.verticalWallCollision()

            #Gravity processing

            self.velocity.add(g)
            self.pos.addVector(self.velocity)


            circle(screen, self.color, (self.pos.x, self.pos.y), self.r)

    def destroy(self):
        global ballsQuantity
        self.isDestroyed = True
        circle(screen, BLACK, (self.pos.x, self.pos.y), self.r)
        ballsQuantity -= 1

    def checkVerticalWallCollision(self):
        global SCREEN_WIDTH
        return (self.pos.x <= self.r and self.velocity.x < 0) or (self.pos.x >= SCREEN_WIDTH - self.r and self.velocity.x > 0)

    def checkHorizontalWallCollision(self):
        global SCREEN_HEIGHT
        return (self.pos.y <= self.r and self.velocity.y < 0) or (self.pos.y >= SCREEN_HEIGHT - self.r and self.velocity.y > 0)

    def verticalWallCollision(self):
        global SCREEN_WIDTH
        self.velocity.x = -self.velocity.x
        if self.pos.x <= self.r:
            self.pos.r = self.r
        else:
            self.pos.x = SCREEN_WIDTH - self.r

    def horizontalWallCollision(self):
        global SCREEN_HEIGHT
        self.velocity.y = -self.velocity.y
        if self.pos.y <= self.r:
            self.pos.y = self.r
        else:
            self.pos.y = SCREEN_HEIGHT - self.r





import pygame
import math
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
ballsQuantity = 0

#Display resolution
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 864

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

balls = []
g = Vector(0, 2.5)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    global ballsQuantity
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(15, 60)
    vx = randint(-20, 20)
    vy = randint(5, 20) * (randint(0, 1) * 2 - 1)
    color = COLORS[randint(0, 5)]
    ball = Ball(Position(x, y), r, color, Vector(vx, vy))
    balls.append(ball)
    balls[-1].draw()
    ballsQuantity += 1


def newScoreBall():
    global ballsQuantity
    x = randint(100, 1100)
    y = randint(100, 900)
    r = 80
    vx = randint(-20, 20)
    vy = randint(5, 20) * (randint(0, 1) * 2 - 1)
    color = WHITE
    return Ball(Position(x, y), r, color, Vector(vx, vy))



def gameUpdate():
    for ball in balls:
        ball.update()


def check_for_balls(pos):
    for ball in balls:
        if ball.pos.distance(pos) <= ball.r:
            return ball
    return None


pygame.display.update()
clock = pygame.time.Clock()
finished = False

f1 = pygame.font.Font(None, 20)


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ball = check_for_balls(Position(event.pos[0], event.pos[1]))
            if ball != None:
                ball.destroy()

    if randint(1, ballsQuantity * 3 + 1) == 1:
        new_ball()
    gameUpdate()
    pygame.display.update()

pygame.quit()
