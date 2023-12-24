import pygame
import random
from copy import deepcopy

def main():
    # pygame setup
    pygame.init()
    pygame.display.set_caption('Snake')
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    pygame.font.init()

    # init variables
    random.seed(a = None, version = 2)
    snakeCoords = [[660, 360], [680, 360]]
    snakeLen = 2
    apple = [random.randint(1, 1280/20)*20, random.randint(1, 720/20)*20]
    displaceX = 0
    displaceY = 0
    moved = False
    
    # events
    APPLE_EATEN = pygame.USEREVENT + 0
    GAME_OVER = pygame.USEREVENT + 1
    
    # consts
    MOVE_SPEED = 20
    
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                moved = True
                displaceX = 0
                displaceY = 0
                key = event.key
                if key == pygame.K_UP:
                    displaceY -= MOVE_SPEED
                if key == pygame.K_LEFT:
                    displaceX -= MOVE_SPEED
                if key == pygame.K_DOWN:
                    displaceY += MOVE_SPEED
                if key == pygame.K_RIGHT:
                    displaceX += MOVE_SPEED

            if event.type == APPLE_EATEN:
                # DEBUG
                print("Apple Eaten\n")
                #put new apple
                apple = [random.randint(1, 1280/20)*20, random.randint(1, 720/20)*20]
                #change snake
                newBody = [snakeCoords[snakeLen-1][0], snakeCoords[snakeLen-1][1]]
                snakeCoords.append(newBody)
                snakeLen += 1
                
            if event.type == GAME_OVER:
                # init variables
                moved = False
                snakeCoords = [[660, 360], [680, 360]]
                snakeLen = 2
                apple = [random.randint(1, 1260/20)*20, random.randint(1, 700/20)*20]
                displaceX = 0
                displaceY = 0
                
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        #change body positions
        tempPos = snakeCoords[0];
        
        if moved:
            # move body forwards by a piece
            for x in range(len(snakeCoords)-1, 0, -1):
                snakeCoords[x] = deepcopy(snakeCoords[x-1])
                
            # move head
            snakeCoords[0][0] += displaceX
            snakeCoords[0][1] += displaceY
        
        #check for collision
        if snakeCoords[0] == apple:
            pygame.event.post(pygame.event.Event(APPLE_EATEN))
        if snakeCoords[0][0] > 1260 or snakeCoords[0][0] < 0 or snakeCoords[0][1] > 720 or snakeCoords[0][1] < 20:
            pygame.event.post(pygame.event.Event(GAME_OVER))
        # body collision
        for x in range(len(snakeCoords)-1, 0, -1):
            if snakeCoords[x] == snakeCoords[0]:
                pygame.event.post(pygame.event.Event(GAME_OVER))
                

        # add objects to the screen
        render(screen, apple, snakeCoords)

        # change display
        pygame.display.flip()

        clock.tick(15)  # limits FPS to 15

    pygame.quit()

def render(screen, apple, snakeCoords):
    # init vars
    BLOCK_SIZES = (20, 20)
    # draw score
    scoreFont = pygame.font.SysFont('Small Fonts Regular', 32)
    scoreSurface = scoreFont.render(str(len(snakeCoords)), False, (255, 255, 255))
    # draw apple
    appleRect = pygame.Rect(apple, BLOCK_SIZES)
    pygame.draw.rect(screen, pygame.Color(255,0,0,255), appleRect)
    # draw snake
    head = True
    for part in snakeCoords:
        snakeRect = pygame.Rect(part, BLOCK_SIZES)
        if head:
            pygame.draw.rect(screen, pygame.Color(255,255,255,255), snakeRect)
            head = False
        else:
            pygame.draw.rect(screen, pygame.Color(255,255,255,255), snakeRect)
            
    screen.blit(scoreSurface, (0,0))

main()