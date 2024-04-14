import sys
import os


## TODO: For program that buildsa curated suite:
##      Figure out a way of comparing csv files
###         RECOMMENDATION: Utilize a checksum - maybe write one for fun??
######          JPEG Checksum? ? ? → Odd 256 x 256 x (4 x 4 cosine)
######               |- Cosine filter:: << Figure out the preliminary filter>>
#########                   Maybe a binary sum filter?
#########                   Maybe a vowel sum filter + int summer filter? 
######               |- Hilbert Transform Data Aggregation
######               |- Split into sections of 4096 bytes
######               |- Hilbert Transform Even portion
######               |- Sum 23rd 256 with 256 reset (value range: 1-254)
######               |- lshift rotate outter shell of 1020 pixels via coupling stack
######               |- first difference into shiftee stack (clockwise)
######               |- remaining pixels into outter shell starting @ 0,0
######               |- once complete continue with shiftee stack until 1,0
######               |- Finally, flatten into 2 uint16 with (0xB threshold filter of 4x4)
#
## today =date.today()
## file_has_been_updated = False
#
## with open(BODY_TEX, 'r', encoding="UTF-8") as f:
#
###


APP_DIR = "\\..\\..\\"
PY_DIR = APP_DIR+"py_files\\"
TEST_DIR = PY_DIR+"test\\"

TEX_FILE = TEST_DIR + 'test.tex'

CSV_FILE = sys.path[0] + "\\db\\test_checklist.csv"

SRC_FILE = sys.path[0] + PY_DIR + "src\\tex_writer.py"

# print(f'cmd /c {SRC_FILE} -f {CSV_FILE}')

os.system(f'python {SRC_FILE} -f {CSV_FILE}')
