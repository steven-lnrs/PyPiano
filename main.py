import pygame
import fluidsynth
from randomNote import note_to_midi
from time import sleep

# Initialize Pygame
pygame.init()

# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload(r"config\FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)

# Constants
WIDTH, HEIGHT = 1000, 300  # Increased width for multiple octaves
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (100, 149, 237)  # Highlight color for pressed keys
OCTAVES = 2  # Number of octaves to support
KEYS_PER_OCTAVE = 7  # White keys per octave
TOTAL_WHITE_KEYS = KEYS_PER_OCTAVE * OCTAVES
KEY_WIDTH = WIDTH // TOTAL_WHITE_KEYS  
KEY_HEIGHT = HEIGHT

# Define keys and mappings for multiple octaves
WHITE_KEYS = ['Z', 'X', 'C', 'V', 'B', 'N', 'M',  # First octave (C4-B4)
              'A', 'S', 'D', 'F', 'G', 'H', 'J']  # Second octave (C5-B5)

BLACK_KEYS = ['Q', 'W', 'R', 'T', 'Y',  # First octave (C#4 - A#4)
              '1', '2', '4', '5', '6']  # Second octave (C#5 - A#5)

WHITE_KEY_ORDER = ['C', 'D', 'E', 'F', 'G', 'A', 'B'] * OCTAVES
BLACK_KEY_ORDER = ['C#', 'D#', 'F#', 'G#', 'A#'] * OCTAVES

# Calculate black key positions dynamically for all octaves
BLACK_KEY_POSITIONS = []
for octave in range(OCTAVES):
    BLACK_KEY_POSITIONS += [(octave * 7) + offset for offset in [0.7, 1.7, 3.7, 4.7, 5.7]]

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPiano Visualizer")

# Create key rectangles for multiple octaves
white_key_rects = [pygame.Rect(i * KEY_WIDTH, 0, KEY_WIDTH, KEY_HEIGHT) for i in range(TOTAL_WHITE_KEYS)]
black_key_rects = [pygame.Rect(pos * KEY_WIDTH, 0, KEY_WIDTH * 0.6, HEIGHT * 0.6) for pos in BLACK_KEY_POSITIONS]

# Key press state
pressed_keys = {}
currently_playing = {}

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
            octave = (i // KEYS_PER_OCTAVE) + 4  # Assign octaves dynamically (starting from 4)
            midi_num = note_to_midi(note, octave)
            if midi_num not in currently_playing:  # Use MIDI number for tracking
                fs.noteon(0, midi_num, 100)
                currently_playing[midi_num] = True
        else:
            note = WHITE_KEY_ORDER[i]
            octave = (i // KEYS_PER_OCTAVE) + 4
            midi_num = note_to_midi(note, octave)
            if midi_num in currently_playing:  # Ensure it's playing before stopping
                fs.noteoff(0, midi_num)
                currently_playing.pop(midi_num, None)  # Remove from playing dictionary

    # Draw black keys and handle note-on/note-off
    for i, rect in enumerate(black_key_rects):
        color = GRAY if BLACK_KEYS[i] in pressed_keys else BLACK
        pygame.draw.rect(screen, color, rect)

        # Handle note-on and note-off for black keys
        if BLACK_KEYS[i] in pressed_keys:
            note = BLACK_KEY_ORDER[i]
            octave = (i // 5) + 4  # There are 5 black keys per octave
            midi_num = note_to_midi(note, octave)
            if midi_num not in currently_playing:  # Use MIDI number for tracking
                fs.noteon(0, midi_num, 100)
                currently_playing[midi_num] = True
        else:
            note = BLACK_KEY_ORDER[i]
            octave = (i // 5) + 4
            midi_num = note_to_midi(note, octave)
            if midi_num in currently_playing:  # Ensure it's playing before stopping
                fs.noteoff(0, midi_num)
                currently_playing.pop(midi_num, None)  # Remove from playing dictionary

    pygame.display.flip()

pygame.quit()
