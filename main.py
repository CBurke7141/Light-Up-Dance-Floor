# main.py
import pygame
from menu import MainMenu
from game import Game
from song_selection import SongSelectionMenu

# Initialize Pygame
pygame.init()
pygame.font.init()  # Ensure the font module is initialized

# Constants
FPS = 60

# Setup the window in fullscreen mode
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Light Up Dance Floor")
clock = pygame.time.Clock()

def main():
    running = True
    while running:
        main_menu = MainMenu(win)
        option = main_menu.run()
    
        if option == 'Start the Game':
            while True:
                song_selection = SongSelectionMenu(win)
                selected_song = song_selection.run()
                if selected_song is None:
                    break  # Go back to main menu if user selects 'Exit'

                game = Game(win, clock, win.get_width(), win.get_height(), FPS, selected_song)
                game_option = game.run()

                if game_option == 'SongSelectionMenu':
                    continue  # Go back to song selection menu
                elif game_option == 'Main Menu':
                    break  # Go back to main menu
                elif game_option == 'Exit':
                    running = False
                    break  # Exit the game
     
        elif option == 'Exit':
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
