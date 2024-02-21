import pygame
from sys import exit
import random
import math
import os


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\walk_left.png")).convert_alpha()
        player_walk2 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\walk_mid.png")).convert_alpha()
        player_walk3 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\walk_right.png")).convert_alpha()
        self.player_walk = [player_walk1, player_walk2, player_walk3]

        self.player_index = 0

        self.player_jump = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\jump.png")).convert_alpha()
        self.player_stand = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\walk_mid.png")).convert_alpha()


        self.image = self.player_walk[self.player_index]                                     
        self.rect = self.image.get_rect(midbottom = (50,250))

        self.gravity = 0

        self.scroll = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 420:
            self.gravity = -20
        if keys[pygame.K_d]:
            self.moving = "right"
            self.move_right()
            if keys[pygame.K_d and pygame.K_SPACE]:
                self.moving = "right"
                self.move_right()
        elif keys[pygame.K_a]:
            self.moving = "left"
            self.move_left()
            if keys[pygame.K_a and pygame.K_SPACE]:
                self.moving = "left"
                self.move_left()
        elif not (keys[pygame.K_d] or keys[pygame.K_a]):
            self.moving = False    
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 420:
            self.rect.bottom = 420

    def move_right(self,pixels = 5):
        self.rect.x += pixels

    def move_left(self, pixels = 5):
        self.rect.x -= pixels

    def animation(self):
        if self.rect.bottom < 420:
            self.image = self.player_jump
        elif not self.moving:
            self.image = self.player_stand    
        elif self.moving and (self.moving == "left" or self.moving == "right"):
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    
    def draw_bg(self):
        self.bg1 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\bg1.jpg")).convert()
        screen.blit(self.bg1, (0,0))


    def bg_scroll(self):
        for i in range (0,3):
            if self.moving == "right":
                self.scroll += 2
            if self.moving == "left":
                self.scroll -= 2
        if abs(self.scroll) > 1024:
            self.scroll = 0
    
    def draw_bg(self):
        self.bg1 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\bg1.jpg")).convert()
        bg1_width = self.bg1.get_width()
        
        for i in range(-1,3):
            screen.blit(self.bg1, ((i * bg1_width - self.scroll % bg1_width, 0)))

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.move_right()
        self.move_left()
        self.animation()
        self.draw_bg()
        self.bg_scroll()
    
class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\platform.png")).convert_alpha()
        self.rect = self.image.get_rect(bottomright=(1000,420))
        self.random_position()

    def random_position(self):
        self.rect.x = random.randrange(screen_widht)
        self.rect.y = 250

    def draw(self):    
        screen.blit(self.image,(self.rect.x, self.rect.y))




class GameStage():
    def __init__(self):
       self.stage = "intro"
    
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.stage = "main_game" 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.stage = "controls"  
                                   
        # draw elements
        self.text = text.render("> press space to start", True, "#ffffff")
        self.text2 = text2.render("> press C for game controls", True, "#ffffff")

        screen.blit(welcome_screen,(0,0))
        screen.blit(logo, (200,15))
        screen.blit(self.text, (330,150))
        screen.blit(self.text2, (380,210))
        screen.blit(screen_char, (480,300))

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.stage = "pause_game"  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.stage = "outro"        
        # draw elements
        screen.blit(ground, ground_rect)
        player.sprites()[0].draw_bg()
        player.update()
  
        obstacle.draw(screen)
        player.draw(screen)

    def pause_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.stage = "main_game"     

        # draw elements
        self.text = text.render("press R to continue :)", True, "#ffffff")
        screen.blit(controls_bg, (0,0))

        screen.blit(self.text, (400,50))
        screen.blit(pause_char, (0,150))

    
    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.stage = "intro"     

        # draw elements
        
        self.text = text.render("GAME CONTROLS", True, "#ffffff")
        self.text2 = text2.render("or press SPACE to go back", True, "#ffffff")

        screen.blit(controls_bg, (0,0))
        screen.blit(self.text, (50,50))
        screen.blit(self.text2, (60,100))
        screen.blit(controls_char, (480,340))
        screen.blit(controls_enemy,(50,340))

        
        controll_text = ["A - move right", "D - move left", "SPACE - jump", "P - pause", "Q - quit"]
        self.texts = [text.render(line, True, "#ffffff") for line in controll_text]
        pos_x = 450
        pos_y = 50
        text_height = 30
        for rendered_text in self.texts:
            screen.blit(rendered_text, (pos_x, pos_y))
            pos_y += text_height + 10

    def outro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.stage = "intro"     

        # draw elements
        self.text = text.render("Leaving already? press Q one more time", True, "#ffffff")

        screen.fill("#57a8d4")
        screen.blit(self.text, (200,150))
        screen.blit(screen_char, (480,300))

    def stage_mn(self):
        if self.stage == "intro":
            self.intro()
        if self.stage == "main_game":
            self.main_game()
        if self.stage == "pause_game":
            self.pause_game()
        if self.stage == "controls":
            self.controls()
        if self.stage == "outro":
            self.outro()    

# general game setup
pygame.init()
game_stage = GameStage()



# screen setup
screen_height = 448
screen_widht = 1024
screen = pygame.display.set_mode((screen_widht, screen_height))

text = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "assets\\font.otf"), 30)
text2 = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "assets\\font.otf"), 25)

pygame.display.set_caption("Rat game")

# frame rate
clock = pygame.time.Clock()
FPS = 60

# intro screen
screen_char = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\char_screen.png")).convert_alpha()
welcome_screen = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\into_screen.jpg")).convert_alpha()
logo = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\logo.png")).convert_alpha()

# controls screen
controls_bg = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\bg3.jpg")).convert_alpha()
controls_char = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\run_char.png")).convert_alpha()
controls_enemy = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "enemies\\cat_screen.png")).convert_alpha()
text = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "assets\\font.otf"), 40)

#pause screen
pause_char = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "char\\char_pause.png")).convert_alpha()

# background
bg1 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\bg1.jpg")).convert()
bg1_rect = bg1.get_rect(topright = (screen_widht,0))

ground = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "assets\\ground.jpg")).convert()
ground_rect = ground.get_rect(bottomright = (screen_widht,440))


# player

player = pygame.sprite.GroupSingle()
player.add(Player())

# obstacles

obstacle = pygame.sprite.GroupSingle()
obstacle.add(Obstacles())

while True:

    game_stage.stage_mn()

    pygame.display.update()
    clock.tick(FPS)

