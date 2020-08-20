#include <stdio.h>
#include <stdlib.h>

int main () {

	int status;
	char buffer[1000];
	//itoa (338150, buffer,10);
	// printf ("the number is: %d\n", atoi ("0"));
	status = sprintf (buffer, "%d", 338150);
	printf ("first password is: %s\n", buffer);
	// printf ("first password is: %s\n", itoa (13371337, buffer,10));
	return 0;
}