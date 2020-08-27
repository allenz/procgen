import urllib.request
from subprocess import run
from pathlib import Path
import numpy as np
from PIL import Image

"""
Generate sprites for player (white.png), barrier (red.png),
good objects (foods), and bad objects (animals) at a fixed resolution.
"""
resolution = 32

DL_URL = 'https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/'
BASE = Path.home()/'Desktop'
svg_dir = BASE/'svg'
INKSCAPE = BASE/'Tools/inkscape/inkscape.exe'

FOOD_DIR = BASE/'food'
FOOD_DIR.mkdir(exist_ok=True)
FOODS = ['1f33d',
	'1f344', '1f345', '1f346', '1f347', '1f348', '1f349', '1f34a', '1f34b', '1f34c', '1f34d', '1f34e',
	'1f350', '1f351', '1f352', '1f353',
	'1f951', '1f952', '1f955', '1f95d',
	'1f966', '1f96c', '1f96d']

ANIMAL_DIR = BASE/'animal'
ANIMAL_DIR.mkdir(exist_ok=True)
ANIMALS = ['1f400', '1f402', '1f405', '1f407', '1f40a', '1f40b', '1f40c', '1f40d',
	'1f411', '1f412', '1f413', '1f419', '1f41b', '1f41d', '1f41e', '1f41f',
	'1f421', '1f424', '1f426', '1f427', '1f429', '1f42c',
	'1f433']

white = np.full((resolution, resolution, 4), 255, dtype=np.uint8)
red = np.full((resolution, resolution, 4), 255, dtype=np.uint8)
red[..., 1:3] = 0
Image.fromarray(white).save(str(BASE/'white.png'))
Image.fromarray(red).save(str(BASE/'red.png'))

for outdir, imgs in [(FOOD_DIR, FOODS), (ANIMAL_DIR, ANIMALS)]:
	for code in imgs:
		svg_f = svg_dir/(code+'.svg')
		png_f = outdir/(code+'.png')
		if png_f.exists():
			continue
		urllib.request.urlretrieve(DL_URL + code + '.svg', svg_f)
		run([INKSCAPE, 'z', '-f', str(svg_f), '-w', str(resolution), '-j', '-e', str(png_f)])
		print(png_f)
