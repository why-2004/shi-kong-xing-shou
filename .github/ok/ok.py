#!/usr/bin/python

from hashlib import md5
import os
import re

def check_md5(file_, compare):
	'''
	Returns True/False
	'''
	with open(file_, 'rb') as f:
		return md5(f.read()).hexdigest() == compare.lower()

def check_dr(dir_, rom_size, per_file=False):
	'''
	Returns how many bytes are decoded
	'''
	undecoded_bytes = 0
	flist = {}
	for i in os.walk(dir_):
		dir_ = i[0]
		files = [f for f in i[2] if f.endswith('.asm')]
		if files:
			for file_ in files:
				with open(os.path.join(dir_, file_), 'r', encoding="ISO-8859-1") as fn:
					if os.path.join(dir_, file_) not in files:
						flist[os.path.join(dir_, file_)] = 0
					for line in fn:
						dr_match = re.search(r'dr\s+(\$[0-9a-fA-F]+),\s+(\$[0-9a-fA-F]+)', line)
						if dr_match:
							start = int(dr_match.group(1)[1:], 16)
							end = int(dr_match.group(2)[1:], 16)
							if per_file:
								flist[os.path.join(dir_, file_)] += (end - start)
							else:
								undecoded_bytes += (end - start)
	if per_file:
		return flist
	else:
		return (rom_size - undecoded_bytes)

def check_syms(symfile):
	'''
	Returns how many symbols are unknown
	'''
	undoc = 0
	partdoc = 0
	totals = 0
	with open(symfile, 'r') as syms:
		for line in syms:
			sym_match = re.search(r'[0-9a-fA-F]{2}:[0-9a-fA-F]{4}\s+(\w+)', line)
			if sym_match:
				totals += 1
				label = sym_match.group(1)
				found_undoc = re.search(r'^Func_|^unk_|^asm_|^w[cd]|^hFF', label)
				found_part = re.search(r'^Layout_|^Metatiles_|^Blocks_|^AttrMap_|^Palettes_|^Collision_|^Script_|^text_|^gfx_|^unkText_|^PointerTable_|^palette_|^image_', label)
				if found_undoc:
					undoc += 1
				if found_part:
					partdoc += 1
	return (totals, undoc, partdoc)

if __name__ == '__main__':
	exit_state = 0
	
	# check matching
	print('\nMatching ROM: ', end='')
	if check_md5('shi_kong_xing_shou.gbc', '24e73734490ad40f9d8228a80ff15c0b'):
		print('OK')
	else:
		print('MISMATCHED')
		exit_state += 1
	
	# check percentage
	with open('baserom.gbc', 'rb') as rom:
		rom.seek(0, 2)
		rom_size = rom.tell()
		bytes = check_dr('.', rom_size)
		print('\nDisassembled:\n\t%d out of %d bytes (%.2f%%)' %
			(
				bytes,
				rom_size,
				(bytes/rom_size) * 100
			)
		)
	
	# check symfile
	totals, undoc, partdoc = check_syms('shi_kong_xing_shou.sym')
	print('\nDecoded symbols:\n\tTotal: %d\n\tDocumented: %d (%.2f%%)\n\tPartially documented: %d (%.2f%%)\n\tUndocumented: %d (%.2f%%)' %
		(
			totals,
			totals-undoc-partdoc, (totals-undoc-partdoc)/totals*100,
			partdoc, partdoc/totals*100,
			undoc, undoc/totals*100
		)
	)
	
	exit(exit_state)
