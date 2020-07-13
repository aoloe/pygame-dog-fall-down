import pygame
import random
import time
from pygame.mixer import Sound

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_SPACE,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def make_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()  
        
def stop_sound():
    pygame.mixer.music.stop()

def show_go_screen():
    #screen.blit(background, background_rect)
    screen.fill((0, 0, 0))
    #draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, "GAME OVER", 90,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30)
    #draw_text(screen, "press any key - naciśnij klawisz", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    #draw_text(screen, "naciśnij klawisz", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4 + 20)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (250, 250, 250))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y
        surf.blit(img, img_rect)    
        
def draw_score(surf, x, y, wins, img):
    for i in range(wins):
        img_rect = img.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y 
        surf.blit(img, img_rect) 


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.original_image = pygame.image.load("chmurka.png")
        self.size = self.original_image.get_size()
        self.surf = pygame.transform.scale(self.original_image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        #self.rect.top = 0
        #self.rect.centerx = 0
        
    #def platform_moves_up(self):
        #self.rect.move_ip(0, -2)

class Meadow(pygame.sprite.Sprite):
    def __init__(self):
        super(Meadow, self).__init__()
        self.original_image = pygame.image.load("meadow.png")
        self.size = self.original_image.get_size()
        self.surf = pygame.transform.scale(self.original_image, (int(self.size[0]/4), int(self.size[1]/4)))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2))
        
    #def level_moves_up(self):
        
        #self.rect.move_ip(0, +2)
        #if self.rect.top > SCREEN_HEIGHT:
            #transitioning = False
            #self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load('PinClipart.com_corgi-clip-art_2877425.png')
        self.size = self.original_image.get_size()
        self.image_unflipped = pygame.transform.scale(self.original_image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.surf = pygame.transform.scale(self.original_image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.rect = self.surf.get_rect()
        self.rect.bottom = SCREEN_HEIGHT 
        self.rect.centerx = SCREEN_WIDTH / 2
        self.image_flipped = pygame.transform.flip(self.image_unflipped, True, False)
        self.moving_left = False
        self.moving_right = False
        self.speed = 8
        self.time = 0
        #self.time_start = global_time
        self.time_duration = 1500 #1 sec in ms
        self.dt = clock.tick(50)
        self.is_jump = False
        #self.is_bark = True
        #self.is_outch = True
        self.jump_count = 15
        self.mini_img = pygame.transform.scale(self.original_image, (int(self.size[0]/10), int(self.size[1]/10)))
        self.lives = 5
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.knochen = pygame.image.load("knochen_kleiner.png")
        self.mini_food = pygame.transform.scale(self.knochen, (int(self.size[0]/10), int(self.size[1]/19)))#.convert()
        #self.black = (0, 0, 0)
        #self.mini_food.set_colorkey(self.black)
        self.wins = 0
        self.current_level = int(self.wins / 5)
        
        
        
        
        
        
    def update(self, pressed_keys):

        if self.current_level == 0:
            self.rect.bottom = SCREEN_HEIGHT
          
        keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT] and not transitioning:
            self.rect.bottom = SCREEN_HEIGHT
            self.rect.move_ip(-self.speed, 0)
            self.surf = self.image_flipped
            self.moving_left = True
            
        if pressed_keys[K_RIGHT] and not transitioning:
            self.rect.bottom = SCREEN_HEIGHT
            self.rect.move_ip(self.speed, 0)
            self.surf = self.image_unflipped
            self.moving_right = True
        
        if not(self.is_jump): 

            if pressed_keys[K_SPACE] and not transitioning:
                make_sound("bark_h.wav")
                self.jump_count = 15
                self.is_jump = True
        else: # Diese ganze Jump-Funktion kommt offenbar nicht ohne self.rect.bottom = SCREEN_HEIGHT in 139 aus :(
            if self.jump_count >= -15:
                self.rect.move_ip(0, self.jump_count * abs(self.jump_count) * 0.5)
                self.jump_count -= 3
            else: 
                self.is_jump = False          

        # Keep the player on the screen and flip according to direction
        if self.moving_left and self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
            #self.surf = self.image_unflipped
        elif self.moving_right and self.rect.left >= SCREEN_WIDTH:
            self.rect.right = 0
            #self.surf = self.image_flipped
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        doniczka = random.choice(("doniczka_1.png", "doniczka_2.png", "doniczka_3.png", "doniczka_4.png", "kitty.png"))
        self.original_image = pygame.image.load(doniczka)
        self.size = self.original_image.get_size()
        self.surf = pygame.transform.scale(self.original_image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(50, SCREEN_WIDTH-50),
                random.randint(-400, -200),
            )
        )

        self.speed = random.randint(8, 15)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, +self.speed)
        if self.rect.bottom > SCREEN_HEIGHT+150:
            self.kill()

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        jedzonko = random.choice(("wurst2000.png", "knochen_mittel.png"))
        self.original_image = pygame.image.load(jedzonko)
        self.size = self.original_image.get_size()
        self.surf = pygame.transform.scale(self.original_image, (int(self.size[0]/3), int(self.size[1]/3)))
        #self.rect = self.surf.get_rect(topleft=(random.randrange(0,SCREEN_WIDTH-80),400))
        
        self.rect = self.surf.get_rect(
            center=(
                random.randint(80, SCREEN_WIDTH - 80),
                random.randint(SCREEN_HEIGHT/2, SCREEN_HEIGHT + 100),
            )
        )
        
        self.time_start = global_time
        self.time_duration = 2500 #sec in ms
        
    # Makes food wibble
    def update(self):
        self.rect.move_ip(random.randint(-1, 2), 0)
        
        if global_time > self.time_start + self.time_duration:
            self.kill()
            
        #elif pygame.sprite.spritecollideany(player, foods):
            #make_sound("bite.wav")
            #self.kill()
            
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.original_image = pygame.image.load("chmurka.png")
        self.size = self.original_image.get_size()
        self.surf = pygame.transform.scale(self.original_image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 200),
                random.randint(0, SCREEN_HEIGHT-300),
            )
        )

    # Move cloud and remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()
            
