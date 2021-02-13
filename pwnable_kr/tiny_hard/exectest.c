#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/ptrace.h>


char *ARG = "/bin/sh";
char exploit[] = "cat /home/meow/Documents/pwnable_kr/Learning/pwnable_kr/tiny_hard/source > /home/meow/Documents/pwnable_kr/Learning/pwnable_kr/tiny_hard/DESTTT\n";
char *child_trace = "/home/meow/Documents/pwnable_kr/Learning/pwnable_kr/tiny_hard/child_ptrace";

int main()
{
	struct user_regs_struct regs = { 0 };
	int status;
	int pipefd[2];
    if (pipe(pipefd) < 0) {
        perror("pipe");
        return -1;
    }
	pid_t pid = fork();
    if (-1 == pid) {
        perror("fork");
        return -1;
    }

    if (0 == pid) {
    	close(pipefd[1]);
        dup2(pipefd[0], 0);
    	//printf("[*] Child entered\n");
        execl(child_trace, child_trace, NULL);
        perror("execl");
    }
    else {
	//printf("[*] Parent entered. Child pid: %d\n", pid);
    	close(pipefd[0]);
        write(pipefd[1], exploit, sizeof(exploit));
        wait(&status);
        printf("Child started, status: %d\n", status);
        ptrace(PTRACE_GETREGS, pid, 0, &regs);
        printf("Registers values:\nEAX:%08x\nORIG_EAX:%08x\nEBX:%08x\nECX:%08x\nEDX:%08x\nESP:%08x\nEBP:%08x\nEIP:%08x\n\n\n\n\n\n", regs.eax, regs.orig_eax, regs.ebx, regs.ecx, regs.edx, regs.esp, regs.ebp, regs.eip);

    }
	return 0;
}