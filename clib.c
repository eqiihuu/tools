#include <stdio.h>
using namespace std;

float uint16_to_float(int value, float min, float range) {
    return min + range * 1.52590218966964e-05 * value;
}

class Matrix
{
    public:
    Matric(int** data, col_headers, float globmin, float globrange);
    decompress();

    private:
    int** data;
    int** col_headers;
    float globmin;
    float globrange;
    float** decm_data;
}


Matrix::Matrix(int** data, int**col_headers, float globmin, float globrange)
{
    this.data = data;
    this.col_headers = col_headers;
    this globmin = globmin;
    this.globrange = globrange;
    this.decm_data = new float*[40];
    for (int i = 0; i < 40; ++i) {
        decm_data[i] = new float[30];
    }
}


float** Matrix::decompress()
{
    for (int i = 0; i < 40; ++i) {
        float col_header_flt[4];
        for (int j = 0; j < 4; ++j) {
            col_header_flt[j] = uint16_to_float(this.col_headers[i][j], this.globmin, this.globrange)
        }
        this.decm_data[i] = uint8_to_float_v2(this.data[i], col_header_flt)
    }
    return this.decm_data;
}


//void CompressedMatrix::CopyToMat(int32 row_offset,
//                                  int32 col_offset,
//                                  MatrixBase<Real> *dest) const {
//   KALDI_PARANOID_ASSERT(row_offset < this->NumRows());
//   KALDI_PARANOID_ASSERT(col_offset < this->NumCols());
//   KALDI_PARANOID_ASSERT(row_offset >= 0);
//   KALDI_PARANOID_ASSERT(col_offset >= 0);
//   KALDI_ASSERT(row_offset+dest->NumRows() <= this->NumRows());
//   KALDI_ASSERT(col_offset+dest->NumCols() <= this->NumCols());
//   // everything is OK
//   GlobalHeader *h = reinterpret_cast<GlobalHeader*>(data_);
//   int32 num_rows = h->num_rows, num_cols = h->num_cols,
//       tgt_cols = dest->NumCols(), tgt_rows = dest->NumRows();
//
//   DataFormat format = static_cast<DataFormat>(h->format);
//   if (format == kOneByteWithColHeaders) {
//     PerColHeader *per_col_header = reinterpret_cast<PerColHeader*>(h+1);
//     uint8 *byte_data = reinterpret_cast<uint8*>(per_col_header +
//                                                 h->num_cols);
//
//     uint8 *start_of_subcol = byte_data+row_offset;  // skip appropriate
//     // number of columns
//     start_of_subcol += col_offset*num_rows;  // skip appropriate number of rows
//
//     per_col_header += col_offset;  // skip the appropriate number of headers
//
//     for (int32 i = 0;
//          i < tgt_cols;
//          i++, per_col_header++, start_of_subcol+=num_rows) {
//       byte_data = start_of_subcol;
//       float p0 = Uint16ToFloat(*h, per_col_header->percentile_0),
//           p25 = Uint16ToFloat(*h, per_col_header->percentile_25),
//           p75 = Uint16ToFloat(*h, per_col_header->percentile_75),
//           p100 = Uint16ToFloat(*h, per_col_header->percentile_100);
//       for (int32 j = 0; j < tgt_rows; j++, byte_data++) {
//         float f = CharToFloat(p0, p25, p75, p100, *byte_data);
//         (*dest)(j, i) = f;
//       }
//     }
//   } else if (format == kTwoByte) {
//     const uint16 *data = reinterpret_cast<const uint16*>(h+1) + col_offset +
//         (num_cols * row_offset);
//     float min_value = h->min_value,
//         increment = h->range * (1.0 / 65535.0);
//
//     for (int32 row = 0; row < tgt_rows; row++) {
//       Real *dest_row = dest->RowData(row);
//       for (int32 col = 0; col < tgt_cols; col++)
//         dest_row[col] = min_value + increment * data[col];
//       data += num_cols;
//     }
//   } else {
//     KALDI_ASSERT(format == kOneByte);
//     const uint8 *data = reinterpret_cast<const uint8*>(h+1) + col_offset +
//         (num_cols * row_offset);
//     float min_value = h->min_value,
//         increment = h->range * (1.0 / 255.0);
//     for (int32 row = 0; row < tgt_rows; row++) {
//       Real *dest_row = dest->RowData(row);
//       for (int32 col = 0; col < tgt_cols; col++)
//         dest_row[col] = min_value + increment * data[col];
//       data += num_cols;
//     }
//   }
// }

if __name__ == "__main__":
    float a = uint16_to_float(100, -99, 200);
    cout << a << '\n';