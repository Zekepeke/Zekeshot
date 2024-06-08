import pygame, sys, math, random, time

from pygame import Vector2, sprite,mixer
from pygame.draw import rect

global dt

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Zeke Shot")
icon = pygame.image.load("data/images/Player.png")
pygame.display.set_icon(icon)

is_menu = True

class Bullet():
    global frame
    def __init__(self, position):
        #Makes a bullet following the player and size of bullet explosion can be changed by width 
        self.explosion = None
        self.position = Vector2()
        self.position.x = position.x
        self.position.y = position.y
        self.width = 100

    def draw(self, screen):
        w = math.fabs(self.width)
        self.explosion = pygame.image.load('data/images/Explosion.png').convert_alpha()
        self.explosion = pygame.transform.scale(self.explosion, (w, w))
        screen.blit(self.explosion, self.position)
    
    def scale_down(self):
        #Rate of change of bullet explosion being diminished
        if(self.width > 0):
            self.width -= frame * 100


class Chicken():
    def __init__(self):
        self.chicken_sprite = None
        self.position = Vector2()
        self.is_flipped = False
        self.bullet_count = 3
        pygame.font.init()
        self.font = pygame.font.Font("data/fonts/DripOctober-vm0JA.ttf", 300)
        self.position = pygame.Vector2()
        self.refresh_sprite()
        self.explosions = []

    def render_current_ammo(self, screen):
        text = self.font.render(str(self.bullet_count), False, (200,200,200))
        screen.blit(text, (300,200))
    
    def shoot(self):
        if(self.bullet_count > 0):
            exp_pos = Vector2()
            exp_pos.x = self.position.x
            exp_pos.y = self.position.y
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.position.x, mouse_y - self.position.y
            mag = Vector2(rel_x, rel_y).magnitude()
            exp_pos.x += (rel_x / mag) * 100
            exp_pos.y += (rel_y / mag) * 100
            bullet = Bullet(exp_pos)
            self.explosions.append(bullet)
            self.bullet_count -= 1

    def explode(self, screen):
        #Removes a bullet when the bullet is scaled down
        for bullet in self.explosions:
            if(bullet.width <= 1):
                self.explosions.remove(bullet)
                break
            bullet.scale_down()
            bullet.draw(screen)

    def refresh_sprite(self):
        self.chicken_sprite = pygame.image.load('data/images/Chicken.png').convert_alpha()
        self.chicken_sprite = pygame.transform.scale(self.chicken_sprite, (50, 50))

    def draw(self, screen):
        screen.blit(self.chicken_sprite, self.blit_position())
        self.explode(screen)

    def set_position(self, position):
        self.position = position
    
    def set_rotation(self, degrees):
        self.refresh_sprite()
        self.chicken_sprite = pygame.transform.rotate(self.chicken_sprite, degrees)
          
    def blit_position(self):
        return self.position.x - 30, self.position.y + 10

