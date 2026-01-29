#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void cisd(size_t nocc, size_t nvir, double* data_1e, double* data_2e) {
    
}

int main() {
    double data_1e[] = {-0.48444168, 0.0, 0.0, 0.45750194};
    double a = 0.626402500, b = 0.621706763, c = 0.196790583, d = 0.653070747;
    double data_2e[] = {a,   0.0, 0.0, b,   0.0, c, c, 0.0,
                        0.0, c,   c,   0.0, b,   0, 0, d};

    cisd(1, 1, data_1e, data_2e);

    printf("[%7.3f %7.3f]\n[%7.3f %7.3f]\n", data_1e[0], data_1e[1], data_1e[2],
           data_1e[3]);
}
