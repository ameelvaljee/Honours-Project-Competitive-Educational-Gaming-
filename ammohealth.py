from settings import *
import pygame as pg

class ammohealth:
    def __init__(self, game, x=0, y=HALF_HEIGHT+200, ammo = 25, health = 100):
        """Health and ammo object: Manages player health, and ammo. To display ammo and health on screen call draw"""
        self.game = game
        self.x = x
        self.y = y
        self.ammo_og = ammo
        self.health_og = health
        self.ammo = ammo
        self.health = health

        #UI set up
        #icon
        self.ammohealth_icon = pg.image.load("./resources/UI/ammo_and_health.png").convert_alpha()
        self.ammohealth_icon = pg.transform.scale(self.ammohealth_icon, (0.1*(RES[0]), 0.1*(RES[0])*(466/461)))
        #ammo and health values
        self.font_ammo = pg.font.SysFont(None, 38)
        self.font_health = pg.font.SysFont(None, 32)
        self.ammo_text = self.font_ammo.render(str(self.ammo), True, (237, 125, 49))
        self.health_text = self.font_health.render(str(self.health), True, (0, 176, 240))

    def draw(self):
        """Used to display object on the screen"""
        #draw icon
        self.game.screen.blit(self.ammohealth_icon, (self.x, self.y))

        #draw ammo and health values
        self.game.screen.blit(self.ammo_text, (self.x + 0.5*self.ammohealth_icon.get_width(), self.y + 0.225*self.ammohealth_icon.get_height()))
        self.game.screen.blit(self.health_text, (self.x + 0.5*self.ammohealth_icon.get_width(), self.y + 0.775*self.ammohealth_icon.get_height()))

    def add_ammo(self, new_ammo: int):
        """Adds ammo 'new_ammo' to current ammo count"""
        self.ammo = self.ammo + new_ammo
        self.ammo_text = self.font_ammo.render(str(self.ammo), True, (237, 125, 49))

    def subtract_ammo(self, used_ammo: int):
        """Subtracts ammo 'used_ammo' from current ammo count"""
        self.ammo = max(0, self.ammo - used_ammo)
        self.ammo_text = self.font_ammo.render(str(self.ammo), True, (237, 125, 49))

    def reset_ammo(self):
        """Resets ammo to the ammo count when the object was created"""
        self.ammo = self.ammo_og
        self.ammo_text = self.font_ammo.render(str(self.ammo), True, (237, 125, 49))

    def add_health(self, new_health: int):
        """Adds health 'new_health' to current health value"""
        self.health = self.health + new_health
        self.health_text = self.font_health.render(str(self.health), True, (0, 176, 240))

    def subtract_health(self, used_health: int):
        """Subtracts health 'used_health' from current health value"""
        self.health = max(0, self.health - used_health)
        self.health_text = self.font_health.render(str(self.health), True, (0, 176, 240))

    def reset_health(self):
        """Resets health value to the health value when the object was created"""
        self.health = self.health_og
        self.health_text = self.font_health.render(str(self.health), True, (0, 176, 240))