import pygame
import random
from song_selection import SongSelectionMenu  # Import the SongSelectionMenu

class Game:
    def __init__(self, win, clock, WIDTH, HEIGHT, FPS, song):
        self.win = win
        self.clock = clock
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.FPS = FPS
        self.song = song
        self.score = 0
        self.arrows = []
        self.last_spawn_time = 0
        self.pause_start_time = 0

        self.difficulty_settings = {
            'Easy': (3, 2000),
            'Medium': (5, 1500),
            'Hard': (7, 1000)
        }

        self.arrow_speed = 3
        self.spawn_interval = 2000

        self.arrow_imgs = {
            'UP': pygame.transform.scale(pygame.image.load('assets/up.png'), (50, 50)),
            'DOWN': pygame.transform.scale(pygame.image.load('assets/down.png'), (50, 50)),
            'LEFT': pygame.transform.scale(pygame.image.load('assets/left.png'), (50, 50)),
            'RIGHT': pygame.transform.scale(pygame.image.load('assets/right.png'), (50, 50))
        }

        self.x_positions = {
            'UP': WIDTH // 2 - 100,
            'DOWN': WIDTH // 2 - 50,
            'LEFT': WIDTH // 2,
            'RIGHT': WIDTH // 2 + 50
        }

        self.shadow_arrows = [
            (self.x_positions['UP'], 50, 'UP'),
            (self.x_positions['DOWN'], 50, 'DOWN'),
            (self.x_positions['LEFT'], 50, 'LEFT'),
            (self.x_positions['RIGHT'], 50, 'RIGHT')
        ]

    def reset_game(self):
        self.score = 0
        self.arrows = []
        self.last_spawn_time = 0

    def choose_difficulty(self):
        font = pygame.font.SysFont(None, 55)
        difficulty_options = ['Easy', 'Medium', 'Hard']
        selected_option = 0

        while True:
            self.win.fill((0, 0, 0))

            for i, option in enumerate(difficulty_options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                text = font.render(option, True, color)
                self.win.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 + i * 60))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'Exit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(difficulty_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(difficulty_options)
                    elif event.key == pygame.K_RIGHT:
                        return difficulty_options[selected_option]
                    elif event.key == pygame.K_LEFT:
                        return 'SongSelectionMenu'

    def spawn_arrow(self, current_time):
        if current_time - self.last_spawn_time > self.spawn_interval:
            direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.arrows.append([self.x_positions[direction], self.HEIGHT, direction])
            self.last_spawn_time = current_time

    def move_arrows(self):
        for arrow in self.arrows[:]:
            arrow[1] -= self.arrow_speed
            if arrow[1] < 0:
                self.arrows.remove(arrow)
                print("Miss")

    def draw(self):
        self.win.fill((0, 0, 0))
        for shadow in self.shadow_arrows:
            self.win.blit(self.arrow_imgs[shadow[2]], (shadow[0], shadow[1]))
        for arrow in self.arrows:
            self.win.blit(self.arrow_imgs[arrow[2]], (arrow[0], arrow[1]))
        font = pygame.font.SysFont(None, 25)
        score_text = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.win.blit(score_text, (self.WIDTH - 200, 20))
        pygame.display.update()

    def pause_menu(self):
        pygame.mixer.music.pause()
        font = pygame.font.SysFont(None, 55)
        pause_options = ['Resume', 'Main Menu', 'Exit']
        selected_option = 0
        self.pause_start_time = pygame.time.get_ticks()

        while True:
            self.win.fill((0, 0, 0))

            for i, option in enumerate(pause_options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                text = font.render(option, True, color)
                self.win.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 + i * 60))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'Exit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(pause_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(pause_options)
                    elif event.key == pygame.K_RIGHT:
                        if pause_options[selected_option] == 'Resume':
                            pygame.mixer.music.unpause()
                            self.last_spawn_time += pygame.time.get_ticks() - self.pause_start_time
                            return 'Resume'
                        elif pause_options[selected_option] == 'Main Menu':
                            pygame.mixer.music.stop()
                            return 'Main Menu'
                        elif pause_options[selected_option] == 'Exit':
                            pygame.mixer.music.stop()
                            return 'Exit'
                    elif event.key == pygame.K_LEFT:
                        return 'Main Menu'

    def run(self):
        self.reset_game()

        while True:
            difficulty = self.choose_difficulty()
            if difficulty == 'SongSelectionMenu':
                return 'SongSelectionMenu'
            elif difficulty == 'Main Menu':
                return 'Main Menu'
            elif difficulty == 'Exit':
                return 'Exit'
            self.arrow_speed, self.spawn_interval = self.difficulty_settings[difficulty]

            pygame.mixer.music.load(self.song)
            pygame.mixer.music.play()

            game_running = True
            while game_running:
                self.clock.tick(self.FPS)
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'Exit'
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            option = self.pause_menu()
                            if option == 'Resume':
                                pygame.mixer.music.unpause()
                                continue
                            elif option == 'Main Menu':
                                return 'Main Menu'
                            elif option == 'Exit':
                                return 'Exit'
                        else:
                            for arrow in list(self.arrows):
                                if arrow[1] - 50 <= 50 <= arrow[1] + 50:
                                    if (event.key == pygame.K_UP and arrow[2] == 'UP') or \
                                       (event.key == pygame.K_DOWN and arrow[2] == 'DOWN') or \
                                       (event.key == pygame.K_LEFT and arrow[2] == 'LEFT') or \
                                       (event.key == pygame.K_RIGHT and arrow[2] == 'RIGHT'):
                                        self.arrows.remove(arrow)
                                        self.score += 1
                                        print("Hit!")

                self.spawn_arrow(current_time)
                self.move_arrows()
                self.draw()
