# Console for maze game input language
# Calvin Nyoni
# 19/07/2022

import re
import pygame
from pygame.locals import *
import time
import queue
from datetime import datetime

import sys
import ply.yacc as yacc
import ply.lex as lex

import subprocess

#global variables
global_code = -1
global_iterate = -1
global_text = ""
global_lst_of_functions = ["move.left", "move.right", "move.up", "move.down", "help", "writeToFile", "runGame"]
function_descriptions = ["Moves game character left", "Moves game character right", "Moves game character up", "Moves game character down", "Lists all available commands", "Writes action queue to input file", "Runs the game with currently saved input file"]


#token types
tokens = ('SYMBOL_LPAREN','SYMBOL_RPAREN','KEYWORD_FOR','KEYWORD_IN', 'KEYWORD_RANGE', 'INTEGER', 'SYMBOL_COLON', 'SYMBOL_POINT', 'VALID_STRING', 'SYMBOL_COMMA')

#reg ex rules
t_SYMBOL_LPAREN = r'\('
t_SYMBOL_RPAREN = r'\)'
t_SYMBOL_COLON = r':'
t_SYMBOL_COMMA = r','
t_SYMBOL_POINT = r'\.'
t_VALID_STRING = r'(?!for)(?!in)(?!range)[a-zA-Z][a-zA-Z]*'
t_KEYWORD_FOR = r'for'
t_KEYWORD_IN = r'in'
t_KEYWORD_RANGE = r'range'
t_INTEGER = r'0|[1-9][0-9]*'

#ignore whitespace
def t_WHITESPACE(t):
    r'[ \t]'
    pass
#error catch
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#build the lexer
lexer = lex.lex()

#productions
def p_function_call(p):
    '''expression : VALID_STRING SYMBOL_LPAREN SYMBOL_RPAREN'''
    global global_code, global_text, global_lst_of_functions
    print("function " + p[1] + " was called")
    if p[1] in global_lst_of_functions:
        if p[1] == "help":
            global_code = 3
        elif p[1] == "writeToFile":
            global_code, global_text = 4, p[1]
        elif p[1] == "runGame":
            global_code, global_text = 5, p[1]
        else:
            global_code, global_text = 1, p[1]
    else:
        global_code, global_text = 0, "Error function not recognised: "
def p_function_call_with_subroutine(p):
    '''expression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN SYMBOL_RPAREN'''
    print("function " + p[1] + " was called with subroutine " + p[3])
    global global_code, global_text
    global_code, global_text = 1, p[1] + "." + p[3]
def p_for_loop(p):
    '''expression : KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_RPAREN SYMBOL_COLON'''
    iterations = int(p[6]) 
    print("for loop to iterate " + str(iterations) + " times")
    global global_code, global_iterate
    global_code, global_iterate = 2, iterations
def p_for_loop_with_bounds(p):
    '''expression : KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_COMMA INTEGER SYMBOL_RPAREN SYMBOL_COLON'''
    iterations = int(p[8]) - int(p[6])
    global global_code, global_iterate
    global_code, global_iterate = 2, iterations
# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print("Command or text not recognised")
    #print(p[0])
    print(p)
    global global_code, global_text
    global_code, global_text = 0, "Error command not recognised: "
    return 100

#function to display list of all available functions
def help_display(line_q_fonts, line_q_imgs):
    global global_lst_of_functions, function_descriptions
    current_time = str(datetime.now())[11:19]
    to_display = [current_time + " help()"]

    colour = (0, 255, 0)
    white = (255, 255, 255)

    i = 0
    while i < len(global_lst_of_functions):
        to_display.append(global_lst_of_functions[i] + " - " + function_descriptions[i])
        i = i + 1

    i = 0
    while i < len(to_display):
        if len(line_q_imgs) == 16:
            line_q_fonts.pop(0)
            line_q_imgs.pop(0)

            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[9].render(to_store, True, colour))
        elif len(line_q_imgs) == 0:
            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[0].render(to_store, True, colour))
        else:   
            current_pos = len(line_q_imgs) - 1
            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, colour))
        colour = white
        i = i + 1

