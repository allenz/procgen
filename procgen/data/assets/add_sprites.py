import xml.etree.ElementTree as ET
from PIL import Image
from pathlib import Path
from shutil import copy2
from os.path import expanduser

"""
mkdir kenney && cd kenney
wget https://kenney.nl/content/3-assets/17-toon-characters-1/kenney_tooncharacters1.zip
unzip kenney_tooncharacters1.zip
export DIR=~/procgen/procgen/data/assets/
mkdir $DIR/kenney/Players/128x256/Abstract
cp "$DIR/kenney-abstract/Players/Player Blue/playerBlue_stand.png" $DIR/kenney/Players/128x256/Abstract/alienAbstract_stand.png
cp "$DIR/kenney-abstract/Players/Player Blue/playerBlue_up2.png" $DIR/kenney/Players/128x256/Abstract/alienAbstract_jump.png
cp "$DIR/kenney-abstract/Players/Player Blue/playerBlue_walk1.png" $DIR/kenney/Players/128x256/Abstract/alienAbstract_walk1.png
cp "$DIR/kenney-abstract/Players/Player Blue/playerBlue_walk2.png" $DIR/kenney/Players/128x256/Abstract/alienAbstract_walk2.png
"""

BASE = expanduser('~/g/kenney/')
OUTBASE = expanduser('~/procgen/procgen/data/assets/kenney/Players/128x256/')

chars = ['Female adventurer/Tilesheet/character_femaleAdventurer_sheetHD',
        'Female person/Tilesheet/character_femalePerson_sheetHD',
        'Male adventurer/Tilesheet/character_maleAdventurer_sheetHD',
        'Male person/Tilesheet/character_malePerson_sheetHD',
        'Robot/Tilesheet/character_robot_sheetHD',
        'Zombie/Tilesheet/character_zombie_sheetHD',]
colors = ["F1","F2","M1","M2","Robot","Zombie"]

names = ['idle','jump','walk0','walk1']
outnames = ['stand','jump','walk1','walk2']

wi, hi = 192, 256
wo, ho = 128, 256

for char, color in zip(chars, colors):
	Path(OUTBASE + color).mkdir(exist_ok=True)
	f_img = BASE + char + '.png'
	f_xml = BASE + char + '.xml'
	for name, outname in zip(names, outnames):
		outfile = OUTBASE + color + '/alien' + color + '_' + outname + '.png'
		tree = ET.parse(f_xml)
		e = tree.find("SubTexture[@name='{}']".format(name))
		x, y, w, h = [int(e.attrib[s]) for s in ['x', 'y', 'width', 'height']]

		# We need to resize since QPainter::draw_image() apparently doesn't
		# copy2(f_img, outfile)
		img = Image.open(f_img)
		img = img.crop((x,y,x+w,y+h)) # size (192, 256)
		img = img.resize((wo, round(wo/wi*ho)))
		# mybe https://www.imagemagick.org/Usage/filter/#support
		# img = ImageOps.pad(img, (128,256))
		img.save(outfile, 'PNG')
