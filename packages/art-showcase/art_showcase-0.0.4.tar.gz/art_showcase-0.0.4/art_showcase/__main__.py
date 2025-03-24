
import argparse

from .showcase import showcase



parser = argparse.ArgumentParser()

parser.add_argument("text" , help = "The text to use during the showcase")

parser.add_argument("-l" ,"--limit" , help = "The maximum number of fonts to showcase . 0 is equal to no limit " ,
					type = int , default = 0)
parser.add_argument("-ew" , "--endswith" , help = "The string a font name should end with in order to be showcased")
parser.add_argument("-sw" , "--startswith" , help = "The string a font name should start with in order to be showcased")
parser.add_argument("-c" , "--contains" , help = "The string a font name should contain in order to be showcased")
parser.add_argument("-s" , "--sleep" , type = int , default = 0.7, 
					help = "The time in seconds to wait before showing the next font ")
parser.add_argument("-r" , "--random" ,
					 help = "If set , this option enables the showcase to be randomized" ,
						action = "store_true")



args = parser.parse_args()

showcase(args.text  , 
	endswith = args.endswith ,
	startswith = args.startswith , 
	contains = args.contains , 
	randomize = args.random , 
	sleep = args.sleep , 
	limit = args.limit  )
