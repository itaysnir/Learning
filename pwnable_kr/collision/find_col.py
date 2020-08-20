import binascii
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
	# num1 = ('0' + hex(113626824) [2:]) .decode ("hex")
	#num2 = ('0' + hex (113626828) [2:]) .decode ("hex")
	num1 = 113626824
	num2 = 113626828
	
	total_string = bytes_string(num1) * 4 + bytes_string (num2)
	print (total_string)
	return

	# binary_data_1 = binascii.unhexlify ('06c5cec8')
	# print (binary_data_1)

if __name__ == '__main__':
	main()