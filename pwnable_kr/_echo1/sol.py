import socket, struct
import pwn

HOST = 'pwnable.kr'
PORT = 9010

def main():
	
	s = socket.socket()
	s.connect((HOST,PORT))
	# data = s.recvall()
	# print(data)

	return

if __name__ == '__main__':
	main()