CPSC 353 - Text in Image
By Steve Sanchez

This program hides text in a JPEG which is converted to a PNG on output. It also reveals text hidden in a PNG image. 
This program was developed with Python 3.6 and uses the Pillow, a fork of Python's Imaging Library. 


Files Included:
	message.txt		= Write the text you wish to hide here
	README.txt		= Description and program usage
	sourceCode.jpg		= Original image used for encoding
	sourceCode_E.png	= Encoded image with source code
	testImage.png		= Given to test decoder

Usage:
	(For reference):
		-d 		decode
		-e		encode

	Open terminal in the directory of the program.
	Enter the name of the program.
	For decrypting:
		Enter -d followed by the name of the png file.
		Wait for the message to be displayed in the terminal.
	For encrypting:
		First, write the text you wish to hide in the message.txt file.
		Back at terminal, enter -e followed the name of the jpeg file.
		Wait for a png file with the same source name + _E appended to it to be created.

	Example commands:
	 .\textInImage.py -d "sourceCode_E.png"
	 .\textInImage.py -e "sourceCode.jpg"