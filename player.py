from pkg_resources import to_filename
from settings import *
import pygame as pg
import math
from button import *
from textwrap import fill


class Player:
    '''*************************************
        Initialise player attributes
    ***************************************'''
    def __init__(self, game,pos = PLAYER_POS,points=0):
        self.game = game
        self.x, self.y = pos
        self.angle = PLAYER_ANGLE
        self.health = MAX_HEALTH 
        self.movementlist = []
        self.shot = False
        self.count = 0
        self.points = points
        self.pickedupgun = False
        self.ammo = 25
        self.attempts = 3
        self.tempangle=0
        self.numtokill = 0
        self.tokill = []
        self.button_pos_x = 0.875*RES[0]
        self.button_pos_y = 0.015*RES[1]
        self.button_size_x = 0.11*(RES[0])
        self.button_size_y = 0.11*0.25*(RES[0])
        self.instructions = ["Welcome to MazePy Tutorial!\nMake the player walk forward once, turn right, and walk forward one block by typing:\nplayer.move(forward)\nplayer.turn(right)\nplayer.move(forward)",
         "Clear the editor\nUse player.move(forward) method to make the player walk to the gun and \nuse the player.pickup(gun) method to pick it up. \nHINT: Use a for loop with range (5) to make the player walk forward 5 blocks",
         "Clear the editor\nAfter checking that you have ammo, use the player.aim() and player.shoot() \nto aim and shoot at the demon", 
         "Congradulations, you have completed the tutorial!\nYou will be automatically redirected to the main menu\nwhere you can play the competitive game modes"]
        self.displayinstruction = self.instructions[0].split('\n')
        self.tutlist = []
        for i in range(1,6):
            txt = 'resources/tut' + str(i) +'.PNG'
            tut = pg.image.load(txt)
            self.tutlist.append(tut)

        self.tutimg = self.tutlist[0]
        self.button = Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Display Text Editor', self.editorButton, False, (0, 122, 122), (0, 250, 250), (0, 102, 0), 16)


    def single_shot(self):
        '''************************************************************************

        Method: single_shot --> Handles variable change mechanics for a gun shot

        ***************************************************************************'''
        if self.shot == False and self.game.gun.reloading ==False:
            self.shot = True
            self.ammo -= 1
            self.game.ammohealth.subtract_ammo(1)
            self.game.gun.reloading = True
    
    def editorButton(self):
        '''******************************************************************************

        Method: editorButton --> Hides the text editor for better first person game view

        *********************************************************************************'''
        if self.game.timeg1 or self.game.timeg2 or self.game.timeg3:
            self.game.timer.resume()
            self.game.mapdisplay = True

        self.game.editor_display = True
            
    def process_editor(self, input):
        '''*****************************************************************************************************

        Method: process_editor --> takes input from Python intepretor and converts them to an list of game moves

        PARAM: input --> list [] of char
        ********************************************************************************************************'''
        for i in input:
            if i=='w' or i == 's':
                #move forward or backward
                for s in range (20):
                    self.movementlist.append(i)

            elif i == 'l' or i == 'r':
                #turn left or right 
                for s in range (100):
                    self.movementlist.append(i)

            elif i == 'a':
                #aim and shoot enemy
                self.movementlist.append('b')
                for s in range (300):
                    self.movementlist.append(i)
            else:
                #pick up object 
                    self.movementlist.append(i)


    def move(self):
        '''*****************************************************************************************************

        Method: move --> Controls the movements and actions of the character based on the processed user inputs

        ********************************************************************************************************'''
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED 
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        

        if self.count < len(self.movementlist):
            pg.time.delay(1)
            if self.movementlist[self.count]== 'w':
                #move forward
                dx += speed_cos
                dy += speed_sin
            
            elif self.movementlist[self.count] == 's':
                #move backward
                dx -= speed_cos
                dy -= speed_sin

            elif self.movementlist[self.count] == 'l':
                #turn left
                for i in range(156):
                    self.angle -= 0.0001

            elif self.movementlist[self.count] == 'r':
                #turn right
                for i in range(156):
                    self.angle += 0.0001

            elif self.movementlist[self.count] == 'b':
                #store current player angle before aiming
                self.tempangle = self.angle
                                       

            elif self.movementlist[self.count] == 'a':
                #checks if theres an enemy within 180 degree FOV
                enemynum = self.game.gamepieces_handler.getClosestEnemy()
                
                if enemynum !=-1:

                    #auto aim
                    enemy = self.game.gamepieces_handler.enemylist[enemynum]
                    delta = enemy.theta - self.angle
                    if -math.pi< delta <-0.009 or delta < -6.30:
                        self.angle -= 0.0156
                    elif delta > 0.009 or -6.27< delta <= -math.pi:
                        self.angle += 0.0156

                    #auto shoot    
                    else:   
                        if (enemy.alive):
                            self.single_shot()
                            pg.time.delay(5)

                #auto return to original player angle                
                elif(self.angle != self.tempangle):
                            delta1 = self.tempangle - self.angle
                            if -math.pi< delta1 <-0.009 or delta1 < -6.30:
                                self.angle -= 0.0156
                        
                            elif delta1 > 0.009 or -6.27< delta1 <= -math.pi:
                                self.angle += 0.0156
                          
                
            else:
                #pick up object
                self.checkobject(self.movementlist[self.count])
                
            self.count += 1 
            self.angle %= math.tau


        self.check_wall_collision(dx, dy) #checks for player wall collision 
        self.endgamecheck() #checks if the game mode has ended
        
            
        
    def endgamecheck(self):
        '''*****************************************************************************************************

        Method: endgame --> Determines, based on player attributes, whether they have reached the end of the game 
                            and updates UI elements 

        ********************************************************************************************************'''
        if self.game.tutorialmode:
            if 2<self.x<3 and 2< self.y<3:
                self.tutimg = self.tutlist[1]
                
            if 2<self.x<3 and 7<self.y<8 and self.pickedupgun:
                self.tutimg = self.tutlist[2]

            if self.ammo> 0:

                self.tutimg = self.tutlist[3]
            
            if not self.game.gamepieces_handler.enemylist[0].alive:
                
                self.tutimg = self.tutlist[4]
                for i in range(len(self.tutlist)-1):
                    
                    self.tutlist[i] = self.tutimg 

                self.movementlist = []

                self.game.gamepieces_handler.gamepiecerandomiser()

        elif self.game.pointg1:
            if self.health<=0 or self.attempts==0:
                tempscore = self.game.client_manager.calculate_final_score(self.points)
                self.game.client_manager.add_new_score(tempscore,0)
                self.game.endmenu.update("score", 0)
                self.game.mapdisplay = False
                self.game.editor_display = False
                #self.game.client_manager.send_update_scores()
                self.game.endmenu_display = True
                print(self.points)
            elif self.game.gamepieces_handler.enemiesleft() ==0:
                print('hi')
                self.attempts = 3
                self.x, self.y = PLAYER_POS
                self.angle = 0
                self.movementlist = []
                pg.time.delay(5)
                self.game.gamepieces_handler.gamepiecerandomiser()
            elif self.count>2 and self.count == len(self.movementlist):
                self.attempts-=1
                self.movementlist = []
        
        elif self.game.pointg2:
            if self.health<=0 or self.attempts==0:
                tempscore = self.game.client_manager.calculate_final_score(self.points) 
                self.game.client_manager.add_new_score(tempscore,1)
                self.game.endmenu.update("score", 1)
                self.game.endmenu_display = True
                self.game.mapdisplay = False
                self.game.editor_display = False
                #self.game.client_manager.send_update_scores()
                print(self.points)
            elif self.game.gamepieces_handler.enemiesleft() ==0:
                print('hi')
                self.attempts = 3
                self.x, self.y = PLAYER_POS
                self.angle = 0
                self.movementlist = []
                pg.time.delay(5)
                self.game.gamepieces_handler.gamepiecerandomiser()
            elif self.count>2 and self.count == len(self.movementlist):
                self.attempts-=1
                self.movementlist = []
        
        elif self.game.pointg3:
            if self.health<=0 or self.attempts==0:

                tempscore = self.game.client_manager.calculate_final_score(self.points)
                self.game.client_manager.add_new_score(tempscore,2)
                self.game.endmenu.update("score", 2)
                self.game.mapdisplay = False
                self.game.editor_display = False

                self.game.endmenu_display = True
                #self.game.client_manager.send_update_scores()
                print(self.points)
            elif self.game.gamepieces_handler.enemiesleft() ==0:
                print('hi')
                self.x, self.y = PLAYER_POS
                self.attempts = 3
                self.angle = 0
                self.movementlist = []
                pg.time.delay(5)
                self.game.gamepieces_handler.gamepiecerandomiser()
            elif self.count>2 and self.count == len(self.movementlist):
                self.attempts-=1

                self.movementlist = []
        
        elif self.game.timeg1:
            if self.x == 13.5:
                self.game.timer.add_time()

            if (18<self.x<19 and 4<self.y<5) or self.game.timer.get_time() == 0:
                temptime = self.game.client_manager.calculate_final_time(self.game.timer.get_time())
                self.game.client_manager.add_new_time(temptime,0)
                self.game.endmenu.update("time", 0)
                self.game.mapdisplay = False
                self.game.editor_display = False
                self.game.endmenu_display = True
                #self.game.client_manager.send_update_times()
            elif self.count>2 and self.count == len(self.movementlist):
                self.game.timer.resume()
        elif self.game.timeg2:
            if self.x == 15.5:
                self.game.timer.add_time()
            if (18<self.x<19 and 1<self.y<2) or self.game.timer.get_time() == 0:
                temptime = self.game.client_manager.calculate_final_time(self.game.timer.get_time())
                self.game.client_manager.add_new_time(temptime,1)
                self.game.endmenu.update("time", 1)
                self.game.endmenu_display = True
                self.game.mapdisplay = False
                self.game.editor_display = False
                #self.game.client_manager.send_update_times()
            elif self.count>2 and self.count == len(self.movementlist):
                self.game.timer.resume()

        elif self.game.timeg3:
            if self.x == 13.5 or self.x == 16.5:
                self.game.timer.add_time()

            if (18<self.x<19 and 7< self.y<8) or self.game.timer.get_time() == 0:
                temptime = self.game.client_manager.calculate_final_time(self.game.timer.get_time())
                self.game.client_manager.add_new_time(temptime,2)
                self.game.endmenu.update("time", 2)
                self.game.endmenu_display = True
                self.game.mapdisplay = False
                self.game.editor_display = False
                #self.game.client_manager.send_update_times()
            elif self.count>2 and self.count == len(self.movementlist):
                self.game.timer.resume()



        
        
    def checkobject(self,type):
        '''*****************************************************************************************************

        Method: checkobject --> Determines if a game object is near by and what type of object it is. User needs
                                to enter correct type to pick up the object 

        PARAM: type --> String of the type of object to be picked up
        ********************************************************************************************************'''
        temp = type.split(' ')
        for i in self.game.gamepieces_handler.sprites:
            ox, oy = i.getPos()
            
            if abs(ox-self.x) <1.3 and abs(oy-self.y) <1.3:
                print('in range')
                if temp[1] == i.type:
                    self.game.gamepieces_handler.sprites.remove(i)
                    self.points +=i.value

                    if self.game.pointg1 or self.game.pointg2 or self.game.pointg3:
                        self.game.points.addPoints(i.value)
                    if i.type == 'gun':
                        print('yes')
                        self.pickedupgun= True
                    elif i.type == 'ammo':
                        self.game.ammohealth.add_ammo(i.value)
                        self.ammo += i.value
                        print(i.type)
                    elif i.type == 'health':
                        self.health += i.value
                        self.game.ammohealth.add_health(i.value)


            


  
        

    def update(self):
        self.move()
        #self.movement()

    def draw_button(self):
        self.button.process()

    def draw(self):
        '''*************************************

        Method: draw --> Draws player on minimap 

        ****************************************'''
        if 0.25*math.pi<=self.angle<= 0.75*math.pi:
            pg.draw.polygon(self.game.screen, 'green', [(self.x*25+HALF_WIDTH*2-20*25-10, self.y*25+HALF_HEIGHT*2-10*25),(self.x*25+5+HALF_WIDTH*2-20*25-10,self.y*25-5+HALF_HEIGHT*2-10*25),(self.x*25+HALF_WIDTH*2-20*25-10,self.y*25+10+HALF_HEIGHT*2-10*25),(self.x*25-5+HALF_WIDTH*2-20*25-10,self.y*25-5+HALF_HEIGHT*2-10*25)])
        elif 0.75*math.pi<self.angle<= 1.25*math.pi:
            pg.draw.polygon(self.game.screen, 'green', [(self.x*25+HALF_WIDTH*2-20*25-10, self.y*25+HALF_HEIGHT*2-10*25),(self.x*25+5+HALF_WIDTH*2-20*25-10,self.y*25+5+HALF_HEIGHT*2-10*25),(self.x*25-10+HALF_WIDTH*2-20*25-10,self.y*25+HALF_HEIGHT*2-10*25),(self.x*25+5+HALF_WIDTH*2-20*25-10,self.y*25-5+HALF_HEIGHT*2-10*25)])

        elif 1.25*math.pi<self.angle<= 1.75*math.pi:            
            pg.draw.polygon(self.game.screen, 'green', [(self.x*25+HALF_WIDTH*2-20*25-10, self.y*25+HALF_HEIGHT*2-10*25),(self.x*25-5+HALF_WIDTH*2-20*25-10,self.y*25+5+HALF_HEIGHT*2-10*25),(self.x*25+HALF_WIDTH*2-20*25-10,self.y*25-10+HALF_HEIGHT*2-10*25),(self.x*25+5+HALF_WIDTH*2-20*25-10,self.y*25+5+HALF_HEIGHT*2-10*25)])

        elif 1.75*math.pi<self.angle<= 2*math.pi or self.angle< 0.25*math.pi:       
            pg.draw.polygon(self.game.screen, 'green', [(self.x*25+HALF_WIDTH*2-20*25-10, self.y*25+HALF_HEIGHT*2-10*25),(self.x*25-5+HALF_WIDTH*2-20*25-10,self.y*25+5+HALF_HEIGHT*2-10*25),(self.x*25+10+HALF_WIDTH*2-20*25-10,self.y*25+HALF_HEIGHT*2-10*25),(self.x*25-5+HALF_WIDTH*2-20*25-10,self.y*25-5+HALF_HEIGHT*2-10*25)])


    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):

        '''*****************************************************************************************************

        Method: check_wall_collision --> Restricts players movements to within the map

        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

        ********************************************************************************************************'''
        s = PLAYER_SIZE/self.game.delta_time
        
        if self.check_wall(int(self.x + dx *s), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy*s)):
            self.y += dy

    def take_damage(self, damage):
        '''**************************************************************************

        Method: take_damage --> Updates player attritubes if enemy attack successful
       
        ****************************************************************************'''
        self.health -= damage 
        self.game.ammohealth.subtract_health(damage)
        self.game.textures.bloodscreen()
    
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)