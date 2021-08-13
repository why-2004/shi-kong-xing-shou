#!/usr/bin/python

from PIL import Image
import ok
import subprocess
import os
import sys

import requests
import json

# Generate image
base = os.path.dirname(__file__)

commit_hash = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE).communicate()[0].decode('ascii').strip()

if ok.check_md5('shi_kong_xing_shou.gbc', '24e73734490ad40f9d8228a80ff15c0b'):
	match_string = 'OK'
else:
	match_string = 'FAILED'

# check percentage
with open('baserom.gbc', 'rb') as rom:
	rom.seek(0, 2)
	rom_size = rom.tell()
	bytes = ok.check_dr('.', rom_size)

# check symfile
totals, undoc, partdoc = ok.check_syms('shi_kong_xing_shou.sym')

string = f'''
Build: OK

Match: {match_string}


Disassembled:

  {bytes}/{rom_size} ({(bytes/rom_size) * 100:.2f}%)


Symbols (ROM and RAM):

     Total: {totals}
  
  Complete: {totals-undoc-partdoc} ({(totals-undoc-partdoc)/totals*100:.2f}%)
  
   Partial: {partdoc} ({partdoc/totals*100:.2f}%)
  
     Undoc: {undoc} ({undoc/totals*100:.2f}%)
'''

x_tiles = 32
y_tiles = 23

fontimg = Image.open(os.path.join(base, 'font.png'))
boximg = Image.open(os.path.join(base, 'textbox.png'))

def getchar(c):
	i = ord(c) - ord(' ')
	y, x = divmod(i, 16)
	return fontimg.crop((x*8,y*8,x*8+8,y*8+8))

test = Image.new('RGB', (x_tiles*8, y_tiles*8), (255, 255, 255))

# render border
get_tile_in_row = lambda i, x: i.crop((x*8,0,x*8+8,8))
border_tiles = {
	'space': get_tile_in_row(boximg, 0),
	'tl': get_tile_in_row(boximg, 1),
	'tr': get_tile_in_row(boximg, 2),
	'bl': get_tile_in_row(boximg, 3),
	'vv': get_tile_in_row(boximg, 4),
	'hh': get_tile_in_row(boximg, 5),
	'egb_tl': get_tile_in_row(boximg, 6),
	'egb_tr': get_tile_in_row(boximg, 7),
	'egb_bl': get_tile_in_row(boximg, 8),
	'egb_br': get_tile_in_row(boximg, 9),
}

for yy in range(y_tiles):
	if yy == 0:
		# top
		for xx in range(x_tiles):
			if xx == 0:
				test.paste(
					border_tiles['tl'],
					(xx*8, yy*8)
				)
			elif xx == x_tiles-1:
				test.paste(
					border_tiles['tr'],
					(xx*8, yy*8)
				)
			else:
				test.paste(
					border_tiles['hh'],
					(xx*8, yy*8)
				)
	
	elif yy == y_tiles-2:
		for xx in range(x_tiles):
			if xx == 0:
				test.paste(
					border_tiles['vv'],
					(xx*8, yy*8)
				)
			elif xx == x_tiles-1:
				test.paste(
					border_tiles['egb_tr'],
					(xx*8, yy*8)
				)
			elif xx == x_tiles-2:
				test.paste(
					border_tiles['egb_tl'],
					(xx*8, yy*8)
				)
			else:
				test.paste(
					border_tiles['space'],
					(xx*8, yy*8)
				)
	
	elif yy == y_tiles-1:
		for xx in range(x_tiles):
			if xx == 0:
				test.paste(
					border_tiles['bl'],
					(xx*8, yy*8)
				)
			elif xx == x_tiles-2:
				test.paste(
					border_tiles['egb_bl'],
					(xx*8, yy*8)
				)
			elif xx == x_tiles-1:
				test.paste(
					border_tiles['egb_br'],
					(xx*8, yy*8)
				)
			else:
				test.paste(
					border_tiles['hh'],
					(xx*8, yy*8)
				)
	
	else:
		for xx in range(x_tiles):
			if xx == 0:
				test.paste(
					border_tiles['vv'],
					(xx*8, yy*8)
				)
			elif xx == x_tiles-1:
				test.paste(
					border_tiles['vv'],
					(xx*8, yy*8)
				)
			else:
				test.paste(
					border_tiles['space'],
					(xx*8, yy*8)
				)

# draw text
x_base = 1
y_base = 1
y_ = 0
for line in string.split('\n'):
	x_ = 0
	for char in line:
		test.paste(getchar(char), (x_base*8+(x_*8), y_base*8+(y_*8)))
		x_ += 1
	y_ += 1

test = test.resize((x_tiles*8*2, y_tiles*8*2), 0)
test.save(os.path.join(base, 'IMAGE.png'))

# Send off webhook
url = sys.argv[1]

embed_json = {
	"username": "巴克 (Buck)",
	"avatar_url": "https://cdn.discordapp.com/attachments/874592023204737044/875625368982269972/buckbox.png",
	"embeds": [
		{
			"title": "Build results",
			"description": "Commit #%s" % commit_hash,
			"image":{"url": "attachment://IMAGE.png"}
		}
	]
}

embed_files = {
	"payload_json": (None, json.dumps(embed_json), 'application/json'),
	"file1": open(os.path.join(base, 'IMAGE.png'), "rb")
}

requests.post(url, files=embed_files)
