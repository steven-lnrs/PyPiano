import pygame
import fluidsynth
from randomNote import note_to_midi
from time import sleep

# Initialize Pygame
pygame.init()

# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload(r"cofig\FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)

# Constants
WIDTH, HEIGHT = 700, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (100, 149, 237)  # Highlight color for pressed keys
KEY_WIDTH = WIDTH // 14  # 14 keys (C to B, 1 full octave)
KEY_HEIGHT = HEIGHT

# Define keys and mappings
WHITE_KEYS = ['A', 'S', 'D', 'F', 'G', 'H', 'J']
BLACK_KEYS = ['W', 'E', 'T', 'Y', 'U']
WHITE_KEY_ORDER = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
BLACK_KEY_ORDER = ['C#', 'D#', 'F#', 'G#', 'A#']
BLACK_KEY_POSITIONS = [0.7, 1.7, 3.7, 4.7, 5.7]  # Relative positions over white keys

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPiano Visualizer")

# Create key rectangles
white_key_rects = [pygame.Rect(i * KEY_WIDTH, 0, KEY_WIDTH, KEY_HEIGHT) for i in range(7)]
black_key_rects = [pygame.Rect((pos * KEY_WIDTH), 0, KEY_WIDTH * 0.6, HEIGHT * 0.6) for pos in BLACK_KEY_POSITIONS]

# Key press state
pressed_keys = {}
currently_playing_white = {} # creating a latch system so that keys already pressed don't constantly replay
currently_playing_black = {} # I honestly couldn't tell you why but keeping them seperate works
# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key).upper()
            if key in WHITE_KEYS or key in BLACK_KEYS:
                # Only add the key if it's not already pressed
                if key not in pressed_keys:
                    pressed_keys[key] = True
        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key).upper()
            if key in pressed_keys:
                del pressed_keys[key]

    # Draw white keys and handle note-on/note-off
    for i, rect in enumerate(white_key_rects):
        color = BLUE if WHITE_KEYS[i] in pressed_keys else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Key outlines

        # Handle note-on and note-off for white keys
        if WHITE_KEYS[i] in pressed_keys:
            note = WHITE_KEY_ORDER[i]
            midi_num = note_to_midi(note, 5)
            if i not in currently_playing_white:
                fs.noteon(0, midi_num, 100)
                currently_playing_white[i] = True
        else:
            note = WHITE_KEY_ORDER[i]
            midi_num = note_to_midi(note, 5)
            fs.noteoff(0, midi_num)  
            try: del currently_playing_white[i]
            except: pass


    # Draw black keys and handle note-on/note-off
    for i, rect in enumerate(black_key_rects):
        color = GRAY if BLACK_KEYS[i] in pressed_keys else BLACK
        pygame.draw.rect(screen, color, rect)

        # Handle note-on and note-off for black keys
        if BLACK_KEYS[i] in pressed_keys:
            note = BLACK_KEY_ORDER[i]
            midi_num = note_to_midi(note, 5)
            if i not in currently_playing_black:
                fs.noteon(0, midi_num, 100)
                currently_playing_black[i] = True  # Play note (use channel 0 and velocity 30)
        else:
            note = BLACK_KEY_ORDER[i]
            midi_num = note_to_midi(note, 5)
            fs.noteoff(0, midi_num)  
            try: del currently_playing_black[i]
            except: pass
 # Stop the note (velocity 0)

    pygame.display.flip()

pygame.quit()