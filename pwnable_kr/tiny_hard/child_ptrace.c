#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/ptrace.h>

void main()
{
	ptrace(PTRACE_TRACEME, 0, 0, 0);

}