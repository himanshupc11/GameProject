# Import modules
import os
import random
import pygame
from pygame.locals import *

# Constants
WIDTH = 400
HEIGHT = 500
FPS = 30
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

score = 0
bossScore = 300
flag = 0
elements = 0
count = -1
Messages = ['Ohh no ,not those assignments again', 'Ohh not those dreaded unit test', 'Ohh no , not the cursed semester']
gameOver = "I knew you would butcher it, NOOB!!!"

# Initializing And Creating Windows
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Revenge")

# Clock object and user event
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT + 1, 1000)
pygame.time.set_timer(USEREVENT + 2, 100)

# Setting upd paths
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")
snd_folder = os.path.join(game_folder, "sounds")

# Loading Images
assignment_img = pygame.image.load(os.path.join(img_folder, "assignment.png")).convert()
assignment_img = pygame.transform.scale(assignment_img, (60, 90))

ut_img = pygame.image.load(os.path.join(img_folder, "ut.png")).convert()
ut_img = pygame.transform.scale(ut_img, (100, 112))

sem_img = pygame.image.load(os.path.join(img_folder, "book3.png")).convert()
sem_img = pygame.transform.scale(sem_img, (100, 100))

player_img = pygame.image.load(os.path.join(img_folder, "girl.png")).convert()
player_img = pygame.transform.scale(player_img, (80, 135))

bullet_img = pygame.image.load(os.path.join(img_folder, "arrow.png")).convert()
bullet_img = pygame.transform.scale(bullet_img, (12, 48))

boss_img = pygame.image.load(os.path.join(img_folder, "bk.png")).convert()
boss_img = pygame.transform.scale(boss_img, (120, 160))

background = pygame.image.load(os.path.join(img_folder, "blackboard.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Loading sounds
loop_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'back.ogg'))
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, '7.wav'))
hbd_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'bd.wav'))

# Drawing Text
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Players, Mobs and Bullets
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Player Image
        self.image = player_img
        self.image.set_colorkey((41, 42, 49))
        # self.image.fill(GREEN)

        # Player Rectangle
        self.temp = pygame.Surface((30, 120))
        self.rect = self.temp.get_rect()

        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 135

        # Player unique attributes
        self.speedx = 0
        self.life = 1

    def update(self):

        self.speedx = 0
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx

        # Constraining player between display
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Self Image initialization
        self.image = pygame.Surface((30, 30))
        # self.image.fill(RED)

        # Self Rect initialization with random position
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 32)
        self.rect.y = random.randint(-60, -30)

        # Unique attributes
        self.speedx = random.randint(1, 5)
        self.speedy = random.randint(1, 5)
        self.status = True

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x < 0 or self.rect.x + 30 > WIDTH:
            self.speedx = -self.speedx
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 32)
            self.rect.y = random.randint(-60, -30)


class MobAssignment(Mob):

    def __init__(self):
        Mob.__init__(self)

        self.speedx = random.randint(1, 3)
        self.speedy = random.randint(1, 5)
        self.status = True

        self.image = assignment_img
        self.image.set_colorkey((0, 0, 0))
        self.temp = pygame.Surface((40, 70))

        self.rect = self.temp.get_rect()
        self.life = 1
        self.score = 10

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x < 0 or self.rect.x + 90 >= WIDTH:
            self.speedx = -self.speedx
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 60)
            self.rect.y = random.randint(-120, -90)


class utAssignment(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.image = ut_img
        self.temp = pygame.Surface((90, 100))
        self.rect = self.temp.get_rect()
        self.image.set_colorkey((245, 245, 245))
        self.life = 2
        self.score = 30

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x < 0 or self.rect.x + 100 >= WIDTH:
            self.speedx = -self.speedx
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 60)
            self.rect.y = random.randint(-120, -90)


class semAssignment(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.image = sem_img
        self.image.set_colorkey((255, 255, 255))

        self.temp = pygame.Surface((70, 70))
        self.rect = self.temp.get_rect()
        self.life = 3
        self.score = 50

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x < 0 or self.rect.x + 100 >= WIDTH:
            self.speedx = -self.speedx
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 60)
            self.rect.y = random.randint(-120, -90)