# Setup the clock for a decent framerate
clock = pygame.time.Clock()   

# Initialize pygame
pygame.init()

#Initialize sounds
pygame.mixer.init()

# Set global time
global_time = 0



# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1300)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 2700)
ADDFOOD = pygame.USEREVENT + 3
pygame.time.set_timer(ADDFOOD, 4900)


# Instantiate player and background
meadow = Meadow()
player = Player()


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
foods = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(meadow)
all_sprites.add(player)

# Decorator to execute a function within the while loop only once
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper
 
# The decorated level_up function
@run_once
def level_up():
    make_sound("auuuuu.ogg")
    platform = Platform()
    all_sprites.add(platform)
    player.surf = player.image_unflipped
    player.rect.bottom = platform.rect.top
    player.rect.centerx = platform.rect.centerx
    #print(player.current_level)
    player.current_level += 1
    #print(player.current_level)


    
    
# Main loop
game_over = False
transitioning = False
platform_created = False
running = True

while running:
    
    if transitioning:
        
        action = run_once(level_up)
        action() # run once the first time
        player.lives = 5
        meadow.rect.move_ip(0, +2)
        all_sprites.remove()
        if meadow.rect.top > SCREEN_HEIGHT:
            meadow.kill()
            transitioning = False
  
    elif game_over:
        make_sound("sad_trombone.wav")
        show_go_screen()
        game_over = False # WHY?
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        foods = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        player = Player()
        meadow = Meadow()
        all_sprites.add(meadow)
        all_sprites.add(player)
        player.wins = 0
    if player.lives == -1:
        game_over = True

    else:
        dt = clock.tick(50)
        global_time += dt        
     
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
    
        # Add a new enemy?
        elif event.type == ADDENEMY and not transitioning:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)    
            
        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            
        # Add a new food?
        elif event.type == ADDFOOD and not transitioning:
            # Create the new cloud and add it to sprite groups
            new_food = Food()
            foods.add(new_food)
            all_sprites.add(new_food)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    # Update enemy position
    enemies.update()
    foods.update()
    clouds.update()

    
    # Fill the screen with blue
    screen.fill((178, 211, 235))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    draw_lives(screen, SCREEN_WIDTH - 240, 5, player.lives, player.mini_img)
    draw_score(screen, 20, 5, player.wins, player.mini_food)
        
    # Check if any enemies have collided with the player, remove enemy, subtract player life
    if pygame.sprite.spritecollide(player, enemies, dokill=True, collided = None) and not transitioning:
        make_sound("Computer Error Alert-SoundBible.com-783113881.wav")
        player.lives -=1
        
        #make_sound("fail.wav")
        #pygame.time.delay(1500) 
        pygame.time.wait(1500)
        
    if pygame.sprite.spritecollide(player, foods, dokill=True, collided = None) and not transitioning:
        player.wins +=1
        make_sound("bite.wav")
    
    
    if player.wins == 1:
        transitioning = True
        
    # If so, then remove the player and stop the loop
    if player.lives == -1:
        game_over = True

        #player.kill()
        #make_sound("sad_trombone.wav")
        #pygame.time.wait(4500)
        #running = False
    
    #if player.wins == 1:
        #player.lives = 5
        #make_sound("bark_h.wav")
        
        
    # Update the display (show the new frame)
    pygame.display.flip()
    
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(50)
    
    