#include <stdio.h>

typedef struct  {
  int * labels;
  float *** features;
} Examples;


int multiply(int num1, int num2)
{
    int n = 0;
    for (int i = 0; i <100000; ++i) {
        n += 1;
    }
    return num1 * num2;
}

void read_file(FILE * f) {
    char str1[20];
    fscanf(f,"%s ",str1);
    printf("%s", str1);
}


Examples read_egs(char[] ark_path) {
    Examples egs;
    egs.labels = new int[10];
    egs.feature = new float**[10];
    for (int i = 0; i < 10; ++i) {
        egs.feature[i] = new float*[23];
        for (int j = 0; j < 23; ++j) {
            egs.feature[i][j] = new float[40]
        }
    }
    return egs;
}

int main(int argc, char *argv[]) {
    Examples egs = read_egs("tmp.txt");
    return 0;
}