import sys

assert len(sys.argv) == 2


result_list = sys.argv[1]

with open(result_list, 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

f_correct = open('result/correct.txt', 'w')
f_wrong = open('result/wrong.txt', 'w')
prev_line = ''
for line in lines:
    if '.wav' in prev_line:
        sample_path = prev_line.split(' ')[-1]
        if 'YES' in line:
            f_correct.write(sample_path+'\n')
        else:
            f_wrong.write(sample_path + '\n')
    prev_line = line

f_correct.close()
f_wrong.close()


