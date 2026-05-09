
import struct

def get_dll_arch(path):
    with open(path, 'rb') as f:
        # DOS Header
        if f.read(2) != b'MZ':
            return "Not a PE file"
        f.seek(60)
        pe_offset = struct.unpack('<I', f.read(4))[0]
        f.seek(pe_offset)
        if f.read(4) != b'PE\0\0':
            return "Invalid PE header"
        machine = struct.unpack('<H', f.read(2))[0]
        if machine == 0x14c:
            return "x86 (32-bit)"
        elif machine == 0x8664:
            return "x64 (64-bit)"
        else:
            return hex(machine)

print(f"Tolk.dll: {get_dll_arch('Tolk.dll')}")
print(f"nvdaControllerClient64.dll: {get_dll_arch('nvdaControllerClient64.dll')}")
