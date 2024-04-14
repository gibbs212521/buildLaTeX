import sys

import csv

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

## NOTE: Application Directory is the location where the program is intended
#       to be called from



    ################################
    ###                          ###
    ###    SETUP FILES & PATHS   ###
    ###                          ###
    ################################

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


csv_filename = args.__dict__['file']
base_filename = csv_filename.split('\\')[-1][:-4]

TEX_FILE = TEX_DIR + f'{base_filename}.tex'

csv_file = sys.argv[-1]

print(base_filename)

# print('test')


def parseLine(line):
    if "OPERATION Checklist%" in line: 
        line = line.replace("OPERATION",OPERATION)
    elif "%\\fancyfoot[R]{PROPRIETOR \copyright}" in line: 
        line = line.replace("PROPRIETOR",PROPRIETOR)
    return line



    ################################
    ###                          ###
    ###     GENERAL FUNCTIONS    ###
    ###                          ###
    ################################


body_items = []
body_text = []

header_not_found = 1
table_under_evaluation = 0
checklist_interrupted = 0

def LaTeXize_contents(contents):
    count = 0
    ## The contents LaTeX-ification loop
    while (count + 1) < len(contents):
        for count, character in enumerate(contents):
            if "|" == character and "|" == contents[count-1] and \
                contents[count-2:count+2] != "$||$":
                contents = contents[:count-1] + "$||$" + contents[count+1:]
                break
            if "VOC" == contents[count-2:count+1]:
                contents = contents[:count-2] + "V$_{O"+"C}$" + contents[count+1:]
                break
            if "ISC" == contents[count-2:count+1]:
                contents = contents[:count-2] + "I$_{S"+"C}$" + contents[count+1:]
                break
            if "https:" == contents[count-5:count+1] and\
                "url{https:" != contents[count-9:count+1]:
                for p in range(len(contents[count+1:])):
                    if " " == contents[p + count]:
                        contents = contents[:p+count] + '}' + contents[p+count:]
                        break
                if '}' not in contents:
                    contents = contents + '}'
                contents = contents[:count-5] + "\\url{" + contents[count-5:]
                break
            if (character == '<')\
                and contents[count-1] is not "$"\
                and contents[count+1] is not "$":#\
                contents = contents[:count] + '$' + contents[count:count+1] \
                    + '$' + contents[count+1:]
                break
            if (character == '>')\
                and contents[count-1] is not "$":#\
                contents = contents[:count] + '$' + contents[count:count+1] \
                    + '$' + contents[count+1:]
                break
            if character == '[' and contents[count+2] == ']' and\
                contents[count-1] != "\\":
                contents = contents[:count] + "\\" + contents[count:count+2]\
                    + "\\" + contents[count+2:]
                break
            if character == '[' and contents[count+3] == ']' and\
                contents[count-1] != "\\":
                contents = contents[:count] + "\\" + contents[count:count+3]\
                    + "\\" + contents[count+3:]
                break
            if (character == "&" or character == "%")\
                and contents[count-1] is not "\\"\
                and contents[count-1] is not "|":#\
                # and contents[count+1] is not "_" \
                # and contents[count+1] is not "*" \
                # and contents[count+1] is not "\\":
                contents = contents[:count] + '\\' + contents[count:]
                break
    return contents

def process_csv_contents(row):
    if '"' == row[1][0]:
        old_contents = row[1]
        for collected in row[2:-3]:
            old_contents += ',' + collected
        old_contents = old_contents[1:-2]
    else:
        old_contents = row[1]
    new_contents = LaTeXize_contents(old_contents)

    return new_contents



    ################################
    ###                          ###
    ###      TABLE FUNCTIONS     ###
    ###                          ###
    ################################


def start_form(section_name):
    body_text.append('\\begin{Form}')
    body_text.append('\\def\\LayoutCheckField#1#2{\\parbox[c][5mm]{5mm}{\\centering\\footnotesize\\strut #2} #1}\\centering%')
    body_text.append('\\setupCheckListSet{'+f'{section_name}'+'}%')

def end_form():
    body_text.append('%\n\\closeoutChecklistSet%\n')
    body_text.append('\n\\\\\n\\end{Form}')

