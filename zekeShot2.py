import pygame, sys, math, random, time

from pygame import Vector2, sprite
from pygame import mixer
from pygame.draw import rect

global dt
GAME_WIDTH = 800
GAME_HEIGHT = 800
pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Zeke Shot")
favicon = pygame.image.load("data/images/Player.png")
pygame.display.set_icon(favicon)

is_menu = True

class Explosion():
    global dt
    def __init__(self, position):
        self.position = Vector2()
        self.position.x = position.x
        self.position.y = position.y
        self.width = 20

    def draw(self, screen):
        pygame.draw.circle(screen, (220, 0, 0), self.position, self.width)
        pygame.draw.circle(screen, (255, 153, 51), self.position, self.width - (self.width / 2))
    
    def scale_down(self):
        if(self.width > 0):
            self.width -= dt * 50


class Trap():
    global dt
    global frame
    
    def __init__(self):
        self.refresh_sprite()
        w, h = pygame.display.get_surface().get_size()
        self.position = pygame.Vector2()
        
        self.position = h - (h/5)
        self.position = w/2
        
        self.velocity = pygame.Vector2()
        self.trap_sprite = pygame.image.load('data/images/Trap.png').convert_alpha()
        self.trap_sprite = pygame.transform.scale(self.trap_sprite, (50, 50))
        self.position = pygame.Vector2()
        self.drag = 100
    
    def move(self):
        #Make sure to ade a player dectection 
        self.air_resistance()
        #self.player_detection()
        if():       
            self.position.x -= self.velocity.x * frame
        self.position.y -= self.velocity.y * frame
    
    

    def refresh_sprite(self):
        self.trap_sprite = pygame.image.load('data/images/Trap.png').convert_alpha()
        self.trap_sprite = pygame.transform.scale(self.trap_sprite, (50, 50))

    def draw(self, screen):
        screen.blit(self.trap_sprite, self.blit_position())

    def set_position(self, position):
        self.position = position
    
          
    def blit_position(self):
        return self.position.x, self.position.y
    

        
        
    def handle_events(self):   
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_A: 
                    self.blit_position(self, -1)      
                if event.key == pygame.K_D:   
                    self.blit_position(self, 1)    
    def air_resistance(self):
        if(self.velocity.y > 0):
            self.velocity.y -= self.drag * frame
        if(self.velocity.x > 0):
            self.velocity.x -= (self.drag - 50) * frame
        else:
            self.velocity.x += (self.drag - 50) * frame
  
                
                
    def add_force(self, vector, magnitude):
        self.velocity.x += vector.x * magnitude
        self.velocity.y += vector.y * magnitude
        

