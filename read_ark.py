import numpy as np
import sys, os, re
import time
import copy
import gc

import ctypes

clib = ctypes.cdll.LoadLibrary("./clib.so")


class Matrix(object):
    def __init__(self, data_fixed, col_headers, glob_min, glob_range, num_rows):
        data_type = np.ctypeslib.ndpointer(dtype=np.uint8)  # flags='c_contiguous'
        header_type = np.ctypeslib.ndpointer(dtype=np.uint16)
        clib.Matrix_new.argtypes = [data_type, header_type, ctypes.c_float, ctypes.c_float, ctypes.c_int]
        clib.Matrix_new.restype = ctypes.c_void_p

        ans_type = ctypes.POINTER(ctypes.c_float)
        # ans_type = np.ctypeslib.ndpointer(dtype=np.float32)
        clib.Matrix_decompress.argtypes = [ctypes.c_void_p, ans_type]
        clib.Matrix_decompress.restype = None

        self.obj = clib.Matrix_new(data_fixed, col_headers, glob_min, glob_range, num_rows)

    def decompress(self, ans):
        clib.Matrix_decompress(self.obj, ans)

    def get_matrix(self):
        return clib.Matrix_get_matrix(self.obj)

    def delete(self):
        clib.Matrix_delete(self.obj)


str_scale = '0.05650041 0.05735592 0.05522531 0.0511494 0.04412092 0.0499179 0.04703798 0.05111559 0.05365805 0.05459757 0.05229066 0.05489335 0.05983111 0.06496345 0.0690463 0.07643595 0.08496485 0.0993112 0.1238712 0.1573954 0.2273206 0.3836897 1.05652 1.98494 0.5740751 0.3598067 0.2728572 0.2342321 0.2086831 0.1990069 0.190391 0.1907221 0.1948006 0.1937644 0.2068325 0.2342431 0.238941 0.2661745 0.3093348 0.3530013 '
str_offset = '-6.840126 0.5238378 0.5119987 0.2633039 1.02675 0.1639121 0.4053167 0.6204673 0.7598802 0.3652654 0.6938077 0.2685322 0.5218956 0.2037287 0.4743526 0.2736759 0.2785844 -0.00926731 0.1192668 -0.09163697 0.1830888 0.0165769 0.09751914 0.002896077 -0.1656169 0.0009794156 -0.1869099 0.04733974 -0.1178754 0.08223968 -0.151346 0.02770026 -0.1372308 -0.02639182 -0.1415839 -0.0770141 -0.1457596 0.04200698 0.1398909 0.08422083 '

scale = np.array([float(ele) for ele in str_scale.strip().split()], dtype=np.float32)
offset = np.array([float(ele) for ele in str_offset.strip().split()], dtype=np.float32)


# Modify from https://github.com/vesis84/kaldi-io-for-python/blob/master/kaldi_io.py
def read_vec_int(f):
    assert(f.read(1).decode() == '\4'); # int-size
    vec_size = np.frombuffer(f.read(4), dtype='int32', count=1)[0] # vector dim
    vec = np.frombuffer(f.read(vec_size*4), dtype='int32', count=vec_size)
    return vec


def read_compressed_mat(f):
    # Mapping for percentiles in col-headers
    def uint16_to_float(value, min, range):
        return np.float32(min + range * 1.52590218966964e-05 * value)

    # Mapping for matrix elements
    def uint8_to_float_v2(vec, p0, p25, p75, p100):
        # Split the vector by masks
        mask_0_64 = (vec <= 64)
        mask_65_192 = np.all([vec>64, vec<=192], axis=0)
        mask_193_255 = (vec > 192)
        # Sanity check (useful but slow...)
        # assert(len(vec) == np.sum(np.hstack([mask_0_64,mask_65_192,mask_193_255])))
        # assert(len(vec) == np.sum(np.any([mask_0_64,mask_65_192,mask_193_255], axis=0)))
        # Build the float vector
        ans = np.empty(len(vec), dtype='float32')
        ans[mask_0_64] = p0 + (p25 - p0) / 64. * vec[mask_0_64]
        ans[mask_65_192] = p25 + (p75 - p25) / 128. * (vec[mask_65_192] - 64)
        ans[mask_193_255] = p75 + (p100 - p75) / 63. * (vec[mask_193_255] - 192)
        return ans

    # Format of header
    global_header = np.dtype([('minvalue','float32'),('range','float32'),('num_rows','int32'),('num_cols','int32')])
    per_col_header = np.dtype([('percentile_0','uint16'),('percentile_25','uint16'),('percentile_75','uint16'),('percentile_100','uint16')])
    # Read global header
    globmin, globrange, rows, cols = np.frombuffer(f.read(16), dtype=global_header, count=1)[0]
    # The data is structed as [Colheader, ... , Colheader, Data, Data , .... ]
    #                         {           cols           }{     size         }
    col_headers = np.frombuffer(f.read(cols*8), dtype=per_col_header, count=cols)
    data = np.reshape(np.frombuffer(f.read(cols*rows), dtype='uint8', count=cols*rows), newshape=(cols,rows)) # stored as col-major
    mat = np.zeros((cols,rows), dtype='float32')
    global decm_time
    t0 = time.time()
    for i, col_header in enumerate(col_headers):
        col_header_flt = [uint16_to_float(percentile, globmin, globrange) for percentile in col_header]
        mat[i] = uint8_to_float_v2(data[i], *col_header_flt)
    t1 = time.time()
    decm_time += t1 - t0
    return mat.T  # transpose! col-major -> row-major


