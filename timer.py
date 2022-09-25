from time import time
import pygame as pg
import datetime

class timer:
    def __init__(self, game, x, y, time_remaining, running = False):
        self.game = game
        self.x = x
        self.y = y
        self.og_time = time_remaining
        self.time_remaining = time_remaining
        
        self.font = pg.font.SysFont(None, 50)
        self.timer_text = self.font.render("TIME REMAINING:", True, (255, 255, 255))
        self.font = pg.font.SysFont(None, 100)
        self.time_to_display = self.font.render(self.seconds_to_min(), True, (255, 255, 255))
        self.added_time = None
        self.added_animation_time = 0

        self.clock = pg.time.Clock()
        self.timer_event = pg.USEREVENT+1
        pg.time.set_timer(self.timer_event, 1000)
        
        self.running = running

    def draw(self, events):
        self.clock.tick(60)
        for event in events:
            if event.type == self.timer_event:
                if self.running:
                    self.time_remaining = self.time_remaining - 1
                    if self.time_remaining < 10:
                        self.time_to_display = self.font.render(self.seconds_to_min(), True, (255, 0, 0))
                    elif self.time_remaining < 30:
                        self.time_to_display = self.font.render(self.seconds_to_min(), True, (255, 172, 28))
                    else:
                        self.time_to_display = self.font.render(self.seconds_to_min(), True, (255, 255, 255))
                    if self.time_remaining == 0:
                        pg.time.set_timer(self.timer_event, 0)
                    if self.added_animation_time > 0:
                        self.added_animation_time = self.added_animation_time - 1
        #pg.draw.rect(self.game.screen, (255, 255, 255), (self.x, self.y, self.timer_text.get_width(), self.timer_text.get_height()+20))
        self.game.screen.blit(self.timer_text, (self.x, self.y))
        self.game.screen.blit(self.time_to_display, (self.x + 0.175*(self.timer_text.get_width()), self.y + 1.1*(self.timer_text.get_height())))
        if self.added_animation_time > 0:
            self.game.screen.blit(self.added_time, (self.x + 1.3*(self.time_to_display.get_width()), self.y + 1.5*(self.timer_text.get_height())))

    def seconds_to_min(self):
        """Converts seconds from the integer value to a minutes and seconds representation like: 02:36"""
        time_string = str(datetime.timedelta(seconds = self.time_remaining))

        return time_string[2:]

    def pause(self):
        """Pause the timer object from counting down time"""
        self.running = False
    
    def resume(self):
        """Resume the timer object from counting down time"""
        self.running = True

    def reset(self):
        """Reset the time remaining for the timer object to the original time when instantiated"""
        self.time_remaining = self.og_time

    def addTime(self, time = 10):
        """Add the time remaining for the timer object"""
        self.time_remaining = self.time_remaining + time
        font = pg.font.SysFont(None, 50)
        self.added_time = font.render("+{0}".format(time), True, (0, 150, 0))
        self.added_animation_time = 2

    def set_time(self, time: int):
        """Set the time remaining for the timer object"""
        self.og_time = time
        self.time_remaining = time

    def get_time(self):
        """Return the time remaining for the timer object"""
        return self.time_remaining