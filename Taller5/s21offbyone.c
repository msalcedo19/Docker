#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[]) {
        char source[10];
        strcpy(source, argv[1]);
        char *dest = (char *) malloc(strlen(source));
        int i = 0;
        do {
                i ++;
                dest[i] = source[i];
        } while (i < 10);
        dest[i] = '\0';
        printf("dest = %s", dest);
}