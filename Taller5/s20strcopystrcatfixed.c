#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main (int argc, char* argv[]) {
        if (argc < 3)
                return 1;
        char *fullname = (char *) malloc(strlen(argv[1]) + strlen(argv[2]) + 2);
        strcpy(fullname, argv[1]);
        strcat(fullname, " ");
        strcat(fullname, argv[2]);
        printf("fullname : %s\n", fullname);
        return 0;
}