# Copy from https://github.com/vesis84/kaldi-io-for-python/blob/master/kaldi_io.py
def read_compressed_mat_c(f):
    # Mapping for percentiles in col-headers
    global_header = np.dtype(
        [('minvalue', 'float32'), ('range', 'float32'), ('num_rows', 'int32'), ('num_cols', 'int32')])
    globmin, globrange, rows, cols = np.frombuffer(f.read(16), dtype=global_header, count=1)[0]

    col_headers = np.frombuffer(f.read(cols * 4 * 2), dtype=np.uint16, count=cols*4)
    data = np.frombuffer(f.read(cols * rows), dtype=np.uint8, count=cols * rows)

    m = Matrix(data, col_headers, globmin, globrange, rows)
    mat = (ctypes.c_float*(cols*rows))()
    # mat = np.zeros((cols*rows,), dtype=np.float32)

    global decm_time
    t0 = time.time()
    m.decompress(mat)
    t1 = time.time()
    decm_time += t1-t0
    ans = np.reshape(np.array(mat), newshape=(cols, rows)).T
    # print ans[0]
    return ans  # transpose! col-major -> row-major


def read_key(f):
    key = ''
    while 1:
        char = f.read(1).decode("latin1")
        if char == '' or char == ' ': break
        key += char
    key = key.strip()
    if key == '':
        return None  # end of file
    return key


def read_feature(f):
    header = f.read(14)
    header = header.decode().strip()
    assert(header == '<InputFrames>')
    format = f.read(3).decode()
    assert(format == 'CM ')
    # Read compressed Matrix
    feature = read_compressed_mat_c(f)
    # feature = feature * scale + offset
    return feature


def expand_context(feature):
    len_block = feature.shape[0]
    len_context = 23
    num_frame = len_block - len_context + 1
    ans = [feature[i:i+len_context, :] for i in range(0, num_frame)]
    return ans


def read_label(f):
    header = f.read(8).decode().strip()
    assert(header == '<Lab1>')
    label = read_vec_int(f)
    return label


def parse_label(txt):
    header = txt[0:8]
    assert (header == '<Lab1>')
    # label = parse_vec_int(txt[8:])
    return header


def read_ark_seq(file_path):
    fd = open(file_path, 'rb')
    key = read_key(fd)
    while key:
        binary = fd.read(2).decode()
        assert(binary == '\0B')
        nnet = fd.read(13).decode()
        assert(nnet == '<NnetExample>')
        label = read_label(fd)
        # print(key, label)
        feature = read_feature(fd)
        fd.read(52)  # skip
        yield key, feature, label
        key = read_key(fd)
    fd.close()


# Get the list of offsets from .scp file
def read_scp(file_path):
    f = open(file_path)
    lines = f.readlines()
    num_lines = len(lines)
    egs_list = []
    for i in range(num_lines):
        line = lines[i].split(' ')
        key = line[0]
        path = line[1].split(':')[0]
        start = int(line[1].split(':')[1])
        egs_list.append({'key': key, 'path': path, 'start': start, 'end': -1});
        if i > 0:
            egs_list[i-1]['end'] = start
    return egs_list


# Read a single block
def read_block(f, start, end):
    f.seek(start)
    binary = f.read(2).decode()
    assert (binary == '\0B')
    nnet = f.read(13).decode()
    assert (nnet == '<NnetExample>')
    label = read_label(f)
    feature = read_feature(f)
    return label, feature


