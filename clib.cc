#include <iostream>
#include <cstdlib>
#include <stdint.h>

using namespace std;

float uint16_to_float(int value, float min, float range)
{
    return min + range * 1.52590218966964e-05 * value;
}

void uint8_to_float_v2(const uint8_t* data, float * ans, float * col_header_flt, int rows)
{
    float p0 = col_header_flt[0], p25 = col_header_flt[1], p75 = col_header_flt[2], p100 = col_header_flt[3];
    for (int k = 0; k < rows; ++k) {
        int value = data[k];  // not necessary "static_cast<unsigned int>(data[i])"
        if (value <= 64) {
            ans[k] = p0+(p25-p0)/64.*value;
        } else if (value <= 192) {
            ans[k] = p25+(p75-p25)/128.*(value - 64);
        } else {
            ans[k] = p75+(p100-p75)/63.*(value - 192);
        }
    }
}

class Matrix
{
    private:
        const uint8_t * dataFixed;
        uint16_t * colHeaders;
        int cols;
        int rows;
        int sizeHeader;
        float globMin;
        float globRange;

    public:
        Matrix(const uint8_t * initDataFixed, uint16_t* initColHeaders, float initGlobMin, float initGlobRange, int numRows);
        Matrix(fstream * file, int offset);

        ~Matrix(void);
        void decompress(float * dataFloat);
};


Matrix::Matrix(const uint8_t * initDataFixed, uint16_t * initColHeaders, float initGlobMin, float initGlobRange, int numRows)
{
    dataFixed = initDataFixed;
    colHeaders = initColHeaders;
    globMin = initGlobMin;
    globRange = initGlobRange;
    cols = 40;
    rows = numRows;
    sizeHeader = 4;
}


// Directly use C++ to read data from file
Matrix::Matrix(fstream * file, int offset)
{

}


Matrix::~Matrix(void)
{
}


void Matrix::decompress(float * dataFloat)
{
    for (int i = 0; i < cols; ++i) {
        float col_header_flt[sizeHeader];
        for (int j = 0; j < sizeHeader; ++j) {
            col_header_flt[j] = uint16_to_float(colHeaders[i*sizeHeader+j], globMin, globRange);
        }
        uint8_to_float_v2(dataFixed+i*rows, dataFloat+i*rows, col_header_flt, rows);
    }
}


extern "C"
{
    Matrix* Matrix_new(uint8_t * initDataFixed, uint16_t * initColHeaders, float initGlobMin, float initGlobRange, int numRows)
    {return new Matrix(initDataFixed, initColHeaders, initGlobMin, initGlobRange, numRows);}

    void Matrix_decompress(Matrix* mat, float * dataFloat) {mat->decompress(dataFloat);}

}


int main()
{
    float a = uint16_to_float(100, -99, 200);
    cout<< a << '\n';
}
