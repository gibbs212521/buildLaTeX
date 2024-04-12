import csv


# APP_DIR = "./checklist_builder/"
APP_DIR = "./"
PY_DIR = APP_DIR+"py_files/"
C_DIR = APP_DIR+"c_files/"
TEX_DIR = APP_DIR+"tex_files/"
TEST_DIR = PY_DIR+"test/"

TEX_FILE = APP_DIR + 'output.tex'

OPERATION = "NONE"
PROPRIETOR = "NONE"

tex_lines = []

PRETEX_DIR = PY_DIR + "LaTeX_templates/"

PRE_TAG = "preTeX_"
PRETEX_TAG = PRETEX_DIR  + PRE_TAG

preTexFiles = []
preTexFiles.append(PRETEX_TAG + "open.txt")
preTexFiles.append(PRETEX_TAG + "package.txt")
preTexFiles.append(PRETEX_TAG + "preamble.txt")
preTexFiles.append(PRETEX_TAG + "body.txt")
preTexFiles.append(PRETEX_TAG + "close.txt")



def parseLine(line):
    if "OPERATION Checklist%" in line: 
        line = line.replace("OPERATION",OPERATION)
    elif "%\\fancyfoot[R]{PROPRIETOR \copyright}" in line: 
        line = line.replace("PROPRIETOR",PROPRIETOR)
    return line
        
### TODO: MUST BUILD OUT body.txt file prior to collecting pre-tex files

csv_db = [[],[],[],[]]
csv_file = TEST_DIR + "db/"


with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        if len(row) is 0: continue
        # print(row)
        


for preTeX in preTexFiles:
    print(preTeX)
    with open(preTeX,'r') as f:
        #  print(f)
         for line in f.readlines():
            if not len(line[1:]): continue
            line = parseLine(line)
            tex_lines.append(line)
         

with open(TEX_FILE, 'w') as f:
    f.writelines(tex_lines)

        
print(csv_db)
