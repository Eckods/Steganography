# Author: Steve Sanchez
# Course: CPSC 353
# Due date: 10/31/17
# This program hides and reveals text from a PNG image. To hide a message,
# store the message in the message.txt file in the program directory. 
from PIL import Image
import getopt
import sys
import argparse
import time
import os


# Functions for decoding and encoding the images
def decode(fileName):
    # Open the image file
    imageFile = Image.open(fileName)
    
    # Rotate image to read from top left to bottom right
    # (Would be bottom right to top left in original orientation)
    imageFile = imageFile.rotate(180)

    # Get width and height of images for nested for-loop traversal
    width = imageFile.width
    height = imageFile.height
    
    # Get an RGB copy of the image
    rgbImage = imageFile.convert("RGB")

    # Get the LSB from every pixel rgb value
    lsb = []
    for y in range(height):
        for x in range(width):
            (r,g,b) = rgbImage.getpixel((x,y))
            lsb.append(r & 1)
            lsb.append(g & 1)
            lsb.append(b & 1)

    # Get the 32 bits used to encode length
    lengthInBinary = []
    for i in range(0,3*11-1):
        lengthInBinary.append(lsb[i])
        
    # Convert the 32 bit binary string to integer
    textLength = int("".join(map(str, lengthInBinary)), 2)
    print("The text # of bits is", textLength)
    
    # Cycle through the characters containing encoded message
    # starting from 34th LSB (initial point containing text)
    byte = [0,1,2,3,4,5,6,7]
    message = []
    byteCount = 0
    
    for j in range(33, 33 + textLength + 1):
        # If a byte has been formed, convert it to an integer, then
        # to character and append to form the hidden message
        if (byteCount == 8):
            intVal = int("".join(map(str, byte)), 2)
            message.append(chr(intVal))
            byteCount = 0
            
        # Store the LSB into the list and increase the counter used
        # to determine if a byte has been formed
        byte[byteCount] = lsb[j]
        byteCount += 1


    # Join the characters of message and display the hidden text
    msg = "".join(map(str,message))
    print(msg)
    
    return


def encode(fileName):
    # Open the image file
    imageFile = Image.open(fileName)

    # Rotate image to write from top left to bottom right
    # (Would be bottom right to top left in original orientation)
    imageFile = imageFile.rotate(180)

    # Read in text file containing message to hide
    text = open('message.txt', 'r')
    message = text.read()

    # If the message length cannot be stored in the image, print error and exit
    if (len(message)*8 + (11*3) > imageFile.width * imageFile.height * 3):
        print("Message cannot be stored in image provided. Please use a larger image.")
        time.sleep(5.5) 
        sys.exit(0)
        
    # Convert text # of bits to binary
    # Get rid of 0b prefix and add leading 0s if needed to get max 32 bits
    textLength = bin(len(message)*8)[2:]
    textLength = "{:0>32}".format(textLength)
    
    # Create list of characters from string
    charMsg = list(message)

    # Convert each character to an integer, then to binary 8 bit value
    binaryMsg = []
    for i in range(len(charMsg)):
        intVal = (ord(charMsg[i]))
        binaryMsg.append(bin(intVal)[2:])
        binaryMsg[i] = "{:0>8}".format(binaryMsg[i])

    # Get width and height of images for nested for-loop traversal
    width = imageFile.width
    height = imageFile.height

    # Get an RGBA copy of the image and create a new image
    # that will store the hidden text
    rgbaImage = imageFile.convert("RGBA")
    pngImage = Image.new('RGBA',(width,height))

    # Create a list of LSBs from the text length binary
    # Append the 33rd bit that will be ignored when decoding
    lsb = list(textLength)
    lsb.append('0')

    # Append the bits holding the message to the list of LSBs
    for j in range(len(binaryMsg)):
        lsb = lsb + list(binaryMsg[j])

    # Append the LSB to appropriate pixel rgb values
    counter = 0
    for y in range(height):
        for x in range(width):
            (r,g,b,a) = rgbaImage.getpixel((x,y))
            # If the counter is under the length of our LSB list,
            # convert each rgb to binary, append the LSB, and convert
            # back to integer
            if (counter < len(lsb)-1):
                r = "{:0>8}".format(bin(r)[2:])
                g = "{:0>8}".format(bin(g)[2:])
                b = "{:0>8}".format(bin(b)[2:])
 
                r = r[:7]
                r += lsb[counter]

                g = g[:7]
                g += lsb[(counter+1)]

                b = b[:7]
                b += lsb[(counter+2)]

                r = int(r, 2)
                g = int(g, 2)
                b = int(b, 2)
                
            # If the counter has reached the last LSB in list,
            # convert ONLY the r to binary, append the LSB, and convert
            # back to integer
            elif (counter == len(lsb)-1):
                r = "{:0>8}".format(bin(r)[2:])
                r = r[:7]
                r += lsb[counter]
                r = int(r, 2)
            # Store the pixel in the png image using the rgba values
            # and increment the count by 3 (3 for every rbg pairing)
            pngImage.putpixel((x,y),(r,g,b,a))
            counter += 3

    
    # Rotate image back to original orientation before saving
    # and close text file
    pngImage = pngImage.rotate(180)
    text.close()
    
    # Split the file name into the name and extension
    # This is to re-use the same file name for saving to PNG
    name, extension = os.path.splitext(fileName)

    # Save as a PNG
    pngImage.save('{}_E.png'.format(name), "PNG")
    
    return


# Placeholder for console-entered file name
fileName = "testImage.png"


# Parse arguments to determine when user is decoding/encoding as well as to obtain image filename
parser = argparse.ArgumentParser(description = "Process some image file")
parser.add_argument('-d', metavar = 'Decode', type = str, help = 'An image to decode')
parser.add_argument('-e', metavar = 'Encode', type = str, help = 'An image to encode')
args = parser.parse_args()


# Print args
print(args)


# Run appropriate function depending on arguments entered
# Decodes testImage by default if nothing was entered
if (args.__dict__['d'] != None):
    fileName = args.__dict__['d']
    decode(fileName)
elif (args.__dict__['e'] != None):
    fileName = args.__dict__['e']
    encode(fileName)
else:
    encode(fileName)

time.sleep(5.5) 
