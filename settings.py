import math

#Standard game settings 
RES = WIDTH, HEIGHT = 1450, 900
FPS = 60
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

PLAYER_ROT_SPEED = 0.002
PLAYER_POS = 1.5, 1.5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.05
PLAYER_SIZE = 60
MAX_HEALTH = 100

FLOOR = (0,25,0)

FOV = math.pi / 3
HALF_FOV = FOV / 2
RAY_NUM = WIDTH // 2
HALF_NUM_RAYS = RAY_NUM // 2
DELTA_ANGLE = FOV / RAY_NUM
MAX_DEPTH = 20


SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // RAY_NUM


TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2



POSG1 = [(3.5, 8.5), (9.5,1.5), (11.5,2.5), (15.5,1.5), (8.5,8.5)]
POSG2 = [(1.5,8.5), (4.5,4.5), (6.5,8.5), (9.5,1.5) ,(12.5,2.5 ),(11.5,8.5)]
POSG3 = [(3.5,6.5), (1.5,4.5), (3.5,8.5), (6.5,5.5), (9.5,2.5),(12.5,5.5), (14.5,6.5),(18.5,6.5),(17.5,4.5)]

#exit to main menu help tutorial pointg1 pointg2 pointg3 time stuff