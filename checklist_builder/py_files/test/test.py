import csv


# APP_DIR = "./checklist_builder/"
APP_DIR = "."
PY_DIR = APP_DIR+"py_files/"
C_DIR = APP_DIR+"c_files/"
TEX_DIR = APP_DIR+"tex_files/"
TEST_DIR = PY_DIR+"test/"

TEX_FILE = APP_DIR+"output.tex"

OPERATION = "NONE"
PROPRIETOR = "NONE"

tex_lines = []


csv_db = [[],[],[],[]]

csv_file = TEST_DIR+"db/test_checklist.csv"

with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        if len(row) is 0: continue
        print(row)
        
        
print(csv_db)
