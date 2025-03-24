# ART SHOWCASE

- A  library for custom showcasing  fonts from the 'art' Pypi package , it is helpful when trying to choose a font . 
- It contains one function **showcase()**
- You can use it in a Python file or on a command line 

---


### Installation using pip

```
pip install art-showcase
```

#### Dependencies

- <a href="https://pypi.org/project/art/" target="_blank"> art</a> == 6.4


---

### Command line usage

- You'll need Python already installed and added to path


```
python -m art_showcase  HelloWorld --limit 10  --random 
```
- The command above will give you an output like :


- See all available commands by typing :

```
python -m art_showcase -h
```

- The above command gives you :

```
usage: __main__.py [-h] [-l LIMIT] [-ew ENDSWITH] [-sw STARTSWITH] [-c CONTAINS] [-s SLEEP] [-r] text

positional arguments:
  text                  The text to use during the showcase

options:
  -h, --help            show this help message and exit
  -l, --limit LIMIT     The maximum number of fonts to showcase . 0 is equal to no limit
  -ew, --endswith ENDSWITH
                        The string a font name should end with in order to be showcased
  -sw, --startswith STARTSWITH
                        The string a font name should start with in order to be showcased
  -c, --contains CONTAINS
                        The string a font name should contain in order to be showcased
  -s, --sleep SLEEP     The time in seconds to wait before showing the next font
  -r, --random          If set , this option enables the showcase to be randomized
```


---

## Quick start

- Let's get you started !

~~~python
from art_showcase import showcase 

# showcase a maximum 5 fonts only , limit = 0 returns everthing font that meets the specs
fonts_showcased = showcase( "Hellothere", limit = 2 )
# fonts_showcased =  ['1943', '1row']


# Set the pause time in seconds in between fonts
fonts_showcased = showcase("Hellothere" , sleep = 0.1 , limit = 3 )
# fonts_showcased = ['1943', '1row', '3-d']


# Set constraints for the fonts to showcase

# Check if a font name contains the text provided
fonts_showcased = showcase( "Hellothere",
							contains = "re",
							sleep = 0.1,
							  )
# fonts_showcased = ['barbwire', 'fire_font-s', 'fireing', 'future_1', 'future_2', 'future_3', 'future_4', 'future_5', 'future_6', 'future_7', 'future_8', 'greek', 'green_be', 'ogre', 'rectangles', 'red_phoenix', 'rev', 'stforek', 'threepoint', 'trek']

# Check if a font name starts the text provided
fonts_showcased = showcase( "Hellothere",
							startswith = "3",
							sleep = 0.1,
							  )
# fonts_showcased = ['3-d', '3d_diagonal', '3x5']



# Check if a font name endswith the text provided
fonts_showcased = showcase( "Hellothere",
							endswith = "zy",
							sleep = 0.1,
							  )
# fonts_showcased = ['fuzzy']


# Randomize the showcase output
fonts_showcased = showcase( "Hellothere",
							startswith = "3",
							sleep = 0.1,
							randomize =  True
							  )
# fonts_showcased will be a random list containing these values :
#  ['3x5', '3d_diagonal', '3-d']



# Add the font names you want to showcase specifically 
# Note that they must be in the list art.FONT_NAMES
fonts_showcased = showcase( "Hellothere", fonts = ["fuzzy" , "os2"])


~~~



##### Thanks for reading , or installing or whatever . Have a good one. Cheers !

![Adios! ](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnI4bmV1MGVhcjIyZGdpam44NHJscndwcmNkazF0eW5tOHppOXhiMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kaBU6pgv0OsPHz2yxy/giphy.gif)



