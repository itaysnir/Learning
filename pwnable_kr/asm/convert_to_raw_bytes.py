

FILENAME = './testo'

def bytes_string (num_bytes):
	
	output_string = ''
	for i in num_bytes:
		if (len (hex(ord(i))[2:]) < 2):
			curr_byte = r'\x' + '0' + hex(ord(i))[2:]
		else:
			curr_byte = r'\x' + hex(ord(i))[2:]

		output_string += curr_byte
		
	return output_string


def main():

	with open (FILENAME, 'r') as f:
		data = f.read()

	print (bytes_string(data))

if __name__ == '__main__':
	main()