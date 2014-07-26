One of the challenges at Pwnium 2014 was a stego challenge (appropriately named Stego75).

After downloading the challenge and opening it you see the following PNG image of a blue flag.

[Steg75.png]

one of the first things you will immidiately notice are a few diagonal lines that are one pixel wide
that cross the image from the top left to bottom right into a depth of exactly 55 pixels down into the image.

That looks interesting!, lets take a closer look...

So, just by opening paint you can check the pixel offsets and you'll notice there's a pattern, each line is perfectly diagonal
and is exactly 55 pixels long, and at the location that one line cuts ends, a new one continues again from the top of the image.

There are six of these lines, these are the beginning and ending points of the six pixel ladders:
1,   0 to 56,  55
57,  0 to 113, 55
114, 0 to 168, 55
169, 0 to 224, 55
225, 0 to 280, 55
281, 0 to 336, 55


Okay, this is good, lets write a bit of code so we can extract the data, we will use Python & PIL (Python Imaging Library).

[code_basic.png]

Now that we have our code, lets take a look at the actual RGB data of the pixels to see if there is something we can conclude from it.

[stego-ascii.png]

After extracting the RGB data and looking at the actual RGB numbers there is a noticable pattern of some relation between the red channel and the blue channel,
looking at the data at various cuts/offsets i noticed that it seems to stay in some proportion to each other, i tried a operation or two and noticed that every time
that i subtract the blue channel from the red channel i get a character which is the ASCII range (a printable character).

Neat!, lets print out all the data.

[stego-ascii2.png]

Looks like there's a base64 string in the beginning of our text (it's even easier to notice with the == base64 padding)it's length is exactly 56 characters, 
it's our first "ladder" beginning at 0,1!.

lets decode it!

[stego3-ascii.png]

Win!.


I rather enjoyed this stego challenge, it was short and to the point, when the challenge was released most of us at 0xAWES0ME jumped at it and threw some powerful stego tools
at it, sometimes it's better to look at things at ground level first :).

Here is the full solution which will print out the flag, it requires PIL as mentioned.

[solve_stego.py]

See you at the next CTF!,
Matan M. Mates


