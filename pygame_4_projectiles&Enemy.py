import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption('First Game')

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

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:                                #reset walkCount after 27 frames
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('./assets/Game/R1E.png'), pygame.image.load('./assets/Game/R2E.png'),
                 pygame.image.load('./assets/Game/R3E.png'), pygame.image.load('./assets/Game/R4E.png'),
                 pygame.image.load('./assets/Game/R5E.png'), pygame.image.load('./assets/Game/R6E.png'),
                 pygame.image.load('./assets/Game/R7E.png'), pygame.image.load('./assets/Game/R8E.png'),
                 pygame.image.load('./assets/Game/R9E.png'), pygame.image.load('./assets/Game/R10E.png'),
                 pygame.image.load('./assets/Game/R11E.png')]
    walkLeft = [pygame.image.load('./assets/Game/L1E.png'), pygame.image.load('./assets/Game/L2E.png'),
                pygame.image.load('./assets/Game/L3E.png'), pygame.image.load('./assets/Game/L4E.png'),
                pygame.image.load('./assets/Game/L5E.png'), pygame.image.load('./assets/Game/L6E.png'),
                pygame.image.load('./assets/Game/L7E.png'), pygame.image.load('./assets/Game/L8E.png'),
                pygame.image.load('./assets/Game/L9E.png'), pygame.image.load('./assets/Game/L10E.png'),
                pygame.image.load('./assets/Game/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:                # Since we have 11 images for each animtion our upper bound is 33.
                                                    # We will show each image for 3 frames. 3 x 11 = 33.
            self.walkCount = 0
        if self.vel > 0:                            # If we are moving to the right we will display our walkRight images
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))   # //3 to slow down
            self.walkCount += 1
        else:                                       # Otherwise we will display the walkLeft images
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:               #moving to the right
            if self.x + self.vel < self.path[1] :
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


#mainloop
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = []
run = True
while run:
    # framerate to 27
    clock.tick(27)
    # when pressing x pygame quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # bullets
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:         # bullet  is within window
            bullet.x += bullet.vel                  # bullet gets shot
        else:
            bullets.pop(bullets.index(bullet))    #bullet gets deleted at border

    #define keypresses to move sprite
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:                                            #max nb of bullets on screen
            bullets.append(projectile(round(man.x + man.width//2),
                                      round(man.y + man.height//2),    #round for int and bullet starts at edge of player object
                                      6,                               #radius
                                      (0,0,0),                          #color
                                      facing))
    if keys[pygame.K_LEFT] and man.x > man.vel:           #direction + stop at border
        man.x-=man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x+=man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.standing = True

    if not (man.isJump):                              # jump
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
    else:                                          # jump physics
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.QUIT