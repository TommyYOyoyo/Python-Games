import pygame
import random
import sys
from pygame.locals import *
from sys import exit
import os
import time
import playsound
from pygame import error, mixer
from threading import Event

# ATTENTION! Define function all arguments should be given in funtion created, or ex:   TypeErroe: function takes exactly 2 arguments(1 given)
"""initializing_"""
pygame.init()
mixer.init()
pygame.font.init()

pygame.display.set_caption("SpaceWar Beta")
# =============initialization============
Width, Height = 500, 600
win = pygame.display.set_mode((Width, Height))
shipwidth = 150
shipheight = 150
bigshipwidth = 250
bigshipwidth = 250

"""============PLAYER======================"""
#playerfront = pygame.image.load(os.path.join('Assets', "player.png"))
#playerback = pygame.image.load(os.path.join('Assets', 'playerback.png'))
#playerright = pygame.image.load(os.path.join('Assets', 'playerright.png'))
#playerleft = pygame.image.load(os.path.join('Assets', 'playerleft.png'))
player = pygame.image.load(os.path.join('Assets', "player.png"))
player = pygame.transform.scale(player, (shipwidth, shipheight))

""" >>>>>>>>>>>    ENEMY(enemy)   <<<<<<<<<<<<           """
bigenemyship = pygame.image.load(
    os.path.join('Assets', "enemyship1.png"))
bigenemyship = pygame.transform.scale(bigenemyship, (shipwidth, shipheight))
smallenemyship = pygame.image.load(
    os.path.join('Assets', "enemyship2.png")
)
smallenemyship = pygame.transform.rotate(
    pygame.transform.scale(smallenemyship, (shipwidth, shipheight)), 180)

explosion = pygame.image.load(os.path.join('Assets', "explosion.png"))
exp1 = pygame.image.load(os.path.join('Assets', "exp1.png"))
exp2 = pygame.image.load(os.path.join('Assets', "exp2.png"))
exp3 = pygame.image.load(os.path.join('Assets', "exp3.png"))
exp4 = pygame.image.load(os.path.join('Assets', "exp4.png"))
exp5 = pygame.image.load(os.path.join('Assets', "exp5.png"))

bosscat = pygame.image.load(os.path.join('Assets', 'bossneoncat.png'))
bosscat = pygame.transform.scale(bosscat, (200, 200))
lifesaver = pygame.image.load(os.path.join('Assets', "lifesaver.png"))
lifesaver = pygame.transform.scale(lifesaver, (50, 50))

# ============BULLETS,LAZERS================
redlaser = pygame.image.load(os.path.join("Assets", "redlazer.png"))
greenlaser = pygame.image.load(os.path.join("Assets", "greenlazer.png"))
superlaser = pygame.image.load(os.path.join("Assets", "superbullet.png"))
superlaser = pygame.transform.scale(superlaser, (350, 350))
cloudy = pygame.image.load(os.path.join('Assets', 'cloudy.png'))
angry = pygame.image.load(os.path.join('Assets', 'angry.png'))
#::::::::::::::::::SOUNDTRACKS:::::::::::::::::
explosionsound = mixer.Sound(os.path.join("Assets/explosionsound.ogg"))
gameoversound = mixer.Sound(os.path.join("Assets/gameoversound.ogg"))
lasersound = mixer.Sound(os.path.join("Assets/lasersound.ogg"))
alarmsound = mixer.Sound(os.path.join("Assets/alarmsound.ogg"))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, height):
        return not(self.y <= height and self.y + 30 >= 0)

    def move(self, movepixels):
        self.y += movepixels

    def collision(self, obj):
        return collide(self, obj)

