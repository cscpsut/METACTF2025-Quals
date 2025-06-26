#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <iomanip>
#include "obfuscator.hpp"
#include <winternl.h>
#include <windows.h>
#include <stdio.h>

#define FLG_HEAP_ENABLE_TAIL_CHECK   0x10
#define FLG_HEAP_ENABLE_FREE_CHECK   0x20
#define FLG_HEAP_VALIDATE_PARAMETERS 0x40
#define NT_GLOBAL_FLAG_DEBUGGED (FLG_HEAP_ENABLE_TAIL_CHECK | FLG_HEAP_ENABLE_FREE_CHECK | FLG_HEAP_VALIDATE_PARAMETERS)

PVOID g_pLastVeh = nullptr;
std::string userFlag;

#pragma comment (lib, "user32.lib")
#pragma comment(lib, "ntdll.lib")

#ifndef _PEB_DEFINED
#define _PEB_DEFINED
typedef struct _PEB {
    BOOLEAN InheritedAddressSpace;
    BOOLEAN ReadImageFileExecOptions;
    BOOLEAN BeingDebugged;
    union {
        BOOLEAN BitField;
        struct {
            BOOLEAN ImageUsesLargePages : 1;
            BOOLEAN IsProtectedProcess : 1;
            BOOLEAN IsImageDynamicallyRelocated : 1;
            BOOLEAN SkipPatchingUser32Forwarders : 1;
            BOOLEAN IsPackagedProcess : 1;
            BOOLEAN IsAppContainer : 1;
            BOOLEAN IsProtectedProcessLight : 1;
            BOOLEAN SpareBits : 1;
        };
    };
    HANDLE Mutant;
    PVOID ImageBaseAddress;
    PVOID SubSystemData;
    PVOID ProcessHeap;
    PRTL_CRITICAL_SECTION FastPebLock;
    PVOID AtlThunkSListPtr;
    PVOID IFEOKey;
    union {
        ULONG CrossProcessFlags;
        struct {
            ULONG ProcessInJob : 1;
            ULONG ProcessInitializing : 1;
            ULONG ProcessUsingVEH : 1;
            ULONG ProcessUsingVCH : 1;
            ULONG ProcessUsingFTH : 1;
            ULONG ReservedBits0 : 27;
        };
    };
    union {
        PVOID KernelCallbackTable;
        PVOID UserSharedInfoPtr;
    };
    ULONG SystemReserved[1];
    ULONG AtlThunkSListPtr32;
    PVOID ApiSetMap;
    ULONG TlsExpansionCounter;
    PVOID TlsBitmap;
    ULONG TlsBitmapBits[2];
    PVOID ReadOnlySharedMemoryBase;
    PVOID HotpatchInformation;
    PVOID* ReadOnlyStaticServerData;
    PVOID AnsiCodePageData;
    PVOID OemCodePageData;
    PVOID UnicodeCaseTableData;
    ULONG NumberOfProcessors;
    ULONG NtGlobalFlag;
    LARGE_INTEGER CriticalSectionTimeout;
    SIZE_T HeapSegmentReserve;
    SIZE_T HeapSegmentCommit;
    SIZE_T HeapDeCommitTotalFreeThreshold;
    SIZE_T HeapDeCommitFreeBlockThreshold;
    ULONG NumberOfHeaps;
    ULONG MaximumNumberOfHeaps;
    PVOID* ProcessHeaps;
} PEB, * PPEB;
#endif

DWORD checkNtGlobalFlag() {
    PPEB ppeb = (PPEB)__readgsqword(0x60);
    DWORD myNtGlobalFlag = *(PDWORD)((PBYTE)ppeb + 0xBC);
    if (myNtGlobalFlag & NT_GLOBAL_FLAG_DEBUGGED) return 1; else return 0;
}

//BOOL checkBeingDebugged() {
//    PPEB peb = (PPEB)__readgsqword(0x60);
//    return peb->BeingDebugged;
//}
//
//BOOL checkRemoteDebuggerPresent() {
//    BOOL isDebuggerPresent = FALSE;
//    CheckRemoteDebuggerPresent(GetCurrentProcess(), &isDebuggerPresent);
//    return isDebuggerPresent;
//}
//
//BOOL checkDebuggerPresentAPI() {
//    return IsDebuggerPresent();
//}

__declspec(noinline) static BOOL performAntiDebuggingChecks() {
    BOOL debuggerDetected = FALSE;

    //// Check 2: BeingDebugged flag
    //if (checkBeingDebugged()) {
    //    debuggerDetected = TRUE;
    //}

    //// Check 3: Remote debugger
    //if (checkRemoteDebuggerPresent()) {
    //    debuggerDetected = TRUE;
    //}

    //// Check 4: IsDebuggerPresent API
    //if (checkDebuggerPresentAPI()) {
    //    debuggerDetected = TRUE;
    //}

    if (checkNtGlobalFlag()) {
        debuggerDetected = TRUE;
    }

    return debuggerDetected;
}

