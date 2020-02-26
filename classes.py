import pygame
import os
import random

pygame.init()
size = width, height = 720, 420
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

Font = pygame.font.SysFont(None, 30)
Font2 = pygame.font.SysFont(None,72)


def load_image(name, colorkey=None):
    fullname = os.path.join('data1', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Brick_group = pygame.sprite.Group()

fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
screen.blit(fon, (0, 0))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Управление: A , D",
                  "Выход: esc",
                  "Нажмите кнопку"]
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ball_group, all_sprites)
        im = load_image('red_ball.png')
        self.image = pygame.transform.scale(im, (20, 20))
        self.rect = self.image.get_rect()
        self.v = 6
        self.vx = 5
        self.vy = 5
        self.score = 0

    def spawn(self):
        self.rect.x = (size[0] - int(self.rect.width)) // 2
        self.rect.y = (size[1] - int(self.rect.height)) // 2
        self.vx = 3
        self.vy = 3

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            sound2.play()
        if pygame.sprite.spritecollideany(self, player_group):
            ball1 = ball.rect.x + ball.rect.width // 2
            h = pygame.sprite.spritecollideany(self, player_group)
            hero1 = h.rect.x + h.rect.width // 2
            self.vy = -self.vy
            if self.vx < 0:
                self.vx = -abs(ball1 - hero1)
            else:
                self.vx = abs(ball1 - hero1)
            v = h.rect.width
            self.vy = -(abs(v**2 - self.vx**2))**0.5 // 3 + 10
            self.vx = self.vx // 5
            self.score += 1
            sound2.play()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            sound2.play()
        self.rect.x += self.vx
        self.rect.y += self.vy
        delta = random.randint(1, 6)
        if delta % 6 == 0:
            self.v += 1

    def game_over(self):
        if self.rect.y > height:
            return True

    def ball_coor(self):
        return [self.rect.x, self.rect.y]


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        if y1 == y2:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect()
        self.vx = 10
        self.start_position_x = (width - self.rect.x) // 2
        self.rect.x = self.start_position_x
        self.rect.y = height - 40

    def move_right(self):
        if self.rect.x + self.rect.width + self.vx > width:
            self.rect.x += width - self.rect.x - self.rect.width
        else:
            self.rect.x += self.vx

    def move_left(self):
        if self.rect.x - self.vx < 0:
            self.rect.x = 0
        else:
            self.rect.x -= self.vx

    def spawn(self):
        self.rect.x = self.start_position_x

    def die(self):
        self.rect.x = -100


def lost():
    screen.fill(BLACK)

    font = pygame.font.Font(None, 50)
    text1 = font.render("press 'space' to replay", 1, (255, 255, 255))
    text2 = Font2.render("GAME OVER", True, WHITE, BLACK)
    text3 = Font.render("Press 'esc' to exit", True, WHITE, BLACK)
    text4 = Font.render(f"Score:{ball.score}", True, WHITE, BLACK)

    textrect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect7 = text4.get_rect()

    textrect1_x = 170
    textrect1_y = 100

    textRect2.center = screen.get_rect().center
    textRect3.midbottom = screen.get_rect().midbottom
    textRect7.midtop = screen.get_rect().midtop

    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect7)
    screen.blit(text1, (textrect1_x, textrect1_y))
    hero.die()


ball = Ball()
ball.spawn()
fps = 24
hero = Hero()
move_left = False
move_right = False
lose = False
startsc = True
start_screen()
move_mouse = False
pygame.mixer.music.load('data1\mk.mp3')
pygame.mixer.music.set_volume(10)
pygame.mixer.music.play()
sound2 = pygame.mixer.Sound('data1\cock.wav')
sound1 = pygame.mixer.Sound('data1\game_over.wav')
U = 0
while startsc:
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            startsc = False
    pygame.display.flip()

while running:
    screen.blit(fon, (0, 0))
    screen.fill((255, 255, 255))

    Border(0, 0, 0, height)  # чтоб не улетал
    Border(width, 0, width, height)
    Border(0, 0, width, 0)

    if ball.game_over():  # проверка на проигрыш
        lose = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            move_mouse = False
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                if lose:
                    ball.spawn()
                    hero.spawn()
                    lose = False
                    U = 0
                    ball.score = 0
                    pygame.mixer.music.play()
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            X = event.pos[0]
            move_mouse = True
    if lose:
        lost()
        pygame.mixer.music.stop()
        if U == 0:
            sound1.play()
            U += 1
    if move_mouse:
        if hero.rect.x + hero.rect.width // 2 != X:

            if hero.rect.x + hero.rect.width // 2 < X:
                if X - hero.rect.x + hero.rect.width // 2 < 10:
                    hero.rect.x = X + hero.rect.width // 2
                else:
                    hero.rect.x += 10

            else:
                if X - hero.rect.x + hero.rect.width // 2 > 10:
                    hero.rect.x = X - hero.rect.width // 2
                else:
                    hero.rect.x -= 10
        else:
            move_mouse = False
    if move_right:
        hero.move_right()
    if move_left:
        hero.move_left()
    font = pygame.font.Font(None, 50)
    text = font.render(f'Scores: {ball.score}', 1, (0, 0, 0))
    screen.blit(text, (0, 0))
    ball.update()
    all_sprites.update()  # апдейт и фриз
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
