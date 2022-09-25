import pygame as pg
import random
import sys

class scoreboard:
    def __init__(self, game, title, leaderboard, player_pos, x = 0, y = 0, w = 300, h = 200, points = None, client_manager = None):
        self.game = game
        self.id = random.randint(100, 999)
        self.leaderboard = leaderboard
        self.not_on_board = False
        if player_pos == -1:
            self.player_pos = 1
            self.not_on_board = True
        else:
            self.player_pos = player_pos
        self.title = title

        self.points = points
        self.client_manager = client_manager
        #print("On intialization (in scoreboard{1}) pos is {0}".format(self.player_pos, self.id))

        self.four_to_display = []
        self.get_four()

        self.text_to_draw = []
        self.create_leaderboard_text()

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.font_size = 22
        self.title_size = self.font_size + 12
        self.sub_size = self.font_size + 8

        self.scoreboard_title_bar = pg.Rect((self.x, self.y), (self.w, (self.h)/4))
        self.scoreboard_details_bar = pg.Rect((self.x, self.y + ((self.h)/4)), (self.w, (self.h)/4))
        self.scoreboard_bar = pg.Rect((self.x, self.y + ((self.h)/2)), (self.w, (self.h)/2))
        
        font_renderer = pg.font.SysFont(None, self.title_size)
        self.scoreboard_title = font_renderer.render("{0} Leaderboard".format(self.title), True, (0, 0, 0))
        font_renderer = pg.font.SysFont(None, self.sub_size)
        self.scoreboard_pos_title = font_renderer.render("Pos", True, (255, 255, 255))
        self.scoreboard_player_title = font_renderer.render("Player", True, (255, 255, 255))
        self.scoreboard_score_title = font_renderer.render("Score", True, (255, 255, 255))

    def get_four(self):
        """Get the four players (and their information) to be displayed"""
        # print("Leaderboard get_four is using")
        # print(self.leaderboard)
        # print("Get four call")
        pos = self.player_pos - 1
        last_four = len(self.leaderboard) - 4
        # print("Pos is " + str(pos))
        # print("Last four are " + str(last_four))

        if len(self.leaderboard) <= 4:
            #print("Leaderboard smaller than 4 path")
            self.four_to_display = self.leaderboard
        else:
            if pos >= 0 and pos < 4:
                #print("Leaderboard pos less than 4 path")
                self.four_to_display = self.leaderboard[0:4]
            elif pos > last_four:
                #print("Leaderboard pos greater than 4 path")
                self.four_to_display = [self.leaderboard[0]] + self.leaderboard[-3:]
            else:
                #print("Leaderboard pos last 4 path")
                self.four_to_display = [self.leaderboard[0], self.leaderboard[pos-1], self.leaderboard[pos], self.leaderboard[pos+1]]

        #print(self.four_to_display)

        self.get_relative_pos()

    def get_relative_pos(self):
        """Get the relative position of the player and the players around them"""
        pos = self.player_pos - 1
        last_pos = len(self.leaderboard)
        last_four = len(self.leaderboard) - 4

        #print("In scoreboard{2} in relative_pos func pos is {0} while leader board is {1}".format(pos, self.leaderboard, self.id))
        
        if len(self.leaderboard) == 1:
            relative_pos = [1]
        elif len(self.leaderboard) <= 4:
            relative_pos = [x for x in range(1, last_pos + 1)]
        else:
            if pos >= 0 and pos < 4:
                relative_pos = [1, 2, 3, 4]
            elif pos > last_four:
                relative_pos = [1, last_pos - 2, last_pos -1, last_pos]
            else:
                relative_pos = [1, self.player_pos - 1, self.player_pos, self.player_pos + 1]
        i = 0
        loop = min(len(self.leaderboard), 4)
        while (i < loop):
            self.four_to_display[i] = [relative_pos[i]] + self.four_to_display[i]
            #print(i)
            i = i + 1

    def updateTitle(self, title: str):
        """Update the displayed title of the leaderboard"""
        self.title = title
        font_renderer = pg.font.SysFont(None, self.title_size)
        self.scoreboard_title = font_renderer.render("{0} Leaderboard".format(self.title), True, (0, 0, 0))

    def update(self, leaderboard, player_pos):
        """Update the leaderboard with new leaderboard data"""
        if player_pos == -1:
            self.player_pos = 1
            self.not_on_board = True
        else:
            self.player_pos = player_pos
            self.not_on_board = False

        #print("Leaderboard with player")
        leaderboard_until_player = leaderboard[:player_pos]
        #print(leaderboard_until_player)

        #print("Leaderboard without player")
        rest_of_list = leaderboard[player_pos:]
        without_zeros = [player for player in rest_of_list if 0 not in player]
        with_zeros = [player for player in rest_of_list if 0 in player]
        with_zeros.sort(key = lambda x: x[0]) 
        rest_of_list = without_zeros + with_zeros

        #print(rest_of_list)

        # player = leaderboard.pop(player_pos - 1)

        # without_zeros = [player for player in leaderboard if 0 not in player]
        # with_zeros = [player for player in leaderboard if 0 in player]

        # with_zeros.sort(key = lambda x: x[0]) 
        
        # leaderboard = without_zeros + with_zeros

        # leaderboard.insert(player_pos - 1, player)

        #print("In scoreboard{2} in update player_pos is {0} while leader board is {1}".format(self.player_pos, self.leaderboard, self.id))

        self.leaderboard = leaderboard_until_player + rest_of_list

        self.four_to_display = []
        self.get_four()
        self.create_leaderboard_text()

    def create_leaderboard_text(self):
        """Create images for text to be rendered"""
        self.text_to_draw = []
        #print("in leaderboard text")
        num_font_renderer = pg.font.SysFont(None, 22)
        text_renderer = pg.font.SysFont(None, 22)

        gold = (255, 215, 0)
        silver = (125, 125, 125)
        bronze = (103,71,54)
        white = (255, 255, 255)
        colour_gradient = [(100, 223, 223), (78, 168, 222), (94, 96, 206), (116, 0, 184)]

        pos = None
        player = None
        score = None

        i = 0
        for place in self.four_to_display:
            if place[0] == 1:
                pos = num_font_renderer.render(self.make_ordinal(place[0]), True, gold)
            elif place[0] == 2:
                pos = num_font_renderer.render(self.make_ordinal(place[0]), True, silver)
            elif place[0] == 3:
                pos = num_font_renderer.render(self.make_ordinal(place[0]), True, bronze)
            else:
                pos = num_font_renderer.render(self.make_ordinal(place[0]), True, white)
            
            if self.not_on_board:
                if place[0] == self.player_pos:     
                    player = text_renderer.render(place[1], True, white)
                else:
                    player = text_renderer.render(place[1], True, white)
            else:   
                if place[0] == self.player_pos:
                    player = text_renderer.render(place[1] + " (You)", True, white)     
                else:
                    player = text_renderer.render(place[1], True, white)

            score = num_font_renderer.render(str(place[2]), True, colour_gradient[i])

            self.text_to_draw.append([pos, player, score])
            i = i + 1

        #print(self.text_to_draw)

    def draw(self):
        """Draws and displays the leaderboard to the screen"""
        #scoreboard header
        pg.draw.rect(pg.display.get_surface(), (255, 255, 255), (self.scoreboard_title_bar))
        #pg.draw.rect(pg.display.get_surface(), (0, 32, 96), (self.scoreboard_details_bar))
        pg.draw.rect(pg.display.get_surface(), (0, 32, 96), (self.scoreboard_details_bar))
        pg.draw.rect(pg.display.get_surface(), (0, 32, 96), (self.scoreboard_bar))

        self.game.screen.blit(self.scoreboard_title, ((self.x) + 0.03*(self.w), (self.y) + 0.075*(self.h)))
        self.game.screen.blit(self.scoreboard_pos_title, ((self.x) + + 0.03*(self.w), (self.y + ((self.h)/4)) + 0.075*(self.h)))
        self.game.screen.blit(self.scoreboard_player_title, ((self.x) + 0.03*(self.w) + ((self.w)/5), (self.y + ((self.h)/4)) + 0.075*(self.h)))
        self.game.screen.blit(self.scoreboard_score_title, ((self.x) + 0.03*(self.w) + 2*((self.w)/3), (self.y + ((self.h)/4)) + 0.075*(self.h)))

        #player text
        offset = 0
        for player_details in self.text_to_draw:
            self.game.screen.blit(player_details[0], ((self.x) + 0.03*(self.w), (self.y + ((self.h)/2)) + offset))
            self.game.screen.blit(player_details[1], ((self.x) + 0.03*(self.w) + ((self.w)/5), (self.y + ((self.h)/2)) + offset))
            self.game.screen.blit(player_details[2], ((self.x) + 0.03*(self.w) + 2*((self.w)/3), (self.y + ((self.h)/2)) + offset))
            offset = offset + (self.h)/8

    def live_draw(self):
        """Draws and displays the leaderboard to the screen and updates the leaderboard frame by frame"""
        if self.points == None or self.client_manager == None:
            sys.exit()
        else:
            #update the time leaderboard using current time
            self.client_manager.add_new_score(self.points.get_points(), 0)

            #update our stored time
            self.update(self.client_manager.get_scoreboard(0), self.client_manager.get_score_board_pos(0) + 1)

            #scoreboard header
            pg.draw.rect(pg.display.get_surface(), (255, 255, 255), (self.scoreboard_title_bar))
            #pg.draw.rect(pg.display.get_surface(), (0, 32, 96), (self.scoreboard_details_bar))
            pg.draw.rect(pg.display.get_surface(), (0, 32, 96), (self.scoreboard_details_bar))
            pg.draw.rect(pg.display.get_surface(), (0, 32, 96), (self.scoreboard_bar))

            self.game.screen.blit(self.scoreboard_title, ((self.x) + 0.03*(self.w), (self.y) + 0.075*(self.h)))
            self.game.screen.blit(self.scoreboard_pos_title, ((self.x) + + 0.03*(self.w), (self.y + ((self.h)/4)) + 0.075*(self.h)))
            self.game.screen.blit(self.scoreboard_player_title, ((self.x) + 0.03*(self.w) + ((self.w)/5), (self.y + ((self.h)/4)) + 0.075*(self.h)))
            self.game.screen.blit(self.scoreboard_score_title, ((self.x) + 0.03*(self.w) + 2*((self.w)/3), (self.y + ((self.h)/4)) + 0.075*(self.h)))

            #player text
            offset = 0
            for player_details in self.text_to_draw:
                self.game.screen.blit(player_details[0], ((self.x) + 0.03*(self.w), (self.y + ((self.h)/2)) + offset))
                self.game.screen.blit(player_details[1], ((self.x) + 0.03*(self.w) + ((self.w)/5), (self.y + ((self.h)/2)) + offset))
                self.game.screen.blit(player_details[2], ((self.x) + 0.03*(self.w) + 2*((self.w)/3), (self.y + ((self.h)/2)) + offset))
                offset = offset + (self.h)/8

    def print(self):
        print("Pos    Player                        Score")
        for place in self.four_to_display:
            print("{0}    {1}                        {2}".format(place[0], place[1], place[2]))

    def make_ordinal(self, n):
        '''
        Convert an integer into its ordinal representation::

            make_ordinal(0)   => '0th'
            make_ordinal(3)   => '3rd'
            make_ordinal(122) => '122nd'
            make_ordinal(213) => '213th'
        '''
        n = int(n)
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        return str(n) + suffix
