import pygame

class SongSelectionMenu:
    def __init__(self, win):
        self.win = win
        self.font = pygame.font.SysFont(None, 55)
        self.song_options = ['Light It Up']  # Alias name for the song
        self.song_files = ['songs/Camellia - Light It Up.mp3']  # Path to the song file
        self.selected_option = 0
        self.WIDTH, self.HEIGHT = win.get_size()

    def run(self):
        while True:
            self.win.fill((0, 0, 0))

            for i, option in enumerate(self.song_options):
                color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
                text = self.font.render(option, True, color)
                self.win.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 + i * 60))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'Exit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.song_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.song_options)
                    elif event.key == pygame.K_RIGHT:
                        return self.song_files[self.selected_option]
                    elif event.key == pygame.K_LEFT:
                        return None
                    
