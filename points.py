from time import time
import pygame as pg

class points:
    def __init__(self, game, x, y, points = 0):
        self.game = game
        self.x = x
        self.y = y
        self.points = points

        self.font = pg.font.SysFont(None, 50)
        self.points_text = self.font.render("POINTS SCORED:", True, (255, 255, 255))
        self.font = pg.font.SysFont(None, 100)
        self.points_to_display = self.font.render(str(self.points), True, (255, 255, 255))
        self.added_points = None
        self.added_animation_time = 0
        self.subtracted_points = None
        self.subtracted_animation_time = 0

        self.clock = pg.time.Clock()
        self.timer_event = pg.USEREVENT+1
        pg.time.set_timer(self.timer_event, 1000)

    def draw(self, events):
        self.clock.tick(60)
        for event in events:
            if event.type == self.timer_event:
                if self.added_animation_time > 0:
                    self.added_animation_time = self.added_animation_time - 1
                if self.subtracted_animation_time > 0:
                    self.subtracted_animation_time = self.subtracted_animation_time - 1
        self.points_to_display = self.font.render(str(self.points), True, (255, 255, 255))
        self.game.screen.blit(self.points_text, (self.x, self.y))
        self.game.screen.blit(self.points_to_display, (self.x + 0.175*(self.points_text.get_width()), self.y + 1.1*(self.points_text.get_height())))
        if self.added_animation_time > 0:
            self.game.screen.blit(self.added_points, (self.x + 1.5*(self.points_to_display.get_width()), self.y + 0.6 *(self.points_to_display.get_height())))
        if self.subtracted_animation_time > 0:
            self.game.screen.blit(self.subtracted_points, (self.x + 1.6*(self.points_to_display.get_width()), self.y + 1*(self.points_to_display.get_height())))

    def addPoints(self, new_points = 100):
        self.points = self.points + new_points
        font = pg.font.SysFont(None, 50)
        self.added_points  = font.render("+{0}".format(new_points), True, (0, 175, 0))
        self.added_animation_time = 2

    def subtractedPoints(self, lost_points = 50):
        self.points = self.points - lost_points
        font = pg.font.SysFont(None, 50)
        self.subtracted_points = font.render("-{0}".format(lost_points), True, (175, 0, 0))
        self.subtracted_animation_time = 2

    def get_points(self):
        return self.points + 0