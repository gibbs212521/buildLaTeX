import sys

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

## NOTE: Application Directory is the location where the program is intended
#       to be called from


APP_DIR = "./"
PY_DIR = APP_DIR+"py_files/"
C_DIR = APP_DIR+"c_files/"
TEX_DIR = APP_DIR+"tex_files/"

OPERATION = "NONE"
PROPRIETOR = "NONE"

tex_lines = []

PRETEX_DIR = PY_DIR + "LaTeX_templates/"

PRE_TAG = "preTeX_"
PRETEX_TAG = PRETEX_DIR  + PRE_TAG

BODY_TEX = PRETEX_TAG + "body.txt"

preTexFiles = []
preTexFiles.append(PRETEX_TAG + "open.txt")
preTexFiles.append(PRETEX_TAG + "package.txt")
preTexFiles.append(PRETEX_TAG + "preamble.txt")
preTexFiles.append(BODY_TEX)    # body.txt is regenerated at runtime
preTexFiles.append(PRETEX_TAG + "close.txt")

def parseLine(line):
    if "OPERATION Checklist%" in line: 
        line = line.replace("OPERATION",OPERATION)
    elif "%\\fancyfoot[R]{PROPRIETOR \copyright}" in line: 
        line = line.replace("PROPRIETOR",PROPRIETOR)
    return line

csv_filename = args.__dict__['file']
base_filename = csv_filename.split('\\')[-1][:-4]

TEX_FILE = TEX_DIR + f'{base_filename}.tex'

csv_file = sys.argv[-1]

# print(csv_file)
# print(csv_filename.__dict__['file'])
print(base_filename)

# print('test')