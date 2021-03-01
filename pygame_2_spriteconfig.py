import pygame

pygame.init()

win = pygame.display.set_mode((500, 480)) #set window size

pygame.display.set_caption('First Game')  #display widow


# get images for character
walkRight = [pygame.image.load('./assets/Game/R1.png'), pygame.image.load('./assets/Game/R2.png'),
             pygame.image.load('./assets/Game/R3.png'), pygame.image.load('./assets/Game/R4.png'),
             pygame.image.load('./assets/Game/R5.png'), pygame.image.load('./assets/Game/R6.png'),
             pygame.image.load('./assets/Game/R7.png'), pygame.image.load('./assets/Game/R8.png'),
             pygame.image.load('./assets/Game/R9.png')]
walkLeft = [pygame.image.load('./assets/Game/L1.png'), pygame.image.load('./assets/Game/L2.png'),
            pygame.image.load('./assets/Game/L3.png'), pygame.image.load('./assets/Game/L4.png'),
            pygame.image.load('./assets/Game/L5.png'), pygame.image.load('./assets/Game/L6.png'),
            pygame.image.load('./assets/Game/L7.png'), pygame.image.load('./assets/Game/L8.png'),
            pygame.image.load('./assets/Game/L9.png')]
bg = pygame.image.load('./assets/Game/bg.jpg')
char = pygame.image.load('./assets/Game/standing.png')

#framerate and time settings
clock = pygame.time.Clock()

# variables
x = 50
y= 400
width = 64
height = 64
vel = 5

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0


# drawing function outside main loop
def redrawGameWindow():
    global walkCount
    win.blit(bg, (0,0))

    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x,y))

    pygame.display.update()


#mainloop
run = True
while run:
    # set framerate to 27
    clock.tick(27)
    # when pressing x pygame quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #define keypresses to move sprite
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:           #direction + stop at border
        x-=vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x+=vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not (isJump):                              # jump
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
    else:                                          # jump physics
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    redrawGameWindow()

pygame.QUIT