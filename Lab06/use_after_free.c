# include <stdlib.h>

int main() {
    int *ptr = malloc(5 * sizeof(int)) ;
    free(ptr) ;
    return ptr[1] ;
}