class Player():
    global dt
    def __init__(self):
        self.is_dead = False
        self.score = 0
        self.position = pygame.Vector2()
        w, h = pygame.display.get_surface().get_size()
        self.position.xy = w / 2, h / 5
        self.velocity = pygame.Vector2()
        self.rotation = pygame.Vector2()
        self.offset = pygame.Vector2()
        self.drag = 100
        self.gravity_scale = 300
        self.player_sprite = pygame.image.load('data/images/Player.png').convert_alpha()
        self.player_sprite = pygame.transform.scale(self.player_sprite, (50, 60))
        
        
        
        self.font = pygame.font.Font("data/fonts/SoapBubble.ttf", 50)

    def move(self):
        self.gravity()
        self.air_resistance()
        self.wall_detection()
        self.position.x -= self.velocity.x * dt
        self.position.y -= self.velocity.y * dt
    

    def wall_detection(self):
        if(self.position.x < 0):
            self.position.x = GAME_WIDTH
        if(self.position.x > GAME_WIDTH):
            self.position.x = 0
    
    def tap_dection(self):
        return
        

    def get_score(self):
        return self.score
    
    def score_render(self):
        scoreText = self.font.render("Score:", False, (117,97,97))
        text = self.font.render(str(self.get_score()), False, (117,97,97))
        
        x = 30
        y = 50
        screen.blit(scoreText, (x,y))
        screen.blit(text, (x*4 + 10,y))
        
    def gravity(self):
        self.velocity.y -= self.gravity_scale * dt

    def air_resistance(self):
        if(self.velocity.y > 0):
            self.velocity.y -= self.drag * dt
        if(self.velocity.x > 0):
            self.velocity.x -= (self.drag - 50) * dt
        else:
            self.velocity.x += (self.drag - 50) * dt

    def check_state(self):
        global is_menu
        if self.is_dead:
            old_highscore_value = open("data/scores/highscore.csv", "r").readline()
            try:
                if (self.score > int(old_highscore_value)):
                    with open("data/scores/highscore.csv", "w") as highscore_value:
                        highscore_value.write(str(self.score))
            except:
                pass
            is_menu = True

    def collision_detection(self, level_builder):
        for i in range(len(level_builder.refills)):
            other = level_builder.refills[i]
            if(self.get_left() < other.get_right() and self.get_right() > other.get_left() and self.get_top() < other.get_bottom() and self.get_bottom() > other.get_top()):
                level_builder.populate_refill()
                self.score += 1
                print(self.score)

        for i in range(len(level_builder.enemies)):
            other = level_builder.enemies[i]
            if(self.get_left() < other.get_right() and self.get_right() > other.get_left() and self.get_top() < other.get_bottom() and self.get_bottom() > other.get_top()):
                self.is_dead = True
        if(self.position.y > 850):
            self.is_dead = True
    
    def get_right(self):
        return self.position.x + (self.player_sprite.get_width() / 2)

    def get_left(self):
        return self.position.x - (self.player_sprite.get_width() / 2)
    
    def get_top(self):
        return self.position.y - (self.player_sprite.get_height() / 2)
    
    def get_bottom(self):
        return self.position.y + (self.player_sprite.get_height() / 2)

    def draw(self, screen):
        screen.blit(self.player_sprite, self.blit_position())
        


    def blit_position(self):
        return (self.position.x - (self.player_sprite.get_width() / 2), self.position.y - (self.player_sprite.get_height() / 2))

 

    def add_force(self, vector, magnitude):
        self.velocity.x += vector.x * magnitude
        self.velocity.y += vector.y * magnitude
    


class Refill:
    def __init__(self, position):
        self.position = Vector2()
        self.position.x = position.x
        self.position.y = position.y
        self.gun_sprite = pygame.image.load('data/images/Ammo.png').convert_alpha()
        self.gun_sprite = pygame.transform.scale(self.gun_sprite, (30, 40))

    def draw(self, screen):
        screen.blit(self.gun_sprite, self.position)
    
    def get_right(self):
        return self.position.x + 30

    def get_left(self):
        return self.position.x 
    
    def get_top(self):
        return self.position.y
    
    def get_bottom(self):
        return self.position.y + 40
    


class Enemy:
    global dt
    def __init__(self, position):
        self.position = Vector2()
        self.position.x = position.x
        self.position.y = position.y
        self.gravity_scale = random.randrange(20, 41)

        self.xOffset = 0
        self.yOffset = 0
         
        rand = random.randrange(0, 2)
        self.enemy_sprite = None

        if(rand == 0):
            self.enemy_sprite = pygame.image.load('data/images/Fox.png').convert_alpha()
            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (40, 40))
            self.xOffset = 40
            self.yOffset = 40
        elif(rand == 1):
            self.enemy_sprite = pygame.image.load('data/images/EnemyZeke.png').convert_alpha()
            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (30, 50))
            self.xOffset = 30
            self.yOffset = 50
        

    def draw(self, screen):
        screen.blit(self.enemy_sprite, self.position)
        self.gravity()

    def gravity(self):
        self.position.y += self.gravity_scale * dt
    
    def get_right(self):
        return self.position.x + self.xOffset

    def get_left(self):
        return self.position.x - self.xOffset
    
    def get_top(self):
        return self.position.y - self.yOffset
    
    def get_bottom(self):
        return self.position.y + self.yOffset



