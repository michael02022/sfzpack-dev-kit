import os
import argparse

directory = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("-ls", "--list", help="set a list of names")
parser.add_argument("-suffix", "--suffix", help="set a list of names")

args = parser.parse_args()

name_list = []

if args.list is not None:
  with open(args.list, 'r') as file:
    file_content = file.read()
    name_list = file_content.split("\n")

i = 0
for subdir, dirs, files in os.walk(directory):
    for filepath in sorted(files):
      if filepath.endswith(".wav"):
        # Extract the filename without the extension
        filename_without_extension = os.path.splitext(filepath)[0]

        if args.suffix is not None:
          suffix = f" {args.suffix}"
        else:
          suffix = ""

        # Create the output filename with ".txt" extension
        if len(name_list) != 0:
          output_filename = f"{name_list[i]}{suffix}.sfz"
          print(f"{filename_without_extension}, {name_list[i]}")
          i += 1
        else:
          output_filename = f"{str(filepath).split(".")[0]}.sfz"

        output_path = os.path.join(subdir, output_filename)
        #
        with open(output_path, "w") as f:
            f.write(f"<region> sample={filename_without_extension}.wav")
