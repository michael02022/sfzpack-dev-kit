import os
import wave
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="filename")
parser.add_argument("-k", "--key", help="starting keycenter")
parser.add_argument("-s", "--steps", help="step pattern for keycenter (eg. 2 or 3)")

args = parser.parse_args()

wav_size = 0
wav_channels = 1
wav_samplerate = 44100
wav_sample_width = 0
cue_list = []
data = []
sfz = ""

if args.input is None:
    print("please set a wav input with cue/acid markers")
    exit(0)

if args.key is not None:
    key = args.key
else:
    key = 36

if args.steps is not None:
    steps = args.steps
else:
    steps = 1

filename = str(args.input).split(".")[0]

with wave.open(f"{args.input}", "rb") as wav_file:
    wav_size = wav_file.getnframes()
    channels = wav_file.getnchannels()
    samplerate = wav_file.getframerate()
    sample_width = wav_file.getsampwidth()
    print(wav_size)
    print(channels)
    print(samplerate)
    print(sample_width)

with open(f"{args.input}", 'rb') as wav_file:

    data = wav_file.read()
    cue_offset = data.find(bytes.fromhex("63756520")) # "cue "
    cue_points = int.from_bytes(data[cue_offset+0x08:cue_offset+0x0C], "little")
    cue_points_offset = cue_offset+12
    for i in range(cue_points):
        off = cue_points_offset+(24*i)
        cue_chunk = data[off:off+24]
        cue_point = int.from_bytes(cue_chunk[20:24], "little")
        print(f"{i+1}) {cue_point}")
        cue_list.append(cue_point)

    cue_list.append(wav_size)

for i in range(len(cue_list)-1):
    n = int(key)+(int(steps)*i)
    with wave.open(f"{filename} {n:03}.wav", 'wb') as chunk_wf:
        chunk_wf.setnchannels(channels)
        chunk_wf.setframerate(samplerate)
        chunk_wf.setsampwidth(sample_width)

        m = 2 * channels # multiplier of the sample points, 2 = 16-bit

        chunk_wf.writeframes(data[cue_list[i]*m:cue_list[i+1]*m]) # sample_point*(bitdepth*channels)

        if i == 0:
            sfz += f"<region> sample={filename} {n:03}.wav pitch_keycenter={n} hikey={n+(int(steps)-1)}\n"
        elif i == len(cue_list)-2:
            sfz += f"<region> sample={filename} {n:03}.wav pitch_keycenter={n} lokey={n}\n"
        else:
            sfz += f"<region> sample={filename} {n:03}.wav key={n} hikey={n+(int(steps)-1)}\n"

with open(f"{filename}.sfz", "w") as f:
    f.write(sfz)
