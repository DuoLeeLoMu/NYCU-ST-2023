# include <stdio.h>
# include <stdlib.h>

int main(int argc, char **argv) {
    int *a = malloc(8 *sizeof(int)) ;
    int *b = malloc(8 *sizeof(int)) ;
    int res = a[argc+12] ;
    free(a) ;
    free(b) ;
    return res ;
}
