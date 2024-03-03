import pygame, random,  os,  math
pygame.init()  #initialize pygame library
#initialization of global variables
game_speed = 15
score = 0
x_pos_background = 0 
y_pos_background = 380
x_pos_foreground = 0
y_pos_foreground = 500

font = pygame.font.SysFont('arial', 24)
obstacles = []
socks_list = []
collected_socks = 0


# define the RGB value for white purple
white = (255, 255, 255)
purpleL = (51, 0, 102)
purpleD = (229, 204, 255)

#Begging of first block
#THE screen
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
###############
#images
running = [pygame.image.load(os.path.join("images", "james1.png")),
           pygame.image.load(os.path.join("images", "james2.png"))]

jumping = [pygame.image.load(os.path.join("images", "james.jump.png"))]

ducking = [pygame.image.load(os.path.join("images", "james.duck.png"))]

randall = [pygame.image.load(os.path.join("images", "obstacle.2.png"))]

roz = [pygame.image.load(os.path.join("images", "obstacle.3.png"))]

art = [pygame.image.load(os.path.join("images", "obstacle.1.png"))]

fly = [pygame.image.load(os.path.join("images", "high.png"))]

socks = [pygame.image.load(os.path.join("images", "pick.1.png")),
        pygame.image.load(os.path.join("images", "pick.2.png"))]

background = [pygame.image.load(os.path.join("images", "doors.png"))]

foreground = [pygame.image.load(os.path.join("images", "houses.png"))]

pixarCloud = [pygame.image.load(os.path.join("images", "pixarCloud.png"))]

bgMenu = [pygame.image.load(os.path.join("images", "bgMenu.jpeg"))]
#End of first block
#DOCUMENTATION# 
#initial imports and pygame initializations are here, they are self-explanatory