class LevelBuilder:
    def __init__(self):
        self.refills = []
        self.enemies = []
    def populate_refill(self):
        self.refills = []
        for _ in range(2):
            pos = Vector2()
            pos.x = random.randint(100, 700)
            pos.y = random.randint(100, 500)
            refill = Refill(pos)
            self.refills.append(refill)

    def spawn_enemies(self):
        rand = random.randrange(0, 3)
        for _ in range(rand):
            random_pos = random.randint(0, 760)
            position = Vector2()
            position.x = random_pos
            position.y = -30
            enemy = Enemy(position)
            self.enemies.append(enemy)
        
            
    def draw(self, screen):
        enemies_to_remove = []
        
        for i in range(len(self.refills)):
            self.refills[i].draw(screen) 
            
        for i in range(len(self.enemies)):
            self.enemies[i].draw(screen)    
            if(self.enemies[i].position.y > 850):
                enemies_to_remove.append(i)
                
        for i in reversed(enemies_to_remove):
            self.enemies.pop(i)

class Game:
 
    
    def __init__(self, screen):
        self.screen = screen
        self.size = None
        self.width = None
        self.height = None
        self.background_color = 240, 240, 240
        self.player = Player()
        self.trap = Trap()
        self.level_builder = LevelBuilder()
        self.clock = pygame.time.Clock()
        self.score = 0
        

        self.update()

    def update(self):
        global is_menu
        self.level_builder.populate_refill()
        next_time = time.time()
        elapsed_time = time.time()
        min_time = 5
        max_time = 10
        enemiy_iteration = 0
        s = 0
        
        while not is_menu:
            self.handle_dt()
            self.clear_screen()
            
         
            
            self.trap.draw(screen)

            
            self.level_builder.draw(screen)
            self.level_builder.draw(screen)
            
            self.trap.move()
            
            self.player.move()
            self.player.collision_detection(self.level_builder)
            self.player.check_state()
            self.player.draw(self.screen)
            self.player.score_render()
            
            s = self.player.get_score()
        
            self.score = self.player.get_score()
            
            
            
            
            

            pygame.display.flip()
            self.handle_events()


            elapsed_time = time.time()
            if(elapsed_time > next_time):
                next_time = elapsed_time + random.randint(min_time, max_time)
                self.level_builder.spawn_enemies()
                enemiy_iteration += 1
                if(enemiy_iteration > 5 and min_time > 1):
                    min_time -= 1
                    max_time -= 1
                    enemiy_iteration = 0
                    
        
        
     
    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT :  
                        trap_x -= 1
                    if event.key == pygame.K_RIGHT:
                        trap_x += 1
                    if event.key == pygame.K_a:      
                        trap_x -= 1
                    if event.key == pygame.K_d:
                        trap_x += 1
     
    
                        
    def clear_screen(self):
        self.screen.fill(self.background_color)

    def handle_dt(self):
        global dt
        dt = self.clock.tick() / 1000


class Menu():
    def __init__(self, screen):
        
        self.background_color = 240, 240, 240
        self.screen = screen
        self.update()

    def update(self):
        global is_menu
        pygame.font.init()
    

        while is_menu:
            self.clear_screen()

            logo = pygame.image.load('data/images/Logo.png').convert_alpha()
            logo = pygame.transform.scale(logo, (100, 120))
            screen.blit(logo, (350, 60))

            self.font = pygame.font.Font("data/fonts/SoapBubble.ttf", 70)
            text = self.font.render("Zeke shot", False, (100,100,100))
            screen.blit(text, (300, 180))

            self.font = pygame.font.Font("data/fonts/SoapBubble.ttf", 50)
            text = self.font.render("Play NOW!", False, (200,200,200))
            screen.blit(text, (300,340 + (math.sin(time.time() * 10) * 5)))


            self.font = pygame.font.Font("data/fonts/DripOctober-vm0JA.ttf", 30)
            highscore_value = open("data/scores/highscore.csv", "r").readline()
            highscore = self.font.render("Highest score " + str(highscore_value), False, (180,180,180))
            screen.blit(highscore, (250,400 + (math.sin(time.time() * 10) * 5)))
            pygame.display.flip()
            self.handle_events()

    def clear_screen(self):
        self.screen.fill(self.background_color)
            
    def handle_events(self):
        global is_menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_menu = False
                

instance = None


while True:
    instance = Menu(screen) if (is_menu) else Game(screen)
    print(is_menu)
    
    