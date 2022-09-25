from operator import truediv
from gamepieces import *
import os
from collections import deque

from random import randint, random

class Enemy(Animatedgamepieces):
    def __init__(self, game, pos=(5.5,2), path='resources/gamepieces/enemy/0.png', scale=0.5, shift=0.6, value = 420 , type = 'any',animation_time=120, patrolarray = [(6,3),(7,3),(7,2),(4,2)]):
        super().__init__(game, pos, path, scale, shift, value, type, animation_time)
        print (self.path)
        self.attackimages = self.get_images(self.path + '/attack')
        self.idleimages = self.get_images(self.path + '/idlenew')
        self.bleedimages = self.get_images(self.path + '/bleed')
        self.deathimages = self.get_images(self.path + '/death')
        self.movementimages = self.get_images(self.path + '/movement')
        self.alive = True
        self.gotShot = False
        self.health = 120
        self.speed = 0.005
        self.attackaccuracy = 0.1
        self.attackdmg = 10
        self.size = 20
        self.attackdist = 13
        self.deathframe = 0
        self.patrolpos = deque()
        for i in patrolarray:
            self.patrolpos.append(i)


    def update(self):
        self.check_animation_time()
        self.get_gamepiece()
        self.control()

    def bleed(self):
        '''**************************************************************************

        Method: take_damage --> Updates display if player attack successful
       
        ****************************************************************************'''
        self.animate(self.bleedimages)
        if self.animation_trigger:
            self.gotShot = False
            print ('done')

    def patrol(self):
        '''**************************************************************************

        Method: patrol --> Updates enemy movements if player is not seen so enemy can
                            guard multiple parts of the maze
                            (taken out because too difficult for first year Comp Sci students)
       
        ****************************************************************************'''
        if self.map_pos == self.patrolpos[0]:
            self.patrolpos.rotate(-1)
            print(self.patrolpos[0])

        nextPos = self.patrolpos[0]
        next_x, next_y = nextPos
        angle = math.atan2(next_y +0.5 - self.y, next_x +0.5 -self.x)
        dy = math.sin(angle)*self.speed
        dx = math.cos(angle) * self.speed
        self.check_wall_collision(dx,dy)

    def movement(self):
        '''**************************************************************************
        Method: movement --> Updates enemy movements to run to the players position 

        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

        ******************************************************************************'''
        nextPos = self.game.player.map_pos
        next_x, next_y = nextPos
        angle = math.atan2(next_y +0.5 - self.y, next_x +0.5 -self.x)
        dy = math.sin(angle)*self.speed
        dx = math.cos(angle) * self.speed
        self.check_wall_collision(dx,dy)

    def attack(self):
        '''**************************************************************************

        Method: attack --> calls to update player attritubes if enemy attack successful
       
        ****************************************************************************'''
        if self.animation_trigger:
            if random() < self.attackaccuracy:
                self.game.player.take_damage(self.attackdmg)

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        '''*****************************************************************************************************

        Method: check_wall_collision --> Restricts enemy movements to within the map

        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

        ********************************************************************************************************'''
        if self.check_wall(int(self.x + dx *self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy*self.size)):
            self.y += dy

    def ray_cast(self):
        '''*****************************************************************************************************

        Method: ray_cast --> Performs calculations to determine if the enemy can see (cast a ray to) the player

        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

        ********************************************************************************************************'''
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)+1e-6
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def control(self):
        '''**********************************************

        Method: control --> Acts as the AI of the enemy

        **************************************************'''
        if self.alive:
            self.get_shot()
            if self.gotShot:
                self.bleed()
            elif self.ray_cast():
                self.animate(self.movementimages)
                if not self.game.tutorialmode:
                    self.movement()
                    if self.dist < self.attackdist :
                        self.animate(self.attackimages)
                        self.attack()

            else:

                self.animate(self.movementimages)
                
        else:
            self.death()

    def get_shot(self):
        '''**************************************************************************

        Method: get_shot --> Updates enemy attritubes if player attack successful
       
        ****************************************************************************'''
        if self.game.player.shot:
            if  HALF_WIDTH - self.gamepiece_half_width < self.screen_x < HALF_WIDTH + self.gamepiece_half_width:
                self.game.player.shot = False
                self.gotShot = True
                self.health -= self.game.gun.damage
                self.check_health()

    def check_health(self):
        '''****************************************************************

        Method: checkhealth --> Checks to see if the enemy has been killed

        *******************************************************************'''
        if self.health < 1:
            self.game.player.points += 420
            if not self.game.tutorialmode:
                self.game.points.addPoints(420)
            self.alive = False
    


    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def death(self):
        if not self.alive:
            if self.animation_trigger and self.deathframe < len(self.deathimages) - 1:
                self.deathimages.rotate(1)
                self.image = self.deathimages[0]
                
                self.deathframe += 1
    
