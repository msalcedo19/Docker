#include <stdio.h>
#include <stdlib.h>

int main (int argc , char *argv[]) {
        int i, j, n = atoi(argv[1]);
        for (j = 0; j < n; j++) {
                int *x = malloc(n * sizeof(int));
                for (i = 1; i < n; i++) {
                        x[i] += x[i-1] + i;
                }
                printf("%d\n", x[n-1]);
                free(x);
        }
        return 0;
}
