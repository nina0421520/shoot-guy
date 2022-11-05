from calendar import c
from string import whitespace
import pygame
import random #引入隨機模組
import os


FPS=60
WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK =(0,0,0)
RED=(255,0,0)
WIDTH = 500
HEIGHT = 600

#遊戲初始化＋創建視窗
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("HAVE FUN")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("img","back.png")).convert()
player_img = pygame.image.load(os.path.join("img","警察.jpg")).convert()
rock_img = pygame.image.load(os.path.join("img","壞人0.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","子彈.png")).convert()

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#call 內建初始函式
        self.image = pygame.transform.scale(player_img,(50,50))#照片大小
        self.image.set_colorkey(WHITE)#去白背景
        #self.image =pygame.Surface((50,40))#顯示圖片
        #self.image.fill((GREEN))
        self.rect = self.image.get_rect() #定位圖片
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.rect.bottom = HEIGHT -10
        self.speedx = 8
        
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:#判斷按右鍵
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#call 內建初始函式
        self.image = pygame.transform.scale(rock_img,(50,50))#照片大小
        self.image.set_colorkey(BLACK)
        #self.image.fill((RED))
        self.rect = self.image.get_rect() #定位圖片
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) #隨機
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2,10)#掉下速度
        self.speedx = random.randrange(-3,3)#水平

    def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:#一出畫面就重置
                self.rect.x = random.randrange(0, WIDTH - self.rect.width) #隨機
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(2,10)#掉下速度
                self.speedx = random.randrange(-3,3)#水平

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)#call 內建初始函式
        self.image = pygame.transform.scale(bullet_img ,(10,20))#照片大小
        self.image.set_colorkey(BLACK)
        #self.image =pygame.Surface((10,20))#顯示圖片
        #self.image.fill((YELLOW))
        self.rect = self.image.get_rect() #定位圖片
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()#子彈刪除
             

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
rock = Rock()
all_sprites.add(rock)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

running = True

score = 0


#遊戲迴圈
while running:
    clock.tick(FPS) #一秒更新幾次畫面
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


        
#update game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)#判斷石頭子彈碰撞
    for hit in hits:
        score += hit.radius
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.spritecollide(player,rocks,False)#判斷石頭船碰撞
    if hits:
        running = True
        
#畫面 
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    pygame.display.update()


pygame.quit()


