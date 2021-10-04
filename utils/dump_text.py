#!/usr/bin/env python3
import math
import sys
import re
from lib.gbtool import addr2offset, str2addr

chars = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

file = "baserom.gbc"

if len(sys.argv) < 3:
	print(f'{sys.argv[0]} address count')
	print('\taddress can be in BB:AAAA form or as a hex number')
	exit(0)

for line in open("charmap.asm"):
    # Get charset
    if line.startswith("NEWCHARMAP"):
        charset = int(line[18])

    if line.startswith("\tcharmap "):
        line = line[9:].split(";")[0].split(",")
        if len(line) != 2:
            continue

        char = line[0].strip()[1:-1]
        byte = int(line[1].strip()[1:], 16)

        # Remove duplicates in tuple
        if byte not in chars:
            chars[charset][byte] = char

file = open(file, "rb")

s = sys.argv[1]
s_= re.match('([0-9a-fA-F]+):([0-9a-fA-F]{4})$', s)
if s_:
	start = addr2offset(*str2addr(s))
else:
	start = int(s, 16)

file.seek(start)
count = int(sys.argv[2])

def print_text():
    global backup_charset
    done = 0
    while True:
        byte = int.from_bytes(file.read(1), "little")
        """
        if not byte:
            break
        """

        byte_high, new_charset = divmod(byte, 0x10)
        if byte_high == 0xf:
            backup_charset = new_charset
            byte = int.from_bytes(file.read(1), "little")
            char = chars[new_charset][byte]
            print(char, end="")
        elif byte == 0xe2:
            print("\";\n\tdone;")
            done = 1
            break
        elif byte == 0xe5:
            arg = int.from_bytes(file.read(2), "little")
            print("\";\n\tgetchoice $%04x; # TEMP" % arg, end="")
            done = 1
            break
        elif byte == 0xe6:
            print("\";\n\tchoice;", end="")
            done = 1
            break
        elif byte == 0xe7:
            print("\";\n\tunknownE7;", end="")
            break
        elif byte == 0xec:
            print("\";\n\tpara \"", end="")
        elif byte == 0xed:
            print("\";\n\tline \"", end="")
        elif byte == 0xee:
            print("\";\n\tcont \"", end="")
        else:
            try:
                char = chars[backup_charset][byte]
            except KeyError:
                char = 'UNKNOWN'
            print(char, end="")
        
    return done

def get_bank_address(offset):
    offset = file.tell()
    bank = math.floor(offset / 0x4000)
    if bank != 0:
        address = (offset - (bank * 0x4000)) + 0x4000
    else:
        address = (offset - (bank * 0x4000))
    return bank, address

while count != 0:
    bank, address = get_bank_address(file.tell())

    byte = int.from_bytes(file.read(1), "little")
    # print("{:02x}".format(byte))
    if not byte:
            print("not byte")
            break

    # get nybbles from byte
    byte_high, charset = divmod(byte, 0x10)
    backup_charset = charset
    if (byte == 0xe0) or (byte == 0xe1):
        print("@org $%02x, $%04x:" % (bank, address))
    if byte == 0xe0:
        arg1 = int.from_bytes(file.read(1), "little")
        arg2 = int.from_bytes(file.read(1), "little")
        print("\tinit $%02x, $%02x; # TEMP" % (arg1, arg2))
    if byte_high == 0xf:
        count -= 1
        print("\ttext \"", end="")
        if print_text():
            print()
        else:
            print("\"")

file.close()
