#include <stdio.h>

char *gets (char *dest) {
        int c = getchar();
        char *p = dest;
        while (c != EOF && c != '\n') {
                *p++ = c;
                c = getchar();
        }
        *p = '\0';
        return dest;
}

int main (int argc, char* argv[]) {
        char buf[12];
        gets(buf);
        printf("%s", buf);
}
