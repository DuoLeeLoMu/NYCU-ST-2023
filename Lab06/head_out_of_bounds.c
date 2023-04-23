# include <stdio.h>
# include <stdlib.h>
# include <string.h>

int main() {
    char *str = malloc(4) ;
    str[4] = 'a' ;
    printf("%c\n", str[4]) ;
    free(str) ;
    return 0 ;
}
