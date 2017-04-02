# Steganography

**Description**

This is an application to hide the image into an image and read it out depended on the flag. 

**Architecture**

- The message will be store start from the bottom right of the image.
- The last 11 pixels will store the lenght of the message, but will only use 32 pixels. The last pixel will not get use by either the message size or the message itself.
- Each character will get split and store in the last bit of the pixel, inorder to minimize the color change in the image.
- Accept jpg and Exprot png

**How to Use**

To Encode image:
    <program.py> -e <mesage in string> -i <image in jpg> -o <export image in png>
    
To Decode image:
    <program.py> -d <encoded image.png>
