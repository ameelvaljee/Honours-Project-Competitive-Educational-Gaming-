from pyexpat import errors
from re import template
import pygame as pg 
from pygame.locals import *
from texteditor import TextEditor
from textwrap import fill

from inputprocess import input_process
from button import Button
from settings import *

class Editor:
    def __init__(self, game):
        """The editor screen which manages and displays the various UI elements when play the game"""
        self.game = game
        self.pygame_events = pg.event.get()
        #template sizes to scale with resolution
        self.template_pos_x = 0.75*RES[0]
        self.template_pos_y = 0.325*RES[1]/10
        self.template_size_x = 0.25*RES[0]
        self.template_size_y = 0.4*RES[1]


        print(self.template_size_y)
        print(self.template_size_y/5)
        print(self.template_size_y/5 + self.template_size_y)

        #editor set up
        self.texteditor = TextEditor(self.template_pos_x, self.template_pos_y, self.template_size_x, self.template_size_y, pg.display.get_surface())
        self.texteditor.set_syntax_highlighting(True)
        self.texteditor.set_colorscheme_from_yaml("./config/texteditorconfig.yml")
        self.texteditor.set_font_size(16)
        #self.texteditor.set_line_numbers(True)
        self.texteditor.handle_keyboard_arrow_left()
        self.texteditor.handle_keyboard_arrow_down()

        #button set up
        self.button_pos_x = 0.765*RES[0]
        self.button_pos_y = 0.625*RES[1]
        self.button_size_x = 0.1*(RES[0])
        self.button_size_y = 0.1*0.25*(RES[0])

        self.buttons = [
            #Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Run Code', self.testButton, False, (0, 204, 0), (0, 255, 0), (0, 102, 0), 16),
            Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Intepret Script', self.interpretCode, False, (0, 204, 204), (0, 255, 255), (0, 76, 153), 20),
            Button(self.game, self.button_pos_x + 1.25*(self.button_size_x), self.button_pos_y, self.button_size_x, self.button_size_y, 'Clear Editor', self.clearEditors, False, (255, 102, 102), (255, 51, 51), (76, 0, 155), 20),
            #Button(self.game, 20, 120, 150, 40, 'Bye', self.changeScreen, False, (255, 102, 102), (255, 51, 51), (76, 0, 155))
        ]

        self.inputprocessor = input_process()

        consolas_font = pg.font.SysFont('consolas', 15)
        self.outputbox = [consolas_font.render(">> Interpret script before running code", True, (255, 255, 255))]

        self.input_moves = [] #variable is clear to [] when intepret code is called. is empty if the intepreted code was wrong otherwise should have moves

    def draw(self):
        """Draw and display the editor and its various elements to the sceen"""
        #buttons
        for button in self.buttons:
            button.process()

        #header set up
        header_size_x = self.template_size_x
        header_size_y = self.template_size_y/10
        header_pos_x = self.template_pos_x
        header_pos_y = self.template_pos_y

        #headers
        texteditor_header = pg.Rect((header_pos_x, 0), (header_size_x, header_size_y))
        outputbox_header = pg.Rect((header_pos_x, 0.01*RES[1] + header_size_y + self.template_size_y), (header_size_x, header_size_y))
    
        pg.draw.rect(pg.display.get_surface(), (220,220,220), texteditor_header)
        pg.draw.rect(pg.display.get_surface(), (255,204,255), outputbox_header)

        #header text
        consolas_font = pg.font.SysFont(None, 25) 
        texteditor_text = consolas_font.render("Python Script Editor", True, (0, 0, 0))
        outputbox_text = consolas_font.render("Python Script Ouput", True, (0, 0, 0))

        self.game.screen.blit(texteditor_text, ((header_pos_x)*1.005, 3))
        self.game.screen.blit(outputbox_text, ((header_pos_x)*1.005, 0.01*RES[1] + (header_size_y + self.template_size_y)*1.0125))

        #output box
        box = pg.Rect((self.template_pos_x , 0.01*RES[1] + 2*header_size_y + self.template_size_y), (self.template_size_x*1.1, 0.125*RES[1]))
        pg.draw.rect(pg.display.get_surface(), (90, 0, 90), box)
        offset = 0
        for text in self.outputbox:
            self.game.screen.blit(text, (1.005*self.template_pos_x, 0.01*RES[1] + 2*header_size_y + self.template_size_y*1.03 + offset))
            offset = offset + RES[1]*0.02

        #text editor
        # capture input
        #self.pygame_events = pg.event.get()
        #for event in self.pygame_events:
            #if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                #elf.game.quit()
        pressed_keys = pg.key.get_pressed()
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        # display editor functionality once per loop
        self.texteditor.display_editor(self.game.pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)

        # update pygame window
        #pg.display.flip()

    def testButton(self):
        """Function to start the game"""
        self.game.player.movementlist = []
        self.game.player.x, self.game.player.y = PLAYER_POS
        self.game.player.angle = 0

        if self.game.timeg1 or self.game.timeg2 or self.game.timeg3:
            self.game.timer.pause()
            if self.game.timeg1 :
                self.game.player.x, self.game.player.y = (1.5, 5.5)
                #self.game.player.angle = 0
                self.game.timer.pause()
               
            elif self.game.timeg2 :

                self.game.player.x, self.game.player.y = (1.5, 5.5)
                #self.game.player.angle = 0
                self.game.timer.pause()

            elif self.game.timeg3:
                self.game.player.x, self.game.player.y = (1.5, 5.5)
                #self.game.player.angle = 0
                
                self.game.timer.pause()
            
        self.game.editor_display = False
        print(self.input_moves)
        self.game.player.count = 0
        self.game.player.process_editor(self.input_moves)
        
        self.buttons.pop(2)

    def clearEditors(self):
        """On a button click. It clears the current text editor."""
        print("Clearing editors")
        self.texteditor.clear_text()
        consolas_font = pg.font.SysFont('consolas', 15)
        self.outputbox = [consolas_font.render(">> Interpret script before running code ", True, (255, 255, 255))]

    #everytime intepret code is called. it clears the display terminal and clears the input moves array
    def interpretCode(self):
        """When the button is clicked. This function makes a call to the code interpreter function and based on the response it either:
        \nDisplays green if the code was intepreted successfully
        \nDisplays red if the code had some form of an error"""
        self.outputbox = []

        text_from_editor = self.texteditor.get_text_as_list()

        text = [line for line in text_from_editor if line]

        #print(len(text))

        #print("Interpreting code")

        #convert 4 whitespaces to a tab
        for line in text:
            #print(line)
            #print("Line has four spaces at start " + (str(line.startswith("    "))))
            if line.startswith("    "):
                line = "\t" + line.lstrip()
            #print("Line has tab at start " + (str(line[0] == "\t")))

        #print(text)

        self.inputprocessor.input_code(text)

        result = self.inputprocessor.process()

        #print(len(result[1]))

        consolas_font = pg.font.SysFont('consolas', 13)

        if result[0] == 0:
            self.outputbox.append(consolas_font.render("Intepreter failed due to error(s):", True, (255, 0, 0)))
            for error in result[1]:
                error_response = error.split(": ")
                error_message = error_response[0]
                error_cause = error_response[1]
                self.outputbox.append(consolas_font.render(error_message + ":", True, (255, 255, 255)))
                self.outputbox.append(consolas_font.render("    " + error_cause, True, (255, 255, 255)))
                self.input_moves = []
        else:
            self.outputbox.append(consolas_font.render("Intepreter succeeded", True, (0, 255, 0)))
            self.input_moves = result[1]
            button = Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Run Code', self.testButton, False, (0, 204, 0), (0, 255, 0), (0, 102, 0), 16)
            self.buttons.append(button)

    def get_input_moves(self):
        """Get a list of the player moves arising from the code interpretation."""
        #check if the input moves array has input
        if not self.input_moves:
            return False #return False to signal no moves
        else:
            return self.input_moves #return moves