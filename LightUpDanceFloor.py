import pygame
import random

# Initialize Pygame
pygame.init()

# Constants

# Looks into and auto resizing as monitor size may change
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create score variable used for leaderboard
score = 0

# Setup the window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dance Dance Revolution Game")
clock = pygame.time.Clock()

# Load arrow images
# Remember to replace images with more cut out once so they do not look clean
arrow_imgs = {
    'UP': pygame.transform.scale(pygame.image.load('up.png'), (50, 50)),
    'DOWN': pygame.transform.scale(pygame.image.load('down.png'), (50, 50)),
    'LEFT': pygame.transform.scale(pygame.image.load('left.png'), (50, 50)),
    'RIGHT': pygame.transform.scale(pygame.image.load('right.png'), (50, 50))
}

# Positions for arrows
x_positions = {
    'UP': WIDTH // 2 - 100,
    'DOWN': WIDTH // 2 - 50,
    'LEFT': WIDTH // 2,
    'RIGHT': WIDTH // 2 + 50
}

# Shadow arrows at a fixed position
# Remember to change the shadow arrows to a greyed/blacked out shadow, contrast to the background
# Gives people a marker for they to try and hit within that range to get points. 
shadow_arrows = [
    (x_positions['UP'], 50, 'UP'),
    (x_positions['DOWN'], 50, 'DOWN'),
    (x_positions['LEFT'], 50, 'LEFT'),
    (x_positions['RIGHT'], 50, 'RIGHT')
]

# Difficulty settings (Will update, especially during LED testing.)
difficulty_settings = {
    'Easy': (3, 2000),  # Speed, spawn interval in milliseconds
    'Medium': (5, 1500),
    'Hard': (7, 1000)
}

# Choose difficulty
def choose_difficulty():
    print("Choose Difficulty: Easy, Medium, Hard")
    while True:
        choice = input("Enter difficulty: ").capitalize()
        if choice in difficulty_settings:
            return difficulty_settings[choice]
        print("Invalid choice. Please choose 'Easy', 'Medium', or 'Hard'.")

arrow_speed, spawn_interval = choose_difficulty()
arrows = []
last_spawn_time = 0

def spawn_arrow(current_time):
    if current_time - last_spawn_time > spawn_interval:
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        arrows.append([x_positions[direction], HEIGHT, direction])
        return current_time
    return last_spawn_time

def move_arrows():
    for arrow in arrows[:]:
        arrow[1] -= arrow_speed
        if arrow[1] < 0:
            arrows.remove(arrow)
            print("Miss")

def draw():
    win.fill(BLACK)
    # Draw shadow arrows
    for shadow in shadow_arrows:
        win.blit(arrow_imgs[shadow[2]], (shadow[0], shadow[1]))
    # Draw moving arrows
    for arrow in arrows:
        win.blit(arrow_imgs[arrow[2]], (arrow[0], arrow[1]))

    font = pygame.font.SysFont(None, 25) 
    score_text = font.render('Score: ' + str(score), True, WHITE) 
    win.blit(score_text, (WIDTH - 200, 20))
    pygame.display.update()



# Will need to change when adding Main menu/other screens. (Settings, Song choice, etc.)
# Main game loop
running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if the key pressed corresponds to the arrow at the shadow
            for arrow in list(arrows):  # Create a copy of the list to modify while iterating
                if arrow[1] - 50 <= 50 <= arrow[1] + 50:  # Check if within hit range                   # Right here, might want to call function called 'hit" 
                                                                                                        # Will allow us to use a call instead and also be better when 
                                                                                                        # implementing a scoreboard
                    if (event.key == pygame.K_UP and arrow[2] == 'UP') or \
                       (event.key == pygame.K_DOWN and arrow[2] == 'DOWN') or \
                       (event.key == pygame.K_LEFT and arrow[2] == 'LEFT') or \
                       (event.key == pygame.K_RIGHT and arrow[2] == 'RIGHT'):
                        arrows.remove(arrow)
                        score = score + 1
                        print("Hit!")  # Ensure this prints to console

                

    last_spawn_time = spawn_arrow(current_time)
    move_arrows()
    draw()

pygame.quit()
