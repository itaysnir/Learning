import struct

my_packet = "-" * 12 + "abcd"
s = my_packet.split('-')
a = my_packet.split('-')[0]
b = my_packet.split('-')[1]

guest_pw = '8b465d23cb778d3636bf6c4c5e30d031675fd95cec7afea497d36146783fd3a1'

print (len(guest_pw))

print(a)
print(b)
print(s)