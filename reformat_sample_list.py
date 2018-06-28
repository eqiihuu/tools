import sys

if len(sys.argv) != 4:
    print("Require 3 Parameters: action, src_file, dst_file ")
else:
    action = sys.argv[1]
    src_file = sys.argv[2]
    dst_file = sys.argv[3]

    if action == 'train':
        with open(src_file) as f:
            lines = f.readlines()
            samples = [line.strip() for line in lines]
        with open(dst_file, 'w') as f:
            for sample in samples:
                name = sample.split('/')[-1].split('.')[0]
                string = '%s!%s sox -V1 -t wav %s -t wav - | \n' % (name, name, sample)
                f.write(string)

    elif action == 'test':
        with open(src_file) as f:
            lines = f.readlines()
            samples = [line.split(' ')[5] for line in lines]

        with open(dst_file, 'w') as f:
            for sample in samples:
                f.write(sample+'\n')
    else:
        print("First Parameter should be either train or test")