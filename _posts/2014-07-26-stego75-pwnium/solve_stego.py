# Author  : Matan M. Mates
# Purpose : Solve Stego75
import Image

# Color ladders
LADDER_RANGES = [((1,0) ,   (56,55)), 
			     ((57,0),  (112,55)),
			     ((113,0), (168,55)),
			     ((169,0), (224,55)),
			     ((225,0), (280,55)),
			     ((281,0), (336,55))]


# Build the table of bytes we need
LADDERS = []
for (z,t) in LADDER_RANGES:
	LADDERS += [(x,y) for (x,y) in zip(range(z[0], t[0] + 1), range(z[1],t[1] + 1))]

STEG_IMAGE = Image.open('Steg75.png').convert('RGBA')

def get_pixels(img, pixels):
	return [img.getpixel(pixel) for pixel in pixels]


def main():
	pixels = get_pixels(STEG_IMAGE, LADDERS)
	text = ''.join([chr((a-c) % 256) for (a,b,c,d) in pixels])
	print "Flag: " + text[:56].decode('base64')

if __name__ == '__main__':
	main()
