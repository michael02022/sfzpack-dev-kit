import xml.etree.ElementTree as ET
from pathlib import Path
import sys
import os

LOOP_MODES = ("", "loop_continuous")
attrib_list = ("FileName", "Root", "LoKey", "HiKey", "LoVel", "HiVel", "RRGroup", "LoopStart", "LoopEnd", "LoopEnabled", "Pitch")
sfz_list = ("sample=", "pitch_keycenter=", "lokey=", "hikey=", "lovel=", "hivel=", "seq_position=", "loop_start=", "loop_end=", "loop_mode=", "tune=")

print(sys.argv)
filename = f"{os.getcwd()}/{sys.argv[1]}"
mytree = ET.parse(filename)
myroot = mytree.getroot()

final_sfz = ""
for child in myroot:
    final_sfz += "<region> "
    for k, v in child.attrib.items():
        if k in attrib_list:
            match k:
                case "FileName":
                    final_sfz += f"{sfz_list[attrib_list.index(k)]}{Path(v).name} "
                case "LoopEnabled":
                    if int(v) > 0:
                        final_sfz += f"{sfz_list[attrib_list.index(k)]}{LOOP_MODES[int(v)]} "
                    else:
                        pass
                case _:
                    final_sfz += f"{sfz_list[attrib_list.index(k)]}{v} "
    final_sfz += "\n"

fout = open(Path(filename).stem + ".sfz", "w")
fout.write(final_sfz)
fout.close()