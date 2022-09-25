import pygame as pg 
import time  
import sys
from settings import *
from map import *
from player import *
from raycast import *
from textures import *
from gamepieces import *
from gamepiece_handler import *
from gun import *
from start import *
from texteditor import TextEditor
from editor import *
from start import *
from fire import *
from endmenu import *
from scoreboard import *
from mainmenu import *
from client_manager import *
from button import *
from points import*
from endmenu import *
from timer import *
import multiprocessing as mp
import socket
from threading import Thread
from ammohealth import *

from time import sleep
from time import *             #meaning from time import EVERYTHING
import time


class Game:
    def __init__(self):
        '''****************
            initial setup 
        *******************'''

        pg.init()
        #self.screen = pg.display.set_mode((0, 0),pg.FULLSCREEN)
        self.screen = pg.display.set_mode((RES[0], RES[1]))
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.text = 'Enter code:*'
        self.mapdisplay =False
        self.start = start(self)
        self.fire = Fire(self) 
        self.client_process = None #process to manage connection with server
        self.receive_Q = None 
        self.send_Q =  None
        self.client_manager = client_manager(self) #player details and score manager
        self.mainmenu = mainmenu(self)
        self.texteditor = Editor(self)
        self.endmenu = endmenu(self)
        self.start_display =True
        self.editor_display = False
        self.mainmenu_display = False
        self.endmenu_display = False
        self.help_display = False

        self.button_pos_x = 0.005*RES[0]
        self.button_pos_y = 0.005*RES[1]
        self.button_size_x = 0.1*(RES[0])
        self.button_size_y = 0.1*0.25*(RES[0])

        self.buttons = [
            Button(self, self.button_pos_x, self.button_pos_y, self.button_size_x, self.button_size_y, 'Exit to Main Menu', self.exittomainmenu, False, (255, 102, 102), (255, 51, 51), (76, 0, 155), 20),
            Button(self, self.button_pos_x , self.button_pos_y + 1.25*(self.button_size_y), self.button_size_x, self.button_size_y, 'Help', self.helpbutton, False, (0, 204, 204), (0, 255, 255), (0, 76, 153), 20), 
        ]

        #booleans to control which game mode is being played
        self.tutorialmode =False
        self.pointg1 = False
        self.pointg2 = False
        self.pointg3 = False
        self.timeg1 = False
        self.timeg2 = False
        self.timeg3 = False

        #start a new game
        self.player = Player(self)
        self.new_game('tutorial')




        
    def new_game(self,maptype = 'any',pos = (PLAYER_POS),pts = 0,time = 120):
        '''********************************************************************************

            Method: new_game --> Creates a new instance of gameobjects based on which game mode
            is bring played
            
            PARAM: maptype --> String (map name)
                   pos --> tuple (x starting value, y starting value)
                   pts --> int
                   time --> int

        **********************************************************************************'''
        
        self.map = Map(self,maptype)  
        if self.pointg1 or self.pointg2 or self.pointg3:
            self.texteditor = Editor(self) 
        self.player = Player(self,pos,pts)  
        self.textures = Textures(self)  
        self.raycast = Raycast(self)
        self.gamepieces_handler = GamepieceHandler(self)
        self.gun = Gun(self)
        self.ammohealth = ammohealth(self)
        if self.tutorialmode:
            self.player.ammo = 0
            self.ammohealth.subtract_ammo(25)
        if self.pointg1 or self.pointg2 or self.pointg3:
            self.points = points(self,420,10)
        elif self.timeg1 or self.timeg2 or self.timeg3:
            self.timer = timer(self,470,10,time,True)
        self.txtcheck = False


    def update(self):
        '''************************************************************************

        Method: update --> Makes necessary game engine calculations for each frame

        ***************************************************************************'''

        self.player.update()
        self.raycast.update()
        self.gamepieces_handler.update()
        self.gun.update()
        if self.start_display:
            self.fire.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

                      

    def draw(self):
        '''*****************************************************************
        
        Method: draw --> Decides what display should rendered onto the screen
        
        **********************************************************************'''
        
        if self.start_display:
            #Display PyMaze start and login screen 
            self.screen.fill((0, 0, 0))
            self.fire.draw()
            self.start.draw()

        elif self.mainmenu_display:
            #Display PyMaze main menu screen 
            self.mainmenu.draw()

        elif self.endmenu_display:
            #Display PyMaze end of game results screen
            self.endmenu.draw()

        elif self.tutorialmode:
            #Game screen to be displayed when players play tutorial mode
            self.textures.draw()
            self.ammohealth.draw()
            if self.player.pickedupgun:
                self.gun.draw()
            if self.editor_display: 
                self.texteditor.draw() 
            else: 
                self.player.draw_button()

        else:
            #Game screen to be displayed when players play competitive mode
            self.textures.draw()

            if self.pointg1 or self.pointg2 or self.pointg3:
                self.ammohealth.draw()
                self.points.draw(self.texteditor.pygame_events)

            elif self.timeg1 or self.timeg2 or self.timeg3:
                self.timer.draw(self.pygame_events)

            self.gun.draw()
            if self.editor_display: 
                self.texteditor.draw() 
            else: 
                self.player.draw_button()
        
        if self.mapdisplay:
            #Displays the 2D mini map
            self.map.draw()
            self.gamepieces_handler.draw()
            self.player.draw()

        if self.help_display:
            #Displays the help screen
           img = pg.image.load('resources/help.png')
           img = pg.transform.scale(img,(RES))
           self.screen.blit(img, (0,0))       
           self.buttons[1].process()
         
        if (not self.mainmenu_display) and (not self.endmenu_display) and (not self.start_display):
            #Displays the exit to main menu and help button when playing any game mode
            for button in self.buttons:
                button.process()  



    def check_events(self):
        '''************************************************************************
        
        Method: check_events --> Listens to keyboard and mouse input from the user
        
        ****************************************************************************'''

        self.pygame_events = pg.event.get()
        for event in self.pygame_events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit()


    def exittomainmenu(self):
        '''************************************************************************
        
        Method: exittomainmenu --> Returns the user back to the main menu screen
        
        ****************************************************************************'''

        self.mainmenu_display = True
        self.pointg1 = False
        self.pointg2 = False
        self.pointg3 = False
        self.timeg1 = False
        self.timeg2 = False
        self.timeg3 = False
        self.tutorialmode = False
        self.mapdisplay = False
        self.new_game('tutorial')

    
    def helpbutton(self):
        '''***********************************************************
        
        Method: helpbutton --> Displays the help menu when button is pressed
        
        **************************************************************'''
        if not self.help_display:
            self.help_display = True   
            #print('j')
        else: 
            self.help_display = False 
    
    def quit(self):
        '''***********************************************************
        
        Method: quit --> Called when player wants to terminate the game 
        
        **************************************************************'''
        self.client_process.kill()
        pg.quit()
        sys.exit()

    def run(self):
        '''***********************************************************
        
        Method: run --> Allows for the continous cycle of MVC
      
        **************************************************************'''

        while True:
            self.check_events() #controller
            self.update() #model
            self.draw() #view

