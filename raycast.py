import enum
import pygame as pg
import math
from settings import *


'''*****************************************************************************************************

Class: raycast --> Performs calculations to determine which walls are intersected first by the rays in the 
                    player's FOV

Acknowledgement: Stanislav Petrov        
https://github.com/StanislavPetrovV/DOOM-style-Game

********************************************************************************************************'''

class Raycast:

    def __init__(self,game):
        self.game = game
        self.raycasting_output = []
        self.items_render = []
        self.textures = self.game.textures.wall_textures
        
    def raycasting(self): 
        self.raycasting_output = []
        ox,oy = self.game.player.pos
        x_map, y_map =  self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        vert_texture, hor_texture = 1,1

        for ray in range (RAY_NUM):

            sin_angle = math.sin(ray_angle)
            cos_angle = math.cos(ray_angle)
          

                   # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_angle > 0 else (y_map - 0.000006, -1)

            depth_hor = (y_hor - oy) / sin_angle
            x_hor = ox + depth_hor * cos_angle

            delta_depth = dy / sin_angle
            dx = delta_depth * cos_angle

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    hor_texture = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_angle > 0 else (x_map - 0.000006, -1)

            depth_vert = (x_vert - ox) / cos_angle
            y_vert = oy + depth_vert * sin_angle

            delta_depth = dx / cos_angle
            dy = delta_depth * sin_angle

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    vert_texture = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

              # depth, texture offset
            if depth_vert < depth_hor:
                depth = depth_vert
                texture = vert_texture
                y_vert %= 1
                if cos_angle > 0:
                    offset = y_vert
                else:
                    offset = 1-y_vert
            else:
                depth= depth_hor
                texture = hor_texture
                x_hor %= 1
                if sin_angle > 0:
                    offset = 1-x_hor
                else:
                    offset = x_hor
            
            #2D yellow cone ray (player vision)
            #pg.draw.line(self.game.screen, 'yellow', (ox * 100, oy * 100),
                   # ((ox * 100 + depth *100 * cos_angle),(oy * 100 + depth *100 * sin_angle)), 2)
            depth *= math.cos(self.game.player.angle - ray_angle)
            projection_height = SCREEN_DIST / (depth +0.0001)
            #3D grayscale player vision 
            #colour = [200 / (1+ depth ** 5*0.002)] *3
            #pg.draw.rect(self.game.screen, colour, (ray*SCALE, HALF_HEIGHT - projection_height //2, SCALE,projection_height))

            #3D texture drawing 
            self.raycasting_output.append((depth, projection_height,texture,offset))
            ray_angle += DELTA_ANGLE
            

            # remove fishbowl effect
            #depth *= math.cos(self.game.player.angle - ray_angle)

    def update(self):
        self.raycasting()
        self.render_items()

    def render_items(self):
        self.items_render = []
        for ray, stuff in enumerate(self.raycasting_output):
            depth, projection_height,texture,offset = stuff
            #getting subsurface for texture 
            
            if HEIGHT>projection_height:
                column = self.textures[texture].subsurface(offset*(TEXTURE_SIZE - SCALE),0,SCALE,TEXTURE_SIZE)
                column = pg.transform.scale(column, (SCALE,projection_height))
                pos_wall=( ray*SCALE , HALF_HEIGHT - projection_height // 2)

            else: #when player gets too close to wall
                height_texture = TEXTURE_SIZE*HEIGHT/projection_height
                column = self.textures[texture].subsurface(offset*(TEXTURE_SIZE - SCALE),HALF_TEXTURE_SIZE - height_texture //2,SCALE,height_texture)
                column = pg.transform.scale(column, (SCALE,HEIGHT))
                pos_wall=( ray*SCALE , 0)
                
            self.items_render.append((depth,column,pos_wall))