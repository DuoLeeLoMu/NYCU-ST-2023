# include <stdio.h>

int global_arr[5] = {1, 2, 3, 4, 5} ;

int main() {
    printf("%d\n", global_arr[5]) ;
    global_arr[5] = 6 ;
    return 0 ;
}
