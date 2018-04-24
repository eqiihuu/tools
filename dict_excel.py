import xlwt

en_path = './data/en.js'
zh_path = './data/zh-CN.js'
en_file = open(en_path)
zh_file = open(zh_path)
en_lines = en_file.readlines()
zh_lines = zh_file.readlines()
en_num = len(en_lines)
zh_num = len(zh_lines)
out_file = xlwt.Workbook()
sheet = out_file.add_sheet(u'sheet1', cell_overwrite_ok=True)
dict = {}
key_set = set()
for i in range(en_num):
    line = en_lines[i].split(':')
    if len(line) != 2:
        continue
    id = line[0]
    word = line[1].split('\'')[1]
    key_set.add(id)
    if id not in dict.keys():
        dict[id] = {}
    dict[id]['en'] = word

for i in range(zh_num):
    line = zh_lines[i].split(':')
    if len(line) != 2:
        continue
    id = line[0]
    key_set.add(id)
    word = line[1].split('\'')[1]
    if id not in dict.keys():
        dict[id] = {}
    dict[id]['zh'] = word

i = 1
for id in dict.keys():
    entry = dict[id]
    sheet.write(i, 0, id)
    if 'zh' in entry.keys():
        sheet.write(i, 1, entry['zh'].decode('utf-8'))
    if 'en' in entry.keys():
        sheet.write(i, 2, entry['en'])
    i += 1

out_file.save('./result/zh&en.xls')
print len(dict.keys()), len(key_set)