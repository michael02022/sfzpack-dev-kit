import argparse
import os
import pathlib
import sys

opcodes = ("sample=",
           "lokey=",
           "hikey=",
           "lovel=",
           "hivel=",
           "pitch_keycenter=",
           " key=",
           "tune=",
           "loop_tune=",
           "looptune=",
           "loop_start=",
           "loopstart=",
           "loop_end=",
           "loopend=",
           "offset=",
           "lorand=",
           "hirand=",
           "seq_length=",
           "seq_position=")

formats = ('.wav', '.aiff', '.aif', '.aifc', '.flac', '.ogg', '.WAV', '.AIFF', '.AIF', '.AIFC', '.FLAC', '.OGG', ".$EXT")

def clip(n, range):
    if n < range[0]:
        return range[0]
    elif n > range[1]:
        return range[1]
    else:
        return n

def sort_regions(regions):
    vel_indexes = []
    vel_ls = []
    for idx in range(len(regions)):
        vel_ls.append(regions.lovel)
        vel_indexes.append([idx, regions.lovel])
    

class Region:
    def __init__(self):
        self.sample = None
        self.pitch_keycenter = None
        self.key = None
        self.lokey = None
        self.hikey = None
        self.lovel = None
        self.hivel = None
        self.tune = None
        self.loop_tune = None

        self.loop_start = None
        self.loop_end = None
        self.offset = None

        self.lorand = None
        self.hirand = None

        self.seq_length = None
        self.seq_position = None

    def clean(self):
        self.sample = None
        self.lokey = None
        self.hikey = None
        self.lovel = None
        self.hivel = None
        self.pitch_keycenter = None
        self.key = None
        self.tune = None
        self.loop_tune = None
        self.loop_start = None
        self.loop_end = None
        self.offset = None
        self.lorand = None
        self.hirand = None
        self.seq_length = None
        self.seq_position = None
    
    def change_value(self, var, val):
        match var:
            case "looptune":
                var = "loop_tune"
            case "loopstart":
                var = "loop_start"
            case "loopend":
                var = "loop_end"
        if isinstance(val, str):
            if var == "sample":
                self.sample = val
            else:
                exec(f"self.{var} = '{val}'")
        else:
            exec(f"self.{var} = {val}")
    
    def change_sample(self, string):
        self.sample = string
    
    def opcodes(self):
        ls = []
        for k, v in vars(self).items():
            if v is not None:
                ls.append(f"{k}={v}")
        return ls
    
    def get_region(self, path=None, fix=0, trans=0):
        region_line = "<region>"
        for k, v in vars(self).items():
            match k:
                case "pitch_keycenter" | "lokey" | "hikey" | "key":
                    if v is not None:
                        v = clip(int(v) + int(trans), (0, 127))
                case "loop_end":
                    if v is not None:
                        if fix is not None:
                            v = int(v) - int(fix)
                case "sample":
                    if path is not None:
                        v = f"{path}/{pathlib.Path(v).parts[-1]}"
            if v is not None:
                region_line += f" {k}={v}"
        region_line += "\n"
        return region_line

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--sfz", help="sfz file input")
parser.add_argument("-p", "--path", help="add/replace the path for sample opcode with given string")
parser.add_argument("-fix", "--fix", help="subtract the value by 1 in the end_loop opcode to fix errors in sforzando")
parser.add_argument("-trans", "--transpose", help="transpose the mapping with given value")

args = parser.parse_args()

if args.sfz is None:
    print("No SFZ file given.")
    exit()
else:
    pass

if len(pathlib.Path(args.sfz).parts) == 1:
    in_path = f"{os.getcwd()}/{args.sfz}"
else:
    in_path = args.sfz

in_f = os.path.normpath(in_path)
print(in_f)
f = open(in_f, "r", encoding="utf-8")

header = None
group_opcodes = []
region = None

t = 0

#fout = open(f"{os.getcwd()}/{args.sfz}", "w")
final_sfz = ""
for line in f.readlines():
    if line.find("<group>") != -1:
        header = "<group>"
        group_opcodes = []
    elif line.find("<region>") != -1:
        header = "<region>"
        #print(line)
        #print(region)
        #region_lines = 0
        if region is not None:
            if args.transpose is None:
                t = 0
            else:
                t = args.transpose
            final_sfz += region.get_region(path=args.path, fix=args.fix, trans=t)
    
    match header:
        case "<group>":
            tmp_op = []
            for op in opcodes:
                match line.find(op):
                    case -1:
                        pass
                    case _:
                        
                        offset = line.find(op) + len(op)
                        val = line[offset:].split(" ")[0].strip("\n")
                        if op == " key=":
                            op = "key="
                        tmp_op.append(f"{op}{val}")
            for g in tmp_op:
                group_opcodes.append(g)
        case "<region>":
            #print(group_opcodes)
            if not line.isspace(): # if the line is not empty
                if line.find("<region>") >= 0: # if the line contains a region header # to make sure we collected data from the line with header and the lines without the header
                    region = Region() # each time a region header is in the line, creates a region object and fill the data until a new region header shows up                
                for op in opcodes:
                    match line.find(op):
                        case -1:
                            pass
                        case _:
                            offset = line.find(op) + len(op)
                            if op == "sample=":
                                for x in formats:
                                    charlen = len(x)
                                    if line.find(x) >= 0:
                                        smpl = line.find(x)
                                val = line[offset:smpl + charlen].strip("\n")
                            else:
                                val = line[offset:].split(" ")[0].strip("\n")
                            if op == " key=":
                                op = "key="
                            #print(val)
                            region.change_value(op[:-1], val)
                            if len(group_opcodes) != 0:
                                for opstr in group_opcodes:
                                    region.change_value(opstr.split("=")[0], opstr.split("=")[1])
                #region_lines += 1
                #print(count)
                #if count < count + 1:
                    #print(region.opcodes())
final_sfz += region.get_region(path=args.path, fix=args.fix, trans=t)
print(final_sfz)
answer = input("Looks good? (y/n): ")
match answer:
    case "y":
        fout = open(in_path, "w")
        fout.write(final_sfz)
        fout.close()
        print("Changes written.")
    case "n":
        sys.exit(0)
    case _:
        print("Invalid input, no saved changes.")
        sys.exit(0)

