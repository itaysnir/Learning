import socket
import struct

cook = 'you_will_never_guess_this_sugar_honey_salt_cookie'

PORT=9006
HOST='pwnable.kr' # switch to 127.0.0.1 to run faster from pwnable
CHUNK=1024

cookie = ''

def getCipher(data):
	a = data.decode()
	return a[a.find('(')+1:a.find(')')]


def leakByte():

	rel_id = '' + '\n'
	rel_pw = '-' * (64 - 2 - 1) + '\n'
	rel_pkt = rel_id + rel_pw
	s = socket.socket()
	s.connect((HOST,PORT))
	# welcome
	data = s.recv(CHUNK)
	s.send(rel_id.encode())
	data = s.recv(CHUNK)
	s.send(rel_pw.encode())
	data = s.recv(CHUNK)
	rel_cipher = getCipher(data)
	print(rel_cipher)

	for c in '1234567890abcdefghijklmnopqrstuvwxyz-_':
		cur_id = '' + '\n'
		cur_pw = '-' * (64 -1 - 1) + c + '\n'
		cur_pkt = cur_id + cur_pw
		s = socket.socket()
		s.connect((HOST,PORT))
		# welcome
		data = s.recv(CHUNK)
		s.send(cur_id.encode())
		data = s.recv(CHUNK)
		s.send(cur_pw.encode())
		data = s.recv(CHUNK)
		print(data)
		cur_cipher = getCipher(data)
		if cur_cipher == rel_cipher:
			cookie += 'c'
			break

	
	return 


def main():
	
	a = pwn.remote(HOST,PORT)
	leakByte()
	print (cookie)

	return


if __name__ == '__main__':
	main()
        
        