class Superlaser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y 
        self.img = superlaser
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, height):
        return not(self.y <= height and self.y + 30 >= 0)

    def move(self,movepixels):
        self.y += movepixels

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 10
    SUPERLASERCOOLDOWN = 1500

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.superlaser_img = superlaser
        self.lasers = []
        self.superlasers = []
        self.cool_down_counter = 0
        self.super_laser_cooldown = 0


    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        for superlaser in self.superlasers:
            superlaser.draw(window)

    def move_lasers(self, movepixels, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(movepixels)
            if laser.off_screen(Height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter == self.COOLDOWN:
            self.cool_down_counter = 0            
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def superlasercooldown(self):
        if self.super_laser_cooldown == self.SUPERLASERCOOLDOWN:
            self.super_laser_cooldown = 0
        elif self.super_laser_cooldown > 0:
            self.super_laser_cooldown += 1

    def cooldownlabel(self):
        main_font = pygame.font.Font('Assets/PixelOperator.ttf', 20)
        cooldown_label = main_font.render(f"LsCooldown: {self.cool_down_counter}/10", 0, (255, 255, 255))
        win.blit(cooldown_label, (self.x + 105, self.y + 75))
        
    def supercooldownlabel(self):
        main_font = pygame.font.Font('Assets/PixelOperator.ttf', 20)
        cooldown_label = main_font.render(f"SpLCooldown: {self.super_laser_cooldown}/1500", 0, (255, 255, 255))
        win.blit(cooldown_label, (self.x + 105, self.y + 95))

    def shoot(self):
        lasersound.play()
        if self.cool_down_counter == 0:
            laser = Laser((self.x + 26), self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def superlasershoot(self):
        lasersound.play
        if self.super_laser_cooldown == 0:
            superlaser = Superlaser((self.x - 95), self.y, self.superlaser_img)
            self.superlasers.append(superlaser)
            self.super_laser_cooldown = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
    

class Player(Ship):
    def __init__(self, x, y, health=120):
        super().__init__(x, y, health)
        self.ship_img = player
        self.laser_img = greenlaser
        self.superlaserimg = superlaser
        # hit-box, create a pygame perfect collision hitbox of the player ship
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        
    def move_lasers(self, movepixels, objs, group, things):
        self.cooldown()
        for laser in self.lasers:
            laser.move(movepixels)
            if laser.off_screen(Height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):                      
                        explosionsound.play()
                        objs.remove(obj)
                        self.lasers.remove(laser)
                        explosionn = Explosion(obj.x + 60, obj.y + 75, 2)
                        group.add(explosionn)
                        break
                for thing in things:
                    #BOSSAIcontinueTODO
                    if laser.collision(thing):
                        explosionsound.play()
                        explosioN = Explosion(laser.x + 40, laser.y + 40, 1)
                        group.add(explosioN)
                        thing.health -= 13
                        thing.x += random.randint(-30, 30)
                        self.lasers.remove(laser)
                        break

    def move_superlasers(self, movepixels, objs, group, things):
        self.superlasercooldown()
        for superlaser in self.superlasers:
            superlaser.move(movepixels)
            if superlaser.off_screen(Height):
                self.superlasers.remove(superlaser)
            else:
                for obj in objs:
                    if superlaser.collision(obj):
                        explosionsound.play()
                        objs.remove(obj)
                        explosionn = Explosion(obj.x + 25, obj.y, 3)
                        group.add(explosionn)
                        break
                for thing in things:
                    if superlaser.collision(thing):
                        explosionsound.play()
                        explosioNN = Explosion(superlaser.x + 100, superlaser.y, 3)
                        group.add(explosioNN)
                        thing.health -= 180
                        thing.x += random.randint(-30, 30)
                        self.superlasers.remove(superlaser)
                        break
            
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
 
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x + 40, self.y + self.ship_img.get_height() - 40, (self.ship_img.get_width() - 84), 1), 5)
        pygame.draw.rect(window, (0,255,0), (self.x + 40, self.y + self.ship_img.get_height() - 40, (self.ship_img.get_width() - 84) * (self.health/self.max_health), 1), 5)
        
    def death(self):
        explosionsound.play()
        self.ship_img = explosion 
        pygame.display.update()
                       
class Enemy(Ship):
    lasertypes = {
        "bigenemy": (bigenemyship, redlaser),
        "smallenemy": (smallenemyship, redlaser)
    }

    def __init__(self, x, y, lasertypes, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.lasertypes[lasertypes]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, enemymovepixels):
        self.y += enemymovepixels

class Boss(Ship):
    def __init__(self, x, y, health=1000):
        super().__init__(x, y, health)
        self.ship_img = bosscat
        self.laser_img = cloudy, angry
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = 1000
        self.c = 0
        self.cool_down_counter = 0
        
    def pentashoot(self):
        lasersound.play()
        if self.cool_down_counter == 0:
            laser = Laser((random.randint(0, 400)), self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
    def pentamove(self, movepixels, obj, group):
        self.cooldown()
        for laser in self.lasers:
            laser.move(movepixels)
            if laser.off_screen(Height):
                self.lasers.remove(laser)
            else:
                if laser.collision(obj):                      
                    explosionsound.play()
                    obj.health -= 15
                    self.lasers.remove(laser)
                    explosionn = Explosion(obj.x + 60, obj.y + 75, 2)
                    group.add(explosionn)
                    break

    def AI(self, obj, movepixels, objs):           
        if self.x + self.get_width() >= Width:
            self.x -= 30
            
        if self.x <= 0:
            self.x += 30

        self.c += 1
        if self.c % 2 == 0:
            self.y += movepixels

        for thing in objs:
            if collide(self, thing):
                self.x += random.randint(-30, 30)
                break

        if collide(self, obj):
            self.health -= 50
            self.y += 2
                
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x + 40, self.y + self.ship_img.get_height() - 40, (self.ship_img.get_width() - 84), 1), 5)
        pygame.draw.rect(window, (0,255,0), (self.x + 40, self.y + self.ship_img.get_height() - 40, (self.ship_img.get_width() - 84) * (self.health/self.max_health), 1), 5)
        
    def draw(self, window):
        super().draw(window)
        for laser in self.lasers:
            laser.draw(window)
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, stage):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(os.path.join("Assets", f"exp{i}.png"))
            if stage == 1:
                img = pygame.transform.scale(img, (20, 20))
            if stage == 2:
                img = pygame.transform.scale(img, (40, 40))
            if stage == 3:
                img = pygame.transform.scale(img, (120, 120))
            self.images.append(img)
        self.counter = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def update(self):
        expspeed = 3
        self.counter += 1
        
        if self.counter >= expspeed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
            
        if self.index >= len(self.images) - 1 and self.counter >= expspeed:
            self.kill()
            
    def draw(self):
        win.blit(self.image, (self.x, self.y))
                       