#function to write to file
def write_to_file(actions_q, line_q_fonts, line_q_imgs):
    current_time = str(datetime.now())[11:19]
    to_display = [current_time + " writeToFile()"] + ["Writing to input file"]

    colour = (0, 255, 0)
    white = (255, 255, 255)

    i = 0
    while i < len(to_display):
        if len(line_q_imgs) == 16:
            line_q_fonts.pop(0)
            line_q_imgs.pop(0)

            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[9].render(to_store, True, colour))
        elif len(line_q_imgs) == 0:
            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[0].render(to_store, True, colour))
        else:   
            current_pos = len(line_q_imgs) - 1
            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, colour))
        colour = white
        i = i + 1

    f = open("resources/input.txt", "w")

    dict_for_action = {
        "move.left" : "a",
        "move.right" : "d",
        "move.up" : "w",
        "move.down" : "s"
    }
    
    for action in actions_q:
        f.write(dict_for_action[action]+"\n")

    f.close()

#function to run the game
def run_game(line_q_fonts, line_q_imgs):
    current_time = str(datetime.now())[11:19]
    to_display = [current_time + " runGame()"] + ["Running Maze game"]

    colour = (0, 255, 0)
    white = (255, 255, 255)

    i = 0
    while i < len(to_display):
        if len(line_q_imgs) == 16:
            line_q_fonts.pop(0)
            line_q_imgs.pop(0)

            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[9].render(to_store, True, colour))
        elif len(line_q_imgs) == 0:
            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[0].render(to_store, True, colour))
        else:   
            current_pos = len(line_q_imgs) - 1
            to_store = to_display[i]

            line_q_fonts.append(pygame.font.SysFont('consolas', 14))
            line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, colour))
        colour = white
        i = i + 1

    subprocess.run(["python", "main.py"])
    
# Build the parser
parser = yacc.yacc()

pygame.init()

#window set up
caption = "Console for maze game input language"

pygame.display.set_caption(caption)

size = 480, 360

width, height = size

screen = pygame.display.set_mode(size)

background = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

screen.fill(background)

t0 = time.time()
print('time needed for Font creation :', time.time()-t0)

# fonts = pygame.font.get_fonts()
# print(len(fonts))
# for f in fonts:
#     sysfont = f
#     print(f)

current_input_text = "Your command here or help()"
consolas_font = pygame.font.SysFont('consolas', 14)
img_of_text = consolas_font.render(">> " + current_input_text, True, blue)

text_rect = img_of_text.get_rect()
text_rect.topleft = (20, 20)
cursor = Rect(text_rect.topright, (3, text_rect.height))

