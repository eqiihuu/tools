import os

f_binary = open('data/raw_mfcc_librispeech_vqe_hires.22.ark')
f_seg = open('data/1/feats.scp')
data_list = []
data = {}
# First line
line = f_seg.readline().strip().split(' ')
data['id'] = line[0]
data['path'] = line[1].split(':')[0]
data['start'] = int(line[1].split(':')[1])

while 1:
    line = f_seg.readline().strip()
    if not line:
        break
    line = line.split(' ')
    data['end'] = int(line[1].split(':')[1])
    data_list.append(data)
    data = {}
    data['id'] = line[0]
    data['path'] = line[1].split(':')[0]
    data['start'] = int(line[1].split(':')[1])

print(data_list[:3])




