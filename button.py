import pygame as pg

class Button:
    def __init__(self, game, x, y, width, height, buttonText = 'Button', onclickFunction = None, onePress = False, normal = '#ffffff', hover = '#666666', pressed = '#333333', fontSize = 14, arrow_button = False):
        """Creates an object which manages a clickable button.
        \nonclickFunction is the function which will be called when the button is clicked.
        \nIf onePress = True the button will only be clickable once.
        \nCall process to draw and display the button object on the screen.
        \nIf arrow_button = True the button works a button surf between leaderboards.
        """
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': normal,
            'hover': hover,
            'pressed': pressed,
        }

        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)
        consolas_font = pg.font.SysFont(None, fontSize)
        if arrow_button:
            self.buttonSurf = consolas_font.render(buttonText, True, (0, 0, 0))
        else:
            self.buttonSurf = consolas_font.render(buttonText, True, (255, 255, 255))

    def process(self):
        """Draws the button to the screen"""
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.game.screen.blit(self.buttonSurface, self.buttonRect)