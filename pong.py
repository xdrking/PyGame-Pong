# PyGame kütüphanesini projemize ekliyoruz.
from calendar import different_locale
from multiprocessing import reduction
from turtle import right
from urllib.parse import MAX_CACHE_SIZE
import pygame
pygame.init()

#Ekran ile ilgili (Boyut, Pencere ismi, FPS değeri vb.) değişkenleri tanımlıyoruz.
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pin-Pon")
FPS = 60

# Arka plan ve paddle(Raket) renklerini tanımlıyoruz.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Paddle yani raketlerimizin ve topumuzun boyutlarını tanımlıyoruz.
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
#Score font adında bir değişken tanımlıyıp skor ekranımızdaki yazı fontunu ve boyutunu ayarlıyoruz.
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNIG_SCORE = 10


# Paddle isminde bir sınıf oluşturuyoz. Paddle dediğimiz aslında masa tenisi oynunda olduğu gibi raketlerimiz sayılıyor.
class Paddle:
    color = WHITE
    vel = 4
    
    def __init__(self, x, y, width, height ):
        self.x = self.original_x =  x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel 
    def reset (self):
        self.x = self.original_x
        self.y = self.original_y               
             
# Ball isminde bir sınıf oluşturuyoruz. Bizim topumuz ile ilgili değerleri, ayarları vb buranın altına ekleyip,
# bir fonksiyon açarak topumuzun hareketlerini davranışlarını kodluyoruz.
class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius) 
    # Def move fonksiyonu isminden anlaşıldığı gibi topumuzu hareket ettirmek için kullanıyoruz.
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel 
        
    def reset(self): 
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1 
        

# Bu fonksiyon ise parantez içinde yazan tüm değişkenleri pencere içerisinde oluşturuyor.
# Örneğin paddlerın konumları, topun konumları, ve skorların konumları burada ayarlanıyor. 
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:
        paddle.draw(win)
        
    for i in range (10,HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20)) 
    ball.draw(win)       
    pygame.display.update()
    
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
        
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height /2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                
                middle_y = right_paddle.y + right_paddle.height /2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                
            
# Bu fonksiyon ise klavyeden paddlerımızı yönetmemizi sağlayan kodları içeriyor.    
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.vel >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.vel + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
        
        
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.vel + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)                
    
# Bu fonksiyon ise oyunda yer alan tüm parçaların aslında projemize katıldığı bölümdür.
# Oyun ilk açıldığında götdüğümüz tüm elementler yer aldığı kısımdır aslında.

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    
    # Oyunun çalışmasını ve olayların dönmesini sağlayan temel while döngümüz burada yer alıyor.
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle) 
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        
        # Skor tablomuzun çalışmasını sağlayan basit bir if döngüsü.
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()  
        # Kazanma Ekranının ayarlandığı bölüm.    
        won = False   
        if left_score >= WINNIG_SCORE:
            won = True
            win_text = "Left Player Win!"
        elif right_score >= WINNIG_SCORE:
            won = True
            win_text = "Right Player Win!"
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            
            
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()         
            
            
    pygame.quit()
    
if __name__ == '__main__':
    main()            