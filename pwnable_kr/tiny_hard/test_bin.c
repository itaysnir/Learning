#include <stdio.h>

int main(int argc, char *argv[])
{
	printf("Hello there, just got argc: %d\n", argc);
	printf("program name address: %p\n", argv);
	printf("program name value: %s\n", argv[0]);
	printf("first arg address: %p\n", argv[1]);
	printf("first arg value: %s\n", argv[1]);
	
	return 0;
}