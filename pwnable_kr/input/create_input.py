import struct
import os, subprocess
import time
import socket

PROGRAM_NAME = './debug'
FILE_NAME = '\x0a'

def main():

#	stdin_string = r"\x00\x0a\x00\xff"
#	cmd = (("echo", "-e", "-n", "meow"), stdout=subprocess.PIPE)
#	ps = subprocess.Popen (cmd)
	env_name = "\xde\xad\xbe\xef"
	env_data = "\xca\xfe\xba\xbe"
	stdin_string = "\x00\x0a\x00\xff"
	stderr_string = "\x00\x0a\x02\xff"
	stdin_r, stdin_w = os.pipe()
	stderr_r, stderr_w = os.pipe()
	s = socket.socket()
	network_string = "\xde\xad\xbe\xef"

	my_env = os.environ.copy()
	my_env[env_name] = env_data

	with open (FILE_NAME, 'w') as f:
		
		data = "\x00\x00\x00\x00"
		f.write (data)
		print ("SUCCESS WRITING TO FILE")

	c = os.fork()
	if c ==0:
		# a VERY cool trick to pass null byte in python!
		time.sleep(0.1)
		# os.execv (PROGRAM_NAME, [PROGRAM_NAME] + ['A'] * (ord ('A')-1) + [''] + ['\x20\x0a\x0d'] +['B'] * (33))
		subprocess.Popen ([PROGRAM_NAME] + ['A'] * (ord ('A')-1) + [''] + 
			['\x20\x0a\x0d'] + ['8200'] + ['B'] * (32), stdin = stdin_r, stderr = stderr_r, env = my_env)

	else:
		os.close (stdin_r)
		os.close (stderr_r)
		print ("Parent writing to pipes")

		stdin_w = os.fdopen(stdin_w, 'w')
   		stdin_w.write(stdin_string)

   		stderr_w = os.fdopen (stderr_w, 'w')
   		stderr_w.write(stderr_string)

   		stdin_w.close()
   		stderr_w.close()

   		time.sleep(1)

   		s.connect (('127.0.0.1',8200))
   		s.send (network_string)
   		
   		s.close()

	#os.system (cmd)  #+ " | " + PROGRAM_NAME)

	return

if __name__ == '__main__':
	main()