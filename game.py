import pygame

import time
# bring in the math module to use absolute value
from math import fabs

# Get the randon module
from random import randint

# in order to use pygame, we have to run init method
# 2. Init pygame
pygame.init()


# 3. Create a screen with a size
screen = {
    "height": 512,
    "width": 480
}

keys = {
    "right": 275,
    "left": 276,
    "up": 273,
    "down": 274,
    "space": 32
}

keys_down = {
    "right": False,
    "left": False,
    "up": False,
    "down": False
}

hero = {
    "x": 100,
    "y": 100,
    "speed": 20,
    "kills": 0,
    "lives": 5
}

goblin = {
    "x": randint(0,screen['height'] - 32),
    "y": randint(0,screen['width'] - 32),
    "speed": 2,
    "direction": "N"
}

monster = {
    "x": randint(0,screen['height'] - 32),
    "y": randint(0,screen['width'] - 32),
    "speed": 1,
}

powerup = {
    'active': True,
    'tick_gotten': 0
}

game_paused = False

directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']

screen_size = (screen["height"], screen["width"])
pygame_screen = pygame.display.set_mode(screen_size)

# Whatever you put in here shows up at the top of the window when the game is opened
pygame.display.set_caption("Space Goblin Chase")
background_image = pygame.image.load('images/space_background.png')
hero_image = pygame.image.load('images/spaceship.png')
hero_image_scaled = pygame.transform.scale(hero_image, (32,32))
goblin_image = pygame.image.load('images/goblin.png')
monster_image = pygame.image.load('images/monster.png')


# Add music files
pygame.mixer.music.load('./sounds/music.wav')
pygame.mixer.music.play(-1)

win_sound = pygame.mixer.Sound('./sounds/win.wav')
lose_sound = pygame.mixer.Sound('./sounds/lose.wav')

tick = 0

timer = 0

font = pygame.font.Font(None, 25)

def goblin_position(character):
    if (character['direction'] == 'N'):
        character['y'] -= character['speed']
    elif (character['direction'] == 'S'):
        character['y'] += character['speed']
    elif (character['direction'] == 'E'):
        character['x'] += character['speed']
    elif (character['direction'] == 'W'):
        character['x'] += character['speed']
    elif (character['direction'] == 'NE'):
        character['x'] -= character['speed']
        character['y'] += character['speed']  
    elif (character['direction'] == 'NW'):
        character['x'] -= character['speed']
        character['y'] -= character['speed']  
    elif (character['direction'] == 'SE'):
        character['x'] += character['speed']
        character['y'] += character['speed']
    elif (character['direction'] == 'SW'):
        character['x'] += character['speed']
        character['y'] -= character['speed']  

    if (tick % 20 == 0):
        new_dir_index = randint(0, len(directions) - 1)
        character['direction'] = directions[new_dir_index]

    if (character['x'] > screen['width']):
        character['x'] = 0
    elif (character['x'] < 0):
        character['x'] = screen['width']
    if (character['y'] > screen['height']):
        character['y'] = 0
    elif (character['y'] < 0):
        character['y'] = screen['height']

def monster_chase(character):
    if hero['lives'] > 0:
        if hero['x'] > character['x']:
            character['x'] += character['speed']
        if hero['x'] < character['x']:
            character['x'] -= character['speed']
        if hero['y'] > character['y']:
            character['y'] += character['speed']
        if hero['y'] < character['y']:
            character['y'] -= character['speed']

def collision_detect(character1, character2):
    distance_between = fabs(character1['x'] - character2['x']) + fabs(character1['y'] - character2['y'])
    if (distance_between < 32):
        rand_x = randint(0,screen['width'] -32)
        rand_y = randint(0,screen['height'] -32)
        character2['x'] = rand_x
        character2['y'] = rand_y
        return True
    else:
        return False


def random_spawn(character):
    rand_x = randint(0,screen['width'] -32)
    rand_y = randint(0,screen['height'] -32)
    character['x'] = rand_x
    character['y'] = rand_y           
