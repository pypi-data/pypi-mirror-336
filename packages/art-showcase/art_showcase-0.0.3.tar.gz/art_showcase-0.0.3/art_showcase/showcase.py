import time
import random 
import re
from collections.abc import Iterable
import art


def showcase(  
	text:str = "Text",
	endswith:str = "" ,
	startswith:str  = "" ,
	contains:str = ""  ,
	sleep:int = .9 ,
	limit:int = 0 ,
	randomize:bool=False,
	fonts:Iterable = art.ASCII_FONTS ):
	'''This function loops through the art fonts provided and prints the text provided in each font 
		In order for a font to be printed , it must :
			- be in art.ASCII_FONTS
			- meet all the endswith , contains and startswith kwargs' specs


	Parameters
	----------
	endswith:str
		The text a font should end with in order for it  to be printed
	startswith:str
		The text a font should begin with in order for it to be printed
	contains:str
		The text a font should contain in order for it to be printed
	sleep:int
		The time in seconds to wait before printing the next font 
	limit:int
		The max number of font to print 
	fonts:Iterable
		The art package fonts to loop through and print
	randomize:bool
		Whether or not to showcase the fonts in a random order 
	Returns
	-------
	showed_fonts:list
		A list of the fonts displayed '''


	showed_fonts = [] 
	to_showcase = list() # Fonts to be showcased after meeting specs 
	if not fonts:
		fonts = art.ASCII_FONTS
	time.sleep(1.4)
	for font in fonts:
		font   = font.strip()
		if startswith:
			if not font.startswith(startswith):
				continue
		if endswith:
			if not font.endswith(endswith):
				continue
		if contains :
			if not re.search( contains  , font ) :
				continue
		to_showcase.append(font)

	if limit == 0:
		print("About to showcase all ", len(to_showcase) , " FONTS ")
	else:
		print("About to showcase " , limit, " fonts")
	time.sleep(3)
	# randomize
	if randomize:
		random.shuffle(to_showcase)
	for font in list(to_showcase):
		if len(showed_fonts) == limit and limit != 0:
			print("showcase limit reached . Showed {} out of {} fonts".format(
					len(showed_fonts) , 
					len(fonts)
				))
			break

		output = art.text2art(  text ,font    )
		print("\n\n======================== FONT  {} =================".format(font))
		time.sleep(sleep)
		print(output)
		showed_fonts.append(font)
	print("\n--           SHOWCASE COMPLETE        --\n")
	print("="*66)
	print("\n")

	return  showed_fonts


