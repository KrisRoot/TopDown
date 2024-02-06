import pygame
import random
from Player import Player
from Enemy import Enemy
from Projectile import Projectile
import Weapon

pygame.init()
size = (800, 600)
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode(size)
scoreFont = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down")

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
enemies = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()


def move_entities(hero, enemies, timeDelta):
    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.topleft, timeDelta)
        enemy.shoot(hero.sprite.rect.topleft)
    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0:
                hero.sprite.alive = False
    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta)
        enemiesHit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemiesHit:
            proj.kill()
            score += len(enemiesHit)
    return score


def render_entities(hero, enemies):
    hero.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)


def process_keys(keys, hero):
    if keys[pygame.K_w]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_a]:
        hero.sprite.movementVector[0] -= 1
    if keys[pygame.K_s]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movementVector[0] += 1

        
def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())


def game_loop():
    done = False
    hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    enemies = pygame.sprite.Group()
    lastEnemy = pygame.time.get_ticks()
    score = 0
    highscore = int(open('highscore.txt', 'r').readlines()[0].rstrip())
    danger_level = 1
    
    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        screen.fill(BGCOLOR)
        
        process_keys(keys, hero)
        process_mouse(mouse, hero)
        
        if lastEnemy < currentTime - (200 / danger_level) and len(enemies) < 50:
            spawnSide = random.random()
            if spawnSide < 0.25:
                enemies.add(Enemy((0, random.randint(0, size[1]))))
            elif spawnSide < 0.5:
                enemies.add(Enemy((size[0], random.randint(0, size[1]))))
            elif spawnSide < 0.75:
                enemies.add(Enemy((random.randint(0, size[0]), 0)))
            else:
                enemies.add(Enemy((random.randint(0, size[0]), size[1])))
            lastEnemy = currentTime
        
        score += move_entities(hero, enemies, clock.get_time() / 17)
        if score == 50:
            hero.sprite.equippedWeapon = Weapon.Shotgun()
            hero.sprite.health += 1
            score += 1
            danger_level += 1
        elif score == 150:
            hero.sprite.equippedWeapon = Weapon.Shield()
            hero.sprite.health += 1
            score += 1
            danger_level += 1
        elif score == 350:
            hero.sprite.equippedWeapon = Weapon.MachineGun()
            hero.sprite.health += 1
            score += 1
            danger_level += 1
        elif score == 600:
            hero.sprite.equippedWeapon = Weapon.Laser()
            hero.sprite.health += 1
            score += 1
            danger_level += 1

        if score > highscore:
            highscore = score
            open('highscore.txt', 'w').write(str(highscore))

        render_entities(hero, enemies)
        
        for hp in range(hero.sprite.health):
            screen.blit(healthRender, (15 + hp * 35, 0))

        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        highscoreRender = scoreFont.render(str(highscore), True, pygame.Color('black'))

        scoreRect = scoreRender.get_rect()
        highscoreRect = highscoreRender.get_rect()

        scoreRect.right = size[0] - 20
        scoreRect.top = 20
        highscoreRect.right = size[0] - 20
        scoreRect.top = 40

        screen.blit(scoreRender, scoreRect)
        screen.blit(highscoreRender, highscoreRect)
        
        pygame.display.flip()
        clock.tick(60)


done = game_loop()
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if keys[pygame.K_r]:
        done = game_loop()
pygame.quit()