using namespace ob;

class RC4 {
private:
    std::vector<unsigned char> S;

public:
    RC4(const std::string& key) {
        S.resize(256);
        for (int i = 0; i < 256; i++) {
            S[i] = i;
        }

        int j = 0;
        for (int i = 0; i < 256; i++) {
            j = (j + S[i] + key[i % key.length()]) % 256;
            std::swap(S[i], S[j]);
        }
    }

    std::vector<unsigned char> encrypt(const std::vector<unsigned char>& data) {
        std::vector<unsigned char> result = data;
        int i = 0, j = 0;

        for (size_t k = 0; k < data.size(); k++) {
            i = (i + 1) % 256;
            j = (j + S[i]) % 256;
            std::swap(S[i], S[j]);
            unsigned char keystream = S[(S[i] + S[j]) % 256];
            result[k] = data[k] ^ keystream;
        }

        return result;
    }

    std::vector<unsigned char> decrypt(const std::vector<unsigned char>& data) {
        return encrypt(data);
    }
};

std::string generateKeyObfuscated() {
    std::string key;

    int base = 32;
    key += char(base + 65);
    key += char(base + 83);
    key += char((100 + 7) & 0xFF);
    key += char(base + 65);
    key += char(110 ^ 0);
    key += char(50 * 2);
    key += char(117 | 0);
    key += char(230 / 2);
    key += char(208 >> 1);
    key += char(194 / 2);
    key += char(54 * 2); 
    key += char(216 >> 1);
    key += char(57 * 2);
    key += char(202 >> 1);
    key += char(198 >> 1);
    key += char(59 * 2);

    return key;
}

__declspec(noinline) static bool checkFlag(const std::string& userInput) {
    // Obfuscated encrypted flag bytes
    auto encryptedFlag = STR("\x8e\x43\x1e\xa7\xe2\x40\x11\x14\x7d\x3c\x89\x82\xf3\x81\x9a\x06\x6f\x26\xfc\x94\x09\xd1\x22\x68\x0b\x4c\xdf\xe7\x30\x4e\x83\xf3\x04\x08\xa1\x14\x88\xa7\xd1\x38\x39\x0f\xd9\x0a\xde");

    std::vector<unsigned char> encryptedBytes;
    for (int i = 0; i < 45; i++) {
        encryptedBytes.push_back((unsigned char)encryptedFlag[i]);
    }

    std::string rc4Key = generateKeyObfuscated();

    RC4 cipher(rc4Key);

    std::vector<unsigned char> decryptedFlag = cipher.decrypt(encryptedBytes);

    std::string actualFlag(decryptedFlag.begin(), decryptedFlag.end());

    size_t nullPos = actualFlag.find('\0');
    if (nullPos != std::string::npos) {
        actualFlag = actualFlag.substr(0, nullPos);
    }

    return userInput == actualFlag;
}

void displayWelcome() {
    std::cout << std::endl;
    std::cout << STR("shrimple, all i want is a flag: ");
}

void displaySuccess() {
    std::cout << std::endl;
    std::cout << STR("if you see this message, u probably solved the challenge, n1c3 0n3") << std::endl;
}

void displayFailure() {
    std::cout << std::endl;
    std::cout << STR("these flags will come with a 100% tariff increase if you keep getting this wrong.") << std::endl;
}


LONG WINAPI ExeptionHandler2(PEXCEPTION_POINTERS pExceptionInfo)
{
    if (checkFlag(userFlag)) {
        displaySuccess();
    }
    else {
        displayFailure();
    }
    ExitProcess(0);
}

LONG WINAPI ExeptionHandler1(PEXCEPTION_POINTERS pExceptionInfo)
{
    if (g_pLastVeh)
    {
        RemoveVectoredExceptionHandler(g_pLastVeh);
        g_pLastVeh = AddVectoredExceptionHandler(TRUE, ExeptionHandler2);
        if (g_pLastVeh)
            __debugbreak();
    }
    ExitProcess(0);
}


int main() {
    if (performAntiDebuggingChecks()) {
        MessageBoxA(NULL, STR("Access denied - good luck debugging this:)"), STR("Nah"), MB_OK | MB_ICONERROR);
        return -1;
    }
    displayWelcome();

    //std::string userFlag;
    std::getline(std::cin, userFlag);
    
    g_pLastVeh = AddVectoredExceptionHandler(TRUE, ExeptionHandler1);
    if (g_pLastVeh)
        __debugbreak();

    std::cout << std::endl;
    std::cout << STR("Press Enter to exit...") << std::endl;
    std::cin.get();

    return 0;
}