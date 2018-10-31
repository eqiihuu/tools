# This script read the logfile of universal-eval and print the timestamps

import sys
import os
import argparse

sample_rate = 16000

parser = argparse.ArgumentParser(description='Input the log file path.')
parser.add_argument('-l', '--logfile', type=str, nargs='?', help='path of the log file')

args = parser.parse_args()
log_path = args.logfile
assert(os.path.exists(log_path))

with  open(log_path) as f:
    lines = f.readlines()

id = 1
for line in lines:
    if line.find('YES') != -1:
        segments = line.strip().split(' ')
        hotword = int(segments[2])
        start = float(segments[5].strip(','))/sample_rate
        end = float(segments[7].strip(','))/sample_rate
        start_hour = int(start / 3600)
        end_hour = int(end / 3600)
        start_minute = int((start - start_hour * 3600) / 60)
        end_minute = int((end - end_hour * 3600) / 60)
        start_second = start - start_hour * 3600 - start_minute * 60
        end_second = end - end_hour * 3600 - end_minute * 60
        print('%d: Hotword-%d %d:%d:%.1f ~ %d:%d:%.1f' % (id, hotword, start_hour, start_minute, start_second, end_hour, end_minute, end_second))
        id += 1
