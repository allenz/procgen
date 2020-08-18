import cv2
from PIL import Image
from os.path import expanduser
import numpy as np
import re
from tqdm import tqdm

"""
This file processes the C++ resources listing at SRC, computes the average
(dominant) color of each sprite, and writes the result to COLORS. In each line
of COLORS, the first three bytes represents the average color and the rest of
the line represents the sprite path.
"""

SRC = expanduser("~/procgen/procgen/src/resources.cpp")
RE_IMGS = re.compile(r'sprite_paths = std::vector<std::string>{([^}]+)};')
ASSETS = expanduser("~/procgen/procgen/data/assets/")
COLORS = ASSETS + 'colors.bin'

def avg_color(file):
	# https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
	img = np.float32(Image.open(ASSETS + file))
	img = img.reshape((-1, img.shape[-1]))
	if img.shape[-1] == 4:
		img = img[img[:,3] > 0] # remove transparent background
		img = img[:,:3]

	n_colors = 4
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
	flags = cv2.KMEANS_RANDOM_CENTERS
	_, labels, palette = cv2.kmeans(img, n_colors, None, criteria, 10, flags)
	_, counts = np.unique(labels, return_counts=True)
	return palette[np.argmax(counts)].round().astype(np.uint8)[:3]

# read existing file
img_map = {} # map img filename to avg color
with open(COLORS, 'rb') as f:
	rows = f.read().split(b'\n')
assert not rows[-1]
for row in rows[:-1]:
	img_map[row[3:]] = row[:3]

# add new files
with open(SRC) as f:
	files = RE_IMGS.search(f.read()).group(1).split(',')
	files = [file.strip().strip('"') for file in files]
	if not files[-1]:
		files = files[:-1]
	for i, file in enumerate(tqdm(files)):
		file_b = file.encode('utf8')
		if True: # file_b not in img_map:
			color = avg_color(file).tobytes()
			img_map[file_b] = color
			# print(file, np.frombuffer(color, dtype=np.uint8))

# write output
with open(COLORS, 'wb') as f:
	for file, color in img_map.items():
		f.write(color)
		f.write(file + b'\n')
