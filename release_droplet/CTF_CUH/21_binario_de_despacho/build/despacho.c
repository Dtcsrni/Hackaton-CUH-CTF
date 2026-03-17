#include <stdio.h>
    #include <string.h>

    int main(void) {
        char input[128];
        puts("Validador de despacho CUH");
        if (!fgets(input, sizeof(input), stdin)) {
            return 1;
        }
        input[strcspn(input, "\r\n")] = 0;
        size_t len = strlen(input);
        if (len != strlen("DESP-4729-CUH")) {
            puts("rechazado");
            return 1;
        }
        if (input[0] != 'D' || input[1] != 'E' || input[2] != 'S' || input[3] != 'P') { puts("rechazado"); return 1; }
if (input[4] != '-') { puts("rechazado"); return 1; }
if (input[5] + input[6] + input[7] + input[8] != ('4' + '7' + '2' + '9')) { puts("rechazado"); return 1; }
if (input[9] != '-' || input[10] != 'C' || input[11] != 'U' || input[12] != 'H') { puts("rechazado"); return 1; }
        if (strcmp(input, "DESP-4729-CUH") == 0) {
            puts("aceptado");
            return 0;
        }
        puts("rechazado");
        return 1;
    }
