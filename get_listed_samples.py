import sys
import os
import shutil

if len(sys.argv) != 4:
    print("Require 3 Parameters: list_file, src_dir, dst_dir ")
else:
    src_file = sys.argv[1]
    src_dir = sys.argv[2]
    dst_dir = sys.argv[3]
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        os.makedirs(dst_dir)
    with open(src_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        samples = [line.split('/')[-1] for line in lines]
    for sample in samples:
        src_path = os.path.join(src_dir, sample)
        if not os.path.exists(src_path):
            print('%s does not exist!' % src_path)
            continue
        dst_path = os.path.join(dst_dir, sample)
        shutil.copyfile(src_path, dst_path)
