#include <stdio.h>
#include <stdlib.h>

int *table = NULL;
int insert_in_table(int pos, int value){
        if (!table) {
                table = (int *) malloc(sizeof(int) * 100);
        }
        if (pos > 99) {
                return -1;
        }
        table[pos] = value;
        return 0;
}

int main (int argc, char *argv[]) {
        return insert_in_table(atoi(argv[1]), atoi(argv[2]));
}