class Player():
    global frame
    def __init__(self):
        self.is_dead = False
        self.score = 0
        self.position = pygame.Vector2()
        w, h = pygame.display.get_surface().get_size()
        self.position.xy = w / 2, h / 5
        self.velocity = pygame.Vector2()
        self.rotation = pygame.Vector2()
        self.offset = pygame.Vector2()
        self.chicken = Chicken()
        self.drag = 100
        self.gravity_scale = 300
        self.player_sprite = pygame.image.load('data/images/Player.png').convert_alpha()
        self.player_sprite = pygame.transform.scale(self.player_sprite, (50, 60))
        self.chicken.set_position(self.position)
        
        
        self.font = pygame.font.Font("data/fonts/SoapBubble.ttf", 50)

    def move(self):
        self.gravity()
        self.air_resistance()
        self.wall_detection()
        self.position.x -= self.velocity.x * frame
        self.position.y -= self.velocity.y * frame
    
    def handle_chicken(self):
        self.chicken.set_position(self.position)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position.x, mouse_y - self.position.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.chicken.set_rotation(angle)

        self.offset.x = min(rel_x, 4) if (self.offset.x > 0) else max(rel_x, -4)
        self.offset.y = min(rel_y, 4) if (self.offset.y > 0) else max(rel_y, -4)

    def wall_detection(self):
        if(self.position.x < 0):
            self.position.x = 800
        if(self.position.x > 800):
            self.position.x = 0

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
        self.velocity.y -= self.gravity_scale * frame

    def air_resistance(self):
        if(self.velocity.y > 0):
            self.velocity.y -= self.drag * frame
        if(self.velocity.x > 0):
            self.velocity.x -= (self.drag - 50) * frame
        else:
            self.velocity.x += (self.drag - 50) * frame

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
        #detection of touching ammo, increments by 1 for ammo and score, and updating score
        for i in range(len(level_builder.refills)):
            other = level_builder.refills[i]
            if(self.get_left() < other.get_right() and self.get_right() > other.get_left() and self.get_top() < other.get_bottom() and self.get_bottom() > other.get_top()):
                self.chicken.bullet_count += 1
                level_builder.populate_refill()
                self.score += 1
                print(self.score)
        #detection of touching enemies
        for i in range(len(level_builder.enemies)):
            other = level_builder.enemies[i]
            if(self.get_left() < other.get_right() and self.get_right() > other.get_left() and self.get_top() < other.get_bottom() and self.get_bottom() > other.get_top()):
                self.is_dead = True
        #If player touches the bottom of the game, the player is considered dead
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
        self.chicken.draw(screen)
        screen.blit(self.player_sprite, self.blit_position())
        


    def blit_position(self):
        return (self.position.x - (self.player_sprite.get_width() / 2), self.position.y - (self.player_sprite.get_height() / 2))

    def shoot(self):
        if(self.chicken.bullet_count <= 0):
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.position.x, mouse_y - self.position.y
        vector = Vector2()
        vector.xy = rel_x, rel_y
        mag = vector.magnitude()
        vector.xy /= mag
        self.velocity.y = 0
        self.velocity.x = 0
        self.add_force(vector, 500)

    def add_force(self, vector, magnitude):
        self.velocity.x += vector.x * magnitude
        self.velocity.y += vector.y * magnitude
    


class Refill:
    def __init__(self, position):
        self.position = Vector2()
        self.position.x = position.x
        self.position.y = position.y
        self.chicken_sprite = pygame.image.load('data/images/Ammo.png').convert_alpha()
        self.chicken_sprite = pygame.transform.scale(self.chicken_sprite, (30, 40))

    def draw(self, screen):
        screen.blit(self.chicken_sprite, self.position)
    
    def get_right(self):
        return self.position.x + 30

    def get_left(self):
        return self.position.x 
    
    def get_top(self):
        return self.position.y
    
    def get_bottom(self):
        return self.position.y + 40
    


class Enemy:
    global frame
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
        self.position.y += self.gravity_scale * frame
    
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
        
    #How many single pieces of ammo are spawned in the game from the refill class
    def populate_refill(self):
        self.refills = []
        for _ in range(3):
            pos = Vector2()
            pos.x = random.randint(100, 700)
            pos.y = random.randint(100, 500)
            refill = Refill(pos)
            self.refills.append(refill)
    #How many enemies are spawned in the game in a random order
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
        
        #The whole game
        while not is_menu:
            self.handle_frame()
            self.clear_screen()

            self.player.chicken.render_current_ammo(screen)
            
            self.level_builder.draw(screen)
            self.level_builder.draw(screen)
            self.player.move()
            self.player.handle_chicken()
            
            
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
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.player.shoot()      
                    self.player.chicken.shoot() 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:   
                        self.player.shoot()      
                        self.player.chicken.shoot()  
                
                        
                        

    def clear_screen(self):
        self.screen.fill(self.background_color)

    def handle_frame(self):
        #amount of frames, frame rate
        global frame
        frame = self.clock.tick() / 1000


class Menu():
    def __init__(self, screen):
        self.background_color = 240, 240, 240
        self.screen = screen
        self.update()

    def update(self):
        global is_menu
        pygame.font.init()
    

        while is_menu:
            #Menu screen set up
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
                


#Checks if the menu is active
instance = None
while True:
    if is_menu:
        instance = Menu(screen)
    else:
        instance = Game(screen)
    print(is_menu)
    