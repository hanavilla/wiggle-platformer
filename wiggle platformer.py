# Imports
import pygame
import random
import json


# Window settings
GRID_SIZE = 64
WIDTH = 23 * GRID_SIZE
#1380
HEIGHT = 12 * GRID_SIZE
#720
TITLE = "Platformer"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (88, 93, 99)
LIGHT_GRAY = (175, 175, 175)

# Stages
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3
WIN = 4

# Load fonts
font_xl = pygame.font.Font('assets/fonts/Sketchy.otf', 115)
font_lg = pygame.font.Font('assets/fonts/Sketchy.otf', 64)
font_md = pygame.font.Font('assets/fonts/Sketchy.otf', 32)
font_xs = pygame.font.Font(None, 14)

# Load images
hero_idle_imgs_rt = [pygame.image.load('assets/images/characters/alien/alienBeige_stand.png').convert_alpha()]
hero_walk_imgs_rt = [pygame.image.load('assets/images/characters/alien/alienBeige_walk1.png').convert_alpha(),
                    pygame.image.load('assets/images/characters/alien/alienBeige_walk2.png').convert_alpha()]
hero_jump_imgs_rt = [pygame.image.load('assets/images/characters/alien/alienBeige_jump.png').convert_alpha()]
hero_idle_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_idle_imgs_rt]
hero_walk_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_walk_imgs_rt]
hero_jump_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_jump_imgs_rt]
slime_imgs_rt = [pygame.image.load('assets/images/characters/enemies/moreenemies/slime.png').convert_alpha(),
                 pygame.image.load('assets/images/characters/enemies/moreenemies/slime_walk.png').convert_alpha()]
slime_imgs_lt = [pygame.transform.flip(img, True, False) for img in slime_imgs_rt]

wingman_imgs_rt = [pygame.image.load('assets/images/characters/enemies/wingMan1.png').convert_alpha(),
                pygame.image.load('assets/images/characters/enemies/wingMan2.png').convert_alpha(),
                pygame.image.load('assets/images/characters/enemies/wingMan3.png').convert_alpha(),
                pygame.image.load('assets/images/characters/enemies/wingMan4.png').convert_alpha(),
                pygame.image.load('assets/images/characters/enemies/wingMan5.png').convert_alpha()]
wingman_imgs_lt = [pygame.transform.flip(img, True, False) for img in wingman_imgs_rt]

dirt_img = pygame.image.load('assets/images/PNG/tiles/dirt.png').convert_alpha()
block_img = pygame.image.load('assets/images/PNG/tiles/stone_block.png').convert_alpha()
doortop_img = pygame.image.load('assets/images/PNG/tiles/door_top.png').convert_alpha()
door_img = pygame.image.load('assets/images/PNG/tiles/door.png').convert_alpha()
grass_dirt = pygame.image.load('assets/images/PNG/tiles/grass_dirt.png').convert_alpha()
gold_img = pygame.image.load('assets/images/PNG/items/gold_1.png').convert_alpha()
bronze_img = pygame.image.load('assets/images/PNG/items/bronze_1.png').convert_alpha()
heart_img = pygame.image.load('assets/images/PNG/items/heart.png').convert_alpha()
gem_img = pygame.image.load('assets/images/HUD/coin_gold.png').convert_alpha()
bg_img = pygame.image.load('assets/images/background/backgroundColorForest.png').convert_alpha()

# Load sounds
jump_snd = pygame.mixer.Sound('assets/sounds/jump.wav')
gem_snd = pygame.mixer.Sound('assets/sounds/obtained_coin.ogg')
level_up_snd = pygame.mixer.Sound('assets/sounds/level_complete.ogg')
hurt_snd = pygame.mixer.Sound('assets/sounds/hurt.ogg')
lose_snd = pygame.mixer.Sound('assets/sounds/lose.ogg')
win_snd = pygame.mixer.Sound('assets/sounds/win.ogg')

# Load Music
intro = 'assets/music/intro.ogg'


# Levels
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json']

# Game classes
class Entity(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2

        self.vx = 0
        self.vy = 0

    def apply_gravity(self):
        self.vy += gravity

        if self.vy > terminal_velocity:
            self.vy = terminal_velocity


class AnimatedEntity(Entity):

    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.animation_speed = 10

    def set_image_list(self):
        self.images = self.images
        
    def animate(self):
        self.set_image_list()
        self.ticks += 1

        if self.ticks % self.animation_speed == 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]
        

