#!/usr/bin/env python3
import re
import sys
from lib.gbtool import *

if len(sys.argv) < 2:
	print(f'{sys.argv[0]} address')
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
	
	# current bank
	bank_, start_ = offset2addr(start)
	
	selection = ''
	while selection.lower() != 'e':
		cx = addr_str(offset2addr(rom.tell()))
		cy = hex(rom.tell())[2:]
		print(f'({cx}, ${cy}) [W]arp / [H]eader / [E]nd? ', end="")
		selection = input()
		
		if selection.lower() == 'h':
			# is header
			# extract map data
			mb  = get_number(rom, 1)
			mt1 = get_number(rom, 1)
			mt2 = get_number(rom, 1)
			mt3 = get_number(rom, 1)
			ma  = get_number(rom, 2)
			
			ma_location = get_symbol(rom_sym, addr2offset(mb, ma))
			print(f'\t; map XXXXX')
			print(f'\tdb BANK({ma_location})')
			print(f'\tds 3 ; {mt1} {mt2} {mt3}')
			print(f'\tdw {ma_location}')
			print()
		
		elif selection.lower() == 'w':
			# is warp
			x = get_number(rom, 1)
			y = get_number(rom, 1)
			gb = get_number(rom, 2)
			bank = get_number(rom, 1)
			u1 = get_number(rom, 1)
			u2 = get_number(rom, 1)
			u3 = get_number(rom, 1)
			objv = get_number(rom, 2)
			mapv = get_number(rom, 2)
			
			obv = get_symbol(rom_sym, addr2offset(bank, objv))
			mpv = get_symbol(rom_sym, addr2offset(bank_, mapv))
			print(f'\t; warp {x}, {y}, ${hex(gb)[2:]}, {obv}, {mpv}')
			print(f'\tdb {x}, {y}')
			print(f'\tdw ${hex(gb)[2:]}')
			print(f'\tdb BANK({obv})')
			print(f'\tds 3 ; {u1} {u2} {u3}')
			print(f'\tdw {obv}')
			print(f'\tdw {mpv}')
			print()
		
		else:
			pass
	
