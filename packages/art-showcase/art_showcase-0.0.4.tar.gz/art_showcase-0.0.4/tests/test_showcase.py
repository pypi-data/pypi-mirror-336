import re
from unittest import TestCase 

from art_showcase import showcase


class Test_showcase_function(TestCase):

	def test_output_limit(self):
		test_limit = 4
		fonts =  showcase( limit  = test_limit , sleep = 0 )
		self.assertTrue(len(fonts) == test_limit)


	def test_startswith_kwarg(self):
		test_startswith = "f"
		fonts = showcase( limit = 10 , sleep = .1  ,startswith = test_startswith  )
		print("fonts " , fonts)
		self.assertTrue(all( [font.startswith(test_startswith) for font in fonts] ))

	def test_endswith_kwarg(self):
		test_endswith = "zy"
		fonts = showcase( limit = 10 , sleep = .1  , endswith = test_endswith  )
		print("fonts " , fonts)
		self.assertTrue(all( [font.endswith(test_endswith) for font in fonts] ))

	def test_contains_kwarg(self):
		test_contains = "char2"
		fonts = showcase(   sleep = .1  , contains=  test_contains )
		print("fonts " , fonts)
		self.assertTrue(all( [ test_contains in font for font in fonts] ))


	def test_all_kwargs_present(self):
		test_endswith = "t"
		test_startswith = "h"
		test_limit = 3
		test_contains = "h"
		fonts  = showcase(
			contains = test_contains ,
			limit = test_limit ,
			endswith = test_endswith ,
			startswith =test_startswith , sleep = 0 )
		print(fonts)
		self.assertTrue(all( [ test_contains in font for font in fonts] ))
		self.assertTrue(all( [font.endswith(test_endswith) for font in fonts] ))
		self.assertTrue(all( [font.startswith(test_startswith) for font in fonts] ))
		self.assertTrue(len(fonts) == test_limit)
		print(len(fonts))