class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Flag(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Hero(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.speed = 5
        self.jump_power = 13
        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.jumping = False

        self.hearts = 3
        self.gold_coins = 0
        self.bronze_coins = 0
        self.score = 0

        self.hurt_timer = 0

    def move_to(self, x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2
       
    def move_right(self):
    	self.vx = self.speed
    	self.facing_right = True
    	
    def move_left(self):
    	self.vx = -self.speed
    	self.facing_right = False

    def stop(self):
        self.vx = 0
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(hits) > 0:
            self.vy = -1 * self.jump_power
            self.jumping = True
            jump_snd.play()

    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
                self.jumping = False
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > world_width:
            self.rect.right = world_width
        elif self.rect.top > HEIGHT:
            self.hearts = 0
            print( "RIP: hardcore parkour" )

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)
            
    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in hits:
            if self.hurt_timer == 0:
                self.hearts -= 1
                self.hurt_timer = 1.0 * FPS
                print( 'hearts = ' + str(self.hearts) )
                hurt_snd.play()

            if self.rect.centerx < enemy.rect.centerx:
                self.vx = -5
            elif self.rect.centerx > enemy.rect.centerx:
                self.vx = 5
            if self.rect.centery < enemy.rect.centery:
                self.vy = -5
            elif self.rect.centery > enemy.rect.centery:
                self.vy = 5


            if self.hearts == 0:
                self.kill()
                print("RIP: death by enemy")    


        self.hurt_timer -= 1

        if self.hurt_timer < 0:
            self.hurt_timer = 0

    def check_portals(self):
        pass

    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)

    def set_image_list(self):
        if self.facing_right:
            if self.jumping:
                self.images = hero_jump_imgs_rt
            elif self.vx == 0:
                self.images = hero_idle_imgs_rt
            else:
                self.images = hero_walk_imgs_rt
        else:
            if self.jumping:
                self.images = hero_jump_imgs_lt
            elif self.vx == 0:
                self.images = hero_idle_imgs_lt
            else:
                self.images = hero_walk_imgs_lt
        
    def update(self):
        self.apply_gravity()
        self.check_world_edges()
        self.check_items()
        self.check_enemies()
        self.check_portals()
        self.move_and_check_platforms()
        self.reached_goal()
        self.animate()
        
class Currency(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Gold(Currency):
    def apply(self, character):
        character.gold_coins += 1
        print( 'gold coins = ' + str(character.gold_coins) )
        character.score += 10
        gem_snd.play()

class Bronze(Currency):
    def apply(self, character):
        character.bronze_coins += 1
        print( 'bronze coins = ' + str(character.bronze_coins) )
        character.score += 20
        gem_snd.play()

class Enemy(AnimatedEntity):

    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.vx = -2
        self.vy = 0

    def reverse(self):
        self.vx *= -1
        
    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.reverse()

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.reverse()
        elif self.rect.top > HEIGHT:
            self.kill()
        
    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y  -= 2

        must_reverse = True

        for platform in hits:
            if self.vx <= 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx >= 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()

class Slime(Enemy):

    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
        self.speed = 2
        self.vx = -1 * self.speed
        self.vy = 0

    def set_image_list(self):
        if self.vx > 0:
            self.images = slime_imgs_lt
        else:
            self.images = slime_imgs_rt
    
    def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_platform_edges()
        self.animate()

class FlyMan(Enemy):

    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        self.animation_speed = 8

        self.speed = 5
        self.vx = -1 * self.speed
        self.vy = 0

    def set_image_list(self):
        if self.vx > 0:
            self.images = wingman_imgs_lt
        else:
            self.images = wingman_imgs_rt

    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()


# Helper Functions
def show_start_screen():
    text = font_xl.render(TITLE, True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)
    
    text = font_lg.render('Press any key to start', True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)


def show_lose_screen():
    text = font_xl.render('GAME OVER', True, WHITE)

    # hi Hannah it me Kuya
    kuya = font_xl.render('HEEEEEY', True, BLACK)
    
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)
    
    text = font_lg.render("Press 'R' to play again", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_win_screen():
    text = font_xl.render('You Win!', True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)
    
    text = font_lg.render("Press 'R' to play again", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_level_complete_screen():
    text = font_xl.render('Level complete!', True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_hud():
    text = font_md.render( str(hero.score), True, WHITE )
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 16
    screen.blit(text, rect)

    screen.blit(gem_img, [WIDTH - 100, 27]) 
    text = font_md.render('x' + str(hero.gold_coins), True, WHITE )
    rect = text.get_rect()
    rect.topleft =  WIDTH - 60, 24
    screen.blit(text, rect)

    for i in range(hero.hearts):
        x = i * 36
        y = 16
        screen.blit(heart_img, [x, y])

def show_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, LIGHT_GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, LIGHT_GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, LIGHT_GRAY)
            screen.blit(text, [adj_x, adj_y])


# Setup
def start_game():
    global hero, stage, current_level

    hero = Hero(0, 0, hero_idle_imgs_rt)
    stage = START
    current_level = 0
    
    

def start_level():
    global platforms, items, enemies, player, goal, all_sprites
    global gravity, terminal_velocity
    global world_width, world_height

    
    platforms = pygame.sprite.Group()
    items = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()
    goal = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    with open(levels[current_level]) as f:
        data = json.load(f)

    world_width = data['width'] * GRID_SIZE
    world_height = data['height'] * GRID_SIZE

    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)

    for i, loc in enumerate(data['flag_locs']):
        if i == 0:
            goal.add( Flag(loc[0], loc[1], doortop_img) )
        else:
            goal.add( Flag(loc[0], loc[1], door_img) )

    for loc in data['grass_locs']:
        platforms.add( Platform(loc[0], loc[1], grass_dirt) )

    for loc in data['block_locs']:
        platforms.add( Platform(loc[0], loc[1], block_img) )

    for loc in data['dirt_locs']:
        platforms.add( Platform(loc[0], loc[1], dirt_img) )

    for loc in data['gold_locs']:
        items.add( Gold(loc[0], loc[1], gold_img) )

    for loc in data['spikeman_locs']:
        enemies.add( Slime(loc[0], loc[1], slime_imgs_lt) )

    for loc in data['flyman_locs']:
        enemies.add( FlyMan(loc[0], loc[1], wingman_imgs_rt) )


    gravity = data['gravity']
    terminal_velocity = data['terminal_velocity']

    all_sprites.add(player, platforms, items, enemies, goal)

    if stage == START:
        theme = 'assets/music/intro.ogg' # starting theme
    elif stage == PLAYING:
        theme = 'assets/music/theme.ogg' # running theme
    elif stage == LEVEL_COMPLETE:
        theme = 'assets/music/theme.ogg' # ending theme I guess 

    pygame.mixer.music.load(theme)
    pygame.mixer.music.play(-1)
    
# Game loop
play_lose_sound = True
play_win_sound = True
running = True
grid_on = False
earn_points = True

start_game()
start_level()


while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                grid_on = not grid_on
                
            elif stage == START:
                stage = PLAYING
                theme = 'assets/music/theme.ogg' # running theme

                pygame.mixer.music.load(theme)
                pygame.mixer.music.play(-1)
                
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    hero.jump()
                elif event.key == pygame.K_UP:
                    hero.jump()
                elif event.key == pygame.K_w:
                    hero.jump()

            elif stage == LOSE:
                if event.key == pygame.K_r:
                    start_game()
                    start_level()
                    play_lose_sound = False
                    earn_points = True

            elif stage == WIN:
                if event.key == pygame.K_r:
                    start_game()
                    start_level()
                    play_win_sound = False
                    earn_points = True
                    

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            hero.move_left()
        elif pressed[pygame.K_a]:
            hero.move_left()
            
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        elif pressed[pygame.K_d]:
            hero.move_right()
            
        else:
            hero.stop()
   
    # Game logic
    if stage == PLAYING:
        all_sprites.update()

        if hero.hearts == 0:
            stage = LOSE
        elif hero.reached_goal():
            stage = LEVEL_COMPLETE
            countdown = 3 * FPS
            pygame.mixer.music.stop()
            level_up_snd.play()
    elif stage == LEVEL_COMPLETE:
        countdown -= 1
        if countdown <= 0:
            current_level += 1

            if current_level < len(levels):
                start_level()
                stage = PLAYING
            else:
                stage = WIN

        if earn_points == True:
            hero.score += 100
            earn_points = False
    

    if hero.rect.centerx < WIDTH // 2:
        offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH // 2:
        offset_x = world_width - WIDTH
    else:
        offset_x = hero.rect.centerx - WIDTH // 2
    
    bg_offset_x = -1 * (0.05 * offset_x % bg_img.get_width())


    # Drawing code
    screen.blit(bg_img, [bg_offset_x, 0])
    screen.blit(bg_img, [bg_offset_x + bg_img.get_width(), 0])
        
    for sprite in all_sprites:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])
        
    show_hud()

    if grid_on:
        show_grid(offset_x)

    if stage == START:
        screen.fill(GRAY)
        show_start_screen()
    elif stage == LOSE:
        
        screen.fill(BLACK)
        show_lose_screen()
        pygame.mixer.music.stop()

        if play_lose_sound == True:
            lose_snd.play()
            play_lose_sound = False

            
    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()
    elif stage == WIN:
        show_win_screen()

        if play_win_sound == True:
            win_snd.play()
            play_win_sound = False


    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

