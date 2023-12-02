from pygame import *
from random import *
from time import time as timer
mixer.init()
mixer.music.load('space1.ogg')
mixer.music.play()
fire_sound = mixer.Sound('blast.ogg')

img_hero = 'korable.png'
img_back = 'galaxy.jpg'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = 'asteroid.png'


score = 0
lost = 0
max_lost = 3
font.init()
font1 = font.SysFont('Arial', 38)

class GameSprite(sprite.Sprite):

   def __init__(self, player_image, player_x, player_y, player_speed, size_x,
   size_y):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top, -15, 30, 20)
        bullets.add(bullet)
   def draw_health_bar(self):
        if self.health > 0:
            draw.rect(window, (255, 0, 0),
                       (self.rect.x, self.rect.y - 10, self.health, 5))
        else:
            self.kill()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('strelalka')
background = transform.scale(image.load(img_back), (win_width,win_height))

bullets = sprite.Group()
player = Player(img_hero, 270, 400, 10, 100, 100)
monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy(img_enemy, randint(80, win_width -80),
     -40, randint(1, 5), 100, 50,)
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width -30),-40, randint(1, 7), 50,80)
    asteroids.add(asteroid)
finish = False
run = True
reload =False
num_fire = 0
tsel = 5
while run:
    for knopka in event.get():
        if knopka.type ==QUIT:
            run = False
        if knopka.type == KEYDOWN:
            if knopka.key == K_SPACE:
                if num_fire < 5 and reload == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and reload == False:
                    soot_time = timer()
                    reload == True
    if not finish:
        window.blit(background, (0,0))
        text = font1.render("Счёт: " + str(score),
         1, (255, 255, 255))
        window.blit(text, (10,20))
        text_lose = font1.render( "Пропущено: " + str(lost),
         1, (255, 255, 255))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        player.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        if reload == True:
            now_time = timer()
            if now_time - soot_time < 3:
                reload1 = font1.render('Перезарядка.....',1, (150, 0, 0))
                window.blit(reload1, (260, 460))
            else:
                num_fire = 0
                reload = False
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score = score + 1
                monster = Enemy(img_enemy, randint(80, win_width - 80), 
                                -40, 80, 50, randint(1, 5))
                monsters.add(monster)
            if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False) or lost >= max_lost:
                finish = True 
                window.blit(lose, (250, 200))
            if score >= tsel:
                finish = True
                window.blit(win, (250, 200))
        display.update()
    time.delay(50)
