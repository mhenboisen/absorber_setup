from pygame_functions import *
import math, random, time, pickle

screenSize(1000,1000)
setBackgroundColour("black")
creatures = []

class Creature:
    def __init__(self,x,y,image, velocity, size):
        self.x = x
        self.y = y
        self.velocity = velocity # as an ij vector
        self.size =size   # size is a percentage of the full size image
        self.the_power_up = None 
        self.sprite = makeSprite(image)
        moveSprite(self.sprite,self.x,self.y,centre=True)
        transformSprite(self.sprite, 0, self.size/100)
        showSprite(self.sprite)
        
    def move(self):
        if self.x + self.velocity[0] > 1100:
            self.x = -100
        elif self.x + self.velocity[0] < -100:
            self.x = 1100
        
        if self.y + self.velocity[1] > 1100:
            self.y = -100
        elif self.y + self.velocity[1] < -100:
            self.y = 1100
        
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        moveSprite(self.sprite,self.x,self.y,centre=True)
    def update(self):
        self.move()
        
class Enemy(Creature):
    def __init__(self,x,y,image,velocity,size):
        super().__init__(x,y,image,velocity,size)
        self.maxSpeed = 5
        
class Player(Creature):
    def __init__(self,x,y,image,velocity,size):
        super().__init__(x,y,image,velocity,size)
        
    def move(self):
        #calculates the x and y displacement between player and mouse
        x_diff = (mouseX() - self.x)/self.size
        y_diff = (mouseY() -self.y)/self.size
        
        #limits the speed to 10px per tick
        if x_diff >= 0:
            self.velocity[0] = min(50,x_diff)
        else:
            self.velocity[0] = max(-50,x_diff)
        
        if y_diff >= 0:
            self.velocity[1] = min(50,y_diff)
        else:
            self.velocity[1] = max(-50,y_diff)

        #updates the position of the player
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        moveSprite(self.sprite,self.x,self.y,centre=True)
        
    def collision(self,object):
        if self.size > object.size:
            self.size += 1
            object.die()
        elif self.size < object.size:
            self.die()
    def update(self):
        self.move()
        

setAutoUpdate(False)
for i in range(10):
    creatures.append(Enemy(random.randint(0,1000),random.randint(0,1000), "enemy.png", [random.choice([-1,1])*random.randint(2,4),random.choice([-1,1])*random.randint(2,4)],random.randint(50,100)) )

p1 = Player(100,100,"player.png",[0,0],10)
gameOver = False

while not gameOver:
    tick(30)
    for creature in creatures:
        creature.update()
    p1.update()
    
    updateDisplay()

        
endWait()

