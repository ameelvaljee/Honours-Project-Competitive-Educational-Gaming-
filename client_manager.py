import datetime
import random
import math
from re import L
import time

class client_manager:
    def __init__(self, game):
        """Creates a client_manager object. This object managers the leaderboards and interaction with the server"""
        self.game = game
        self.name = "player" + str(random.randint(100, 999))
        self.timeboards = [ #stores the leaderboard for times for each respective map
            [],
            [],
            []
        ] 
        self.timeboard_positions = [-1, -1, -1]
        self.previous_times = [0, 0, 0]
        self.scoreboards = [ #stores the leaderboard for scores for each respective map
            [],
            [],
            []
        ]
        self.scoreboard_positions = [-1, -1, -1]
        self.previous_scores = [0, 0, 0]

    def sort(self, leaderboard, reverse_list = False):
        """Function to sort the leaderboards based on the times or scores of each player"""
        leaderboard.sort(key = lambda x: x[1])
        if reverse_list:
            leaderboard.reverse()

    def get_pos(self, leaderboard):
        """"Returns the player's current position on that leaderboard"""
        i = 0
        for position in leaderboard:
            current_player = position[0]
            if current_player == self.name:
                return i
            i = i + 1
        return -1

    def add_new_time(self, time, leaderboard_index):
        """Used to add a player's time to the leaderboard.
        \nTime is an integer represent the number of seconds
        \nLeaderboard index is the respective map leaderboard"""
        timeboard_pos = self.timeboard_positions[leaderboard_index]
        timeboard = self.timeboards[leaderboard_index]
        if timeboard_pos == -1:   
            timeboard.append([self.name, time])
        else:
            self.previous_times[leaderboard_index] = timeboard.pop(timeboard_pos)[1]
            timeboard.append([self.name, time])
        self.sort(timeboard, True)
        self.timeboard_positions[leaderboard_index] = self.get_pos(timeboard)

    def add_new_score(self, score, leaderboard_index):
        """Used to add a player's score to the leaderboard.
        \nTime is an integer represent the number of seconds
        \nLeaderboard index is the respective map leaderboard"""
        scoreboard_pos = self.scoreboard_positions[leaderboard_index]
        scoreboard = self.scoreboards[leaderboard_index]
        #print(scoreboard_pos)
        #print(scoreboard)
        if scoreboard_pos == -1:
            scoreboard.append([self.name, score])
        else:
            self.previous_scores[leaderboard_index] = scoreboard.pop(scoreboard_pos)[1]
            scoreboard.append([self.name, score])
        self.sort(scoreboard, True)
        self.scoreboard_positions[leaderboard_index] = self.get_pos(scoreboard)
        #print(scoreboard)

    def send_update_scores(self):
        """Used to send a player's scores to the server."""
        code = 31
        pos = None
        score = None
        i = 0
        while(i < 3):
            pos = self.scoreboard_positions[i]
            score = self.scoreboards[i][pos][1]
            self.game.send_Q.put("{}><{}><{}".format(code + i, self.name, score))
            i = i + 1

    def send_update_times(self):
        """Used to send a player's times to the server."""
        code = 41
        pos = None
        i = 0
        while(i < 3):
            pos = self.timeboard_positions[i]
            score = self.timeboards[i][pos][1]
            self.game.send_Q.put("{}><{}><{}".format(code + i, self.name, score))
            i = i + 1

    def change_name(self, name):
        """Change the client's ID"""
        self.name = name

    def get_updated_timeboard(self, leaderboard_index):
        """Retrieve the latest leaderboards for times from the leaderboards.
        \nSends a request to the server. Will fail if there is an issue with the server connection."""
        code = 21 + leaderboard_index
        self.game.send_Q.put("{}><{}".format(code, self.name))
        while True:
            if  self.game.receive_Q.empty():
                pass
            else:
                self.timeboards[leaderboard_index] = self.response_to_leaderboard(self.game.receive_Q.get())
                self.timeboard_positions[leaderboard_index] = self.get_pos(self.timeboards[leaderboard_index])
                return self.timeboards[leaderboard_index]

    def get_updated_scoreboard(self, leaderboard_index):
        """Retrieve the latest leaderboards for scores from the leaderboards.
        \nSends a request to the server. Will fail if there is an issue with the server connection."""
        code = 11 + leaderboard_index
        self.game.send_Q.put("{}><{}".format(code, self.name))
        while True:
            if  self.game.receive_Q.empty():
                pass
            else:
                self.scoreboards[leaderboard_index] = self.response_to_leaderboard(self.game.receive_Q.get())
                self.scoreboard_positions[leaderboard_index] = self.get_pos(self.scoreboards[leaderboard_index])
                return True

    def get_score(self, leaderboard_index):
        """Get the player's score for that specific score leaderboard.
            \nLeaderboard index is the respective map leaderboard
        """
        score = 1
        place_in_leaderboard = self.scoreboard_positions[leaderboard_index]
        return self.scoreboards[leaderboard_index][place_in_leaderboard][score]

    def get_time(self, leaderboard_index):
        """Get the player's time for that specific score leaderboard.
            \nLeaderboard index is the respective map leaderboard
        """
        score = 1
        place_in_leaderboard = self.timeboard_positions[leaderboard_index]
        return self.timeboards[leaderboard_index][place_in_leaderboard][score]

    def seconds_to_min(self):
        """Converts seconds from the integer value to a minutes and seconds representation like: 02:36"""

        time_string = str(datetime.timedelta(seconds = self.timeboard_time))

        return time_string[2:]

    def response_to_leaderboard(self, response):
        """Converts the retrieve server response to a leaderboard for storage"""
        response = response.split("><")
        users = response[1].split(",")
        scores = response[2].split(",")
        scores = [int(score) for score in scores]
        leaderboard = []
        i = 0
        while (i < len(users)):
            leaderboard.append([users[i], scores[i]])
            i = i + 1
        return leaderboard

    def get_timeboard(self, leaderboard_index):
        """Returns the leaderboard for time.
        \nLeaderboard index is the respective map leaderboard"""
        return self.timeboards[leaderboard_index]

    def get_time_board_pos(self, leaderboard_index):
        """Returns the player's position on that time leaderboard.
        \nLeaderboard index is the respective map leaderboard"""
        return self.timeboard_positions[leaderboard_index] + 0

    def get_scoreboard(self, leaderboard_index):
        """Returns the leaderboard for score.
        \nLeaderboard index is the respective map leaderboard"""
        return self.scoreboards[leaderboard_index]

    def get_score_board_pos(self, leaderboard_index):
        """Returns the player's position on that score leaderboard.
        \nLeaderboard index is the respective map leaderboard"""
        return self.scoreboard_positions[leaderboard_index] + 0

    def calculate_final_time(self, time: int, num_of_lines = 0, num_of_steps = 0):
        """Calculates the player's final time 
        \nWhere FINAL TIME = [time remaining to solve with a max of 2 minutes] + [code effeciency bonus with a max of 30 seconds]
        \nWhere [code effeciency bonus with a max of 30 seconds] = [time remaining to solve] + [1/log(number lines of code)*15 + 1/log(number of in-game steps taken)*15] 
        \nIf num_of_steps or num_of_steps are not provided (or equal to zero) it returns just the time. 
        \nPlease call this function when adding your score to the client_manager i.e. add_new_time(calculate_final_time(time, num_of_lines, num_of_steps), leaderboard_index)"""
        if num_of_lines == 0 or num_of_steps == 0:
            return time
        else:
            return time + ((1/(math.log(math.e, num_of_lines)))*15 + (1/(math.log(math.e, num_of_steps)))*15)

    def calculate_final_score(self,points):
        """Calculates the player's final score"""
        return points

    def print(self):
        """Prints the client manager field values in the console"""
        print("Client name: {0}".format(self.name))
        print("Timeboard Positions: {0}".format(self.timeboard_positions))
        print("Timeboard: {0}".format(self.timeboards))
        print("Scoreboard Positions: {0}".format(self.scoreboard_positions))
        print("Scoreboard {0}".format(self.scoreboards))