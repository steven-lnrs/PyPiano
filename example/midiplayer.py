import subprocess

# Paths to SoundFont and MIDI file
soundfont_path = r"example\FluidR3_GM.sf2"
midi_file_path = r"example\book1-prelude01.mid"

# Run fluidsynth to play MIDI with correct timing
subprocess.run(["fluidsynth", "-i", soundfont_path, midi_file_path])
