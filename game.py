import pygame
import random
import math


pygame.init()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # myndin er 40 x 40
        self.image = pygame.image.load('big_spacestick.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width-40)
        self.rect.y = -50
        self.speed = 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # myndin er 40 x 40
        self.image = pygame.image.load('sterdestrojer.png')
        self.rect = self.image.get_rect()
        self.missiles = []
        self.rect.x = 340
        self.rect.y = 360
        self.shots = 5

    def fire_missile(self):
        missilin = Missile()
        missilin.rect.x = self.rect.x
        missilin.rect.y = self.rect.y
        self.missiles.append(missilin)
        missile_sprites.add(missilin)
        all_sprites.add(missilin)


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # myndin er 20 x 40
        self.image = pygame.image.load('missilin.png')
        self.rect = self.image.get_rect()
        self.positionX = self.rect.x + 20
        self.positionY = self.rect.y + 40
        self.speed = 3
        self.explosion = []
        self.explosion.append(pygame.image.load('sbrengeng1.png'))
        self.explosion.append(pygame.image.load('sbrengeng2.png'))
        self.explosion.append(pygame.image.load('sbrengeng3.png'))
        self.explosion.append(pygame.image.load('sbrengeng4.png'))
        self.exploded = False
        self.explosion_frame = 0

font = pygame.font.SysFont("monospace", 30)

screen_width = 700
screen_height = 450
screen = pygame.display.set_mode([screen_width, screen_height])

block_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
missile_sprites = pygame.sprite.Group()

player = Player()

all_sprites.add(player)
done = False

clock = pygame.time.Clock()
score = 0

background_image = pygame.image.load("spece.png")
enemies = pygame.sprite.Group()

while not done:
    if player.shots > 0:
        if 1 == random.randint(0, 60):
            enemy = Enemy()
            enemy.speed = random.randint(1, 2)
            enemies.add(enemy)
            enemy = None
        for theEnemy in enemies:
            theEnemy.rect.y += theEnemy.speed
            all_sprites.add(theEnemy)
            if theEnemy.rect.y >= screen_height:
                all_sprites.remove(theEnemy)
                enemies.remove(theEnemy)
                score -= 2
                if score < 0: score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.shots > 0:
                    player.fire_missile()
                    player.shots -= 1

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if player.rect.x < -60:
                player.rect.x = 700
            player.rect.x -= 5
        elif key[pygame.K_RIGHT]:
            if player.rect.x > 700:
                player.rect.x = - 60
            player.rect.x += 5

        if pygame.sprite.spritecollide(player, enemies, True):
            score -= 10
            if score < 0: score = 0
            player.shots /= 2
        for missile in player.missiles:
            if pygame.sprite.spritecollide(missile, enemies, True) and missile.exploded is False:
                score += 1
                missile.exploded = True
                missile.image = missile.explosion[missile.explosion_frame]
                missile.explosion_frame += 1
                missile.speed = 0
                missile.rect.x -= 20
                missile.rect.y -= 20
                player.shots += 2

            if missile.exploded is True:
                if missile.explosion_frame >= 70:
                    missile_sprites.remove(missile)
                    player.missiles.remove(missile)
                    all_sprites.remove(missile)
                else:
                    missile.explosion_frame += 1
                    missile.rect.y -= 1
                    missile.image = missile.explosion[int(math.floor(missile.explosion_frame/20))]

            if missile.rect.y < -50:
                player.missiles.remove(missile)
                missile_sprites.remove(missile)
                all_sprites.remove(missile)
            missile.rect.y -= missile.speed

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        menu_bar = pygame.Rect(0, 400, 700, 50)
        pygame.draw.rect(screen, (0, 0, 0), menu_bar)

        point_string = "Score:" + str(score)
        point_text = font.render(point_string, 1, (255, 255, 0))
        screen.blit(point_text, (10, 410))

        shot_string = "Shots: " + str(player.shots)
        shot_text = font.render(shot_string, 1, (0, 255, 0))
        screen.blit(shot_text, (275,  410))

        fps_string = "FPS: " + str(int(clock.get_fps()))
        fps_text = font.render(fps_string, 1, (255, 255, 0))
        screen.blit(fps_text, (550, 410))

        clock.tick(60)
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        end_screen_rect = pygame.Rect((0, 0), (700, 450))
        pygame.draw.rect(screen, (0, 0, 0), end_screen_rect)

        loss_string = "You lose!"
        loss_text = font.render(loss_string, 1, (255, 0, 0))
        screen.blit(loss_text, (275, 200))

        point_string = "Score:" + str(score)
        point_text = font.render(point_string, 1, (255, 255, 0))
        screen.blit(point_text, (275, 250))

        pygame.display.flip()

pygame.quit()
