#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BINARY_NAME "./debug" // to change back to ./input
#define WANTED_ARGC 100

int main(int argc, char const *argv[])
{
	char *args [WANTED_ARGC + 1] = {0};
	for (int i=0; i<WANTED_ARGC + 1; i++){
		args[i] = "~";
		if (i == 0){args[i] = BINARY_NAME;}
		if (i=='A'){args[i] = "\x00";}
		if (i=='B'){args[i] = "\x20\x0a\x0d";}
		if (i==WANTED_ARGC){args[i] = NULL;	}
	}

	execvp (BINARY_NAME,args);

	return 0;
}