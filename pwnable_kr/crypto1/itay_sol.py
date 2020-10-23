import socket
import struct
import hashlib

PORT=9006
#HOST='pwnable.kr' # switch to 127.0.0.1 to run faster from pwnable
HOST='127.0.0.1'
CHUNK=1024


def getCipher(data):
	a = data
	return a[a.find('(')+1:a.find(')')]


def leakByte(i, cookie):
	
	rel_id = '' + '\n'
	rel_pw = '-' * (64 - 2 - 1 - i) + '\n'
	rel_pkt = rel_id + rel_pw
	s = socket.socket()
	s.connect((HOST,PORT))
	# welcome
	data = s.recv(CHUNK)
	s.send(rel_id)
	data = s.recv(CHUNK)
	s.send(rel_pw)
	data = s.recv(CHUNK)
	rel_cipher = getCipher(data)

	for c in '1234567890abcdefghijklmnopqrstuvwxyz-_':
		cur_id = '' + '\n'
		cur_pw = '-' * (64 -1 - 1 - i) + cookie + c + '\n'
		cur_pkt = cur_id + cur_pw
		s = socket.socket()
		s.connect((HOST,PORT))
		# welcome
		data = s.recv(CHUNK)
		s.send(cur_id)
		data = s.recv(CHUNK)
		s.send(cur_pw)
		data = s.recv(CHUNK)
		cur_cipher = getCipher(data)
		if cur_cipher[:128] == rel_cipher[:128]:
			return c
	
	return -1

def adminLogin(cookie):
	c_id = 'admin'
	pw = hashlib.sha256(c_id+cookie).hexdigest()+'\n'
	c_id += '\n'
	s = socket.socket()
	s.connect((HOST,PORT))
	s.send(c_id)
	s.send(pw)
	s.recv(CHUNK)
	s.recv(CHUNK)
	flag = s.recv(CHUNK)
	print(flag)
	
def main():
	
	solved_cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
	adminLogin(solved_cookie)
	cookie = ''
	for i in range(50):
		c = leakByte(i, cookie)
		cookie += c
		print(cookie)

	return


if __name__ == '__main__':
	main()
        
        




