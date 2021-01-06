import pygame, sys, random
from pygame import mixer
from pygame.locals import *
# initalize the pygame
pygame.init()
clock = pygame.time.Clock()
# # display screen and game name
# screen = pygame.display.set_mode((512, 512))
# pygame.display.set_caption("ClearAllBlocks")
# load background music and loop playback
game_sound = mixer.music.load('resources/bgm.mp3')
mixer.music.play(-1)
# load background image
bg = pygame.image.load('resources/background.png')
###### define elements status ######
# track ball's position and movement
ball_x = 256
ball_y = 480
ball_dx = 0
ball_dy = 0
# game status
GAME_INIT = 0
GAME_RUN = 1
GAME_SHUTDOWN = 2
# define ball size and start position
BALL_SIZE = 6
BALL_START_Y = 256
# define blocks 
NUM_BLOCK_ROWS    = 6
NUM_BLOCK_COLUMNS = 6
BLOCK_WIDTH       = 64
BLOCK_HEIGHT      = 16
BLOCK_ORIGIN_X    = 8
BLOCK_ORIGIN_Y    = 8
BLOCK_X_GAP       = 86
BLOCK_Y_GAP       = 32
# define paddle's initial position and size
PADDLE_START_X  = 230
PADDLE_START_Y  = 490
PADDLE_WIDTH    = 45
PADDLE_HEIGHT   = 9
###### define necessary functions ######
# initialize bricks 
def initBlocks():
    blocks = []
    for i in range(0, 6):
        blocks.append([i+1] * 6)
    return blocks
# detect collision with and determine ball's movement
def processBall(blocks, ball_x, ball_y, platform):
    if(ball_y > 256):
        if(ball_x+BALL_SIZE >= platform['rect'].left and ball_x-BALL_SIZE <= platform['rect'].left+PADDLE_WIDTH and ball_y+BALL_SIZE >= platform['rect'].top and ball_y-BALL_SIZE <= platform['rect'].top+PADDLE_HEIGHT):
            return None
# exit game
def end():
    pygame.quit()
    sys.exit()
# display text in game
def DrawText(input_text, font, surface, x, y):
    text_surface = font.render(input_text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
# user input
def userInput():
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end()
                if event.key == pygame.K_SPACE:
                    score = 0
                    game_status = GAME_INIT
                return
# replace high score with current score if current score is larger than high score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
# define paddle and its movement
paddle = {'rect' :pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)}
paddle_move_left = False
paddle_move_right = False
# initialize game status
game_status = GAME_INIT
blocks = []
score = 0
high_score = 0
# display screen, game name, and beginning surface
game_font = pygame.font.SysFont('Arial', 20)
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("ClearAllBlocks")
screen.fill((0,0,0))
DrawText('Press any SPACE to start the game', game_font, screen, 120, 245)
pygame.display.update()
userInput()

# game main loop 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_move_left = True
            if event.key == pygame.K_RIGHT:
                paddle_move_right = True
            if event.key == pygame.K_ESCAPE:
                end()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddle_move_left = False
            if event.key == pygame.K_RIGHT:
                paddle_move_right = False
    
    if game_status == GAME_INIT:
        ball_x = 256
        ball_y = 256
        # initalize ball's speed in vertical and horizontal direction
        ball_dx = 2
        ball_dy = 6
        paddle['rect'].left = PADDLE_START_X
        paddle['rect'].top = PADDLE_START_Y

        paddle_move_left = False
        paddle_move_right = False
        score = 0
        blocks = initBlocks()
        game_status = GAME_RUN
    elif game_status == GAME_RUN:
        ball_x += ball_dx
        ball_y += ball_dy
        # check if there is collision between ball and screen boundary
        if ball_x > (512-BALL_SIZE) or ball_x < BALL_SIZE:
            ball_dx = -ball_dx
            ball_x  += ball_dx
        elif ball_y < BALL_SIZE:
            ball_dy = -ball_dy
            ball_y  += ball_dy
        elif ball_y >= 512-BALL_SIZE:
            # if ball is out of bound, then check user's input
            # SPACE to restart game, ESC to exit game
            high_score = update_score(score, high_score)
            DrawText('High Score: {}'.format(high_score) , game_font, screen, 120, 225) 
            DrawText('press SPACE to restart or ESC to exit', game_font, screen, 120, 245)
            pygame.display.update()
            userInput()
            game_status = GAME_INIT
        # check if there is collision between ball and paddle    
        if ball_y > 256:
            if (ball_x+BALL_SIZE >= paddle['rect'].left and \
                ball_x-BALL_SIZE <= paddle['rect'].left+PADDLE_WIDTH and \
                ball_y+BALL_SIZE >= paddle['rect'].top and \
                ball_y-BALL_SIZE <= paddle['rect'].top+PADDLE_HEIGHT):
                ball_dy = - ball_dy
                ball_y += ball_dy
                if paddle_move_left:
                    ball_dx -= 2
                elif paddle_move_right:
                    ball_dx += 2
                else:
                    ball_dx += 2
        # chect if there is collision between ball and blocks
        cur_x = BLOCK_ORIGIN_X
        cur_y = BLOCK_ORIGIN_Y
        for row in range(NUM_BLOCK_ROWS):
            cur_x = BLOCK_ORIGIN_X
            for col in range(NUM_BLOCK_COLUMNS):
                if blocks[row][col] != 0:
                    if (ball_x+BALL_SIZE >= cur_x and \
                        ball_x-BALL_SIZE <= cur_x+BLOCK_WIDTH and \
                        ball_y+BALL_SIZE >= cur_y and \
                        ball_y-BALL_SIZE <= cur_y+BLOCK_HEIGHT):
                        blocks[row][col] = 0
                        ball_dy = -ball_dy
                        ball_dx += random.randint(-1, 2)
                        score += 1
                cur_x += BLOCK_X_GAP
            cur_y += BLOCK_Y_GAP
        # paddle movement
        if paddle_move_left:
            paddle['rect'].left -= 8
            if paddle['rect'].left < 0:
                paddle['rect'].left = 0
        if paddle_move_right:
            paddle['rect'].left += 8
            if paddle['rect'].left > 512-PADDLE_WIDTH:
                paddle['rect'].left = 512-PADDLE_WIDTH
        
        # display background image
        screen.blit(bg, (0,0))
        # draw paddle
        pygame.draw.rect(screen, (120, 60, 60), paddle['rect'])
        # draw ball
        pygame.draw.circle(screen, (240, 70, 70), (ball_x, ball_y), BALL_SIZE, 0)
        # draw blocks
        cur_x = BLOCK_ORIGIN_X
        cur_y = BLOCK_ORIGIN_Y
        for row in range(NUM_BLOCK_ROWS):
            cur_x = BLOCK_ORIGIN_X
            for col in range(NUM_BLOCK_COLUMNS):
                if blocks[row][col] != 0:
                    pygame.draw.rect(screen, (200, 200, 200), (cur_x, cur_y, BLOCK_WIDTH, BLOCK_HEIGHT))
                cur_x += BLOCK_X_GAP
            cur_y += BLOCK_Y_GAP

    elif game_status == GAME_SHUTDOWN:
        end()


    pygame.display.update() 
    clock.tick(27)       