from doctest import script_from_examples
import socket
from _thread import *
import sqlite3

class server:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 65432
        self.thread_count = 0

    def register(self, username, password):
        """Manages user register requests from the client"""
        db_conn = sqlite3.connect('mazepy.db')
        users = db_conn.execute("SELECT username from users")

        for row in users:
            user = row[0]
            if user == username:
                return False

        db_conn.execute("INSERT INTO users VALUES ('{0}', '{1}', {2}, {2}, {2}, {2}, {2}, {2})".format(username, password, 0))
        db_conn.commit()
        db_conn.close()
        return True

    def log_in(self, username, password):
        """Manages user log-in requests from the client"""
        db_conn = sqlite3.connect('mazepy.db')
        users = db_conn.execute("SELECT username, password from users")

        for row in users:
            user = row[0]
            pword = row[1]
            if user == username:
                if pword == password:
                    db_conn.close()
                    return 0
                else:
                    db_conn.close()
                    return 1 
        db_conn.close() 
        return 2

    def int_to_en(self, num):
        """Given an int32 number, print it in English. 
        \n Adapted from: https://stackoverflow.com/questions/8982163/how-do-i-tell-python-to-convert-integers-into-words"""
        d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
            6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
            11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
            15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
            19 : 'nineteen', 20 : 'twenty',
            30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
            70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
        assert(0 <= num)

        if (num < 20):
            return d[num]
        else:
            raise "No numbers over 20 allowed"


    def update_timeboard(self, leaderboard_index, username, score):
        """Update time leaderboard with incoming player time
        \nThe incoming time will only be updated if this is the personal best"""
        db_conn = sqlite3.connect('mazepy.db')
        print("Adding {0} with score {1} to timeboard".format(username, score))
        score = int(score)
        highscore_time = 'highscore_time_'
        db_conn.execute("UPDATE users SET {0} = {2} WHERE username = '{1}' AND {0} < {2}".format(highscore_time + self.int_to_en(leaderboard_index), username, score))
        db_conn.commit()
        db_conn.close()
        return "201"

    def update_scoreboard(self, leaderboard_index, username, score):
        """Update time leaderboard with incoming player score
        \nThe incoming score will only be updated if this is the personal best"""
        db_conn = sqlite3.connect('mazepy.db')
        print("Adding {0} with score {1} to scoreboard".format(username, score))
        score = int(score)
        highscore_point = 'highscore_point_'
        db_conn.execute("UPDATE users SET {0} = {2} WHERE username = '{1}' AND {0} < {2}".format(highscore_point + self.int_to_en(leaderboard_index), username, score))
        db_conn.commit()
        db_conn.close()
        return "202"

    def timeboard_to_string(self, leaderboard_index):
        """Converts the sql query to a formatted string which can be sent to the user"""
        db_conn = sqlite3.connect('mazepy.db')
        players = ""
        scores = ""
        highscore_time = 'highscore_time_'

        users = db_conn.execute("SELECT username, {0} from users ORDER BY {0} DESC".format(highscore_time + self.int_to_en(leaderboard_index)))

        for row in users:
            user = row[0]
            score = row[1]
            players = players + user + ","
            scores = scores + str(score) + ","

        db_conn.close()

        print(players)
        print(scores)
        
        return "200><{0}><{1}".format(players[:-1], scores[:-1])

    def scoreboard_to_string(self, leaderboard_index):
        """Converts the sql query to a formatted string which can be sent to the user"""
        db_conn = sqlite3.connect('mazepy.db')
        players = ""
        scores = ""
        highscore_point = 'highscore_point_'

        users = db_conn.execute("SELECT username, {0} from users ORDER BY {0} DESC".format(highscore_point + self.int_to_en(leaderboard_index)))

        for row in users:
            user = row[0]
            score = row[1]
            players = players + user + ","
            scores = scores + str(score) + ","

        db_conn.close()

        print(players)
        print(scores)
        
        return "200><{0}><{1}".format(players[:-1], scores[:-1])


    def client_handler(self, connection, server):
        """Creates a thread to manage the connection between the server and client"""
        connection.send(str.encode('You are now connected to the replay server...'))

        data = connection.recv(2048)
        message = data.decode('utf-8')

        print("Recieved data from user: {0}".format(message))

        result = None    
        
        message_data = message.split("><")
        code = message_data[0]
        username = message_data[1]
        password = message_data[2]

        #register/log-in block
        while True:
            if code == "1":
                result = server.register(username, password)
                if result:
                    connection.sendall(str.encode("100><{0}".format(username)))
                    break
                else:
                    connection.sendall(str.encode("110"))
            elif code == "2":
                result = server.log_in(username, password)
                if result == 0:
                    connection.sendall(str.encode("101><{0}".format(username)))
                    break
                elif result == 1:
                    connection.sendall(str.encode("111"))
                elif result == 2:
                    connection.sendall(str.encode("112"))
            else:
                print("Error")
            
            data = connection.recv(2048)
            message = data.decode('utf-8')
            print("Recieved data from user: {0}".format(message))
            result = None  
            message_data = message.split("><")
            code = message_data[0]
            username = message_data[1]
            password = message_data[2]

        #Leaderboard requests block
        while True:
            data = connection.recv(2048)
            message = data.decode('utf-8')
            print("Recieved data from user: {0}".format(message))
            message_data = message.split("><")
            code = message_data[0]
            code = int(code)
            response = ""

            #send selected scoreboard to user
            if code // 10 == 1:
                board_number = code % 10
                if board_number > 0 and board_number < 4:
                    response = server.scoreboard_to_string(board_number)
                    connection.sendall(str.encode(response))
            #send selected timeboard to user
            elif code // 10 == 2:
                board_number = code % 10
                if board_number > 0 and board_number < 4:
                    response = server.timeboard_to_string(board_number)
                    connection.sendall(str.encode(response))
            #add person to scoreboard
            elif code // 10 == 3:
                board_number = code % 10
                player = message_data[1]
                score = message_data[2]
                if board_number > 0 and board_number < 4:
                    response = server.update_scoreboard(board_number, player, score)
                    connection.sendall(str.encode(response))
            #add person to timeboard
            elif code // 10 == 4:
                board_number = code % 10
                player = message_data[1]
                score = message_data[2]
                if board_number > 0 and board_number < 4:
                    response = server.update_timeboard(board_number, player, score)
                    connection.sendall(str.encode(response))
            else:
                pass


    def accept_connection(self, serversocket):
        """Accepts the connection and creates a thread for the socket connection"""
        client, address = serversocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(self.client_handler, (client, self))

    def start(self):
        """Accepts the connection and creates a socket connection"""
        serversocket = socket.socket()
        try:
            serversocket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))
        print(f'Server is listing on the port {self.port}...')
        serversocket.listen()

        while True:
            self.accept_connection(serversocket)

server_instance = server()
server_instance.start()