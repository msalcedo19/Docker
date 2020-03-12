#include <string.h>
#include <stdio.h>

int main (int argc, char *argv[]) {
        int i = 0;
        char buf[128];
        char *arg1 = argv[1];
        while (arg1[i] != '\0') {
                buf[i] = arg1[i++];
        }
        buf[i] = '\0';
        printf("%s", buf);
}
