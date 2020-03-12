#include <stdio.h>

int main (int argc, char *argv[]) {
        char query[512];
        char buffer[512];
        sprintf(buffer,
                "SELECT username FROM users WHERE user_id ='%.50s'",
                argv[1]);
        printf("%s\n", buffer);
        sprintf(query, buffer);
        printf("%s\n", query);
        /*mysql_query(query);*/
}
