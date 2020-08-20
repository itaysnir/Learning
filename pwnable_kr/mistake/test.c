#include <stdio.h>
#include <fcntl.h>

int main(int argc, char const *argv[])
{
	int fd;
	fd = open("./txt_file",O_RDONLY,0400) < 0  ; 

	int boolea = 1 < 2;
	printf ("True is %d\n", boolea);
	// fd = open("./txt_file",'r') < 0  ; 
	printf ("The fd is: %d\n", fd);

	return 0;
}