def read_block_binary(f, start, end):
    f.seek(start)
    binary = f.read(2).decode()
    assert (binary == '\0B')
    nnet = f.read(13).decode()
    assert (nnet == '<NnetExample>')
    label = read_label(f)
    feature_binary = f.read(end-f.tell()).split('<SpkInfo>')[0]
    return label, feature_binary


def read_ark_rand_binary(scp_path, ark_path):
    egs_list = read_scp(scp_path)
    feature_list = []
    label_list = []
    for info in egs_list:
        f = open(ark_path)  # open(info['path'])
        label, feature = read_block_binary(f, info['start'], info['end'])
        feature_list.append(feature)
        label_list.append(label)
    return label_list, feature_list


def read_compressed_mat_c_binary(binaries):
    # Mapping for percentiles in col-headers
    global_header = np.dtype(
        [('minvalue', 'float32'), ('range', 'float32'), ('num_rows', 'int32'), ('num_cols', 'int32')])
    globmin, globrange, rows, cols = np.frombuffer(binaries[0:16], dtype=global_header, count=1)[0]

    col_headers = np.frombuffer(binaries[16:16+cols * 4 * 2], dtype=np.uint16, count=cols*4)
    data = np.frombuffer(binaries[16+cols * 4 * 2:16+cols * 4 * 2+cols * rows], dtype=np.uint8, count=cols * rows)
    m = Matrix(data, col_headers, globmin, globrange, rows)
    mat = (ctypes.c_float*(cols*rows))()
    # global decm_time
    # t0 = time.time()
    m.decompress(mat)
    # t1 = time.time()
    # decm_time += t1-t0
    ans = np.reshape(np.array(mat), newshape=(cols, rows)).T
    # print ans[0]
    return ans  # transpose! col-major -> row-major


def read_feature_binary(binaries):
    header = binaries[0:14]
    header = header.decode().strip()
    assert(header == '<InputFrames>')
    format = binaries[14:14+3].decode()
    assert(format == 'CM ')
    # Read compressed Matrix
    feature = read_compressed_mat_c_binary(binaries[14+3:])
    # feature = feature * scale + offset
    return feature


def read_ark_rand(scp_path, ark_path):
    # eg. file_path='/home/qihu/snowboy_tf/egs.1.scp'
    # scp_id = scp_path.split('/')[-1].split('.')[1]
    egs_list = read_scp(scp_path)
    feature_list = []
    label_list = []
    for info in egs_list[:-1]:
        f = open(ark_path)# open(info['path'])
        feature, label = read_block(f, info['start'], info['end'])
        feature_list += expand_context(feature)
        label_list += label.tolist()
    return label_list, feature_list


if __name__ == '__main__':
    ark_path = './data/ark/egs.1.ark'
	scp_path = './data/scp/egs.1.scp'
	# ark_path = '/home/snowboy/afs_data/qihu/xiaodu/ark/egs.1.ark'
    # scp_path = '/home/snowboy/afs_data/qihu/xiaodu/scp/egs.1.scp'

# -------------------------------------------------------------- #
    # Random access

#     t0 = time.time()
#     scp_list = read_scp(scp_path)
#     t1 = time.time()
#     decm_time = 0
#     id = 0
#
#     # read_ark_rand(scp_path, ark_path)
#     for scp in scp_list[:]:
#         f = open(ark_path)  # open(scp['path'])
#         start = scp['start']
#         end = scp['end']
#         label, feature = read_block(f, start, end)
#         print id, scp['key'], feature.shape
#         id += 1
#         # break
#     t2 = time.time()
#     print t1 - t0, t2 - t1, decm_time
# ---------------------------------------------------------------- #
    # Read sequencially

    # g = read_ark_seq(ark_path)
    # id = 0
    # features = []
    # labels = []
    # decm_time = 0
    # t0 = time.time()
    # for block in g:
    #     features += expand_context(block[1])
    #     labels += block[2].tolist()
    #     # print block[0], block[2], block[1][0]
    #     # break
    #     if len(labels) >= 2048:
    #         # break
    #         features = []
    #         exp_time = 0
    #         labels = []
    #     id += 1
    #     print id
    # print time.time()-t0
    t0 = time.time()
    label_list, feature_list = read_ark_rand_binary(scp_path, ark_path)
    t1 = time.time()
    print len(label_list), t1-t0
    id = 0
    for feature_binaries in feature_list:
        feature = read_feature_binary(feature_binaries)
        # print id
        id += 1
    t2 = time.time()
    print t2-t1

