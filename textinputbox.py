import pygame as pg

from settings import *

class TextInputBox:
    def __init__(self, game, x, y, w, font, text = "", active = False, in_pair = False, disable_friend = None):
        """Input text object: Creates an object which manages a small text input box. Use update to draw and subsequently update the UI. 
        \nAdapted from StackOverflow Tutorial: https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame"""
        self.game = game
        self.textcolor = (255, 255, 255)
        self.boxcolor = (255, 255, 255)
        self.backcolor = None
        self.x = x
        self.y = y
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = active
        self.text = text
        self.first_time = True
        self.in_pair = in_pair
        self.disable_friend = disable_friend
        t_surf = self.font.render(self.text, True, self.textcolor, self.backcolor)
        self.height = t_surf.get_height()+10

    def render_text(self):
        """Creates new images to render based on the current state of the text box object.
        \n Function is called by update."""
        t_surf = self.font.render(self.text, True, self.textcolor, self.backcolor) 
        self.image = pg.Surface((max(self.width, t_surf.get_width()+20), t_surf.get_height()+10), pg.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        pg.draw.rect(self.game.screen, self.boxcolor, (self.x, self.y, max(self.width, t_surf.get_width()+10), t_surf.get_height()+20), 3)
        self.game.screen.blit(t_surf, (self.x + 7, self.y + 12))
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event_list):
        """Used to draw and display the object on the screen.
        \nevent_list is a variable which has the list of PY_GAME events which have occured since the last iteration."""
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and not self.active:
                mouse = pg.mouse.get_pos()
                if (self.x <= mouse[0] <= (self.x + self.width)) and (self.y <= mouse[1] <= (self.y + self.height)):
                    if self.first_time == True:
                        self.first_time = False
                        self.text = ""
                    self.active = True
                    if self.in_pair:
                        self.disable_friend()
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        self.render_text()

    def get_text(self):
        """Return the text currently in the input box"""
        return self.text

    def change_to_red(self):
        """Change the colour of the textbox UI to red.
        \n Used for an incorrect password."""

        self.boxcolor = (255, 0, 0)

    def disable(self):
        """Disbales the text input box from reading keyboard inputs.
        \n Used when the users presses enter or clicks another text input box."""
        self.active = False
