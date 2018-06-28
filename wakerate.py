import sys
import pdb

assert len(sys.argv) == 3

wav_list = sys.argv[1]
log_file = sys.argv[2]

with open(log_file, 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

start = False

list1 = []
buffer = []
for line in lines:
    if '.wav' in line:
        for item in buffer:
            if 'YES' in item:
                list1.append(filename)
                break
        buffer = []
        start = True
        filename = line.split(' ')[-1]
    elif start:
        buffer.append(line)

with open(wav_list, 'r') as f:
    lines = f.readlines()
    list2 = [line.strip() for line in lines]

print '%d/%d: %.2f%%' % (len(list1),len(list2),len(list1)/float(len(list2))*100.0)
