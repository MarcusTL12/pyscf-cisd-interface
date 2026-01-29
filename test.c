#include <stdio.h>
#include <stdlib.h>

int main() {
    int code = system("bash");

    printf("%d\n", code);
}
