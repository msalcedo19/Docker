#include <stdio.h>
#include <string.h>

int main (int argc, char *argv[]) {
        int j, i = atoi(argv[1]);
        char * my_str = "%s %s %s %s";
        char * my_str2 = " %s";
        for (j=0; j < i; j++){
                strcat(my_str, my_str2);
        }
        printf(my_str);
        return 0;
}
