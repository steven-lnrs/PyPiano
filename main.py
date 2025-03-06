# play_note.py
import time
import fluidsynth
from randomNote import generate_random_note  # Import the random note generator
import os
os.system('cls')
# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start()

# Load the sound font
sfid = fs.sfload(r"example\FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)

# Generate a random note and print it
random_midi, note_name = generate_random_note()
print(f"Playing random note: {note_name} (MIDI: {random_midi})")

# Play the random note
fs.noteon(0, random_midi, 30)  # Velocity (last number) determines how loud the note is
time.sleep(2.0)  # Hold the note for 1 second
fs.noteoff(0, random_midi)

# Clean up
fs.delete()
