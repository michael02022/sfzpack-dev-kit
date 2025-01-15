 
import os
import ctypes

def replace_loop(wav_file_path):
  with open(wav_file_path, 'r+b') as wav_file:
    data = wav_file.read()
    try:
      smpl_offset = data.find(bytes.fromhex("736d706c")) # "smpl" in hex values
      number_loops = data[smpl_offset+0x24:smpl_offset+0x28]
      print(wav_file_path)

      if int.from_bytes(number_loops, "little") == 1:
        start_loop = data[smpl_offset+0x28+0x0C:smpl_offset+0x28+0x10]
        end_loop = data[smpl_offset+0x28+0x10:smpl_offset+0x28+0x14]
        print(int.from_bytes(start_loop, "little"))
        print(int.from_bytes(end_loop, "little"))
        new_end_loop = int.from_bytes(end_loop, "little") + 1 # FIXED!!!!!
        print(new_end_loop)

        wav_file.seek(smpl_offset+0x28+0x10)
        wav_file.write(new_end_loop.to_bytes(4, byteorder='little'))
    except:
      None

# Iterate over all WAV files in the current directory and subfolders
for root, _, files in os.walk("."):
  for file in files:
    if file.endswith(".wav"):
      wav_file_path = os.path.join(root, file)
      replace_loop(wav_file_path)

