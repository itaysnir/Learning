#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
	char *buffer = "START HERE\n";
	// printf ("%d, %d\n", sizeof(buffer),strlen(buffer));
	write (STDOUT_FILENO, buffer, strlen(buffer)+1);

	char *dst_buf;
	char src_buf[20] = "very cool test\n";
	dst_buf = (char *) malloc (20 * sizeof (char));
	strcpy (dst_buf, src_buf);
	write (STDOUT_FILENO, dst_buf, strlen(dst_buf)+1);
	return 0;
}