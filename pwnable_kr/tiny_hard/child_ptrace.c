#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

char my_buffer[1024];
void main()
{
	int fd = open("/home/meow/Documents/pwnable_kr/Learning/pwnable_kr/tiny_hard/source", O_RDONLY);
	ssize_t bytes_read = read(fd, my_buffer, 50);
	printf("Just read %d bytes, message:%s\n",bytes_read, my_buffer);
}
