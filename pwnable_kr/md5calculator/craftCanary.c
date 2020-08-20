#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define FILEPATH "./canaryValue.txt"

int main(int argc, char const *argv[])
{
	int CAPTCHA = atoi(argv[1]);
	// time_t currentTime = atoi(argv[2]);
	srand (atoi(argv[2]));

	int canaryValue;
	int A[8] = { 0 };
	
	for (int i=0; i < 8; i++){
		A[i] = rand();
	}
	
	int part1 = A[1] + A[5];
    //printf("Part1: %d\n", part1);
    int part2 = A[2] - A[3];
    //printf("Part2: %d\n", part2);
    int part3 = A[7];
    //printf("Part3: %d\n", part3);
    int part4 = A[4] - A[6];
    //printf("Part4: %d\n", part4);
    int total = part1 + part2 + part3 + part4;
    //printf("Total is %d\n", total);
    canaryValue = CAPTCHA - total;
    printf("%d", canaryValue);

	FILE *f = fopen (FILEPATH, "w");
	fprintf(f, "%d", canaryValue);
	fclose (f);

	return 0;
}

