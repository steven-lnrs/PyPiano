# 🎹 MIDI Piano Visualizer

## 🎶 Overview
This project is a **MIDI Piano Visualizer** built using **Pygame, Mido, and FluidSynth**. It dynamically generates a piano keyboard based on the notes in a given MIDI file, highlights the keys as they are played, and plays the MIDI sound using a SoundFont (.sf2).

## ✨ Features
- **Scalable Keyboard**: Automatically adjusts to fit the range of notes in the MIDI file.
- **MIDI Playback**: Uses **FluidSynth** to produce high-quality sounds from a SoundFont.
- **Real-time Visualization**: Keys light up as they are played in the MIDI file.
- **Customizable SoundFont**: Use any .sf2 file to change the instrument sound.
- **Dynamic Key Mapping**: Both white and black keys are mapped accurately to their corresponding MIDI numbers.

## 🛠 Installation
### 1️⃣ Install Dependencies
Before running the project, make sure you have the following installed:
- Python 3.x
- [FluidSynth](https://ksvi.mff.cuni.cz/~dingle/2019/prog_1/python_music.html) <- drections of installation
- A SoundFont file (e.g., `FluidR3_GM.sf2`), can be downloaded [here](https://keymusician01.s3.amazonaws.com/FluidR3_GM.zip)
- a midi File (e.g. `book1-prelude01.mid`), can also be downloaded [here](https://www.mfiles.co.uk/downloads/book1-prelude01.mid). After downloading both files, place them under the `config` folder.
After following the website, you can install the required Python packages by running:

```bash
pip install fluidsynth
```

### 2️⃣ Run the Program
Replace `config/book1-prelude01.mid` with your MIDI file and `config/FluidR3_GM.sf2` with your SoundFont path. Then, run:
```sh
python midi_visualizer.py
```

## 🎛 Configuration
- **MIDI File Path:** Change `midi_file` in `main()` to use different MIDI files.
- **SoundFont Path:** Set `soundfont` in `main()` to use different instruments.
- **Window Size:** Adjust `WHITE_KEY_WIDTH` and `KEY_HEIGHT` for a different layout.

## 🎯 How It Works
1. **Extracts MIDI Note Range**: Determines the lowest and highest notes in the MIDI file.
2. **Generates the Keyboard**: Dynamically scales the keyboard based on the MIDI range.
3. **Plays the MIDI**: Uses FluidSynth to generate sound.
4. **Highlights Keys**: As the MIDI plays, corresponding keys are highlighted in **blue**.

## 🎵 Future Enhancements
🚀 Add support for **real-time MIDI input** from a keyboard!
🎨 Custom themes & colors!
📈 Advanced animations!

---
💡 **Created with Python & Pygame** 🐍🎹

