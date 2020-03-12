#include <stdio.h>
#include <limits.h>

int main (int argc, short *argv[]) {
        unsigned long n = UINT_MAX; //4294967295; 
        int m = atoi(argv[1]);
        if (n == m) {
                printf("Will this be printed ?\n");
        }
        printf("n = 0x%x\n", n);
        printf("m = 0x%x\n", m);
        return 0;
}
