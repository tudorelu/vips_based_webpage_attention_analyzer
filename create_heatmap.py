from PIL import Image
from PIL import ImageDraw
import sys

# Take the results obtained by running the Vips program (the images separating the webpage into blocks)
# For example take blocks8.png & page.png And place them in the same folder as this script.
# Also, make sure there is a folder called "block_results" in the same folder as this script, 
# as there is where the results are saved.

# Make sure you have PIL install (if not, install using pip)

# To run, simply call ` python create_heatmap.py ` to run. 


# CHANGE THIS LINE TO DETERMINE WHICH SEGMENTATION TO CHOOSE
Block_Image = './blocks8.png'
Original_Image = './page.png'

sys.setrecursionlimit(10000)

def lerp(a, b, value):
    return a * (1 - value) + b * value

def scaleImage(image, scale):
	width = int(round(image.size[0]*scale))
	height = int(round(image.size[1]*scale))
	return image.resize((width, height), Image.NEAREST)

# marks the whole block in which pixel[i,j] resides
def find_block_of_pixel(pixels, i, j):
	
	step = 1  # how many pixels away are the neighboring pixels 
	
	if i not in range(0,b_width) or j not in range(0,b_height):
		return
	
	r, g, b = pixels[i,j]
	
	if marked[k][i,j] or r>3 or g>3 or b>3:
		return

	# mark the pixel as part of the box number k
	marked[k][i,j] = True
	global_marked[i,j] = True

	# find this pixel in the original image
	ro, go, bo = o_pixels[i,j]
	
	# how colorful is the pixel? (0 -> grayscale, 255 -> intense color )
	rg = abs(ro - go)
	rb = abs(ro - bo)
	gb = abs(go - bo)
	diff[k] += rg + rb + gb	

    # find the top-left, top-right, bottom-left & b-right pixel
    # so that we can generate the box containing this block
	if minx[k]>i: minx[k]=i
	if maxx[k]<i: maxx[k]=i

	if miny[k]>j: miny[k]=j
	if maxy[k]<j: maxy[k]=j

	# check all my neighbouring pixels in the same way
	find_block_of_pixel(pixels, i,j+step)
	find_block_of_pixel(pixels, i,j-step)
	find_block_of_pixel(pixels, i+step,j-step)
	find_block_of_pixel(pixels, i+step,j)
	find_block_of_pixel(pixels, i+step,j+step)
	find_block_of_pixel(pixels, i-step,j-step)
	find_block_of_pixel(pixels, i-step,j)
	find_block_of_pixel(pixels, i-step,j+step)



SCALE_FACTOR = 0.2

# preprocess initial image of web page
original_img = Image.open(Original_Image)
original_img = scaleImage(original_img, SCALE_FACTOR)

if original_img.mode != 'RGB':
	original_img = original_img.convert('RGB')

o_width = original_img.size[0]
o_height = original_img.size[1]

o_pixels = original_img.load()

#	~	#	~	$	~	$	~	%	~	%

#preprocess image outlining the blocks
blocks_img = Image.open(Block_Image)

#scale it down so we don't run in stack overflow & it runs faster
blocks_img = scaleImage(blocks_img,  SCALE_FACTOR)

if blocks_img.mode != 'RGB':
	blocks_img = blocks_img.convert('RGB')

b_width = blocks_img.size[0]
b_height = blocks_img.size[1]

b_pixels = blocks_img.load()

#	~	#	~	$	~	$	~	^	~	^	~	%	~	%

# instantiate a 2D array representing all the pixels of an image,
# all the marked pixels should belong to the same block
global_marked={}
marked=[]
minx=[]
maxx=[]
miny=[]
maxy=[]
diff=[]
mindiff = 1000000000
maxdiff = 0
for k in range (0, 160):
	marked.append({})
	minx.append(10000)
	miny.append(10000)
	maxx.append(0)
	maxy.append(0)
	diff.append(0)
	for i in range(0, b_width):
		for j in range(0, b_height):
			global_marked[i,j] = False
			marked[k][i,j] = False

k=0
maxk=0
all_blocks_image = Image.new('RGBA', (b_width, b_height), (255,255,255,255))

for i in range(0, b_width):
	for j in range(0, b_height):
		if not global_marked[i,j]:
			r, g, b = b_pixels[i,j]
			if r<10 and g<10 and b<10:
				#new_image.load()[i,j] = (255,0,0)

				find_block_of_pixel(b_pixels, i, j)

				#print diff[k]
				diff[k] = diff[k] / ( (maxx[k]-minx[k]) * (maxy[k]-miny[k])) 
				
				if mindiff > diff[k]: mindiff = diff[k]
				if maxdiff < diff[k]: maxdiff = diff[k]
				
				k = k+1
				maxk=k


for k in range(0,maxk):
	

	#print (str(diff[k])+"      red will be "+str(lerp(0, 255, diff[k]/float(maxdiff)))+" while green will be "+str(lerp(0, 255, 1 - diff[k]/float(maxdiff))) )
	new_image = Image.new('RGB', (b_width, b_height), (255,255,255))
	
	for q in range(0, b_width):
		for p in range(0, b_height):
			if marked[k][q,p]:
				new_image.load()[q,p] = (255,0,0)
				all_blocks_image.load()[q,p] = (
					int(round(lerp(0, 255, diff[k]/float(maxdiff)))),
					int(round(lerp(0, 255, 1 - diff[k]/float(maxdiff)))), 
					0, 
					255)
'''
	draw = ImageDraw.Draw(new_image) 
	draw.line((minx[k],miny[k], maxx[k], miny[k]), fill=0, width=2)
	draw.line((minx[k],miny[k], minx[k], maxy[k]), fill=0, width=2)
	draw.line((maxx[k],miny[k], maxx[k], maxy[k]), fill=0, width=2)
	draw.line((minx[k],maxy[k], maxx[k], maxy[k]), fill=0, width=2)
	new_image.save("./block_results/block"+str(k)+".jpg")
	draw = ImageDraw.Draw(all_blocks_image) 
	draw.line((minx[k],miny[k], maxx[k], miny[k]), fill=0, width=2)
	draw.line((minx[k],miny[k], minx[k], maxy[k]), fill=0, width=2)
	draw.line((maxx[k],miny[k], maxx[k], maxy[k]), fill=0, width=2)
	draw.line((minx[k],maxy[k], maxx[k], maxy[k]), fill=0, width=2)
'''

all_blocks_image.save("./block_results/all_blocks.jpg")


print ("maxdiff is "+str(maxdiff))



'''

'block' separation algorithm

 for i in pixels (0, width)
 	for j in pixels (0, height)

Algorithm:

find_block_of pixel(i,j):
	if pixel(i,j) is white or marked:
		return 
	if pixel(i,j) is black:
		mark pixel
		find_block_of pixel(i,j+1)
		find_block_of pixel(i,j-1)
		find_block_of pixel(i+1,j+1)
		find_block_of pixel(i+1,j)
		find_block_of pixel(i+1,j-1)
		find_block_of pixel(i-1,j+1)
		find_block_of pixel(i-1,j)
		find_block_of pixel(i-1,j-1)

after this, all the marked pixels will be inside 1 block.


'''
#	$	^	*	$	^	&	%	^	*	^	$	^	*	^	&	^	#	$	*	&	^	$	%	^	^	^	$	@	^	$	#
