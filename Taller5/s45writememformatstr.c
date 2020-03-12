#include <stdio.h>

int main (int argc, char* argv[]) {
        int i;
        printf("%s%n\n", argv[1], (int *)&i);
        printf("%d", i);
        return 0;
}
