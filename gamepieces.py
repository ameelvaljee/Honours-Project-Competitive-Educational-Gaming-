import pygame as pg
from settings import *
import os
from collections import deque


'''************************************************************************

        Class Gamepieces --> Mechanics for the implementation of game pieces

        Acknowledgement: Stanislav Petrov        
        https://github.com/StanislavPetrovV/DOOM-style-Game

***************************************************************************'''

class Gamepieces:
    def __init__(self, game,pos, path='resources/gamepieces/coin2.png',
                  scale=0.5, shift=0.6, value = 600, type = 'gold'):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.gamepiece_half_width = 0
        self.gamepiece_SCALE = scale
        self.gamepiece_HEIGHT_SHIFT = shift
        self.value = value
        self.type = type

    def get_gamepiece_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.gamepiece_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.gamepiece_half_width = proj_width // 2
        height_shift = proj_height * self.gamepiece_HEIGHT_SHIFT
        pos = self.screen_x - self.gamepiece_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycast.items_render.append((self.norm_dist, image, pos))

    def get_gamepiece(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        #print(delta)


        ################################


        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_gamepiece_projection()

    def update(self):
        self.get_gamepiece()

    def getPos(self):
        pos = (self.x, self.y)
        return pos

class Animatedgamepieces (Gamepieces):
    def __init__(self, game, pos = (11.5,4.5), path='resources/gamepieces/fire/0.png', scale=0.5, shift=0.6, value = 0, type = 'any', animation_time = 120):
        super().__init__(game, pos, path, scale, shift, value,type)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)) and not file_name.startswith('.'):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images

