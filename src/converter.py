import sys, argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data", "-d", help="Set up data", type=str)

import os, subprocess, shutil
import magic
import re
from PIL import Image, ImageOps
import pyheif

import json

# Assets
args = parser.parse_args()
data = json.loads(args.data);

sourcePath = data['src'];
targetPath = data['dest'];
outputType = data['type']
maxSize = data['maxSize'];

if os.path.isfile(f"'{sourcePath}'"):
	print("File Not Found")
	sys.exit()

sourceMime = magic.from_file(sourcePath, mime=True)
success = False

'''

HEIC Converter

'''

if re.search(r'heic', sourceMime):
	heif_file = pyheif.read_heif(sourcePath)
	pic = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)

	width, height = pic.size

	if width > maxSize or height > maxSize:
		scale = maxSize/width
		newWidth = width*scale
		newHeight = height*scale
		if newHeight > maxSize:
			scale = maxSize/height
			newWidth = width*scale
			newHeight = height*scale

		newWidth = int(newWidth)
		newHeight = int(newHeight)
		pic = pic.resize((newWidth, newHeight))

	if pic.mode == 'CMYK':
		pic = pic.convert('RGB')

	pic = ImageOps.exif_transpose(pic)

	pic.save(targetPath, 'png', quality=90, optimize=True)
	print('{"state":true,"size":[%d,%d]}'%(width,height))
	success = True

elif re.search(r'png|jpeg|gif', sourceMime):

'''

PNG, Jpeg or Gif Converter

'''


	pic = Image.open(sourcePath)
	width, height = pic.size

	if width > maxSize or height > maxSize:
		scale = maxSize/width
		newWidth = width*scale
		newHeight = height*scale
		if newHeight > maxSize:
			scale = maxSize/height
			newWidth = width*scale
			newHeight = height*scale

		newWidth = int(newWidth)
		newHeight = int(newHeight)
		pic = pic.resize((newWidth, newHeight))

	if pic.mode == 'CMYK':
		pic = pic.convert('RGB')

	pic = ImageOps.exif_transpose(pic)

	if outputType == 'jpg':
		# if pic.mode == 'RGBA':
		pic = pic.convert('RGB')
		pic.save(targetPath, 'jpeg', quality=90, optimize=True)
	else:
		pic.save(targetPath, 'png', quality=90, optimize=True)

	print('{"state":true,"size":[%d,%d]}'%(width,height))
	success = True

elif re.search(r'bmp', sourceMime):

'''

BMP Converter

'''


	pic = Image.open(sourcePath)
	width, height = pic.size
	
	if pic.mode == 'CMYK':
		pic = pic.convert('RGB')

	if outputType == 'jpg':
		# if pic.mode == 'RGBA':
		pic = pic.convert('RGB')
		pic.save(targetPath, 'jpeg', quality=90, optimize=True)
	else:
		pic.save(targetPath, 'png', quality=90, optimize=True)
	print('{"state":true,"size":[%d,%d]}'%(width,height))
	success = True
elif re.search(r'pdf', sourceMime):