def receiver_thread(receive_Q: mp.Queue, socket: socket.socket):
        """Creates a thread to receive packets from the server
        \nSequentially receives packets and stores it in the receive queue"""
        received = socket.recv(4096).decode('utf-8')
        print("Client receiver thread received: {0}".format(received))
        received = None
        #loop and wait to receive data
        while True:
            received = socket.recv(4096).decode('utf-8')
            receive_Q.put(received)
            print("Client receiver thread received: {0}".format(received))

def sender_thread(send_Q: mp.Queue, socket: socket.socket):
        """Creates a thread to send packets to the server
        \nSequentially sends whatever is in the send queue"""
        to_send = None
        #loop and check if need to send information
        while True:
            #if nothing to send
            if send_Q.empty():
                pass
            #if data to send
            else:
                while not send_Q.empty():
                    to_send = send_Q.get()
                    socket.send(str.encode(to_send))
                    if send_Q.qsize() > 1:
                        time.sleep(0.5)
                    print("Client sender thread sent: {0}".format(to_send))

    
def client_connection(send_Q: mp.Queue,  receive_Q: mp.Queue, host: str, port: str):
        """Creates a client object to manage the client server connection"""
        
        print("Client connection process started")
        
        print('Establishing connection...')
        clientSocket = socket.socket()
        try:
            clientSocket.connect((host, port))
        except socket.error as e:
                print(str(e))

        sender = Thread(target = sender_thread, args = (send_Q, clientSocket))
        receiver = Thread(target = receiver_thread, args = (receive_Q, clientSocket))

        sender.start()
        receiver.start()


if __name__ == '__main__':
    game = Game()
    mp.set_start_method("spawn") #make sure child process has just enough resources
    host = socket.gethostbyname(socket.gethostname()) #'196.47.195.124'
    port = 65432
    game.receive_Q = mp.Queue(100)
    game.send_Q =  mp.Queue(100)
    game.client_process = mp.Process(target = client_connection, args = (game.send_Q, game.receive_Q, host, port))
    game.client_process.start()
    game.run()