from pygame import *
from random import randint
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
sound1 = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 36)
FPS = 60
run = True
clock = time.Clock()
score = 0
lost = 0
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet) 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 420)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 420), -40, 80, 50, randint(1, 5))
    monsters.add(monster) 
bullets = sprite.Group()       
ship = Player("rocket.png", 0, 400, 80, 100, 10)
max_lost = 3
goal = 10
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                sound1.play()
                ship.fire()
    if not finish:
        window.blit( background, (0, 0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, 420), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (250,250))
        if score >= goal:
            finish = True
            window.blit(win, (250, 250))
        text = font1.render('Уничтожено:' + str(score), 1, (255, 255, 255))
        window.blit(text, (0, 0))
        text1 = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text1, (0, 50))
        display.update()
    clock.tick(FPS)
    