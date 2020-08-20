#include <stdio.h>
#include <stdlib.h>

int main(int args, char* argv[]) {

        long timestamp = atol(argv[1]);
        int captcha = atoi(argv[2]);
        // printf("%ld\n", timestamp);
        srand(timestamp);
        int randoms[8] = { 0 };
        int total = 0;
        for(int i = 0; i < 8; ++i) {
                /*if(i == 3 || i == 6)
                        total -= rand();
                else
                        total += rand();*/
                randoms[i] = rand();
                //printf("%d ", randoms[i]);
        }
        int part1 = randoms[1] + randoms[5];
        //printf("Part1: %d\n", part1);
        int part2 = randoms[2] - randoms[3];
        //printf("Part2: %d\n", part2);
        int part3 = randoms[7];
        //printf("Part3: %d\n", part3);
        int part4 = randoms[4] - randoms[6];
        //printf("Part4: %d\n", part4);
        total = part1 + part2 + part3 + part4;
        //printf("Total is %d\n", total);
        int canary = captcha - total;
        printf("%d", canary);
        return 0;
}