class Bullets(pygame.sprite.Sprite):  # 0 means player bullet and 1 means boss bullet
    def __init__(self, x, y, num):
        pygame.sprite.Sprite.__init__(self)

        # Self Image initialization
        self.image = bullet_img
        self.image.set_colorkey((255, 255, 255))

        # Self Rectangle initialization
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Unique attributes
        self.speedx = 0
        if num == 1:
            self.speedy = 5
        else:
            self.speedy = -5

    def update(self):
        self.rect.y += self.speedy

        # Cleaning up bullets that go out of screen
        if self.rect.y < 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Self Image initialization
        self.image = boss_img
        # self.image.fill(GREEN)

        # Boss Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 4
        self.rect.y = 20

        # Unique attributes
        self.life = 10
        self.speedx = -10

    def shoot(self):
        x = self.rect.x + WIDTH / 4
        y = self.rect.y + HEIGHT / 4
        bossBullet = Bullets(x, y, 1)
        all_sprites.add(bossBullet)
        bossesBullets.add(bossBullet)

    def move(self):
        self.rect.x += self.speedx

    def update(self):
        if self.rect.x <= 0:
            self.speedx = 10
        if self.rect.x + WIDTH / 2 >= WIDTH:
            self.speedx = -10


# Add score and delete the correct mob object
def cleanup(b):
    if isinstance(b, MobAssignment):
        b.kill()

    elif isinstance(b, utAssignment):
        b.kill()

    elif isinstance(b, semAssignment):
        b.kill()

    return -1


# Object creation
player = Player()

# Sprite Manipulation
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

assignments = pygame.sprite.Group()
ut = pygame.sprite.Group()
sem = pygame.sprite.Group()

bulletsShot = pygame.sprite.Group()
bossesBullets = pygame.sprite.Group()

all_sprites.add(player)


# Adding mob elements
def Addition(x):
    if 0 <= x < 60:
        mob1 = MobAssignment()
        mob2 = MobAssignment()
        mob3 = MobAssignment()
        mobs.add(mob1, mob2, mob3)
        all_sprites.add(mob1, mob2, mob3)
    elif 60 <= x < 150:
        mob1 = utAssignment()
        mob2 = utAssignment()
        mob3 = utAssignment()
        mobs.add(mob1, mob2, mob3)
        all_sprites.add(mob1, mob2, mob3)
    elif 150 <= x < 300:
        mob1 = semAssignment()
        mob2 = semAssignment()
        mob3 = semAssignment()
        mobs.add(mob1, mob2, mob3)
        all_sprites.add(mob1, mob2, mob3)

    return 3


# Game Loop
elements = Addition(score)
running = True

while running:
    clock.tick(FPS)

    # Process Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullets(player.rect.x + 25, player.rect.y, 0)
            shoot_sound.play()
            all_sprites.add(bullet)
            bulletsShot.add(bullet)
        if score >= bossScore:
            if event.type == USEREVENT + 1:
                for i in range(3):
                    boss.shoot()
            if event.type == USEREVENT + 2:
                boss.move()

    # Update
    all_sprites.update()

    # Checking if player was hit with a mob
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        player.life -= 1
        elements -= 1
        print(elements)
        if player.life <= 0:
            draw_text(screen, gameOver, 30, 20, 20)


    # Checking if bullet hits the mob and removing them and re-adding them
    hits = pygame.sprite.groupcollide(mobs, bulletsShot, False, True)
    for mo, bull in hits.items():
        mo.life -= 1
        if mo.life == 0:
            score += mo.score
            elements += cleanup(mo)
            print("Elements: " + str(elements) + "       Count: " + str(count))
            if elements <= 0:
                count += 1
                elements = Addition(score)


    # Spawning boss if required
    if score >= bossScore and flag == 0:
        flag = 1
        boss: Boss = Boss()
        all_sprites.add(boss)

    # Checking if bullets collided with boss
    if score >= bossScore:
        hits = pygame.sprite.spritecollide(boss, bulletsShot, True)
        if hits:
            boss.life -= 1
            if boss.life == 0:
                boss.kill()
                hbd_sound.play()

    # Removing boss bullets and player bullets if crashed
    hits = pygame.sprite.groupcollide(bossesBullets, bulletsShot, True, True)

    if count >= 3:
        count = 0

    # Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Score: " + str(score), 10, 30, 10)
    draw_text(screen, Messages[count], 20, 190, 10)
    draw_text(screen, "Health: " + str(player.life), 10, WIDTH -50, 10)
    if player.life <= 0:
        draw_text(screen, gameOver, 20, WIDTH/2, 40)
        running = False
    pygame.display.flip()

# Uninitialized Imports
pygame.quit()

