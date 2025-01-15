# sfzpack-dev-kit
Useful tools to create or fix stuff for SFZpacks.

These are vainilla python3 scripts.

## cue2sfz
Parse the cue data of wav files into separated wav files.

## multisample2sfz
Converts Bitwig multisample format into sfz **MAPPING** (no additional opcodes, just the ones to define the mapping), used to port NKI libraries to SFZ with [ConvertWithMoss](https://www.mossgrabers.de/Software/ConvertWithMoss/ConvertWithMoss.html) with injected sample metadata (loop points)

Just run the script in a folder with multisample files.

## hise2sfz
Parse XML files made by [HISE](https://hise.dev/) into sfz **MAPPING**, an alternative way to map samples with a GUI and then convert it into SFZ.

## wav2sfz
Script to set individual SFZ files to each individual wav files. Useful for making percussion in a SFZpack. Run this script in a folder with wav files. `-ls` to load a TXT file with a list of names in the same order as the filenames to rename the SFZ files to each one of those names (**it must to have the same number of files the number of names in the TXT file**).

Example:

```
MaxLow Kick3
Rk CmpKick
Gospel Clap
Boys Kick
Snr Roll
HipHop Kick2
Reg.PHH
Reg.Kick
Frenzy Kick
Vinyl Kick
```

`-suffix` to set a suffix in the SFZ file.

## wavfixer
List ALL wav files through all folders and it will search for the **END LOOP** value in the **smpl** chunk of each one and substract the value by -1, to fix "size of samples = end loop value" error of **Sforzando**. Sample converters do this mistake often and this will fix it. Make sure to run it once. In case you need to add +1 to the value due to some mistake, use `wavfixer +`

## sfzmap-flat
A tool where parses normal SFZ files into the lowest SFZ common denominator (only the opcodes to define the mappings), most of the time works with converted SFZ files.


### These are not perfect scripts, but it saves a lot of time when developing a SFZpack, overtime I'll try to improve them depending of my experiences when porting sample libraries

## HOW TO CONVERT SFZpack FROM WAV TO FLAC (and vice versa)

### Requirements
1. flac CLI tool
2. Bash

### INSTRUCTIONS
1. Install flac command line tool

https://xiph.org/flac/download.html

#### Windows
2. Install [Git for Windows](https://git-scm.com/downloads/win) to use Bash commands in Windows file system.
3. After you download the flac tool, put the .EXE file on any folder you like

4. Open start menu
5. Type Edit environment variables
6. Open the option Edit the system environment variables
7. Click "Environment variables" button
8. There you see two boxes, in System Variables box find `Path` variable
9. Click Edit
10. a window pops up, click New
11. Copy the path folder/directory where the flac tool is in there and paste it.
12. Click OK

To verify, open Git Bash and type `flac` to see if it was installed correctly.

#### macOS

Using [homebrew](https://brew.sh/), run `brew install flac`

#### Linux

Use whatever install package command from your distro as sudo and type `flac`.

Ubuntu/Debian: `sudo apt-get install flac`

Arch: `sudo pacman -S flac`

And so on.

### COMMANDS

These commands must be run in the root folder where all SFZ and WAV files are in. Be patient, it will take time.

* **ENCODE FROM WAV -> FLAC (BASH):**

`find -type f -iname '*.wav' -print0 | while read -d $'\0' FILE ; do flac --delete-input-file --keep-foreign-metadata --compression-level-8 "$FILE" ; done`

* **DECODE FROM FLAC -> WAV (BASH):**

`find -type f -iname '*.flac' -print0 | while read -d $'\0' FILE ; do flac -d "$FILE" --delete-input-file --keep-foreign-metadata; done`

* **CHANGE .wav EXTENSION FROM SFZ FILES TO .flac EXTENSION IN SAMPLE OPCODE (BASH)**

`find -type f -iname '*.sfz' -print0 | while read -d $'\0' FILE ; do sed -r 's/\.wav/\.flac/g' -i "${FILE}"; done`

(swap the extension names to make them back to wav)

