#-------------------------------------------------------------------------------
# Steganograpy program
#   Encode and Decode the image start from the last bit of the image
#-------------------------------------------------------------------------------
# Fin: Fin argument condition and send it to a correct section
# Need: Encode and Decode
#       open and write the image file

from __future__ import print_function
import sys
from PIL import Image

SETSTRING_SIZE = 11


# Print the Information about an incoming arguments
# Use       : sys.argv
# Input     : None
# Output    : None
#  **not use in program
def ArgumentInfo():
    print ('Number of arguments:', len(sys.argv))
    print ('Argument List:', str(sys.argv))

# Print a message and how to use the program
# use       : sys.argv
# Input     : None
# Output    : None
def HelpMessage():
    print ('  Required command line arguments')
    print ('  To Encode image:')
    print ('     <program.py> -e <mesage in string> -i <image in jpg> -o <export image in png>')
    print ('       ** `cat test.txt` to encode the file **')
    print ('  To Decode image:')
    print ('     <program.py> -d <encoded image.png>')

# use to classify the incoming argument and check for any argument error
# Use       : sys.argv
# Input     : None
# Output    : integer value to let the prgram know what function it need to do
#               0 = invalide input , 1 = encode , 2 = decode
def ArgumentClassify():
    print ('Classify argument')
    if (len(sys.argv) == 0):
        HelpMessage()
        return 0
    elif (len(sys.argv) == 7):
        if((str(sys.argv[1]) == '-e') and (str(sys.argv[3]) == '-i') and (str(sys.argv[5]) == '-o')):
            print ('== Encode Classify')
            return 1
        else:
            return 0
    elif (len(sys.argv) == 8):
        if((str(sys.argv[1]) == '-e') and (str(sys.argv[4]) == '-i') and (str(sys.argv[6]) == '-o')):
            print ('== Encode Classify')
            return 2
        else:
            return 0
    elif (len(sys.argv) == 3):
        if((str(sys.argv[1]) == '-d')):
            print ('== Decode Classify')
            return 3
        else:
            return 0
    else:
        print ('Invalid argument')
        HelpMessage()
        return 0

# get one bit (last bit) from original value
# Use:
# Input     :value, and shift
# Output    :modify value (one bit)
def SplitBit(value, shiftNum):
    oneBit = 0
    oneBit = value >> shiftNum
    #print (oneBit)
    oneBit = oneBit & 1
    #print(oneBit)
    return oneBit

# Store the string length into the new pixel base on the setoff
# Use       :
# Input     : string size, image height, image width,
#                pixel of new image(PNG), pixel for old image(JPG)
#                setOff - number of pixel use to contain string size
# Output    : 1 on success
def StoreSize(strSize, varVertical, varHorizontal, pixNew, pixOld, setOff ):
    xVal = varHorizontal - setOff
    yVal = varVertical -1
    test = [0,0,0]
    z = 0
    temp = 0
    u = 0
    rgbControl = 2

    #increase a size to have one empty bit at the end
    k = strSize * 8
    k = k << 1

    for j in range(0, setOff):
        for i in range(2,-1,-1):
            #r,g,b contain int
            r = pixOld[xVal + j, yVal][i]
            u += 1

            if(z < (len(bin(k))-2)):
                temp = SplitBit(k, z)
                temp = r | temp
                test[i] = temp

                z += 1
            else:

                #keep everything the same except 0 the last bit
                temp = r & 254
                test[i] = temp

        #end inner for
        pixNew[(xVal + j), yVal] = tuple(test)
    #end outer for

    return 1

# Store the message into a new image pixel
# use       :
# input     :  the message to store, image height, image width,
#                pixel of new image(PNG), pixel for old image(JPG)
#                 setOff - number of pixel use to contain string size
def StoreMessage(msgIn, height, width, pixelPNG, pixelJPG, setNum):
    mainX = width - (setNum + 1)
    mainY = height - 1
    mainAll = (width * height) - (SETSTRING_SIZE + 1)

    charBin = 7
    charSize = 0
    charIn = msgIn[0]
    temp = 0


    #print ("----------")
    tempList = [0,0,0]
    for y in range(mainY, 0, -1):
        for x in range(mainX, 0, -1):
            for i in range(0,3):
                if (len(msgIn) > charSize): #count number of character

                    pix = pixelJPG[x, y][i]
                    #print (msgIn[charSize])
                    charIn = msgIn[charSize]
                    #print(format(ord(charIn), 'x'))
                    temp = SplitBit(ord(charIn), charBin)
                    temp2 = pix & 254       #set the last bit
                    temp = temp | temp2
                    tempList[i] = temp
                    #print(temp , "--" , charBin)
                    temp = 0

                    charBin -= 1
                    if (charBin < 0) :   #for counting the bit shift
                        charBin = 7
                        charSize += 1
                else:
                    pix = pixelJPG[x, y][i]
                    tempList[i] = pix
                #end if
            #end i for

            pixelPNG[x, y] = tuple(tempList)
            tempList =[0,0,0]
        #end x for
        mainX = width - 1
    #end y for

