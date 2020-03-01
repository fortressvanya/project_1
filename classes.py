import pygame
import os
import random
import datetime
import sys

pygame.init()
size = width, height = 720, 420
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

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


blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Brick_group = pygame.sprite.Group()
Arrow_group = pygame.sprite.Group()

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
        im = load_image('red_ball.png', -1)
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
        hitGroup = pygame.sprite.Group(block)
        spriteHitList = pygame.sprite.spritecollide(self, hitGroup, False)
        if len(spriteHitList) > 0:
            for sprite in spriteHitList:
                if sprite.name == 'block':
                    sprite.kill()
                    sound2.play()
                    self.score += 1
            self.vy *= -1
            self.rect.y += self.vy
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
    def __init__(self, y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect()
        self.vx = 10
        self.start_position_x = (width - self.rect.x) // 2
        self.rect.x = self.start_position_x
        self.rect.y = y - 40

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


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Arrow_group, all_sprites)
        self.image = load_image('arrow.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.ou = 0


info = pygame.Surface((800, 30))


class Menu:
    def __init__(self, punkts=[800, 700, u'Punkt', (250, 250, 250), (0, 0, 0)]):
        self.punkts = punkts

    def render(self, poverhnost, num_punkt):
        font = pygame.font.Font(None, 50)
        self.font_menu = pygame.font.Font(None, 50)
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        done = True

        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0


class Block(pygame.sprite.Sprite):

    def __init__(self):
        self.blockWidth = 72
        self.blockHeight = 20
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.blockWidth, self.blockHeight))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.name = 'block'


def createBlocks():
        for row in range(6):
            for i in range(width):
                block = Block()
                block.rect.x = i * (block.blockWidth + 2)
                block.rect.y = row * (block.blockHeight + 2)
                block.color = setBlockColor(block, row, i)
                block.image.fill(block.color)
                blocks.add(block)

        return blocks


def setBlockColor(block, row, column):
    if column == 0 or column % 2 == 0:
        return YELLOW
    else:
        return CYAN



block = createBlocks()
allSprites = pygame.sprite.Group(block)
ball = Ball()
ball.spawn()
fps = 24
hero = Hero(height)
move_left = False
move_right = False
lose = False
startsc = True
start_screen()
move_mouse = False
Robo = False

pygame.mixer.music.load('data1\mk.mp3')
pygame.mixer.music.set_volume(10)
pygame.mixer.music.play()
sound2 = pygame.mixer.Sound('data1\cock.wav')
sound1 = pygame.mixer.Sound('data1\game_over.wav')
U = 0

back = load_image('back.jpg')
pygame.transform.scale(back, (width, height))
arrow = Arrow()
while startsc:
    start_screen()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            startsc = False
        if event.type == pygame.QUIT:
            running = False
            startsc = False
    pygame.display.flip()


punkts = [(350, 300, u'Play', (250, 250, 250), (250, 250, 250), 0),
          (350, 340, u'Exit', (250, 250, 250), (250, 250, 250), 1)]
game = Menu(punkts)
game.menu()
done = True
while done:
    info.fill((0, 0, 0))
    screen.fill((0, 0, 0))
    punkt = 0
    mp = pygame.mouse.get_pos()
    for i in game.punkts:
        if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
            punkt = i[5]
    game.render(screen, punkts)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(0)
                arrow.rect.x = event.pos[0]
                arrow.rect.y = event.pos[1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_UP:
                if punkt > 0:
                    punkt -= 1
            if event.key == pygame.K_DOWN:
                if punkt < len(game.punkts) - 1:
                    punkt += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if punkt == 0:
                done = False
            elif punkt == 1:
                exit()
    Arrow_group.update()
    Arrow_group.draw(screen)
    screen.blit(info, (0, 0))
    screen.blit(screen, (0, 30))
    pygame.display.flip()

while running:
    screen.blit(back, (0, 0))
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

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(0)
                arrow.rect.x = event.pos[0]
                arrow.rect.y = event.pos[1]
                X = event.pos[0]
                hero.rect.x = X
    if lose:
        lost()
        pygame.mixer.music.stop()
        if U == 0:
            sound1.play()
            U += 1

    if move_right:
        hero.move_right()
    if move_left:
        hero.move_left()
    font = pygame.font.Font(None, 50)
    text = font.render(f'Scores: {ball.score}', 1, (0, 0, 0))
    screen.blit(text, (0, 0))
    blocks.update()
    ball.update()
    all_sprites.update()  # апдейт и фриз
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