def build_table(dictionary_object):
    end_form()

    title = dictionary_object['Checkbox Text']
    captions = dictionary_object['Section Title']
    dimensions = dictionary_object['Dimensions']
    tabular_line = '\\begin{tabular}{| '
    for k in range(len(dimensions)): tabular_line += 'c | '
    tabular_line += '}'
    
    body_text.append('\n\\begin{table}[h!]%\n')
    body_text.append('\\caption{'+f'{title}'+'}%\n')
    body_text.append('\\centering%\n')
    body_text.append(f'{tabular_line}%\n')
    body_text.append('\\hline%\n')
    
    # BUILD HEADERS
    for indx in range(len(dimensions)):
        dimension = str(dimensions[indx])
        dimension += 'pt'
        while dimension[0] == ' ': dimension = dimension[1:]
        item_text = '\\parbox{'+ f'{dimension}' + '}'+\
             '{\\hfill\\\\[-0.3em] \\centering \\textbf{'
             #Inverter} \\\\')
        try:
            range_num = int(int(dimensions[indx]) / 5)
        except:
            raise TypeError("falled")
        evaluated_contents = item['Contents'][0][indx]
        if len(evaluated_contents) <= (range_num):
            item_text += evaluated_contents + '}\\\\[0.1em]}'
        else:
            line_text = item['Contents'][0][indx]
            item['indx_point'] = 0
            sub_num = range_num - 1
            while len(line_text) > range_num:
                for base_indx in range(range_num):
                    indx_point = item['indx_point']
                    novo_indx = base_indx + indx_point
                    sub_indx = sub_num + indx_point
                    super_indx = range_num + indx_point
                    if line_text[sub_indx-novo_indx] == ' ':
                        item_text += line_text[:sub_indx-novo_indx]
                        item_text += '} \\\\ \\textbf{'
                        line_text = line_text[super_indx-novo_indx:]
                        break
            item_text += line_text + '}\\\\[0.1em]}'
        if indx == (len(dimensions) - 1): item_text += ' \\\\%'
        else: item_text += ' &%'
        body_text.append(item_text + '\n')
    body_text.append('\\hline\n')
    body_text.append('\\hline\n')
    # BUILD TABLE OBJECTS
    contents = item['Contents']
    for pre_indx in range(1, len(contents)):
        if 'HLINE' in item['Contents'][pre_indx][0].upper():
            body_text.append('\\hline\n')
            continue
        for indx in range(len(dimensions)):
            dimension = str(dimensions[indx])
            dimension += 'pt'
            while dimension[0] == ' ': dimension = dimension[1:]
            item_text = '\\parbox{'+ f'{dimension}' + '}'+\
                '{\\hfill\\\\[-0.3em] \\centering '
                #Inverter} \\\\')
            range_num = int(int(dimensions[indx]) / 5)
            evaluated_contents = item['Contents'][pre_indx][indx]
            if len(evaluated_contents) <= range_num:
                item_text += evaluated_contents + ' \\\\[0.1em]}'
            else:
                line_text = item['Contents'][pre_indx][indx]
                item['indx_point'] = 0
                sub_num = range_num - 1
                while len(line_text) > range_num:
                    for base_indx in range(range_num):
                        indx_point = item['indx_point']
                        novo_indx = base_indx + indx_point
                        sub_indx = sub_num + indx_point
                        super_indx = range_num + indx_point
                        if line_text[sub_indx-novo_indx] == ' ':
                            item_text += line_text[:sub_indx-novo_indx]
                            item_text += ' \\\\ '
                            line_text = line_text[super_indx-novo_indx:]
                            break
                item_text += line_text + ' \\\\[0.1em]}'
            if indx == (len(dimensions) - 1): item_text += ' \\\\%'
            else: item_text += ' &%'
            body_text.append(item_text + '\n')
        body_text.append('\\hline\n')
    body_text.append('\\hline\n')
    body_text.append('\\end{tabular}%\n')  
    body_text.append('\\\\[0.5em]%\n')  
    if captions[0] == '*':
        captions = '\ensuremath{^*} ' + captions[1:]
    body_text.append(f'{captions}\\\\[1em]%\n')  
    body_text.append('\\end{table}%\n')  



    ################################
    ###                          ###
    ###      READ INPUT CSV      ###
    ###                          ###
    ################################

