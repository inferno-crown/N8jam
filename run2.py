import pygame, sys, random
from pygame.constants import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP
pygame.init()
#wn
wn_height = 608
wn_width = 608
wn_bg = (50,50,50)
wn = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('XZIceCube')
#other basic variables
clock = pygame.time.Clock()
fps = 60
isclicky = False
level_num = 1
boss_level_num = 3
boss_health = 50
starting_game = False
upgrade = [pygame.Rect(64,105,32,8)]
upgrade_sprite = pygame.image.load('sprites\\upgrade.png').convert_alpha()
control_list = False
#classes
class Player():
    def __init__(self):
        self.movement = [0,0]
        self.size = [32,32]
        self.val = [7,16]
        self.isattack = False
        self.sprite = [pygame.image.load('sprites\\play-right.png').convert_alpha(), pygame.image.load('sprites\\play-left.png').convert_alpha()]
        self.rect =pygame.Rect(100,100,self.size[0],self.size[1])
        self.direction = {'left':False, 'right':False, 'up': False,}
        self.sword_sprite = [pygame.image.load('sprites\\sword-right.png').convert_alpha(),pygame.image.load('sprites\\sword-left.png').convert_alpha(),pygame.image.load('sprites\\sword-up.png').convert_alpha(),pygame.image.load('sprites\\sword-down.png').convert_alpha()]
        self.facing = {'left':True, 'right':False,'top':False,'bottom':False}
        self.sword = pygame.Rect(1000,1000,self.size[0],self.size[1])
        self.upgrade = False
