# randomNote.py
import random

# List of note names in standard octave notation
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Function to convert MIDI note number to note name
def midi_to_note(midi_num):
    octave = (midi_num // 12) - 1  # Octave is calculated based on the MIDI number
    note = note_names[midi_num % 12]  # Get the note name from the list
    return f"{note}{octave}"

# Function to generate a random MIDI note and return its name
def generate_random_note():
    random_note = random.randint(12, 115) # Set from 0,127 if you want full range
    note_name = midi_to_note(random_note)
    return random_note, note_name
