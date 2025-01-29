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
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        moveSprite(self.sprite,self.x,self.y,centre=True)
    def update(self):
        self.move()
        
class Enemy(Creature):
    def __init__(self,x,y,image,velocity,size):
        super().__init__(x,y,image,velocity,size)


setAutoUpdate(False)
for i in range(10):
    creatures.append(Enemy(random.randint(0,1000),random.randint(0,1000), "enemy.png", [random.choice([-1,1])*random.randint(2,4),random.choice([-1,1])*random.randint(2,4)],random.randint(50,100)) )


gameOver = False

while not gameOver:
    time.sleep(0.01)
    for creature in creatures:
        creature.update()
    
    updateDisplay()

        
endWait()

