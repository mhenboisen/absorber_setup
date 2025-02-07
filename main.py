from pygame_functions import *
import math, random, time, pickle

sensitivity = 15
max_speed = 15
screen_width = 1920
screen_height = 1080


screenSize(screen_width,screen_height)
setBackgroundColour("black")
creatures = []

class Creature:
    def __init__(self,x,y,image, velocity, size):
        self.x = x
        self.y = y
        self.velocity = velocity # as an ij vector
        self.size = size   # size is a percentage of the full size image
        self.the_power_up = None 
        self.sprite = makeSprite(image)
        moveSprite(self.sprite,self.x,self.y,centre=True)
        transformSprite(self.sprite, 0, self.size/25)
        showSprite(self.sprite)
        
    def move(self, player):
        self.x = (self.x + self.velocity[0]) % 10000
        self.y = (self.velocity[1]+ self.y) % 10000
        
        self.x_onscreen = self.x - player.x + screen_width/2
        self.y_onscreen = self.y - player.y  + screen_height/2
        

        moveSprite(self.sprite,self.x_onscreen,self.y_onscreen,centre=True)
    def update(self,player):
        self.move(player)
        
class Enemy(Creature):
    def __init__(self,x,y,image,velocity,size):
        super().__init__(x,y,image,velocity,size)
        self.maxSpeed = 5
        
class Player(Creature):
    def __init__(self,x,y,image,velocity,size):
        super().__init__(x,y,image,velocity,size)
        self.angle = 0
        moveSprite(self.sprite,screen_width/2,screen_height/2,centre=True)
        transformSprite(self.sprite, 0, self.size/100)
        
    def move(self):
        #calculates the x and y displacement between player and mouse
        x_diff = (mouseX() - screen_width/2)/sensitivity
        y_diff = (mouseY() - screen_height/2)/sensitivity
        
        #limits the speed to 10px per tick
        if x_diff >= 0:
            self.velocity[0] = min(max_speed,x_diff)
        else:
            self.velocity[0] = max(-max_speed,x_diff)
        
        if y_diff >= 0:
            self.velocity[1] = min(max_speed,y_diff)
        else:
            self.velocity[1] = max(-max_speed,y_diff)
        
        self.x = (self.x + self.velocity[0]) % 10000
        self.y = (self.velocity[1]+ self.y) % 10000
        
        self.angle = math.degrees(math.atan2(y_diff, x_diff))
        transformSprite(self.sprite, self.angle, self.size/100)        
    
    def collision(self,creatures):
        for c in creatures:
            if touching(self.sprite,c.sprite):
                print(str(self.size),str(c.size))
                if self.size > c.size:
                    print("Nom")
                    creatures.remove(c)
                    hideSprite(c.sprite)
                    self.size = self.size + c.size/10
                    transformSprite(self.sprite, self.angle, self.size/100)
                elif self.size < c.size:
                    print("dead")
                    self.die()
    def update(self,creatures):
        self.move()
        self.collision(creatures)
        
    def die(self):
        global gameOver
        gameOver = False

def drawBoundary(player):
    clearShapes()
    drawRect(screen_width/2-player.x,screen_height/2-player.y,10000,10000, (0,0,40), 0)
    drawRect(screen_width/2-player.x,screen_height/2-player.y,10000,10000, (255,255,255), 5)

setAutoUpdate(False)
for i in range(300):
    creatures.append(Enemy(random.randint(0,10000),random.randint(0,10000), "enemy.png", [random.choice([-1,1])*random.randint(2,4),random.choice([-1,1])*random.randint(2,4)],random.randint(5,100)) )

p1 = Player(5000,5000,"player.png",[0,0],10)
gameOver = False
initial_time = 0
end_time = 1
while not gameOver:
    initial_time = clock()
    fps = 1/(end_time - initial_time)
    tick(30)
    drawBoundary(p1)
    for creature in creatures:
        creature.update(p1)
    p1.update(creatures)
    
    updateDisplay()
    
        
endWait()

