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

BODY_TEX = PRETEX_TAG + "body.txt"

preTexFiles = []
preTexFiles.append(PRETEX_TAG + "open.txt")
preTexFiles.append(PRETEX_TAG + "package.txt")
preTexFiles.append(PRETEX_TAG + "preamble.txt")
preTexFiles.append(BODY_TEX)
preTexFiles.append(PRETEX_TAG + "close.txt")



def parseLine(line):
    if "OPERATION Checklist%" in line: 
        line = line.replace("OPERATION",OPERATION)
    elif "%\\fancyfoot[R]{PROPRIETOR \copyright}" in line: 
        line = line.replace("PROPRIETOR",PROPRIETOR)
    return line
        
### TODO: MUST BUILD OUT body.txt file prior to collecting pre-tex files

csv_db = [[],[],[],[]]
csv_file = TEST_DIR + "db/test_checklist.csv"

body_items = []

header_not_found = 1
table_under_evaluation = 0
checklist_interrupted = 0

with open(csv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    for row in reader:
        if len(row) is 0: continue
        if OPERATION == "NONE":
            OPERATION = row[0]
        if header_not_found \
            and "Tag" == row[0]\
            and "Checkbox Text" == row[1]\
            and "Section Title" == row[4]:
            # print("FOUND")
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
                body_items[-1]['Dimensions'].append(dimension)
        elif table_under_evaluation:
            body_items[-1]['Contents'].append(row)
        elif 'PAGEBREAK' in row[0].upper():
            body_items.append('PAGEBREAK')
        else:
            body_items.append(
                {
                    'Tag' : row[0],
                    'Checkbox Text': row[1],
                    'Tutorial Text' : row[2],
                    'Image Filename' : row[3],
                    'Section Title' : row[4]
                }
            )
            # print(row)

body_text = []

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
    for k in range(len(dimensions)-1): tabular_line += 'c | '
    tabular_line += '}'
    
    body_text.append('\n\\begin{table}[h!]%\n')
    body_text.append('\\caption{'+f'{title}'+'}%\n')
    body_text.append('\\centering%\n')
    body_text.append(f'{tabular_line}%\n')
    body_text.append('\\hline%\n')
    
    # BUILD HEADERS
    for indx in range(len(dimensions)-1):
        dimension = dimensions[indx+1]
        dimension += 'pt'
        while dimension[0] == ' ': dimension = dimension[1:]
        item_text = '\\parbox{'+ f'{dimension}' + '}'+\
             '{\\hfill\\\\[-0.3em] \\centering \\textbf{'
             #Inverter} \\\\')
        range_num = int(int(dimensions[indx+1]) / 5)
        evaluated_contents = item['Contents'][0][indx]
        if len(evaluated_contents) <= range_num:
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
        if indx == (len(dimensions) - 2): item_text += ' \\\\%'
        else: item_text += ' &%'
        body_text.append(item_text + '\n')
    body_text.append('\\hline\n')
    body_text.append('\\hline\n')
    # BUILD TABLE OBJECTS
    contents = item['Contents']
    print(contents)
    for pre_indx in range(1,len(contents)):
        if 'HLINE' in item['Contents'][pre_indx][0].upper():
            body_text.append('\\hline\n')
            continue
        for indx in range(len(dimensions)-1):
            dimension = dimensions[indx+1]
            dimension += 'pt'
            while dimension[0] == ' ': dimension = dimension[1:]
            item_text = '\\parbox{'+ f'{dimension}' + '}'+\
                '{\\hfill\\\\[-0.3em] \\centering '
                #Inverter} \\\\')
            range_num = int(int(dimensions[indx+1]) / 5)
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
            if indx == (len(dimensions) - 2): item_text += ' \\\\%'
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
    
    
    
    
range_num = 50
for item in body_items:
    if item == 'PAGEBREAK':
        body_text.append('\pagebreak\n')
        continue
    while item['Checkbox Text'][0] == ' ': 
        item['Checkbox Text'] = item['Checkbox Text'][1:]
    if item['Tag'].upper() == 'HEADER':
        if len(body_text) and not checklist_interrupted:
            end_form()
        start_form(item['Checkbox Text'])
        checklist_interrupted = 0
    elif item['Tag'].upper() == 'START TABLE':
        build_table(item)
        checklist_interrupted = 1
    else:
        if len(item['Checkbox Text']) <= range_num:
            item_tag = item['Tag']
            item_text = item['Checkbox Text']
        else:
            item_tag = item['Tag']
            item_text = ''
            line_text = item['Checkbox Text']
            item['indx_point'] = 0
            sub_num = range_num - 1
            while len(line_text) > range_num:
                for base_indx in range(range_num):
                    indx_point = item['indx_point']
                    test_val = len(line_text)
                    indx = base_indx + indx_point
                    sub_indx = sub_num + indx_point
                    super_indx = range_num + indx_point
                    if line_text[sub_indx-indx] == ' ':
                        item_text += line_text[:sub_indx-indx]
                        item_text += '\\\\%\n\\indent\\space\\hspace{0.21in}%\n'
                        line_text = line_text[super_indx-indx:]
                        break
            item_text += line_text

        body_text.append('\\NewCheckBox{'+'%' + ' Label ID Below:')
        body_text.append(f'{item_tag}%')
        body_text.append('}{% Text Below:')
        body_text.append(f'{item_text}%')
        body_text.append('}%')

end_form()

# print(body_items)
# print(body_text)

with open(BODY_TEX, 'w') as f:
    for line in body_text:
        f.write(line + '\n')

for preTeX in preTexFiles:
    # print(preTeX)
    with open(preTeX,'r') as f:
        #  print(f)
         for line in f.readlines():
            if not len(line[1:]): continue
            line = parseLine(line)
            tex_lines.append(line)
         

with open(TEX_FILE, 'w') as f:
    f.writelines(tex_lines)

        
# print(csv_db)
