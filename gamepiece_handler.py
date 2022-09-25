from gamepieces import *
from enemy import *
from settings import *
import random

class GamepieceHandler:
    def __init__(self,game):
        self.game = game
        self.sprites= []
        self.staticsprites = []
        self.enemylist = []

        #sets up Gameobjects for tutorial mode 
        if self.game.tutorialmode:
            self.addSprite(Gamepieces(game,pos=(2.5,8.5),path='resources/gamepieces/gun1.png',value=0,type = 'gun'))
            self.addEnemySprite(Enemy(game,pos = (12,3),value=0))
            self.addSprite(Gamepieces(game, pos = (8.5,4.5),path = 'resources/gamepieces/ammo.png', value = 5, type = 'ammo'))

        # sets up game objects for point mode
        if self.game.pointg1 or self.game.pointg2 or self.game.pointg3:
            self.gamepiecerandomiser()

    def addSprite(self,sprite):
        self.sprites.append(sprite)

    def addEnemySprite(self,sprite):
        self.enemylist.append(sprite)

    def addStaticSprite(self,sprite):
        self.staticsprites.append(sprite)
    
    def update(self):
        [sprite.update() for sprite in self.sprites]
        [staticsprite.update() for staticsprite in self.staticsprites]
        [enemy.update() for enemy in self.enemylist]

    def gamepiecerandomiser(self):
        '''******************************************************************************************
        
        Method: gamepiecerandomiser --> Randonly dispatches loot and enemies around the map based on 
                                        map level  
      
        *********************************************************************************************'''
        self.sprites.clear()
        self.enemylist.clear()

        if self.game.pointg1: 
            #amount of loot and enemies to be dispatched for level 1
            gold = 2
            ammo = 1
            health = 1
            enemy = 2
            enemypos = POSG1 # array of acceptable positions for enemy dispatch
        if self.game.pointg2: 
            #amount of loot and enemies to be dispatched for level 2
            gold = 3
            ammo = 1
            health = 1
            enemy = 3
            enemypos = POSG2# array of acceptable positions for enemy dispatch
        if self.game.pointg3: 
            #amount of loot and enemies to be dispatched for level 3
            gold = 5
            ammo = 1
            health = 1
            enemy = 4
            enemypos = POSG3# array of acceptable positions for enemy dispatch

        if self.game.tutorialmode: 
            gold = 15
            ammo = 10
            health = 10
            enemy = 4
            enemypos = POSG3

        #Dispatching of enemies
        pos = random.randint(0,len(enemypos)-1)
        poslist = []
        poslist.append(pos)
        for i in range (enemy-1):
            while (pos in poslist):
                pos = random.randint(0,len(enemypos)-1)
            
            poslist.append(pos)
        for i in poslist:
            
            self.addEnemySprite(Enemy(self.game,pos = enemypos[i],value=420))

        for i in range(gold):
            #Dispatching of gold
            x = random.randint(1,18)
            y = random.randint(1,8)
            while ((x, y) in self.game.map.world_map or (x,y) in enemypos):
                x = random.randint(1,18)
                y = random.randint(1,8)
            print ('hihi')
            self.addSprite(Gamepieces(self.game,pos = (x+0.5,y+0.5)))

        for i in range(ammo):
            #Dispatching of ammo
            x = random.randint(1,18)
            y = random.randint(1,8) 
            while ((x, y) in self.game.map.world_map or (x,y) in enemypos):
                x = random.randint(1,18)
                y = random.randint(1,8)
            self.addSprite(Gamepieces(self.game,pos = (x+0.5,y+0.5),path = 'resources/gamepieces/ammo.png', value = 25, type = 'ammo'))

        for i in range(health):
            #Dispatching of health
            x = random.randint(1,18)
            y = random.randint(1,8)
            while ((x, y) in self.game.map.world_map  or (x,y) in enemypos):
                x = random.randint(1,18)
                y = random.randint(1,8)
            self.addSprite(Gamepieces(self.game,pos = (x+0.5,y+0.5),path = 'resources/gamepieces/heart.png', value = 30, type = 'health'))
        
        

    def getClosestEnemy(self):
        '''******************************************************************************************
        
        Method: getClosestEnemy --> Returns the closest enemy alive if the player can see the enemy  
      
        *********************************************************************************************'''
        
        p = 10000
        count = 0
        enemy =-1
        for i in self.enemylist:
            
            if i.alive:
                        if i.ray_cast():
                            if i.dist <p:
                                enemy = count
                                p = i.dist
            count= count+1
        return enemy

    def enemiesleft(self):
        '''***********************************************************
        
        Method: enemiesleft --> Returns the num of enemies alive 
      
        **************************************************************'''

        count = 0
        for i in self.enemylist:
            if i.alive:
                count+=1
        return count

    def draw(self):
        '''***********************************************************
        
        Method: draw --> Draws game objects and checkpoints on minimap
      
        **************************************************************'''
        for i in self.sprites:
            if i.type == 'gold':
                colour = (255,215,0)
            elif i.type == 'ammo':
                colour = (50,205,50)
            elif i.type == 'health':
                colour = (255,52,179)
            elif i.type == 'gun':
                colour = (151,255,255)

            pg.draw.circle(self.game.screen, colour, (i.x * 25 +HALF_WIDTH*2-20*25-10, i.y * 25+HALF_HEIGHT*2-10*25), 10)

        for k in self.enemylist:
            pg.draw.circle(self.game.screen, 'black', (k.x * 25 +HALF_WIDTH*2-20*25-10, k.y * 25+HALF_HEIGHT*2-10*25), 10)

        if self.game.timeg1:
            pg.draw.circle(self.game.screen, 'white', (18.5 * 25 +HALF_WIDTH*2-20*25-10, 4.5 * 25+HALF_HEIGHT*2-10*25), 10)

        if self.game.timeg2:
            pg.draw.circle(self.game.screen, 'white', (18.5 * 25 +HALF_WIDTH*2-20*25-10, 1.5 * 25+HALF_HEIGHT*2-10*25), 10)

        if self.game.timeg3:
            pg.draw.circle(self.game.screen, 'white', (18.5 * 25 +HALF_WIDTH*2-20*25-10, 7.5 * 25+HALF_HEIGHT*2-10*25), 10)
    