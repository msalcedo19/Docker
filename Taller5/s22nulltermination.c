#include <string.h>
#include <stdio.h>

int main (int argc, char *argv[]) {
        char a[16];
        char b[16];
        char c[32];
        strcpy(a, argv[1]);
        strcpy(b, argv[2]);
        strcpy(c, a);
        strcat(c, b);
        printf("%s\n%s\n%s\n", a, b, c);
        return 0;
}