class Lifesaver:
    SPAWNCOOLDOWN = 300
    def __init__(self, x, y, img=lifesaver):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.spawncooldown = 0
        
    def draw(self):
        win.blit(self.img, (self.x, self.y)) 

class Kamehameha:
    def __init__(self, x, y, wid):
        self.x = x
        self.y = y
        self.wid = wid
        self.rect = self.get_rect()

    def spawnk(self):
        pygame.draw.rect()
                              
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    score = 0
    win = pygame.display.set_mode((Width, Height))
    FPS = 200
    lives = 5
    level = 5
    clock = pygame.time.Clock()
    run = True
    main_font = pygame.font.Font("Assets/PixelOperator.ttf", 50)
    title_font = pygame.font.Font("Assets/Prototype.ttf", 50)
    playermovepixels = 8
    enemies = []
    bossS = []
    lifesavers = []
    wave_length = 5
    enemymovepixels = 2
    lost = False
    lost_count = 0
    win_count = 0
    winning = False
    lasermovepixels = 15
    bgvel = -400
    lsvel = 0
    warningc = 0
    superlasermovepixels = 15
    bossmovepixels = 1
    player = Player(180, 480)
    explosion_group = pygame.sprite.Group()
    bsp_c = 0
    ls_spawn = True
    lsnum = 0
    bossbeated = False
    
    #MUSIC
    mixer.music.load(os.path.join("Assets/skyhighncs.mp3"))
    mixer.music.set_volume(1)   
    mixer.music.play(-1)

    if level == 6:
        for i in range(2):
            alarmsound.play()

    def redraw_window(lsspawn, lsnum):
        
        lsvel = 0
        lsvel += 1

        # draw texts>>>>>>>>>>>>>>>>>>>>>>>>>
        lives_label = main_font.render(f"Lives: {lives}", 0, (222, 255, 1))
        level_label = main_font.render(f"Levels: {level}", 0, (255, 255, 255))
        gametitle = title_font.render(f"Space War V1", 0, (255, 255, 255))
        versionlabel = main_font.render("Beta", 0, (255, 255, 255))
        lives_label = pygame.transform.scale(lives_label, (60, 25))
        gametitle = pygame.transform.scale(gametitle, (180, 32))
        level_label = pygame.transform.scale(level_label, (60, 25))
        versionlabel = pygame.transform.scale(versionlabel, (50, 25))
        scorelabel = main_font.render(f"Score: {score}", 0, (30, 255, 255))
        scorelabel = pygame.transform.scale(scorelabel, (80, 25))
        player.cooldownlabel()
        player.supercooldownlabel()
        
        win.blit(lives_label, (player.x + 100, player.y + 30))
        win.blit(level_label, (player.x + 100, player.y + 50))
        win.blit(versionlabel, (0, 570))
        win.blit(scorelabel, (0, 0))
        spawnnumber = 0
        # ======================================

        if level == 6:
            if bsp_c >= 60:
                if len(bossS) == 0 and lives != 0 and winning != True and lsnum == 0:
                    boss = Boss(160, -200)
                    bossS.append(boss)
                    lsnum = 1

        if level == 5:
            if player.health <= 30:
                if len(lifesavers) == 0 and lsspawn == True:
                    lifesaver = Lifesaver(random.randint(0, 400), 0)
                    lifesavers.append(lifesaver)

        if level == 6:
            if player.health <= 20:
                lsspawn = True
                if len(lifesavers) == 0 and lsspawn == True:
                    lifesaver = Lifesaver(random.randint(0, 400), random.randint(0, 400))
                    lifesavers.append(lifesaver)

        for ls in lifesavers:    
            if collide(player, ls):
                player.health += player.max_health-player.health
                lifesavers.remove(ls)
                         
        for obj in lifesavers:
            obj.draw()
            obj.y += 3
            if obj.y + 40 >= Height:
                lifesavers.remove(obj)

        for item in bossS:
            item.draw(win)
            item.AI(player, bossmovepixels, player.lasers)
            for laser in player.lasers:
                if collide(item, laser):
                    item.x += random.randint(-30, 30)
            item.healthbar(win)
            item.pentashoot
            item.pentamove(lasermovepixels, player, explosion_group)

        for enemy in enemies:
            enemy.draw(win)

        explosion_group.update()

        for obj in explosion_group:
            obj.draw()

        player.draw(win)

        pygame.display.update()
        
