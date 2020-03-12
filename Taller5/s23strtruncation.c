#include <string.h>
#include <stdio.h>

int main (int argc, char *argv[]) {
        char buf[12];
        char buf2[12] = "bbbbbbb";
        strncpy(buf, argv[1], sizeof(buf));
        printf("%s\n", buf);
        return 0;
}
