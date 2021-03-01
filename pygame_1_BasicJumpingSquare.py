import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption('First Game')

x = 50
y= 425
width = 40
height = 60
vel = 5

isJump = False
jumpCount = 10

run = True
while run:
    # clock to make actions not to quick
    pygame.time.delay(100)

    # when pressing x pygame quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #define keypresses to move rec
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:           #direction + stop at border
        x-=vel
    if keys[pygame.K_RIGHT] and x < 500 - width - vel:
        x+=vel
    if not (isJump):                              # up/down OR jump
        if keys[pygame.K_UP] and y > vel:
            y-=vel
        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y+=vel
        if keys[pygame.K_SPACE]:
            isJump = True
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


    #fill with background color after moving rec otherwise rec will leave trail
    win.fill((0,0,0))

    # make rectangle object set on window, add collor and dimension parameters
    pygame.draw.rect(win, (255,0,0), (x,y, width, height))

    #refresh display to show character
    pygame.display.update()

pygame.QUIT