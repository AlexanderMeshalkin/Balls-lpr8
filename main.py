#Проект еще не закончен, планируется добавить прыгающий счетчик, абсолютно упругие соударения шаров и возможность менять вектор гравитации

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = (x ** 2 + y ** 2) ** 0.5

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def multiplyByNumber(self, k):
        return Vector(self.x * k, self.y * k)

    def scalarProduct(self, vector):
        return self.x * vector.x + self.y * vector.y

    def projection(self, axis):
        return axis.vector.multiplyByNumber(self.scalarProduct(axis.vector))

    def isCollinear(self, vector):
        return self.x * vector.y == self.y * vector.x

    def isCoDirected(self, vector):
        if self.length == 0:
            return True
        if vector.length == 0:
            return True
        return self.isCollinear(vector) and (self.x * vector.x > 0 or self.y * vector.y > 0)

    def isOppositeDirected(self, vector):
        if self.length == 0:
            return True
        if vector.length == 0:
            return True
        return self.isCollinear(vector) and (self.x * vector.x < 0 or self.y * vector.y < 0)



class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def addVector(self, vector):
        self.x += vector.x
        self.y += vector.y

    def distance(self, pos):
        return ((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2) ** 0.5


class Axis:
    def __init__(self, pos, vector):
        self.pos = pos
        self.vector = vector
        self.vector = self.vector.multiplyByNumber(1 / self.vector.length)

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

            self.velocity = self.velocity.add(g)
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



#Balls' collisions processor
class BallsCollision:

    def __init__(self):
        pass

    def checkBallsCollision(self, ball1, ball2):
        if (ball1.pos.distance(ball2.pos) < ball1.r + ball2.r):
            vectorCollision = Vector(ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y)
            if ball1.velocity.add(ball2.velocity.multiplyByNumber(-1)).scalarProduct(vectorCollision) > 0:
                return True
        return False

    def collision(self, ball1, ball2):
        vectorCollision = Vector(ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y)
        collisionAxis = Axis(ball1.pos, vectorCollision)
        v10 = ball1.velocity.projection(collisionAxis)
        v20 = ball2.velocity.projection(collisionAxis)
        v1 = v10.add(v20.multiplyByNumber(-1))
        dv1 = v1.multiplyByNumber(-2 * ball2.mass / (ball1.mass + ball2.mass))
        dv2 = v1.multiplyByNumber(2 * ball1.mass / (ball1.mass + ball2.mass))
        ball1.velocity = ball1.velocity.add(dv1)
        ball2.velocity = ball2.velocity.add(dv2)








import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
ballsQuantity = 0

#Display resolution
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 864

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ballsCollision = BallsCollision()

balls = []
g = Vector(0, 2.5)

g_list = [Vector(0, 2.5), Vector(2.5, 0), Vector(0, -2.5), Vector(-2.5, 0)]
g_index = 0

x_axis = Axis(Position(0, 0), Vector(1, 0))
y_axis = Axis(Position(0, 0), Vector(0, 1))

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
    for i in range(len(balls) - 1):
        if not balls[i].isDestroyed:
            for j in range(i + 1, len(balls)):
                if not balls[j].isDestroyed:
                    if ballsCollision.checkBallsCollision(balls[i], balls[j]):
                        ballsCollision.collision(balls[i], balls[j])
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
            if g_index == 3:
                g_index = 0
            else:
                g_index += 1
            g = g_list[g_index]

    if randint(1, ballsQuantity * 40 + 1) == 1:
        new_ball()
    gameUpdate()
    pygame.display.update()

pygame.quit()