'''

PDF Converter

'''

	from pdfrw import PdfReader
	pdf = PdfReader(sourcePath)
	
	sizes = pdf.pages[0].MediaBox
	if not sizes:
		sizes = pdf.getPage(0)['/Parent']['/MediaBox']

	# print('Sizes', sizes)
	width = int(float(sizes[2]))
	height = int(float(sizes[3]))
	scale = maxSize/width
	newWidth = width*scale
	newHeight = height*scale
	if newHeight > maxSize:
		scale = maxSize/height
		newWidth = width*scale
		newHeight = height*scale

	newWidth = int(newWidth)
	newHeight = int(newHeight)

	if outputType == 'jpg':
		pngTmp = targetPath+".png"
		ls = subprocess.run(['gs', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-dPDFFitPage', '-dEPSCrop', f'-dDEVICEWIDTHPOINTS={newWidth}', f'-dDEVICEHEIGHTPOINTS={newHeight}', '-sDEVICE=pngalpha', f'-sOutputFile={pngTmp}', sourcePath], stdout=subprocess.DEVNULL)
		pic = Image.open(pngTmp)
		pic = pic.convert("RGB")
		pic.save(targetPath, 'jpeg', quality=90, optimize=True)
		os.remove(pngTmp)
	else:
		ls = subprocess.run(['gs', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-dPDFFitPage', '-dEPSCrop', f'-dDEVICEWIDTHPOINTS={newWidth}', f'-dDEVICEHEIGHTPOINTS={newHeight}', '-sDEVICE=pngalpha', f'-sOutputFile={targetPath}', sourcePath], stdout=subprocess.DEVNULL)

	print('{"state":true,"size":[%d,%d],"originalSize":[%d,%d]}'%(newWidth,newHeight,width,height)) #, int(newWidth), int(newHeight));
	# print({'state':True,'size':[newWidth,newHeight]})#'%(newWidth,newHeight)) #, int(newWidth), int(newHeight));
	success = True

elif re.search(r'postscript|eps', sourceMime):

'''

EPS Converter

'''


	pic = Image.open(sourcePath)
	width, height = pic.size
	scale = maxSize/width
	newWidth = width*scale
	newHeight = height*scale
	if newHeight > maxSize:
		scale = maxSize/height
		newWidth = width*scale
		newHeight = height*scale
	
	newWidth = int(newWidth)
	newHeight = int(newHeight)	

	if outputType == 'jpg':
		pngTmp = targetPath+".png"
		ls = subprocess.run(['gs', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-dEPSFitPage', f'-dDEVICEWIDTHPOINTS={newWidth}', f'-dDEVICEHEIGHTPOINTS={newHeight}', '-sDEVICE=pngalpha', f'-sOutputFile={pngTmp}', sourcePath], stdout=subprocess.DEVNULL)
		pic = Image.open(pngTmp)
		pic = pic.convert("RGB")
		pic.save(targetPath, 'jpeg', quality=90, optimize=True)
		os.remove(pngTmp)
	else:
		ls = subprocess.run(['gs', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-dEPSFitPage', f'-dDEVICEWIDTHPOINTS={newWidth}', f'-dDEVICEHEIGHTPOINTS={newHeight}', '-sDEVICE=pngalpha', f'-sOutputFile={targetPath}', sourcePath], stdout=subprocess.DEVNULL)	
		
	print('{"state":true,"size":[%d,%d],"originalSize":[%d,%d]}'%(newWidth,newHeight,width,height))
	success = True

elif re.search(r'photoshop|psd', sourceMime):

'''

PSD Converter

'''


	from psd_tools import PSDImage
	psd = PSDImage.open(sourcePath)
	compose = psd.composite()
	width, height = compose.size
	compose.save(targetPath)
	print('{"state":true,"size":[%d,%d]}'%(width,height))
	success = True

elif re.search(r'svg', sourceMime):

'''

SVG Converter

'''


	import xml.etree.ElementTree as ET
	tree = ET.parse(sourcePath)
	svg = tree.getroot()
	width = svg.get('width')
	height = svg.get('height')
	if not width or height:
		viewbox = re.split('[ ,\t]+', svg.get('viewBox', '').strip())
		width = float(viewbox[2])
		height = float(viewbox[3])

	width = int(width)
	height = int(height)

	scale = maxSize/width
	newWidth = width*scale
	newHeight = height*scale
	if newHeight > maxSize:
		scale = maxSize/height
		newWidth = width*scale
		newHeight = height*scale
	
	newWidth = int(newWidth)
	newHeight = int(newHeight)
	import cairosvg
	if outputType == 'jpg':
		pngTmp = targetPath + ".png"
		cairosvg.svg2png(url=sourcePath, write_to=pngTmp, output_width=newWidth, output_height=newHeight, dpi=72)
		pic = Image.open(pngTmp)
		white_background = Image.new('RGBA', pic.size, 'WHITE')
		white_background.paste(pic, (0, 0), pic)
		pic = white_background.convert('RGB')
		pic.save(targetPath, 'jpeg', quality=90, optimize=True)
		os.remove(pngTmp)
	else:
		cairosvg.svg2png(url=sourcePath, write_to=targetPath, output_width=newWidth, output_height=newHeight, dpi=72)
	print('{"state":true,"size":[%d,%d],"originalSize":[%d,%d],"mime":"%s"}'%(newWidth,newHeight,width,height,sourceMime))
	success = True
elif re.search(r'tiff', sourceMime):

'''

Tiff Converter

'''

	pic = Image.open(sourcePath)
	width, height = pic.size

	if pic.mode == 'CMYK':
		pic = pic.convert('RGB')
		
	if outputType == "jpg":
		if pic.mode == 'RGBA':
			pic = pic.convert('RGB')
		pic.save(targetPath, 'jpeg', quality=90, optimize=True)
	else:
		pic.save(targetPath, 'png', quality=90, optimize=True)
	print('{"state":true,"size":[%d,%d]}'%(width,height))
	success = True
else:

'''

Unsupported format

'''

	print('{"state":false,"msg":"Unsupported format %s"}'%sourceMime)

'''

Remove source image

'''

if data['removeSrc']:
	os.remove(sourcePath)