class Platforms(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load('sprites\\wall.png').convert_alpha()
        self.end_rect =pygame.Rect(self.x,self.y,32,32)
        self.rect = self.sprite.get_rect(center=(self.x, self.y))
class Enemies():
    def __init__(self):
        self.movement = [0,0]
        self.size = [32,32]
        self.val = [8,16]
        self.isattack = False
        self.sprite = pygame.image.load('sprites\\slime.png').convert_alpha()
        self.sprite_b = pygame.image.load('sprites\\boss.png').convert_alpha()
        self.rect =pygame.Rect(100,100,self.size[0],self.size[1])
        self.color = (255,0,0)
play = Player()
tiles = []
en_tiles = []
end_tiles = [Platforms((608-32),0),Platforms((608-64),0),Platforms((608-32),32),Platforms((608-64),32)]
enemies = []
boss_l = []
stop_button = pygame.Rect(0, 0, 32, 32); button_sprite_s = pygame.image.load('sprites\\start.png').convert()
#draw
def draw():
    if play.isattack:
        if play.facing['top']:
            wn.blit(play.sword_sprite[2],play.sword)
        elif play.facing['bottom']:
            wn.blit(play.sword_sprite[3],play.sword)
        elif play.facing['right']:
            wn.blit(play.sword_sprite[0],play.sword)
        else: 
            wn.blit(play.sword_sprite[1],play.sword)
    if level_num < boss_level_num:
        for finish in end_tiles:
            pygame.draw.rect(wn,(0,150,0),finish.end_rect)
    for en in enemies:
        wn.blit(en.sprite,en.rect)
    for en in boss_l:
        wn.blit(en.sprite_b,en.rect)
    if level_num == 1:
        for up in upgrade:
            wn.blit(upgrade_sprite,up)
    for tile in tiles:
        wn.blit(tile.sprite,tile.rect)
    if play.facing['left']:
        wn.blit(play.sprite[1],play.rect)
    else:
        wn.blit(play.sprite[0],play.rect)
    wn.blit(button_sprite_s,stop_button)
def s_button():
    global starting_game, control_list
    mouse = pygame.mouse.get_pos()
    if stop_button.collidepoint(mouse):
        starting_game = False; control_list = False
#player swords
def update_sword():
    if isclicky:
        play.sword.center = play.rect.center
        if play.facing['left'] and not play.facing['top'] and not play.facing['bottom']:
            play.sword.right = play.rect.left
        if play.facing['right'] and not play.facing['top'] and not play.facing['bottom']:
            play.sword.left = play.rect.right
        if play.facing['top']:
            play.sword.bottom = play.rect.top
        if play.facing['bottom']:
            play.sword.top = play.rect.bottom
def play_dead():
    for en in enemies:
        if play.rect.colliderect(en.rect):
            play.rect.x = 32; play.rect.y = wn_height-64
    for boss in boss_l:
        if play.rect.colliderect(boss.rect):
            play.rect.x = 32; play.rect.y = wn_height-64
def new_sword():
    if level_num == 1:
        for up in upgrade:
            if play.rect.colliderect(up):
                play.upgrade = True
                up.x = -1000
                up.y = -1000
def upgrade_text():
    my_font = pygame.font.SysFont('arial', 25)
    my_label = my_font.render('''THUMP THUMP''', 1, (155,0,155))
    if play.upgrade and level_num == 1:
        wn.blit(my_label,(random.randrange(150,201),random.randrange(150,201)))
        play.rect.x += random.randrange(-5,6); play.rect.y += random.randrange(-15,15)
#tile map
def create_levels():
    x = y = 0
    maps = {1:[
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
                ['0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','1'],
                ['2','0','0','0','0','0','0','0','0','0','2','0','0','0','0','0','0','0','0','0'],
                ['1','1','1','1','1','1','1','1','1','1','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','2','0','0','0','2','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','1','1','1','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['1','1','1','1','3','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
                ], 2:[
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','2','0','0','0','0','2','0','0','0'],
            ['0','0','0','1','1','1','0','0','0','0','0','0','1','1','1','1','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','2','0','0','0','0','2','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','1','1','1','1','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','3','0','0','0','0','0','0','0','3','1','1','0','0','0','0','0','0','0','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
        ], 3:[
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']        
        ]}
    level = maps.get(level_num)
    for row in level:
        for col in row:
            if col == '1':
                tiles.append(Platforms(x,y))
            elif col == '2':
                en_tiles.append(Platforms(x,y))
            elif col == '3':
                en_tiles.append(Platforms(x,y))
                tiles.append(Platforms(x,y))
            x+=32
        y+=32
        x=0
def set_level_pos():
    play.rect.x = 0
    play.rect.y = 600-128
def end_level():
    global level_num, tiles, enemies, en_tiles
    for tile in end_tiles:
        if play.rect.colliderect(tile.end_rect):
            level_num += 1
            tiles = []
            en_tiles = []
            enemies = []
            create_levels()
            spawn_en()
            set_level_pos()
#move player
def key_inputs():
    global isclicky
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_d:
                play.direction['right'] = True
                play.facing['left'] = False
                play.facing['right'] = True
                play.facing['top'] = False
                play.facing['bottom'] = False
            if event.key == pygame.K_a:
                play.direction['left'] = True
                play.facing['left'] = True
                play.facing['right'] = False
                play.facing['top'] = False
                play.facing['bottom'] = False
            if event.key == pygame.K_w:
                play.facing['top'] = True
                play.facing['bottom'] = False
            if event.key == pygame.K_s:
                play.facing['top'] = False
                play.facing['bottom'] = True
            if event.key == pygame.K_j and not play.direction['up']:
                play.direction['up'] = True
            if event.key == pygame.K_k and not isclicky:
                isclicky = True
                play.isattack = True
        if event.type == KEYUP:
            if event.key == pygame.K_d:
                play.direction['right'] = False
            if event.key == pygame.K_a:
                play.direction['left'] = False
            if event.key == pygame.K_w:
                play.facing['top'] = False
            if event.key == pygame.K_s:
                play.facing['bottom'] = False
            if event.key == pygame.K_k:
                isclicky = False
                play.isattack = False
                play.sword.centerx = -1000
                play.sword.centery = -1000
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                s_button()
def move_player():
    play.movement = [0,0]
    play.movement[1] += 10
    if play.direction['right'] and play.rect.right < wn_width:
        play.movement[0] += play.val[0]
    if play.direction['left'] and play.rect.left > 0:
        play.movement[0] -= play.val[0]
    if play.direction['up']:
        play.movement[1] = 0
        play.movement[1] -= play.val[1]
        play.val[1] -= 1
        if play.val[1] < -16:
            play.val[1] = 16
            play.direction['up'] = False     
def collision_test(tiles):
    collisions = []
    for tile in tiles:
        if play.rect.colliderect(tile):
            collisions.append(tile)
    return collisions
def update_move(tiles):
    play.rect.x += play.movement[0]
    collisions = collision_test(tiles)
    for tile in collisions:
        if play.movement[0] > 0:
            play.rect.right = tile.rect.left
        if play.movement[0] < 0:
            play.rect.left = tile.rect.right
    play.rect.y += play.movement[1]
    collisions = collision_test(tiles)
    for tile in collisions:
        if play.movement[1] > 0:
            play.rect.bottom = tile.rect.top
        if play.movement[1] < 0:
            play.rect.top = tile.rect.bottom
#enimies
def boss_falls():
    for en in boss_l:
        if en.rect.y > wn_height:
            en.rect.y = -75
            en.rect.x = random.randrange(0,wn_height-en.size[0])
def l_1():
    en_1 = Enemies()
    en_1.rect.x = 300
    en_1.rect.y = wn_height - 49
    en_2 = Enemies()
    en_2.rect.x = 240
    en_2.rect.y = 430
    en_2.val[0] = 5
    en_3 = Enemies()
    en_3.rect.x = 32
    en_3.rect.y = 80
    en_3.val[0] = 7
    en_4 = Enemies()
    en_4.rect.x = 45
    en_4.rect.y = 80
    en_4.val[0] = 8
    en_5 = Enemies()
    en_5.rect.x = 64
    en_5.rect.y = 80
    en_5.val[0] = 9
    enemies.append(en_1)
    enemies.append(en_2)
    enemies.append(en_3)
    enemies.append(en_4)
    enemies.append(en_5)
def l_2():
    en_1 = Enemies()
    en_1.rect.x = 64
    en_1.rect.y = wn_height - 49
    en_2 = Enemies()
    en_2.rect.x = 290
    en_2.rect.y = 210
    en_2.val[0] = 5
    en_3 = Enemies()
    en_3.rect.x = 450
    en_3.rect.y = 110
    en_3.val[0] = 4
    enemies.append(en_1)
    enemies.append(en_2)
    enemies.append(en_3)
def spawn_boss():
    global boss_health
    boss = Enemies()
    boss.size = [96,96]
    boss.val = [24,24]
    boss.rect.size = boss.size[0],boss.size[1]
    boss.rect.x = 300
    boss.rect.y = 0
    boss_health = 50
    boss_l.append(boss)
all_levels = {1: l_1,2:l_2,3:spawn_boss}
def spawn_en():
    all_levels.get(level_num)()
def update_en_pos():
    for en in enemies:
        en.rect.x += en.val[0]
        for tile in en_tiles:
            if en.rect.colliderect(tile.rect):
                en.val[0] *= -1
    for en in boss_l:
        en.rect.y += en.val[1]
#fighting
def hit_en():
    for en in enemies:
        if play.sword.colliderect(en.rect):
            enemies.remove(en)
def hit_boss():
    global boss_health
    for en in boss_l:
        if play.sword.colliderect(en.rect):
            en.rect.y -= 128
            if en.color == (255,255,255):
                en.color = (255,0,0)
            else:
                en.color = (255,255,255)
            if play.upgrade:
                boss_health -= 2
            else:
                boss_health -= 1
            if boss_health <= 0:
                boss_l.remove(en)
                ending()
            else:
                pass             
#combined functions
def all_en():
    boss_falls()
    update_en_pos()
    hit_en()
    hit_boss()
def all_play():
    move_player()
    update_move(tiles)
    update_sword()
def start_game():
    global level_num,stop_button,button_sprite_s
    for up in upgrade:
        play.upgrade = False
        up.x = 64
        up.y = 105
    level_num = 1
    stop_button = pygame.Rect(0, 0, 32, 32); button_sprite_s = pygame.image.load('sprites\\start.png').convert()
    create_levels()
    spawn_en()
    set_level_pos()
#main menues
def play_button():
    global starting_game
    mouse = pygame.mouse.get_pos()
    if button1.collidepoint(mouse):
        starting_game = True
def control_button():
    global control_list
    mouse = pygame.mouse.get_pos()
    if controls.collidepoint(mouse):
        control_list = True
#menues
def main_game1():
    global tiles,en_tiles,end_tiles,enemies,boss_l
    tiles = []
    en_tiles = []
    end_tiles = [Platforms((608-32),0),Platforms((608-64),0),Platforms((608-32),32),Platforms((608-64),32)]
    enemies = []
    boss_l = []
    start_game()
    while starting_game:
    #logic
        new_sword()
        end_level()
        all_play()
        all_en()
        play_dead()
    #key inputs 
        key_inputs()
    #draw
        wn.fill(wn_bg)
        draw()
        upgrade_text()
    #update
        pygame.display.update()
        clock.tick(fps)
def ending():
    global stop_button, button_sprite_s
    stop_button = pygame.Rect(235, 200, 150, 150)
    button_sprite_s = pygame.transform.scale(pygame.image.load('sprites\\start.png').convert(),(150,150))
def controls_and_stuff():
    global stop_button,button_sprite_s
    while control_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    s_button()
        Controls_sprite = pygame.image.load('sprites\\Controls+.png').convert_alpha()
        Controls_Rect = pygame.Rect(64,64,300,300)
        stop_button = pygame.Rect(0,0,32,32)
        button_sprite_s = pygame.transform.scale(button_sprite_s,(32,32))
        wn.fill(wn_bg)
        wn.blit(button_sprite_s,stop_button)
        wn.blit(Controls_sprite,Controls_Rect)
        pygame.display.update()
        clock.tick(fps)
while True:
#logic 
    if starting_game:
        main_game1()
    if control_list:
        controls_and_stuff()
    else:
        pass
    button1=pygame.Rect(100,250, 150, 150)
    button1_sprite = pygame.transform.scale(pygame.image.load('sprites\\start.png').convert_alpha(),(150,150))
    controls=pygame.Rect(350,250, 150, 150)
    controls_sprite = pygame.transform.scale(pygame.image.load('sprites\\control.png').convert_alpha(),(150,150))
#key inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                play_button()
                control_button()
#draw  
    wn.fill(wn_bg)
    wn.blit(button1_sprite,button1)
    wn.blit(controls_sprite,controls) 
#update
    pygame.display.update()
    clock.tick(fps)