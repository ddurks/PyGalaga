import pygame, os

global FPS
FPS=50

global WIN_RESX
WIN_RESX=800

global WIN_RESY
WIN_RESY=600

global REFRESH_TIME
REFRESH_TIME=FPS*3

global GAMEWINDOW
GAMEWINDOW=pygame.Rect(50,0,WIN_RESX-50,WIN_RESY)

global Y_MIN, Y_MAX, X_MIN, X_MAX
Y_MIN = 0
Y_MAX = WIN_RESY
X_MAX = WIN_RESX-50
X_MIN = 50

global PLAYERS, SIDE_PANEL
PLAYERS=pygame.sprite.RenderUpdates()
SIDE_PANEL= pygame.sprite.RenderUpdates()

global BULLET_SPEED, BULLET_WIDTH
BULLET_SPEED=10
BULLET_WIDTH=10

global init_enemy_speed
init_enemy_speed=3

global enemy_spacing_x, enemy_spacing_y, enemy_bullet_odds
enemy_spacing_x=15
enemy_spacing_y=10
enemy_bullet_odds=15

global enemy_width, enemy_height
enemy_width=30
enemy_height=30

global smooth_scroll_var1, smooth_scroll_var2, explosion_speed
smooth_scroll_var1=10
smooth_scroll_var2=2
explosion_speed=5
Y_MIN
global points_x, points_y, health_x, health_y, defaultsize, max_health

global healthbar_offset_y,healthbar_offset_x,healthbar_width
points_x=0
points_y=5
health_x=0
health_y=50
bullets_x=0
bullets_y=105
healthbar_offset_y=60
healthbar_offset_x=10
healthbar_width=7
defaultsize=14
max_health=100

global BG_Speed, init_stars, star_color
BG_Speed=5
init_stars=15
star_color=(155,155,155)

global bgcolor, sidepanelcolor
bgcolor=(0,0,0)
sidepanelcolor=(128,128,128)
menucolor=(128,128,128)

global asdf
asdf=0

global CLOCK
CLOCK = pygame.time.Clock()

defaultfont="freesansbold.ttf"

window = pygame.display.set_mode ((WIN_RESX, WIN_RESY))
pygame.display.set_caption("PyGalaga")
surface = pygame.display.get_surface()

screen = pygame.Surface((WIN_RESX,WIN_RESY))
screen.fill(bgcolor)

pygame.init()

print ("Globals Loaded")
