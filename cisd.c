#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

void cisd(size_t nocc, size_t nvir, double* data_1e, double* data_2e) {
    size_t nmo = nocc + nvir;

    int pid = getpid();

    char dirpath[128], filename_1e[128], filename_2e[128];

    sprintf(dirpath, "/tmp/cisd%zu", pid);
    sprintf(filename_1e, "%s/1e.dat", dirpath);
    sprintf(filename_2e, "%s/2e.dat", dirpath);

    mkdir(dirpath, 0755);

    FILE* file_1e = fopen(filename_1e, "w");
    fwrite(data_1e, sizeof(double), nmo * nmo, file_1e);
    fclose(file_1e);

    FILE* file_2e = fopen(filename_2e, "w");
    fwrite(data_2e, sizeof(double), nmo * nmo * nmo * nmo, file_2e);
    fclose(file_2e);

    // Actually call the python interface

    char command[256];
    sprintf(command, "./.venv/bin/python cisd.py %zu %zu %s %s", nocc, nvir,
            filename_1e, filename_2e);

    system(command);

    file_1e = fopen(filename_1e, "r");
    fread(data_1e, sizeof(double), nmo * nmo, file_1e);
    fclose(file_1e);

    file_2e = fopen(filename_2e, "r");
    fread(data_2e, sizeof(double), nmo * nmo * nmo * nmo, file_2e);
    fclose(file_2e);

    remove(filename_1e);
    remove(filename_2e);
    remove(dirpath);
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
