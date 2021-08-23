#!/usr/bin/env python3
import re
import sys
from lib.gbtool import *

if len(sys.argv) < 3:
	print(f'{sys.argv[0]} address count')
	print('\taddress can be in BB:AAAA form or as a hex number')
	exit(0)

addr_str = lambda x: '%03x:%04x' % x

# extract symbols
with open('shi_kong_xing_shou.sym', 'r') as sym:
	string = sym.read()
	symbol = read_symbols(string)
	rom_sym = symbol['rom']
	ram_sym = symbol['ram']

# get rom
with open('baserom.gbc', 'rb') as rom:
	s = sys.argv[1]
	s_= re.match('([0-9a-fA-F]+):([0-9a-fA-F]{4})$', s)
	if s_:
		start = addr2offset(*str2addr(s))
	else:
		start = int(s, 16)
	
	rom.seek(start)

	count = int(sys.argv[2])

	while count != 0:
		count -= 1
		bank, address = offset2addr(rom.tell())
		print(f'{get_symbol(rom_sym, rom.tell())}:')
		while True:
			byte = int.from_bytes(rom.read(1), "little")

			if byte == 0x00:
				print("\tscr_cont")

			elif byte == 0x01:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_01 $%02x, $%02x ; TEMP" % (arg1, arg2))

			elif byte == 0x02:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_delay $%02x, $%02x ; TEMP" % (arg1, arg2))

			elif byte == 0x03:
				print("\tscr_03")

			elif byte == 0x04:
				arg = int.from_bytes(rom.read(2), "little")
				sym = get_symbol(rom_sym, addr2offset(bank, arg))
				print("\tscr_04 %s" % sym)

			elif byte == 0x05:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_face $%02x ; TEMP" % arg)

			elif byte == 0x06:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_06 $%02x, $%02x ; TEMP" % (arg1, arg2))

			elif byte == 0x07:
				print("\tscr_07")

			elif byte == 0x08:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_08 $%02x ; TEMP" % arg)

			elif byte == 0x09:
				print("\tscr_end")
				print("")
				break

			elif byte == 0x0a:
				arg1 = int.from_bytes(rom.read(2), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				arg3 = int.from_bytes(rom.read(2), "little")
				print("\tscr_checkbit %s, $%02x, %s" % (
							get_symbol(ram_sym, arg1),
							arg2,
							get_symbol(rom_sym, addr2offset(bank, arg3))
					))

			elif byte == 0x0b:
				arg1 = int.from_bytes(rom.read(2), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_setbit $%04x, $%02x ; TEMP" % (arg1, arg2))

			elif byte == 0x0c:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_setmap $%02x, $%02x ; TEMP" % (arg1, arg2))

			elif byte == 0x0d:
				arg = int.from_bytes(rom.read(2), "little")
				print("\tscr_0d $%04x ; TEMP" % arg)

			elif byte == 0x0e:
				print("\tscr_0e")

			elif byte == 0x0f:
				arg = int.from_bytes(rom.read(2), "little")
				print("\tscr_move $%04x ; TEMP" % arg)

			elif byte == 0x10:
				print("\tscr_10")

			elif byte == 0x14:
				arg = int.from_bytes(rom.read(2), "little")
				sym = get_symbol(rom_sym, addr2offset(bank, arg))
				print("\tscr_text %s" % sym)

			elif byte == 0x15:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_emote $%02x, $%02x ; TEMP" % (arg1, arg2))

			elif byte == 0x1a:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				arg3 = int.from_bytes(rom.read(1), "little")
				arg4 = int.from_bytes(rom.read(1), "little")
				print("\tscr_1a $%02x, $%02x, $%02x, $%02x ; TEMP" % (arg1, arg2, arg3, arg4))
			
			elif byte == 0x1b:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_1b $%02x ; TEMP" % arg)
			
			elif byte == 0x1c:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_1c $%02x ; TEMP" % arg)

			elif byte == 0x1f:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_1f $%02x ; TEMP" % arg)
			
			elif byte == 0x2a:
				new_bank = int.from_bytes(rom.read(1), "little")
				new_addr = int.from_bytes(rom.read(2), "little")
				print("\tscr_farjump %s" % get_symbol(rom_sym, addr2offset(new_bank, new_addr)))

			elif byte == 0x34:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				arg3 = int.from_bytes(rom.read(1), "little")
				print("\tscr_34 $%02x, $%02x, $%02x ; TEMP" % (arg1, arg2, arg3))

			elif byte == 0x35:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_35 $%02x ; TEMP" % arg)
			
			elif byte == 0x36:
				print("\tscr_36")

			elif byte == 0x37:
				print("\tscr_37")

			elif byte == 0x3b:
				arg = int.from_bytes(rom.read(2), "little")
				print("\tscr_3b %s" % get_symbol(rom_sym, addr2offset(bank, arg)))

			elif byte == 0x44:
				print("\tscr_44")

			elif byte == 0x48:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_48 $%02x, $%02x" % (arg1, arg2))
			
			elif byte == 0x4a:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_4a $%02x ; TEMP" % arg)
			
			elif byte == 0x4d:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_4d $%02x, $%02x" % (arg1, arg2))
			
			elif byte == 0x4e:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(2), "little")
				sym = get_symbol(rom_sym, addr2offset(bank, arg2))
				print("\tscr_4e $%02x, %s" % (arg1, sym))

			elif byte == 0x5e:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_5e $%02x ; TEMP" % arg)
			
			elif byte == 0x61:
				print("\tscr_61")
			
			elif byte == 0x62:
				arg1 = int.from_bytes(rom.read(1), "little")
				arg2 = int.from_bytes(rom.read(1), "little")
				print("\tscr_62 $%02x, $%02x ; TEMP" % (arg1, arg2))
			
			elif byte == 0x63:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_63 $%02x ; TEMP" % arg)
			
			elif byte == 0x65:
				arg = int.from_bytes(rom.read(1), "little")
				print("\tscr_65 $%02x ; TEMP" % arg)
			
			else:
				print("\tdb $%02x ; TEMP" % byte)
	
	print('; $%x' % rom.tell())