#===============RUN==============

    while run:
        clock.tick(FPS)

        if random.randrange(0, 80) == 1:
            if level < 6:
                if len(enemies) == 0:
                    alarmsound.play()
                    level += 1
                    if level == 3:
                        bgvel = -400
                    elif level == 5:
                        bgvel = -400
                    wave_length += 5
                    for i in range(wave_length):
                        if level > 5:
                            break
                        enemy = Enemy(random.randrange(50, Width-100), random.randrange(-600, -50), random.choice(["bigenemy", "smallenemy"]))
                        enemies.append(enemy)
            elif len(enemies) == 0 and level == 5:
                level += 1

        
        if lost:
            player = pygame.image.load(os.path.join("Assets", "explosion.png"))
            if level < 3:
                lost_label = main_font.render("Game Over lol", 0, (255, 1, 1, 0.1))
                win.blit(lost_label, (Width/2 - lost_label.get_width() / 2, Height/2 - lost_label.get_height()/2))
            elif level >= 3 and level < 5:
                lost_label = main_font.render("Game Over lel", 0, (255, 255, 255, 0.1))
                win.blit(lost_label, (Width/2 - lost_label.get_width() / 2, Height/2 - lost_label.get_height()/2))
            elif level == 5:
                lost_label = main_font.render("!play belupacito", 0, (255, 255, 255, 0.1))
                win.blit(lost_label, (Width/2 - lost_label.get_width() / 2, Height/2 - lost_label.get_height()/2))   
            elif level == 6:
                lost_label = main_font.render("Cat is the best", 0, (255, 255, 255, 0.1))
                win.blit(lost_label, (Width/2 - lost_label.get_width() / 2, Height/2 - lost_label.get_height()/2))                    
        pygame.display.update()
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        """   THOSE ARE KEYS"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + 50 > 0:  # left
            player.x -= playermovepixels
        if keys[pygame.K_d] and player.x + 100 < Width:  # right
            player.x += playermovepixels
        if keys[pygame.K_w] and player.y + 50 > 0:  # up
            player.y -= playermovepixels
        if keys[pygame.K_s] and player.y + 100 < Height:  # down
            player.y += playermovepixels
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_r]:
            player.superlasershoot()
        
          
        for enemy in enemies[:]:
            enemy.move(enemymovepixels)
            enemy.move_lasers(lasermovepixels, player)
            
            if collide(player, enemy):
                explosionsound.play
                enemy.ship_img = explosion
                enemies.remove(enemy)
                for i in range(1):
                    player.health -= 50
                    break 
                
            if random.randrange(0, 60*4) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > Height:
                enemies.remove(enemy)
                lives -= 1
                
        
#        BACKGROUND TRANSFORMER--------------->

        if level == 3 or level == 4:
            bg = pygame.image.load(os.path.join("Assets", "lvl3space.jpeg"))
            bg = pygame.transform.scale(bg, (1000, 1000))
            win.blit(bg, (-230, bgvel))
        elif level == 5:
            bg = pygame.image.load(os.path.join("Assets", "lvl5 neon.jpeg"))
            bg = pygame.transform.scale(bg, (1000, 1000))
            win.blit(bg, (-230, bgvel))
        elif level < 3:
            bg = pygame.image.load(os.path.join("Assets", "spacewar_background.jpeg"))
            bg = pygame.transform.scale(bg, (1000, 1000))
            win.blit(bg, (-230, bgvel))
        elif level == 6:
            bg = pygame.image.load(os.path.join("Assets", "bossfightpng.jpeg"))
            win.blit(bg, (-230, 0))

        if lives <= 0 or player.health <= 0:
            player.death()
            gameoversound.play()
            lost = True
            lost_count += 1
            for i in range(1):
                explosionsound.play()
        
        bgvel += 0.3
        
        if level == 6:
            bsp_c += 1
            if len(bossS) == 0 and bossbeated == False:
                bosswarning = main_font.render("---->BOSS WARNING<----", 0, (255, 0, 0))
                warningc += 1
                if warningc % 15 != 0:
                    win.blit(bosswarning, (Width/2-bosswarning.get_width()/2, Height/2))
                    
        if winning:
            winninglabel = main_font.render("You won the war!", 0, (255, 255, 255))
            smallfont = pygame.font.Font("Assets/PixelOperator.ttf", 20)
            smallwinning = smallfont.render("What a scrub", 0, (255, 255, 255))
            win.blit(winninglabel, (Width/2-winninglabel.get_width()/2, Height/2))
            win.blit(smallwinning, (Width/2-smallwinning.get_width()/2, Height/2 + 50))
     
        redraw_window(ls_spawn, lsnum)

        player.move_lasers(-lasermovepixels, enemies, explosion_group, bossS)
        player.move_superlasers(-superlasermovepixels, enemies, explosion_group, bossS)
        
        if winning:
            if win_count > 3:
                run = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                continue
            
        for enemy in enemies:
            for laser in player.lasers:
                if collide(laser, enemy):
                    score += 1
                
        for boss in bossS:
            if boss.health <= 0:
                score += 1000
                bossbeated = True
            
        for item in bossS:
            if item.health <= 0:
                winning = True
                win_count += 1
                bossS.remove(item)
                
            if item.y + item.get_height() > Height:
                bossS.remove(item)
                lives = 0 
            
            if collide(item, player):
                player.health -= 30
    
        lsvel += 1 
           
        for thing in lifesavers:
            if collide(thing, player):
                ls_spawn = False

        pygame.display.update()

    pygame.quit()
        
main_font = pygame.font.Font('Assets/PixelOperator.ttf', 30)
#playbuttonbutton = Button()

def main_menu():
    pygame.init()
    mixer.init()
    pygame.font.init()
    title_font = pygame.font.Font("Assets/Prototype.ttf", 50)
    undertitlefont = pygame.font.Font("Assets/PixelOperator.ttf", 20)
    run = True
    while run:
        win.fill('black')
        title_label = title_font.render("Space War Beta", 0, (245, 71, 195))
        undertitlelabel = undertitlefont.render("Press space for shoot, R for superlaser, WASD for move.", 0, (61, 222, 255))
        win.blit(undertitlelabel, (Width/2 - undertitlelabel.get_width() / 2, 340))
        win.blit(title_label, (Width/2 - title_label.get_width() / 2, 260))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                main()
                
    pygame.quit()

main_menu()

main()
