import pygame
from pygame.locals import *
from random import uniform, randint, random
from math import pi, sin, cos

pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Sans Helvetica', 30)

w, h = 1000, 500
unit = 6

win = pygame.display.set_mode((w, h))

randomcolor = lambda: [randint(0, 255) for _ in range(3)]

pwidth = h/20
pheight = h/7*2
players = [pygame.Rect(i*(w-pwidth), h/2-pheight/2, pwidth, pheight) for i in [0, 1]]
player_colors = [randomcolor() for _ in range(2)]

ballpos = [w/2, h/2]
ball_r = h/20
ballspeed = [unit*1.5]*2
#ballangle = uniform(-pi/3, pi/3) if random()<0.5 else uniform(pi-pi/3, pi+pi/3)
ballangle = pi/4
ballrand = pi/10
ballcolor = randomcolor()
ball = pygame.draw.circle(win, [0]*3, ballpos, ball_r)

ctrl_keys = (K_w, K_s), (K_UP, K_DOWN)

running = True; gameOver = False; gone = False; loser = None
while running: # game loop
    pygame.time.Clock().tick(60) # maximize frame rate
    #--------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if you press the red X
            running = False

    #--------------------------------------------------------------
    keys = pygame.key.get_pressed() # all the keys in a dict
    for i, (up, down) in enumerate(ctrl_keys):
        player = players[i]
        if   keys[up]   and player.top > 0:
            player.move_ip(0, -unit)
            player_colors[i] = randomcolor()
        elif keys[down] and player.bottom < h:
            player.move_ip(0, unit)
            player_colors[i] = randomcolor()
    #---------------------------------------------------------------
    if not gameOver:
        if ball.top <= 0 or ball.bottom >= h:
            ballspeed[1] *= -1
            ballangle += uniform(-ballrand, ballrand)
        player = players[0] if ball.centerx < w/2 else players[1]
        if ball.left <= pwidth or ball.right >= w-pwidth:
            if player.top < ball.bottom and ball.top < player.bottom:
                ballspeed[0] *= -1
                ballangle += uniform(-ballrand, ballrand)
            else:
                gameOver = True
                loser = player
        ballcolor = randomcolor()

    if pygame.time.get_ticks()>3000:
        ballpos = [ballpos[0]+cos(ballangle)*ballspeed[0], ballpos[1]+sin(ballangle)*ballspeed[1]]
    ############################################################################################
    #win.fill([255]*3)

    if not gameOver or not gone:
        for i, (player) in enumerate(players):
            pygame.draw.rect(win, player_colors[i], player)
        ball = pygame.draw.circle(win, ballcolor, ballpos, ball_r)
        if not -ball_r <= ball.centerx <= w+ball_r:
            gone = True
    else:
        winner = "Left player" if players[0] is not loser else "Right player"
        win.blit(myfont.render("Game Over", False, [0]*3), (w/2-w/5, h/2))
        win.blit(myfont.render(f"Winner is: {winner}", False, [0]*3), (w/2-w/5, h/2+h/10))

    pygame.display.flip()
    ############################################################################################

pygame.quit()