#Begging of second block
class PixarCloud:
#DOCUMENTATION# 
#cloud object that moves across the screen at game_speed and resets after passing the screen  
    def __init__(self):
        self.x = screen_width + random.randint (300,800)
        self.y = random.randint (50,200)
        self.image = pixarCloud[0]
        self.width = self.image.get_width()

    def update (self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint (300,800)
            self.y = random.randint (50,200)

    def draw (self, screen):
        screen.blit (self.image, (self.x, self.y))

class James:
#DOCUMENTATION# 
#player's character class with methods for running, jumping, and ducking animations
    x_pos = 80 #coordinates
    y_pos = 310
    y_pos_duck = 320
    JUMP_VALUE = 22 

    def __init__ (self):
        self.jump_img = jumping
        self.duck_img = ducking 
        self.run_img = running
    
        self.jump = False
        self.duck = False
        self.run = True

        self.step_index = 0
        self.jump_value = self.JUMP_VALUE
        self.image = self.run_img[0]
        self.james_rect = self.image.get_rect()
        self.james_rect.x = self.x_pos
        self.james_rect.y = self.y_pos

    def run_animation(self):
        self.image = self.run_img[self.step_index // 5]
        self.james_rect = self.image.get_rect()
        self.james_rect.x = self.x_pos
        self.james_rect.y = self.y_pos
        self.step_index += 1 #is incremented for the next frame of the animation.
    def jump_animation(self):
        self.image = self.jump_img[0]
        if self.jump:
            self.james_rect.y -= self.jump_value 
            self.jump_value -= 1.3 #amortizatia
        if self.jump_value < - self.JUMP_VALUE:
            self.jump = False
            self.jump_value = self.JUMP_VALUE
    def duck_animation(self):
        self.image = self.duck_img[0]
        self.james_rect = self.image.get_rect()
        self.james_rect.x = self.x_pos
        self.james_rect.y = self.y_pos_duck
        self.step_index += 1 

#james  update logic
    def update (self, userInput, obstacles): #state of James
        if userInput[pygame.K_UP] and not self.jump:  #check for jump and make sure not already jumping
            self.jump = True
            self.duck = False
            self.run = False
        elif userInput[pygame.K_DOWN] and not self.jump:
            if any(isinstance(obstacle, Fly) for obstacle in obstacles): #check if the current obstacle is a "fly" type, and force duck if true
                self.duck = True
                self.jump = False
                self.run = False
        elif not self.jump and not userInput[pygame.K_DOWN]:
            self.run = True
            self.duck = False
            self.jump = False
#james animation update
        if self.jump:
            self.jump_animation()
        elif self.duck:
            self.duck_animation()
        else:
            self.run_animation()

        if self.step_index >= 10:  # reset each 10 steps
            self.step_index = 0
            #s incremented each time the update method is called, and when it reaches a value of 10, it is reset back to 0. 


    def draw (self, screen):
        screen.blit(self.image, (self.james_rect.x, self.james_rect.y))
###########################OBSTACLE#########################
class Obstacles:
#DOCUMENTATION# 
#generic Obstacle superclass used as a template for specific obstacle types

    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        #if self.rect.x < -self.rect.width:
            # obstacles.pop()


    def draw (self, screen):
        screen.blit (self.image, self.rect)

#DOCUMENTATION# 
#subclass for different obstacles with variations and specific behavior
class Randall(Obstacles):
#DOCUMENTATION# 
#Randall obstacle initialized at a random type and y-position
    def __init__(self):
        self.type = random.randint(0,3)
        super ().__init__(randall[0])
        self.rect.y = 330

class Roz(Obstacles):
#DOCUMENTATION# 
 #Roz obstacle, shares behavior with Randall 
    def __init__(self):
        self.type =random.randint(0,3)
        super ().__init__(roz[0])
        self.rect.y = 330

class Art(Obstacles):
#DOCUMENTATION# 
#Art obstacle, similar to Randall and Roz
    def __init__(self):
        self.type =random.randint(0,3)
        super ().__init__(art[0])
        self.rect.y = 350

class Fly(Obstacles):
#DOCUMENTATION# 
#Fly obstacle with a sine wave movement pattern to vary game difficulty
    def __init__(self):
        self.type =0
        super ().__init__(fly[0])
        self.rect.y = 318 #starting y position
        self.fly_count = 0  #count for the sine wave

    def update(self):
        super().update()  #this will move the Fly to the left (call the update function from the superclass)
        self.fly_count += 1  #increment count
        wave_amplitude = 17  #  waves
        self.rect.y = 237 + math.sin(self.fly_count * 0.1) * wave_amplitude  #calculates the new y-position of the object based on a sine wave function
#A smaller multiplier (0.1 in this case) will result in a slower wave.

    def draw(self, screen):
        self.image = fly[0]
        screen.blit(self.image, self.rect)
###########################OBSTACLE######################### 


class Socks(Obstacles):#inherit from Obstacles or create a new base class if the mechanics are different
 #DOCUMENTATION# 
#Socks collectible items that provide the player with extra points     
    def __init__(self):
        self.type = random.choice([0, 1])  #alegi ciorapii diferit
        self.image = socks[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = screen_width + random.randint(300, 800)  #distance from the right-hand side of the screen
        self.rect.y = random.randint(100, 320) 

    def update(self):
        self.rect.x -= game_speed  #  to move the socks at the same speed as the obstacles
        if self.rect.x < -self.rect.width:  #check if off screen; remove from list if true
            socks_list.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def spawn_socks():
#DOCUMENTATION# 
#Function to occasionally spawn socks collectibles onto the screen
    # randomly add a sock to the game if there are fewer than 1 on the screen
    if len(socks_list) < 1 and random.randint(0, 200) == 10:
        socks_list.append(Socks())
#End of second block
        
#Begging of third block
        

#meniul central
def menu():
#DOCUMENTATION# 
# menu screen of  the game that displays after launch and after game over
    global score, font, bgMenu, collected_socks
    running = True
    background_menu = bgMenu[0]
    background_menu = pygame.transform.scale(background_menu, (screen_width, screen_height))  #scale the image to match the screen size
    while running:
        screen.fill((255, 255, 255))
        screen.blit(background_menu, (0, 0))  #top-left corner of the screen
        if score == 0:
            text_surface = font.render("Press any button to start", True, purpleL, purpleD)
        else:
            
            text_surface = font.render(f'Press any button to restart. Your score was {score}. You managed to collect {collected_socks} pairs of socks', True, purpleL, purpleD)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.quit()  
                return
            if event.type == pygame.KEYDOWN:
                score = 0  # restart la scor inainte de un nou joc
                obstacles.clear()
                main()  


def main():
#DOCUMENTATION# 
#main game loop handling game state, background/foreground movement, and event processing
    global game_speed
    global x_pos_background
    global y_pos_background
    global score
    global obstacles
    global font
    global socks_list
    global bgMenu
    global collected_socks
    global x_pos_foreground
    global y_pos_foreground
##############################

    # Reset game state
    game_speed = 15
    x_pos_background = 0
    y_pos_background = 420
    x_pos_foreground = 0
    y_pos_foreground = 111
    score = 0
    obstacles = []
    clock = pygame.time.Clock()
    player = James()
    pixar_cloud = PixarCloud()

    obstacle_classes = [Randall, Roz, Art, Fly]
    spawn_rate = 100
    obstacles_spacing = 370 
    score_after_death = 0
##############################

##############################
    def Score():
#DOCUMENTATION# 
# Score handling function. Increases score and difficulty as game progresses
        global game_speed, score
        score += 1
        if score % 200 == 0:
            game_speed +=1
        text = font.render("Your score: " + str(score), True, purpleL, purpleD)
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit (text, textRect)
##############################
  

##############################
    def Background ():
#DOCUMENTATION# 
# rendering functions for the scrolling backgrounds and foregrounds
        global x_pos_background, y_pos_background
        image_width = background[0].get_width()
        screen.blit (background[0], (x_pos_background, y_pos_background))
        screen.blit (background[0], (image_width + x_pos_background, y_pos_background))
        if x_pos_background <= -image_width:
            x_pos_background += image_width
        x_pos_background -= game_speed
##############################
    def Foreground():
        global x_pos_foreground, y_pos_foreground
        image_width = foreground[0].get_width()
        screen.blit(foreground[0], (x_pos_foreground, y_pos_foreground))
        screen.blit(foreground[0], (image_width + x_pos_foreground, y_pos_foreground))
        if x_pos_foreground <= -image_width:
            x_pos_foreground += image_width
        x_pos_foreground -= game_speed
  

##############################
    last_obstacle = None
    running = True
#DOCUMENTATION# 
# Main game loop starting here:
    while running:
#DOCUMENTATION# 
#event processing loop, detecting key presses and quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #for button exit window
                running = False
        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
#DOCUMENTATION# 
 # update and draw each component of the game
        pixar_cloud.draw(screen) #function
        pixar_cloud.update()

        Background() #function
        Foreground() #function
#DOCUMENTATION# 
    # player character animation and movement logic
        player.draw (screen) #player update
        player.update (userInput, obstacles) #pt racheta ultimul 

#DOCUMENTATION# 
# obstacle spawning logic. Determines when a new obstacle is created based on a random condition
        if (len(obstacles) == 0 or
            (random.randint(0, spawn_rate) == 0 and
            last_obstacle and
            (last_obstacle.rect.x + last_obstacle.rect.width + obstacles_spacing < screen_width))):
            obstacle_choice = random.choice(obstacle_classes)()  #added () to instantiate the obstacle
            obstacles.append(obstacle_choice)  
            last_obstacle = obstacle_choice

        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw(screen)
            if player.james_rect.colliderect(obstacle.rect):
#DOCUMENTATION# 
    # collision detection between player and obstacles. Ends the game if collision occurs
                # Detected collision
                running = False
                pygame.time.delay(2000) #end the game loop, effectively ending the game
                score_after_death += 1
                menu()
        spawn_socks()  #call this function to potentially add socks to the game

        for sock in socks_list[:]:  #make sure to iterate over a copy of the list
            sock.update()
            sock.draw(screen)
            if player.james_rect.colliderect(sock.rect):  #check for collision with James
                score += 10  
                collected_socks += 1
                socks_list.remove(sock)  #remove the sock from the game
##############################




        Score () #function
#DOCUMENTATION# 
#   control the frame rate to be consistent across different hardware
        clock.tick(30)  
#DOCUMENTATION# 
# update the display with everything that's been drawn
        pygame.display.update()
    pygame.quit()
#end of third block

menu()
