import pygame
import math

class Vector2f:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2f(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector2f(self.x - other.x, self.y - other.y)
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: float):
        return Vector2f(self.x * other, self.y * other)
    def __truediv__(self, other: float):
        return Vector2f(self.x / other, self.y / other)
    


class Planet:
    displayRadius = 0.0
    mass = 0.0
    name = ""
    color = (255, 255, 255)
    pos = Vector2f(0.0, 0.0)
    velocity = Vector2f(0.0, 0.0)

    def __init__(self, r, m, p, n, c):
        self.displayRadius = r
        self.mass = m
        self.name = n
        self.color = c
        self.pos = Vector2f(p[0], p[1])


def dist(p: Vector2f) -> float:
    return math.sqrt(p.x * p.x + p.y * p.y)


def logic(p, dt):#planets
    
    #Brute force for each planet and calculate its attraction to other planets
    for i in p:
        for j in p:
            #F = G(m1m2/ r^2)
            d = i.pos - j.pos
            distD = dist(d)

            if(distD != 0.0):
                
                #F = (G(m1m2)) / r^2, where G, the gravitational constant, is massive for a better result
                F = 25000.0 * (i.mass * j.mass) / math.pow(distD, 2) 
               
                a = d / distD * F / j.mass #Normalise distance vector and then scale to Fg, then use F = ma to get a
                j.velocity += a * dt
                j.pos += j.velocity * dt #Semi-Implicit Euler
                
            

def process():
    pygame.init()

    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("2D N-body sim where n=2")

    running = True

    g = 1.0
    
    planets = [Planet(7.5, 100.0, (100, 100), "Mars", (255, 0, 0)), Planet(7.5, 100.0, (500, 500), "Earth", (0, 255, 25))]
    planets[0].velocity = Vector2f(25.0, 0.0)
    planets[1].velocity = Vector2f(-10.0, 0.0)


    #dt
    deltaTime = 0.0
    dtClock = pygame.time.Clock()


    #Game loop
    while running:

        #Event loop
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                running = False

        #Fetch dt
        deltaTime = dtClock.get_time() * 0.001 #Got to convert to seconds
        dtClock.tick()
        

        #Run logic
        logic(planets, deltaTime)

        #Clear
        screen.fill((0, 0, 0))
        #Drawing
        for i in planets:#Planets
            pygame.draw.circle(screen, i.color, (i.pos.x, i.pos.y), i.displayRadius)

        #Update
        pygame.display.flip()

if __name__ == "__main__":
    process()