#Encode image with the message
# Use       : sys.argv,
# Input     : None
# Output    : 1 for success, 0 for fail
def EncodeFunction(flagNum):
    #print -e
    msgMain = sys.argv[2]
    imgMain = sys.argv[4]
    imgOut = sys.argv[6]
    if(flagNum == 2):
        msgMain = sys.argv[2]
        imgMain = sys.argv[5]
        imgOut = sys.argv[7]

    print ('Message: ' ,str(msgMain))
    print ('Image to Encode: ' ,str(imgMain))
    print ('Encoded Image: ' ,str(imgOut))

    setNum = SETSTRING_SIZE

    mainString = msgMain
    stringSize = len(mainString)
    print ('String size: ', stringSize)

    #try to open an image
    try:
        #change the image name to im
        with Image.open(imgMain) as im:
            print(im, im.format, "%dx%d" % im.size, im.mode)
            #if the message is too long
            if(stringSize * 8 > len(im.tobytes())):
                print("Message is too long for this image.")
                return 0

            pixelJPG = im.load()
            width = im.size[0]
            height = im.size[1]

            #create an new image with size of im.size(old image)
            #   fill with black
            imgPNG = Image.new( 'RGB', im.size, "black")
            pixelPNG = imgPNG.load() # create pixel map

            #store lenght of the message
            StoreSize(stringSize, height, width, pixelPNG, pixelJPG, setNum)

            #store the message
            StoreMessage(mainString, height, width, pixelPNG, pixelJPG, setNum)

            #save the new image with an new value
            imgPNG.save(imgOut)

    except IOError:
        print("Error IO")
        pass


    return 1
    #a == '-e'

#decode first SETSTRING_SIZE pixel
# Use       :
# Input     : width of image, height of image, Pixel Access
# Output    : number of string in the image
def DecodeStringSize(width, height, pixelIn,setOff):
    itemSizeList = []
    for j in range(0,setOff):
        #print (pixelDe[width-j, height])
        for i in range(0,3):
            temp = pixelIn[width - j, height][i]
            temp = temp & 1
            #add to a list of string
            itemSizeList.append(str(temp))
            #print(temp)
        #end inner for
    #end outer for

    itemSizeList = ''.join(itemSizeList) #combine the list together
    #print (itemSizeList)
    itemSizeList = int(itemSizeList,2)  # string binary  to int
    itemSizeList = itemSizeList >> 1
    #print (itemSizeList)
    itemSizeList = int(itemSizeList/8)
    #print ("numb --", itemSizeList)
    return itemSizeList

#decodeMessage from bit by bit
# use        :
# input     :x-value, y-value, pixel for PNG
#               stringSize offset, stringSize
# out       : None
#    ** will print out the character from here
def DecodeMessage(width, height, pixelIn,setOff, stringSize):
    mainX = width - setOff
    mainY = height
    mainAll = (width * height) - setOff

    charSize = 0    # control the size of the expected string
    charLim = 0     # control the size 8 bit for each char
    tempList = [0,0,0,0,0,0,0,0] #store the char

    # y-value loop
    for y in range(mainY, 0 , -1):
        #x-value loop
        for x in range(mainX, 0 , -1):
            # loop within the pixel
            for i in range(0,3):
                if(charSize < stringSize):

                    #check the 8 slot is full
                    if(charLim < 8):
                        pix = pixelIn[x,y][i]
                        #print (pix)
                        temp = pix & 1 #isolate the last bit
                        #print(str(pix))
                        tempList[charLim] = str(temp)
                        charLim += 1

                    #if all 8 slot is full then it can be turn into char
                    if(charLim >= 8):
                        #reset for the next loop
                        charSize +=1
                        charLim = 0
                        testOut = ''.join(tempList) #combine the list together
                        #print(testOut)
                        testOut = int(testOut,2)  # string binary  to int
                        print(chr(testOut), end="") # write out
            #end i for
        #end x for
        mainX = width # reset the x value without offset
    #end y for
    print()


#decode image with the message
# Use       : sys.argv,
# Input     : None
# Output    : 1 for success, 0 for fail
def DecodeFunction():
    #print -e
    print ('Image to Decode: ' ,str(sys.argv[2]))
    setNum = SETSTRING_SIZE

    #decode the image lenght
    try:
        #change the image name to im
        with Image.open(sys.argv[2]) as im:
            print(im, im.format, "%dx%d" % im.size, im.mode)

            pixelDe = im.load()
            width = im.size[0]-1
            height = im.size[1]-1
            print (width)
            print (height)

            #print(pixelDe[width-10,height-10])
            #print('tt')
            #decode message size
            stringSize = DecodeStringSize(width, height, pixelDe, setNum)
            print ("Image contain: ", stringSize, " character")

            #decode message
            DecodeMessage(width, height, pixelDe, setNum, stringSize)

    except IOError:
        print("Error IO")
        pass




    '''
    https://mail.python.org/pipermail/python-list/2013-November/660356.html
    import io
    import PIL

    photo_data = # … get the byte string from wherever it is …
    photo_infile = io.StringIO(photo_data)
    photo_image = PIL.Image.frombytes(photo_infile)
    '''
    return 1
    #a == '-e'


#-------------------------------------------------------------------------------
# execution area
#-------------------------------------------------------------------------------

condition = ArgumentClassify()

if(condition == 1)or(condition == 2):
    print ('Encode')
    if(EncodeFunction(condition)):
        print ('Success Encode')
    else:
        print ('Fail C1--')
elif (condition == 3):
    print ('Decode')
    if(DecodeFunction()):
        print ('Success Decode')
    else:
        print ('Fail C2--')
else:
    print ('Error Command')
