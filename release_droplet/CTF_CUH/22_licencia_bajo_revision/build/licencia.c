#include <stdio.h>
    #include <string.h>

    int main(void) {
        char input[128];
        puts("Licencia CUH en revision");
        if (!fgets(input, sizeof(input), stdin)) {
            return 1;
        }
        input[strcspn(input, "\r\n")] = 0;
        size_t len = strlen(input);
        if (len != strlen("CUH26-REV7-1142-LOCK")) {
            puts("rechazado");
            return 1;
        }
        if (strncmp(input, "CUH26", 5) != 0) { puts("rechazado"); return 1; }
if (input[5] != '-') { puts("rechazado"); return 1; }
if (strncmp(input + 6, "REV7", 4) != 0) { puts("rechazado"); return 1; }
if (input[10] != '-') { puts("rechazado"); return 1; }
if ((input[11]-'0') + (input[12]-'0') + (input[13]-'0') + (input[14]-'0') != 8) { puts("rechazado"); return 1; }
if (input[15] != '-') { puts("rechazado"); return 1; }
if (strncmp(input + 16, "LOCK", 4) != 0) { puts("rechazado"); return 1; }
        if (strcmp(input, "CUH26-REV7-1142-LOCK") == 0) {
            puts("aceptado");
            return 0;
        }
        puts("rechazado");
        return 1;
    }
