
import sys
import os
import json
import hashlib
from scapy.all import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class PCAPChallengeSolver:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file
        self.packets = rdpcap(pcap_file)
        self.encryption_key = None
        self.chunks = {}

    def _extract_npm_json(self, packet):
        
        try:
            if Raw not in packet:
                return None
            
            data = packet[Raw].load.decode('utf-8', errors='ignore')
            if 'HTTP/1.1 200 OK' not in data:
                return None

            
            json_start = data.find('{')
            if json_start == -1:
                return None
                
            json_data = data[json_start:]
            return json.loads(json_data)
        except:
            return None

    def _extract_encryption_key(self):
        
        print("[+] Searching for encryption key in NPM traffic...")
        
        for packet in self.packets:
            if Raw not in packet:
                continue

            json_data = self._extract_npm_json(packet)
            if not json_data:
                continue

            
            if '_key' in json_data:
                key_hex = json_data['_key']
                if len(key_hex) == 64:  
                    self.encryption_key = bytes.fromhex(key_hex)
                    print(f"[+] Found key: {key_hex}")
                    return True

        return False

    def _decrypt_chunk(self, encrypted_data):
        
        if not encrypted_data or len(encrypted_data) < 29:  
            return None
            
        try:
            iv = encrypted_data[:12]
            tag = encrypted_data[-16:]
            ciphertext = encrypted_data[12:-16]
            
            cipher = Cipher(
                algorithms.AES(self.encryption_key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            return decryptor.update(ciphertext) + decryptor.finalize()
        except Exception as e:
            print(f"[-] Decryption error: {e}")
            return None

    def _extract_http_content(self, packet):
        
        if Raw not in packet:
            return None, None

        try:
            data = packet[Raw].load
            if b"POST /upload" not in data:
                return None, None

            
            headers, body = data.split(b"\r\n\r\n", 1)
            
            
            chunk_key = None
            for header in headers.split(b"\r\n"):
                if b"X-Chunk-Id:" in header:
                    chunk_key = int(header.split(b": ")[1])
                    break

            return chunk_key, body
        except:
            return None, None

    def _extract_chunks(self):
        
        print("[+] Extracting encrypted chunks from C2 traffic...")
        chunk_count = 0

        for packet in self.packets:
            chunk_key, encrypted_data = self._extract_http_content(packet)
            if chunk_key is None or encrypted_data is None:
                continue

            decrypted = self._decrypt_chunk(encrypted_data)
            if decrypted:
                self.chunks[chunk_key] = decrypted.decode('utf-8')
                chunk_count += 1

        print(f"[+] Found {chunk_count} encrypted chunks")
        return chunk_count > 0

    def _reassemble_shadow_file(self):
        
        if not self.chunks:
            return None

        try:
            
            shadow_content = ''
            for i in range(max(self.chunks.keys()) + 1):
                if i not in self.chunks:
                    print(f"[-] Missing chunk {i}")
                    return None
                shadow_content += self.chunks[i]
            print(shadow_content)
            return shadow_content
        except Exception as e:
            print(f"[-] Error reassembling file: {e}")
            return None

    def solve(self):
        
        print("[+] Starting solution...")
        
        
        if not self._extract_encryption_key():
            print("[-] Failed to find encryption key")
            return None

        
        if not self._extract_chunks():
            print("[-] Failed to extract encrypted chunks")
            return None

        
        print("[+] Reassembling shadow file...")
        shadow_content = self._reassemble_shadow_file()
        if not shadow_content:
            print("[-] Failed to reassemble shadow file")
            return None

        
        print("[+] Calculating flag...")
        flag_hash = hashlib.sha256(shadow_content.encode()).hexdigest()
        flag = f"METACTF{{{flag_hash}}}"
        
        
        return flag

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pcap_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    if not os.path.exists(pcap_file):
        print(f"[-] File not found: {pcap_file}")
        sys.exit(1)

    solver = PCAPChallengeSolver(pcap_file)
    flag = solver.solve()
    
    if flag:
        print(f"\n[+] Found flag: {flag}")
    else:
        print("\n[-] Failed to solve challenge")

if __name__ == "__main__":
    main()