# /////////////////////MAIN GAME LOOP/////////////////////////
# /////////////////////MAIN GAME LOOP/////////////////////////
# /////////////////////MAIN GAME LOOP/////////////////////////
game_on = True
# 4. Create the game loop (while 1)
while game_on:
    tick += 1
    # we are inside the main game loop it will run as long as game_on is true
    # -----EVENTS-----
    for event in pygame.event.get():
        # Looping through all events that happened this game loop cycle
        # 5. Add a quit event (requires sys)
        if event.type == pygame.QUIT:
            # the user clicked on the red X to leave the game
            game_on = False
            # update our boolean so pygame can escape loop
        elif event.type == pygame.KEYDOWN:
            if event.key == keys['up']:
                keys_down['up'] = True
            elif event.key == keys['down']:
                keys_down['down'] = True
            elif event.key == keys['left']:
                keys_down['left'] = True
            elif event.key == keys['right']:
                keys_down['right'] = True
            elif event.key == keys['space']:
                game_paused = not game_paused
        elif event.type == pygame.KEYUP:
            if event.key == keys['up']:
                # the user let go of a key... and that key was the up arrow
                keys_down['up'] = False
            if event.key == keys['down']:
                keys_down['down'] = False
            if event.key == keys['left']:
                keys_down['left'] = False
            if event.key == keys['right']:
                keys_down['right'] = False

    if(not game_paused):
        if hero['lives'] > 0:
        # Update hero postion
            if keys_down['up']:
                hero['y'] -= hero['speed']
            elif keys_down['down']:
                hero['y'] += hero['speed']
            if keys_down['left']:
                hero['x'] -= hero['speed']
            elif keys_down['right']:
                hero['x'] += hero['speed']


    # Goblin position
    # get random direction (up down left or right)
    # move goblin in that direction 
    goblin_position(goblin)


    # Monster Chasing Hero
    monster_chase(monster)

    # COLLISION DETECTION
    # check hero/goblin
    if collision_detect(hero, goblin):
        hero['kills'] += 1
        win_sound.play()

    # check hero/monster
    if collision_detect(hero, monster):
        hero['lives'] -= 1

    pygame_screen.blit(background_image, [0,0])
    
# TIMER (SECONDS ALIVE)
    if (not game_paused):
        if (tick % 30 == 0):
            timer += 1
        timer_text = font.render("Seconds Alive: %d" % (timer), True, (255,255,255))
        pygame_screen.blit(timer_text, [360,10])
    # distance_between = fabs(hero['x'] - 100) + fabs(hero['y'] - 200)
    # if (distance_between < 32):
    #     print "Hero powered up!"

    
    
    if (game_paused):
        screen_text_paused = font.render("GAME PAUSED", True, (255,255,255))
        pygame_screen.blit(screen_text_paused,[200, 200])
    

    # GAME OVER MESSAGE
    if hero['lives'] <= 0:
        screen_text = font.render("GAME OVER! TRY AGAIN?", True, (255,0,0))
        pygame_screen.blit(screen_text,[150, 200])

        
    # -----RENDER-----
    # blit takes 2 arguments
    # 1. What?
    # 2. Where?
    # Screen.fill (pass bg_color)


    # Draw the hero wins on the screen
    wins_text = font.render("Kills: %d" % (hero['kills']), True, (255,255,255))
    lives_text = font.render("Lives: %d" % (hero['lives']), True, (255,255,255))
    pygame_screen.blit(wins_text, [20,10])
    pygame_screen.blit(lives_text, [120,10])

    #draw the hero
    pygame_screen.blit(hero_image_scaled, [hero['x'],hero['y']])

    pygame_screen.blit(goblin_image, [goblin['x'],goblin['y']])

    pygame_screen.blit(monster_image, [monster['x'],monster['y']])

    # clear the screen for the next time
    pygame.display.flip()

# 7. Flip the screen and start ove4