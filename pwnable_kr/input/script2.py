import os
import random
import socket
import time
import subprocess
PATH = './debug'
# PATH = "/home/input2/input"

os.system("ln -s /home/input2/flag flag")
port = random.randrange(10000, 20000)
args = ["0"] * 99
args[ord("A")-1] = ""
args[ord("B")-1] = "\x20\x0a\x0d"
args[ord("C")-1] = str(port)

stdinr, stdinw = os.pipe()
stderrr, stderrw = os.pipe()

os.write(stdinw, "\x00\x0a\x00\xff")
os.write(stderrw, "\x00\x0a\x02\xff")

environ = {"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"}

with open("\x0a", "wb") as f:
    f.write(b"\x00\x00\x00\x00")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pro = subprocess.Popen([PATH]+args, stdin=stdinr, stderr=stderrr, env=environ)

time.sleep(2)
s.connect(("127.0.0.1", port))
s.send("\xde\xad\xbe\xef")
s.close()