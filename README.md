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



