import argparse
import os
import glob
import datetime
import shutil
import struct

def read_ips_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    assert data[:5] == b'PATCH', 'Invalid IPS file'
    patches = []
    i = 5
    while data[i:i+3] != b'EOF':
        offset = struct.unpack('>I', b'\x00' + data[i:i+3])[0]
        i += 3
        size = struct.unpack('>H', data[i:i+2])[0]
        i += 2
        if size == 0:
            rle_size = struct.unpack('>H', data[i:i+2])[0]
            i += 3
            patches.append((offset, rle_size))
        else:
            patches.append((offset, size))
            i += size
    return patches

def compare_patches(patch_files):
    all_patches = {}
    for file in patch_files:
        patches = read_ips_file(file)
        for offset, length in patches:
            if offset in all_patches:
                if all_patches[offset] != length:
                    return False, f"Conflict detected in file: {file}"
            else:
                all_patches[offset] = length
    return True, "No conflicts. Files are in harmony."

def apply_ips_patch(patchpath, filepath):
    patchfile = open(patchpath, 'rb')
    target = open(filepath, 'r+b')

    if patchfile.read(5) != b'PATCH':
        raise Exception('Invalid patch header.')

    r = patchfile.read(3)
    patch_size = os.path.getsize(patchpath)
    while patchfile.tell() not in [patch_size, patch_size - 3]:
        offset = struct.unpack('>I', b'\x00' + r)[0]
        r = patchfile.read(2)
        size = struct.unpack('>H', r)[0]

        if size == 0:
            r = patchfile.read(2)
            rle_size = struct.unpack('>H', r)[0]
            data = patchfile.read(1) * rle_size
        else:
            data = patchfile.read(size)

        target.seek(offset)
        target.write(data)
        r = patchfile.read(3)

    if patch_size - 3 == patchfile.tell():
        trim_size = struct.unpack('>I', b'\x00' + patchfile.read(3))[0]
        target.truncate(trim_size)

    target.close()
    patchfile.close()

def apply_patches(patch_files, rom_path):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    base, ext = os.path.splitext(rom_path)
    new_rom_path = f"{base}_{timestamp}{ext}"

    shutil.copyfile(rom_path, new_rom_path)
    for patch_file in patch_files:
        apply_ips_patch(patch_file, new_rom_path)

    return new_rom_path

def main():
    parser = argparse.ArgumentParser(description='Compare and apply IPS patches to a ROM file.')
    parser.add_argument('-d', '--directory', required=True, help='Directory containing IPS files')
    parser.add_argument('-r', '--rom', required=True, help='Path to the ROM file')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        sys.exit(1)

    if not os.path.isfile(args.rom):
        print(f"Error: {args.rom} is not a valid ROM file")
        sys.exit(1)

    patch_files = glob.glob(os.path.join(args.directory, '*.ips'))
    if not patch_files:
        print("No IPS files found in the directory.")
        sys.exit(1)

    in_harmony, message = compare_patches(patch_files)
    print(message)
    if in_harmony:
        new_rom = apply_patches(patch_files, args.rom)
        print(f"All patches applied successfully. New ROM file created: {new_rom}")
    else:
        print("Patches not applied due to conflicts.")

if __name__ == "__main__":
    main()
