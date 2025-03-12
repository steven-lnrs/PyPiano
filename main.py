import pygame
import mido
import time
import fluidsynth

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)  # Highlight color for pressed keys
KEY_HEIGHT = 200
WHITE_KEY_WIDTH = 40
BLACK_KEY_WIDTH = 20
# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load SF2 SoundFont using FluidSynth
def init_synth(soundfont_path):
    fs = fluidsynth.Synth()
    fs.start()
    sfid = fs.sfload(soundfont_path) 
    fs.program_select(0, sfid, 0, 0)
    return fs

# Function to get the minimum and maximum notes from a MIDI file
def get_min_max_notes(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path)
    min_note = 128  # MIDI note range is from 0 to 127
    max_note = -1
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                min_note = min(min_note, msg.note)
                max_note = max(max_note, msg.note)
    return min_note, max_note

# Function to create the keyboard visualization
def create_keyboard(min_note, max_note):
    # Calculate the relevant range of notes to display
    start_note = min_note - (min_note % 12)  # Start of the octave for the lowest note
    end_note = max_note + (12 - (max_note % 12))  # End of the octave for the highest note

    # We want to show one octave below the lowest and one octave above the highest
    start_octave = (min_note // 12) - 1
    end_octave = (max_note // 12) + 2
    num_octaves = end_octave - start_octave

    screen_width = num_octaves * 7 * WHITE_KEY_WIDTH  # 7 white keys per octave
    screen = pygame.display.set_mode((screen_width, KEY_HEIGHT))
    pygame.display.set_caption("Scalable Piano Visualization")

    white_key_rects = []
    black_key_rects = []

    for octave in range(start_octave, end_octave):
        for i in range(7):  # 7 white keys per octave (C, D, E, F, G, A, B)
            x = (octave - start_octave) * 7 * WHITE_KEY_WIDTH + i * WHITE_KEY_WIDTH
            white_rect = pygame.Rect(x, 0, WHITE_KEY_WIDTH, KEY_HEIGHT)
            white_key_rects.append(white_rect)
            # Black keys (C#, D#, F#, G#, A#) (not on E or B)
            if i in [0, 1, 3, 4, 5]:  # Black keys are placed after C, D, F, G, A
                black_rect = pygame.Rect(x + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH / 2, 0, BLACK_KEY_WIDTH, KEY_HEIGHT // 2)
                black_key_rects.append(black_rect)

    return screen, white_key_rects, black_key_rects, start_note, end_note, start_octave, num_octaves

# Function to convert MIDI note to the corresponding index for the key on the keyboard
def midi_to_key_index(note, start_note):
    return note - start_note

# Function to play the MIDI file and visualize the corresponding piano keys
def play_midi_and_visualize(midi_file_path, screen, white_key_rects, black_key_rects, synth, start_octave, num_octave):
    # Load MIDI file
    midi_file = mido.MidiFile(midi_file_path)
    WHITE_KEY_ORDER = [1,3,5,6,8,10,12] * num_octave
    # Track note press/release events
    pressed_keys = set()
    midi_ticks_per_beat = midi_file.ticks_per_beat

    running = True
    for msg in midi_file.play():
        if msg.type == 'note_on':
            pressed_keys.add(msg.note)
            synth.noteon(msg.channel, msg.note, msg.velocity)
        elif msg.type == 'note_off':
            if msg.note in pressed_keys:
                pressed_keys.remove(msg.note)
            synth.noteoff(msg.channel, msg.note)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        screen.fill(WHITE)  # Clear screen
        
        # Draw white keys
        for i, rect in enumerate(white_key_rects):
            # Compute the corresponding MIDI note
            octave = start_octave + (i // 7)  # Determine which octave this key is in
            note_in_octave = [0, 2, 4, 5, 7, 9, 11][i % 7]  # Map index to white key MIDI offset
            white_key_index = (octave * 12) + note_in_octave  # Compute actual MIDI note number
    
            color = WHITE
            if white_key_index in pressed_keys:
                color = BLUE
    
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
        # Draw black keys
        BLACK_KEY_OFFSETS = [1, 3, 6, 8, 10]
        for i, rect in enumerate(black_key_rects):
            octave = start_octave + (i // 5)
            note_in_octave = BLACK_KEY_OFFSETS[i % 5]  # Get the correct MIDI offset
            black_key_index = (octave * 12) + note_in_octave
            color = BLACK

            if black_key_index in pressed_keys:
                color = BLUE
            pygame.draw.rect(screen, color, rect)
        
        pygame.display.flip()  # Update the display
        time.sleep(msg.time / midi_ticks_per_beat)  # Sleep to match MIDI timing

    pygame.quit()

def main():
    midi_file = 'config/book1-prelude01.mid'  # Replace with the path to your MIDI file
    soundfont = 'config/FluidR3_GM.sf2'  # Replace with the path to your Synthwave SoundFont (SF2)

    # Get the minimum and maximum note range from the MIDI file
    min_note, max_note = get_min_max_notes(midi_file)
    print(f"Lowest note: {min_note}, Highest note: {max_note}")

    # Initialize the synthesizer with the SF2 file
    synth = init_synth(soundfont)

    # Create the keyboard and visualization based on the note range
    screen, white_key_rects, black_key_rects, start_note, end_note, start_octave, num_octave = create_keyboard(min_note, max_note)

    # Play the MIDI and visualize it
    play_midi_and_visualize(midi_file, screen, white_key_rects, black_key_rects, synth, start_octave, num_octave)

if __name__ == "__main__":
    main()