#make shift queues to store last 10 entered line
line_q_fonts = []
line_q_imgs = []
#variables for loop
current_time = str(datetime.now())[11:16]
to_store = ""
current_pos = 0
inLoop = False                 
actions_Q = []
loop_Q = []
temp_actions_Q = []
iterate = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if len(current_input_text)>0:
                    current_input_text = current_input_text[:-1]
            elif event.key == K_RETURN:
                a = parser.parse(current_input_text)
                print(str(a))
                #Error code
                if global_code == 0:
                    #catch unrecognised commands
                    if len(line_q_imgs) == 16:
                        line_q_fonts.pop(0)
                        line_q_imgs.pop(0)

                        current_time = str(datetime.now())[11:19]
                        to_store = current_time + " " + global_text + current_input_text

                        line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                        line_q_imgs.append(line_q_fonts[9].render(to_store, True, red))
                        current_input_text = ""
                    elif len(line_q_imgs) == 0:
                        current_time = str(datetime.now())[11:19]
                        to_store = current_time + " " + global_text + current_input_text

                        line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                        line_q_imgs.append(line_q_fonts[0].render(to_store, True, red))
                        current_input_text = ""
                    else:   
                        current_pos = len(line_q_imgs) - 1
                        current_time = str(datetime.now())[11:19]
                        to_store = current_time + " " + global_text + current_input_text

                        line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                        line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, red))
                        current_input_text = ""
                #Help code
                elif global_code == 3:
                    help_display(line_q_fonts, line_q_imgs)
                    current_input_text = ""
                #Write to file code
                elif global_code == 4:
                    write_to_file(actions_Q, line_q_fonts, line_q_imgs)
                    actions_Q = []
                    current_input_text = ""
                #Run the game code
                elif global_code == 5:
                    run_game(line_q_fonts, line_q_imgs)
                    current_input_text = ""
                else:
                    if inLoop:
                        #catch nested for loop
                        if global_code == 2:
                            if len(line_q_imgs) == 16:
                                line_q_fonts.pop(0)
                                line_q_imgs.pop(0)

                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "Error nested for loops not supported "

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[9].render(to_store, True, red))
                                current_input_text = ""
                            elif len(line_q_imgs) == 0:
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "Error nested for loops not supported "

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[0].render(to_store, True, red))
                                current_input_text = ""
                            else:   
                                current_pos = len(line_q_imgs) - 1
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "Error nested for loops not supported "

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, red))
                                current_input_text = ""
                            inLoop = False
                        elif global_code == 1:
                            #add action to action queue
                            temp_actions_Q.append(global_text)
                            if len(line_q_imgs) == 16:
                                line_q_fonts.pop(0)
                                line_q_imgs.pop(0)

                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "    " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[9].render(to_store, True, green))
                                current_input_text = ""
                            elif len(line_q_imgs) == 0:
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "    " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[0].render(to_store, True, green))
                                current_input_text = ""
                            else:   
                                current_pos = len(line_q_imgs) - 1
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "    " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, green))
                                current_input_text = ""
                        else:
                            if len(line_q_imgs) == 16:
                                line_q_fonts.pop(0)
                                line_q_imgs.pop(0)

                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "Error cannot loop on non-action function calls "

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[9].render(to_store, True, red))
                                current_input_text = ""
                            elif len(line_q_imgs) == 0:
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "Error cannot loop on non-action function calls "

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[0].render(to_store, True, red))
                                current_input_text = ""
                            else:   
                                current_pos = len(line_q_imgs) - 1
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + "Error cannot loop on non-action function calls "

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, red))
                                current_input_text = ""
                            inLoop = False
                    else:
                        if global_code == 2:
                            inLoop = True
                            iterate = global_iterate
                            if len(line_q_imgs) == 16:
                                line_q_fonts.pop(0)
                                line_q_imgs.pop(0)

                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + " " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[9].render(to_store, True, green))
                                current_input_text = ""
                            elif len(line_q_imgs) == 0:
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + " " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[0].render(to_store, True, green))
                                current_input_text = ""
                            else:   
                                current_pos = len(line_q_imgs) - 1
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + " " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, green))
                                current_input_text = ""
                        else:
                            #do action here
                            actions_Q.append(global_text)
                            if len(line_q_imgs) == 16:
                                line_q_fonts.pop(0)
                                line_q_imgs.pop(0)

                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + " " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[9].render(to_store, True, green))
                                current_input_text = ""
                            elif len(line_q_imgs) == 0:
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + " " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[0].render(to_store, True, green))
                                current_input_text = ""
                            else:   
                                current_pos = len(line_q_imgs) - 1
                                current_time = str(datetime.now())[11:19]
                                to_store = current_time + " " + current_input_text

                                line_q_fonts.append(pygame.font.SysFont('consolas', 14))
                                line_q_imgs.append(line_q_fonts[current_pos].render(to_store, True, green))
                                current_input_text = ""
            elif event.key == K_TAB:
                print("inLoop is " + str(inLoop))
                print("TAB was pressed")
                inLoop = False
                loop_Q = iterate*temp_actions_Q
                actions_Q = actions_Q + loop_Q

                loop_Q = []
                temp_actions_Q = []
                print("inLoop is " + str(inLoop))
            else:
                current_input_text  += event.unicode
    
    screen.fill(background)

    text_pos = 20
    for i in line_q_imgs:
        screen.blit(i, (20, text_pos))
        text_pos = text_pos + 20

    text_rect.topleft = (20, text_pos)
    screen.blit(img_of_text, text_rect)

    if (inLoop):
        img_of_text = consolas_font.render(">>in loop>> " + current_input_text , True, blue)
        text_rect.size= img_of_text.get_size()
        cursor.topleft = text_rect.topright
    else:
        img_of_text = consolas_font.render(">> " + current_input_text , True, blue)
        text_rect.size= img_of_text.get_size()
        cursor.topleft = text_rect.topright
        # print("Actions sent:")
        # for action in actions:
        #     print(action)

    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, blue, cursor)

    pygame.display.update()

pygame.quit()
print(actions_Q)