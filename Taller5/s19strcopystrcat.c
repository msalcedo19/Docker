#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main (int argc, char* argv[]) {
	    char fullname[62];
        if (argc < 3)
                return 1;
        strcpy(fullname, argv[1]);
        strcat(fullname, " ");
        strcat(fullname, argv[2]);
        printf("fullname : %s\n", fullname);
        return 0;
}
