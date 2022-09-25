import pygame as pg
import sys
import datetime
import statistics
from pygame.locals import *


from button import *
from settings import *

class endmenu:
    def __init__(self, game):
        #window set up
        self.game = game
        
        self.client_manager = None

        self.leaderboard_index = None

        self.type = None

        #title set up
        self.game_title = pg.image.load("./resources/titles/maze_title_2.png").convert_alpha()
        self.game_title = pg.transform.scale(self.game_title, (0.2*(RES[0]), 0.2*(RES[0])*(1299/2366)))

        #text set up
        font_renderer = pg.font.SysFont(None, 125)
        self.final_score_title = font_renderer.render("Your Map Score", True, (255, 255, 255))
        self.final_time_title = font_renderer.render("Your Map Time", True, (255, 255, 255))

        font_renderer = pg.font.SysFont(None, 73)
        self.leaderboard_title = font_renderer.render("Leaderboard Position", True, (255, 255, 255))
        self.prev_best_title = font_renderer.render("Current Map Score/Time", True, (255, 255, 255))

        font_renderer = pg.font.SysFont(None, 73)
        self.change_title = font_renderer.render("Change", True, (255, 255, 255))

        font_renderer = pg.font.SysFont(None, 50)
        self.player_to_beat_title = font_renderer.render("Player to beat:", True, (255, 255, 255))
        self.next_best_title = font_renderer.render("Next best player:", True, (255, 255, 255))
        font_renderer = pg.font.SysFont(None, 30)
        self.average_text = font_renderer.render("Player average score/time was x points/seconds", True, (255, 255, 255))
        self.average_score = font_renderer.render("1234", True, (255, 255, 255))

        self.player_pos = None
        self.player_below = None
        self.player_above = None


        #button set up
        self.button_pos_x = 0.125*RES[0]
        self.button_pos_y = 0.85*RES[1]
        self.button_size_x = 0.2*(RES[0])
        self.button_size_y = 0.2*0.25*(RES[0])

        self.buttons = [
            Button(self.game, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Play Again', self.playAgain, False, (0, 204, 204), (0, 255, 255), (0, 76, 153), 34),
            Button(self.game, self.button_pos_x + 1*(1.25*self.button_size_x), self.button_pos_y, self.button_size_x, self.button_size_y, 'Play Next Map', self.playNext, False, (0, 204, 0), (0, 255, 0), (0, 102, 0), 34),
            Button(self.game, self.button_pos_x + 2*(1.25*self.button_size_x), self.button_pos_y, self.button_size_x, self.button_size_y, 'Return to Menu', self.mainmenuButton, False, (255, 102, 102), (255, 51, 51), (76, 0, 155), 34)
        ]

    def draw(self):
        """Displays the players most recent score/time, their leaderboard position, and those around them. If the player has played before they have a personal best display otherwise 0.
        Also note update must be called before drawing to get the latest information"""
        self.game.screen.fill((0, 0, 0))

        #game title
        self.game.screen.blit(self.game_title, (0.38*RES[0], 0.025*RES[1]))

        #main title
        main_title_pos_x = 0.25*RES[0]
        main_title_pos_y = 0.2*RES[1]

        if self.type == "score":
            self.game.screen.blit(self.final_score_title, (main_title_pos_x, main_title_pos_y))
        else:
            self.game.screen.blit(self.final_time_title, (main_title_pos_x, main_title_pos_y))

        #score
        current = self.change_info_to_display[0]
        #print("Current is:")
        #print(current)
        #print("-------")
        self.game.screen.blit(current, (1.9*main_title_pos_x, main_title_pos_y + 1.2*(self.final_score_title.get_height())))
        #self.game.screen.blit(current, (main_title_pos_x, main_title_pos_y + 1.1()))

        #subheadings
        leaderboard_title_pos_x = 0.05*RES[0]
        prev_best_title_pos_x = 0.625*RES[0]
        subheadings_pos_y = 0.45*RES[1]
        self.prev_best_title = self.average_text
        self.game.screen.blit(self.leaderboard_title, (leaderboard_title_pos_x, subheadings_pos_y))
        self.game.screen.blit(self.prev_best_title, (prev_best_title_pos_x, subheadings_pos_y))

        #position and prev score
        position = self.player_pos
        #prev = self.change_info_to_display[1]
        prev = self.average_score
        self.game.screen.blit(position, (2.5*leaderboard_title_pos_x, subheadings_pos_y + 1.5*(self.leaderboard_title.get_height())))
        if self.type == "time":
            self.game.screen.blit(prev, (1.025*prev_best_title_pos_x, subheadings_pos_y + 1.6*(self.prev_best_title.get_height())))
        else:
            self.game.screen.blit(prev, (1.25*prev_best_title_pos_x, subheadings_pos_y + 1.7*(self.prev_best_title.get_height())))

        #to beat/next player
        to_beat_pos_x = 0.025*RES[0]
        next_best_title_pos_x = 0.25*RES[0]
        to_beat_next_best_pos_y = 0.65*RES[1]
        self.game.screen.blit(self.player_to_beat_title, (to_beat_pos_x, to_beat_next_best_pos_y))
        self.game.screen.blit(self.next_best_title, (next_best_title_pos_x, to_beat_next_best_pos_y))

        #player above and player below
        player_above_pos = self.player_above[0]
        player_above_detail = self.player_above[1]
        self.game.screen.blit(player_above_pos, (0.75*to_beat_pos_x, to_beat_next_best_pos_y + 1.8*(self.player_to_beat_title.get_height())))
        self.game.screen.blit(player_above_detail, (0.75*to_beat_pos_x + 1.4*(player_above_pos.get_width()), to_beat_next_best_pos_y + 1.8*(self.player_to_beat_title.get_height())))

        player_below_pos = self.player_below[0]
        player_below_detail = self.player_below[1]
        self.game.screen.blit(player_below_pos, (1.1*next_best_title_pos_x, to_beat_next_best_pos_y + 1.8*(self.player_to_beat_title.get_height())))
        self.game.screen.blit(player_below_detail, (1.1*next_best_title_pos_x + 1.4*(player_below_pos.get_width()), to_beat_next_best_pos_y + 1.8*(self.next_best_title.get_height())))

        #improvement
        #player_change_pos_x = 0.625*RES[0]
        #player_change_pos_y = 0.67*RES[1]
        # change = self.change_info_to_display[2]

        #self.game.screen.blit(self.average_text, (player_change_pos_x, player_change_pos_y))
        #self.game.screen.blit(self.average_score, (player_change_pos_x*1.225, player_change_pos_y + 1.6*(self.average_text.get_height())))
        # self.game.screen.blit(self.change_title, (player_change_pos_x + 1.15*(change.get_width()), player_change_pos_y))

        #start menu buttons
        for button in range(len(self.buttons)):
            if button == 1 and (self.game.timeg3 or self.game.pointg3):
                pass
            else:
                self.buttons[button].process()

        pg.display.flip()

    def assign_manager(self, client_manager):
        """Assign a client manager for rendering"""
        self.client_manager = client_manager
    
    def update(self, new_type, leaderboard_index):
        self.type = new_type
        self.leaderboard_index = leaderboard_index

        print(self.type)
        font_renderer = pg.font.SysFont(None, 73)

        if self.type == "score":
            self.prev_best_title = font_renderer.render("Cummulative Score", True, (255, 255, 255))
            self.update_score(leaderboard_index)
        else:
            self.prev_best_title = font_renderer.render("Cummulative Time", True, (255, 255, 255))
            self.update_time(leaderboard_index)

    def update_score(self, leaderboard_index):
        """Update the UI to correspond with respective score UI elements"""
        pos = self.client_manager.scoreboard_positions[leaderboard_index] + 1
        leaderboard = self.client_manager.scoreboards[leaderboard_index]

        if (leaderboard_index == 0):
            prev_round = self.client_manager.scoreboards[leaderboard_index][pos - 1][1]
            current_round = self.client_manager.scoreboards[leaderboard_index][pos - 1][1]
        else:
            prev_pos = self.client_manager.scoreboard_positions[leaderboard_index - 1]
            prev_round = self.client_manager.scoreboards[leaderboard_index - 1][prev_pos][1]
            current_round = self.client_manager.scoreboards[leaderboard_index][pos - 1][1]

        leaderboard = self.client_manager.scoreboards[leaderboard_index].copy()
        leaderboard_until_player = leaderboard[:pos]
        rest_of_list = leaderboard[pos:]
        without_zeros = [player for player in rest_of_list if 0 not in player]
        with_zeros = [player for player in rest_of_list if 0 in player]
        with_zeros.sort(key = lambda x: x[0]) 
        rest_of_list = without_zeros + with_zeros
        leaderboard = leaderboard_until_player + rest_of_list

        self.player_pos = self.leaderboard_pos_text(pos)
        self.player_below = self.next_best_person(pos, leaderboard, "score")
        self.player_above = self.person_to_beat(pos, leaderboard, "score")

        #print("Change info array:")
        self.change_info_to_display = self.create_change_score_text(current_round, prev_round, leaderboard_index)
        self.update_average_text(leaderboard_index, True)
        print(self.change_info_to_display)

    def update_time(self, leaderboard_index):
        """Update the UI to correspond with respective time UI elements"""
        pos = self.client_manager.timeboard_positions[leaderboard_index] + 1
        leaderboard = self.client_manager.timeboards[leaderboard_index]

        if (leaderboard_index == 0):
            prev_round = self.client_manager.timeboards[leaderboard_index][pos - 1][1]
            current_round = self.client_manager.timeboards[leaderboard_index][pos - 1][1]
        else:
            prev_pos = self.client_manager.timeboard_positions[leaderboard_index - 1]
            prev_round = self.client_manager.timeboards[leaderboard_index - 1][prev_pos][1]
            current_round = self.client_manager.timeboards[leaderboard_index][pos - 1][1]

        leaderboard = self.client_manager.timeboards[leaderboard_index].copy()
        leaderboard_until_player = leaderboard[:pos]
        rest_of_list = leaderboard[pos:]
        without_zeros = [player for player in rest_of_list if 0 not in player]
        with_zeros = [player for player in rest_of_list if 0 in player]
        with_zeros.sort(key = lambda x: x[0]) 
        rest_of_list = without_zeros + with_zeros
        leaderboard = leaderboard_until_player + rest_of_list

        self.player_pos = self.leaderboard_pos_text(pos)
        self.player_below = self.next_best_person(pos, leaderboard, "time")
        self.player_above = self.person_to_beat(pos, leaderboard, "time")

        #print("Change info array:")
        self.change_info_to_display = self.create_change_time_text(current_round, prev_round, leaderboard_index)
        self.update_average_text(leaderboard_index, False)
        print(self.change_info_to_display)

    def update_average_text(self, leaderboard_index, score = True):
        """Update average text image for score"""
        font_renderer = pg.font.SysFont(None, 73)
        if score:
            leaderboard = self.client_manager.scoreboards[leaderboard_index]
            player_scores = [player[1] for player in leaderboard]
            avg = int(statistics.mean(player_scores))
            self.average_text = font_renderer.render("Average player points:", True, (255, 255, 255))
            font_renderer = pg.font.SysFont(None, 120)
            self.average_score = font_renderer.render("{0} points".format(avg), True, (255, 0, 255))
        else:
            leaderboard = self.client_manager.timeboards[leaderboard_index]
            player_times = [player[1] for player in leaderboard]
            avg = int(statistics.mean(player_times))
            self.average_text = font_renderer.render("Average player time:".format(avg), True, (255, 255, 255))
            font_renderer = pg.font.SysFont(None, 120)
            self.average_score = font_renderer.render("{0} seconds".format(avg), True, (255, 0, 255))

    def leaderboard_pos_text(self, pos):
        """Render leaderboard position text"""
        gold = (255, 215, 0)
        silver = (125, 125, 125)
        bronze = (103,71,54)
        blue = (94, 96, 206)

        font_renderer = pg.font.SysFont(None, 125)

        if pos == 1:
            return font_renderer.render(self.make_ordinal(pos), True, gold)
        elif pos == 2:
            return font_renderer.render(self.make_ordinal(pos), True, silver)
        elif pos == 3:
            return font_renderer.render(self.make_ordinal(pos), True, bronze)
        else:
            return font_renderer.render(self.make_ordinal(pos), True, blue)

    def person_to_beat(self, pos, leaderboard, type):
        """Generate image text to be rendered for the previous position/below the player"""
        gold = (255, 215, 0)
        silver = (125, 125, 125)
        bronze = (103,71,54)
        blue = (94, 96, 206)
        purple = (112, 48 , 160)
        white = (255, 255, 255)
        pink = (255, 0, 255)

        if type == "score":
            measure = " pts"
        else:
            measure = "s"

        font_renderer = pg.font.SysFont(None, 40)

        if pos == 1:
            return [font_renderer.render("No one else, but YOU!", True, purple), font_renderer.render("       ", True, purple)]
        elif pos == 2:
            return [font_renderer.render(self.make_ordinal(pos-1), True, gold), font_renderer.render("{0} {1}{2}".format(leaderboard[pos-2][0], leaderboard[pos-2][1], measure), True, white)]
        elif pos == 3:
            return [font_renderer.render(self.make_ordinal(pos-1), True, silver), font_renderer.render("{0} {1}{2}".format(leaderboard[pos-2][0], leaderboard[pos-2][1], measure), True, white)]
        elif pos == 4:
            return [font_renderer.render(self.make_ordinal(pos-1), True, bronze), font_renderer.render("{0} {1}{2}".format(leaderboard[pos-2][0], leaderboard[pos-2][1], measure), True, white)]
        else:
            return [font_renderer.render(self.make_ordinal(pos-1), True, pink), font_renderer.render("{0} {1}{2}".format(leaderboard[pos-2][0], leaderboard[pos-2][1], measure), True, white)]

    def next_best_person(self, pos, leaderboard, type):
        """Generate image text to be rendered for the next position/above the player"""
        gold = (255, 215, 0)
        silver = (125, 125, 125)
        bronze = (103,71,54)
        blue = (94, 96, 206)
        purple = (112, 48 , 160)
        white = (255, 255, 255)
        pink = (255, 0, 255)

        if type == "score":
            measure = " pts"
        else:
            measure = "s"

        font_renderer = pg.font.SysFont(None, 40)

        if pos == len(leaderboard):
            return [font_renderer.render("No one, you are last :(", True, white), font_renderer.render("       ", True, white)]
        elif pos == 1:
            return [font_renderer.render(self.make_ordinal(pos+1), True, silver), font_renderer.render("{0} {1}{2}".format(leaderboard[pos][0], leaderboard[pos][1], measure), True, white)]
        elif pos == 2:
            return [font_renderer.render(self.make_ordinal(pos+1), True, bronze), font_renderer.render("{0} {1}{2}".format(leaderboard[pos][0], leaderboard[pos][1], measure), True, white)]
        else:
            return [font_renderer.render(self.make_ordinal(pos+1), True, purple), font_renderer.render("{0} {1}{2}".format(leaderboard[pos][0], leaderboard[pos][1], measure), True, white)]

    def create_change_score_text(self, current_round, prev_round, leaderboard_index):
        """Creates image to be rendered for the quasi leaderboard in the end screen"""
        print('curr')
        print(current_round)
        print ('prev')
        print([prev_round])
        green = (0, 176, 80)
        red = (255, 0, 0)
        orange = (255,69,0)
        yellow = (255, 255, 0)
        cyan = (0,255,255)

        font_renderer = pg.font.SysFont(None, 50)
        num_font_renderer = pg.font.SysFont(None, 125)

        if leaderboard_index == 0:
            cummulative_score = num_font_renderer.render(str(current_round), True, yellow)
            current_round_score = num_font_renderer.render(str(current_round - prev_round), True, cyan)

            change = current_round - self.client_manager.previous_scores[leaderboard_index]

            if change < 0:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render(str(change), True, red)
                self.change_title = font_renderer.render("worse than last time. Try Harder!", True, (255, 255, 255))
            else:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render("+" + str(change), True, green)
                self.change_title = font_renderer.render("Improvement", True, (255, 255, 255))
            
            return [cummulative_score, cummulative_score, change]
        else:
            num_font_renderer = pg.font.SysFont(None, 125)
            cummulative_score = num_font_renderer.render(str(current_round), True, yellow)
            current_round_score = num_font_renderer.render(str(current_round), True, cyan)

            change = current_round - self.client_manager.previous_scores[leaderboard_index]

            if change < 0:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render(str(change), True, red)
                self.change_title = font_renderer.render("worse than last time. Try Harder!", True, (255, 255, 255))
            else:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render("+" + str(change), True, green)
                self.change_title = font_renderer.render("Improvement", True, (255, 255, 255))
            
            return [current_round_score, cummulative_score, change]

    def create_change_time_text(self, current_round, prev_round, leaderboard_index):
        """Creates image to be rendered for the quasi leaderboard in the end screen"""
        print('curr')
        print(current_round)
        print ('prev')
        print([prev_round])
        green = (0, 176, 80)
        red = (255, 0, 0)
        orange = (255,69,0)
        yellow = (255, 255, 0)
        cyan = (0,255,255)

        font_renderer = pg.font.SysFont(None, 50)

        if leaderboard_index == 0:
            num_font_renderer = pg.font.SysFont(None, 125)
            cummulative_time = num_font_renderer.render(str(current_round), True, yellow)
            current_round_time = num_font_renderer.render(str(self.seconds_to_min(current_round)), True, cyan)
    

            change = current_round - self.client_manager.previous_scores[leaderboard_index]

            if change < 0:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render(str(change), True, red)
                self.change_title = font_renderer.render("worse than last time. Try Harder!", True, (255, 255, 255))
            else:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render("+" + str(change), True, green)
                self.change_title = font_renderer.render("Improvement", True, (255, 255, 255))
            
            return [cummulative_time, cummulative_time, change]
        else:
            num_font_renderer = pg.font.SysFont(None, 125)
            cummulative_time = num_font_renderer.render(str(current_round), True, yellow)
            current_round_time = num_font_renderer.render(str(self.seconds_to_min(current_round)), True, cyan)

            change = current_round - self.client_manager.previous_scores[leaderboard_index]

            if change < 0:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render(str(change), True, red)
                self.change_title = font_renderer.render("worse than last time. Try Harder!", True, (255, 255, 255))
            else:
                num_font_renderer = pg.font.SysFont(None, 50)
                change = num_font_renderer.render("+" + str(change), True, green)
                self.change_title = font_renderer.render("Improvement", True, (255, 255, 255))
            
            return [current_round_time, cummulative_time, change]

    def make_ordinal(self, n):
        '''Convert an integer into its ordinal representation:
            \nmake_ordinal(0)   => '0th'
            \nmake_ordinal(3)   => '3rd'
            \nmake_ordinal(122) => '122nd'
            \nmake_ordinal(213) => '213th'
            Adapted from: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
        '''
        n = int(n)
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        return str(n) + suffix

    def seconds_to_min(self, time):
        """Converts seconds from the integer value to a minutes and seconds representation like: 02:36"""
        time_string = str(datetime.timedelta(seconds = time))

        return time_string[2:]

    def mainmenuButton(self):
        
        '''***************************************************************

        Method: mainmenubutton --> returns to mainmenu and ends the games

        ********************************************************************'''
        self.game.client_manager.send_update_scores()
        self.game.client_manager.send_update_times()
        self.game.mainmenu.scoreboard_one.update(self.game.client_manager.scoreboards[0], self.game.client_manager.scoreboard_positions[0]+1)
        self.game.mainmenu.scoreboard_two.update(self.game.client_manager.timeboards[0], self.game.client_manager.timeboard_positions[0]+1)
        self.game.endmenu_display = False
        self.game.mainmenu_display = True
        self.game.pointg1 = False
        self.game.pointg2 = False
        self.game.pointg3 = False
        self.game.timeg1 = False
        self.game.timeg2 = False
        self.game.timeg3 = False
        self.game.player.points = 0

    def playAgain(self):

        '''*****************************************************************************************************

        Method: playagain --> resets game mode when a player presses play again

        ********************************************************************************************************'''
        #print("Play Again clicked")
        self.game.client_manager.send_update_scores()
        self.game.client_manager.send_update_times()
        if self.game.pointg1:
            self.game.pointg1 = True
            self.game.new_game('pointg1')
            self.game.endmenu_display = False
            self.game.editor_display = True
            self.game.mapdisplay = True
        elif self.game.pointg2:
            self.game.pointg2 = True
            self.game.new_game('pointg2')
            self.game.endmenu_display = False
            self.game.editor_display = True
            self.game.mapdisplay = True
        elif self.game.pointg3:
            self.game.pointg3 = True
            self.game.new_game('pointg3')
            self.game.endmenu_display = False
            self.game.editor_display = True
            self.game.mapdisplay = True
        elif self.game.timeg1:
            self.game.timeg1 = True
            self.game.endmenu_display = False
            self.game.new_game('timeg1', pos = (1.5, 5.5), time = 300)  
            self.game.editor_display = True
            self.game.mapdisplay = True
            self.game.timer.resume()
        elif self.game.timeg2:
            self.game.timeg2 = True
            self.game.endmenu_display = False
            self.game.new_game('timeg2', pos = (1.5, 5.5), time = 360)
            self.game.editor_display = True
            self.game.mapdisplay = True
            self.game.timer.resume()
        elif self.game.timeg3:
            self.game.timeg3 = True
            self.game.endmenu_display = False
            self.game.new_game('timeg3', pos = (1.5, 5.5), time = 420)
            self.game.editor_display = True
            self.game.mapdisplay = True
            self.game.timer.resume()

    def playNext(self):
        '''*****************************************************************************************************

        Method: playNext -->makes the game level updates and starts the next game mode

        ********************************************************************************************************'''
        #print("Next game clicked")
        self.game.client_manager.send_update_scores()
        self.game.client_manager.send_update_times()
        if self.game.pointg1:
            self.game.pointg1 = False
            self.game.pointg2 = True
            self.game.new_game('pointg2')
            self.game.endmenu_display = False
            self.game.editor_display = True
            self.game.mapdisplay = True
        elif self.game.pointg2:
            self.game.pointg2 = False
            self.game.pointg3 = True
            self.game.new_game('pointg3')
            self.game.endmenu_display = False
            self.game.editor_display = True
            self.game.mapdisplay = True
        elif self.game.timeg1:
            self.game.timeg1 = False
            self.game.timeg2 = True
            self.game.endmenu_display = False
            self.game.new_game('timeg2', pos = (1.5, 5.5), time = 360)
            self.game.timer.resume()
            self.game.editor_display = True
            self.game.mapdisplay = True
        elif self.game.timeg2:
            self.game.timeg2 = False
            self.game.timeg3 = True
            self.game.endmenu_display = False
            self.game.new_game('timeg3', pos = (1.5, 5.5), time = 420)
            self.game.timer.resume()
            self.game.editor_display = True
            self.game.mapdisplay = True
            