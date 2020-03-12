#include <string.h>
#include <stdio.h>

#define MAX_BUF 256
int main (int argc, char *argv[]) {
        char buf[MAX_BUF];
        short len = strlen(argv[1]);
        if (len < MAX_BUF)
                strcpy(buf, argv[1]);
        printf("%s", buf);
}
