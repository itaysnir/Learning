#include <stdio.h>

char flag[100];
char* key = "3\rG[S/%\x1c\x1d#0?\rIS\x0f\x1c\x1d\x18;,4\x1b\x00\x1bp;5\x0b\x1b\x08\x45+";

void calc_flag(int* s){
	int i;
	for(i=0; i<100; i++){
		flag[i] = s[i] ^ key[i];
	}
	printf("%s\n", flag);
}

int main(int argc, char const *argv[])
{
	int password_array[100] = {99, 97, 116, 58, 32, 112, 97, 115, 115, 119, 111, 114, 100, 58, 32, 80, 101, 114, 109, 105, 115, 115, 105, 111, 110, 32, 100, 101, 110, 105, 101, 100, 10, 0};
	calc_flag (password_array);
	return 0;
}