with open(csv_file, 'r', newline='', encoding='ANSI') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    
    for row in reader:
        if len(row) is 0: continue
        if OPERATION == "NONE":
            OPERATION = row[0]
        if header_not_found \
            and "Tag" == row[0]\
            and "Checkbox Text" == row[1]\
            and "Section Title" == row[4]:
            header_not_found = 0
        elif header_not_found:
            continue
        elif 'START TABLE' in row[0].upper():
            table_under_evaluation = 1
            body_items.append(
                {
                    'Tag' : row[0],
                    'Checkbox Text': row[1],
                    'Section Title' : row[2],
                    'Dimensions' : [],
                    'Contents' : []
                }
            )
        elif 'END TABLE' in row[0].upper() and table_under_evaluation:
            table_under_evaluation = 0
        elif 'DIMENSIONS' in row[0].upper() and table_under_evaluation:
            for dimension in row:
                try:
                    body_items[-1]['Dimensions'].append(int(dimension))
                except:
                    continue
        elif table_under_evaluation:
            for index in range(len(row)):
                old_contents = row[index]
                ### TODO: Refactor this as a function that returns new contents
                new_contents = LaTeXize_contents(old_contents)
                row[index] = new_contents
                    
            body_items[-1]['Contents'].append(row)
        elif 'PAGEBREAK' in row[0].upper():
            body_items.append('PAGEBREAK')
        elif 'INLINE' in row[0].upper():
            body_items.append(row[1])
        elif len(row[1]):
            new_contents = process_csv_contents(row)
            body_items.append(
                {
                    'Tag' : row[0],
                    'Checkbox Text': new_contents,
                    'Tutorial Text' : row[-3],
                    'Image Filename' : row[-2],
                    'Section Title' : row[-1]
                }
            )



    ################################
    ###                          ###
    ###      START OPERATION     ###
    ###                          ###
    ################################


range_num = 50
for item in body_items:
    if item == 'PAGEBREAK':
        end_form()
        checklist_interrupted = 1
        body_text.append('\pagebreak\n')
        continue
    try:
        if not len(item['Checkbox Text']):
            continue
    except TypeError:
        continue
    while item['Checkbox Text'][0] == ' ': 
        item['Checkbox Text'] = item['Checkbox Text'][1:]
    
    evaluated_contents = item['Checkbox Text']
    
    if item['Tag'].upper() == 'HEADER':
        if len(body_text) and not checklist_interrupted:
            end_form()
        start_form(evaluated_contents)
        checklist_interrupted = 0
    elif item['Tag'].upper() == 'START TABLE':
        build_table(item)
        checklist_interrupted = 1
    else:
        range_adder = 0
        for j in range(len(evaluated_contents)):
            try:
                if "\&" in evaluated_contents[j:j+2]:
                    range_adder += 1
                elif "$_{" in evaluated_contents[j:j+3] or \
                    "$^{" in evaluated_contents[j:j+3]: 
                    range_adder += 5
                elif "$||$" in evaluated_contents[j:j+4]: 
                    range_adder += 2
                elif "\\textbf{" in evaluated_contents[j:j+9]: 
                    range_adder += 8
            except:
                pass
        if len(evaluated_contents) <= range_num + range_adder:
            item_tag = item['Tag']
            item_text = evaluated_contents
        else:
            item_tag = item['Tag']
            item_text = ''
            line_text = evaluated_contents
            item['indx_point'] = 0
            sub_num = range_num - 1
            html_limiter = 4
            html_counter = 0
            while len(line_text) > range_num:
                for base_indx in range(range_num):
                    indx_point = item['indx_point']
                    test_val = len(line_text)
                    indx = base_indx + indx_point
                    sub_indx = sub_num + indx_point
                    super_indx = range_num + indx_point
                    if line_text[sub_indx-indx] == ' ' and 'url{' not in line_text:
                        item_text += line_text[:sub_indx-indx]
                        item_text += '\\\\%\n\\indent\\space\\hspace{0.21in}%\n'
                        line_text = line_text[super_indx-indx:]
                        break
                    if line_text[sub_indx-indx] == ' ' and 'url{' in line_text:
                        item_text += line_text[:sub_indx-indx]
                        item_text += '\\\\%\n\\indent%\n'
                        line_text = line_text[super_indx-indx:]
                        break
                html_counter += 1
                if html_counter > html_limiter:
                    break
                    
            item_text += line_text

        body_text.append('\\NewCheckBox{'+'%' + ' Label ID Below:')
        body_text.append(f'{item_tag}%')
        body_text.append('}{% Text Below:')
        body_text.append(f'{item_text}%')
        body_text.append('}%')

if not checklist_interrupted:
    end_form()


with open(BODY_TEX, 'w', encoding="UTF-8") as f:
    for line in body_text:
        f.write(line + '\n')

for preTeX in preTexFiles:
    with open(preTeX,'r') as f:
         for line in f.readlines():
            if not len(line[1:]): continue
            line = parseLine(line)
            tex_lines.append(line)
         

with open(TEX_FILE, 'w') as f:
    f.writelines(tex_lines)

print(TEX_FILE)
