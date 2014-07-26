---
layout: post
title: "Matter of Combination - Stego75 - (Pwnium CTF)"
date:   2014-07-26 16:00
categories: writeups
author: Matan Mates
tags: ctf, stego
---

This is a writeup of the challenge Matter of combination from the 2014 Pwnium CTF.

The team that participated for in this CTF representing 0xAWES0ME consisted of Joey Geralnik, Yoav Ben Shalom, Itay Yona, Gal Dor and me.

We came in first place!.

There have been multiple requests for a writeup for Stego75 and there weren't any yet (and Joey was getting pushy about me writing this already) so here i is.

## Le Challenge

After downloading the challenge and opening it you see the following PNG image of a blue flag.

![The file we got](/images/stego75pwnium2014/Steg75.png)  

one of the first things you will immidiately notice are a few diagonal lines that are one pixel wide
that cross the image from the top left to bottom right into a depth of exactly 55 pixels down into the image.

That looks interesting!, lets take a closer look...

## Pattern?

So, just by opening paint you can check the pixel offsets and you'll notice there's a pattern, each line is perfectly diagonal
and is exactly 55 pixels long, and at the location that one line cuts ends, a new one continues again from the top of the image.

There are six of these lines, these are the beginning and ending points of the six pixel ladders, each with a length of 56 pixels, you can see the X,Y's of the ladders in the picture below.


## Extraction

Okay, this is good, lets write a bit of code so we can extract the data, we will use Python & PIL (Python Imaging Library).

![Basic code](/images/stego75pwnium2014/code_basic.png)

Now that we have our code, lets take a look at the actual RGB data of the pixels to see if there is something we can conclude from it.

![Steganography ASCII](/images/stego75pwnium2014/stego-ascii.png)

After extracting the RGB data and looking at the actual RGB numbers there is a noticable pattern of some relation between the red channel and the blue channel,
looking at the data at various cuts/offsets i noticed that it seems to stay in some proportion to each other, i tried a operation or two and noticed that every time
that i subtract the blue channel from the red channel i get a character which is the ASCII range (a printable character).

Neat!, lets print out all the data.

![Stego ASCII Text](/images/stego75pwnium2014/stego-ascii2.png)

Looks like there's a base64 string in the beginning of our text (it's even easier to notice with the == base64 padding)it's length is exactly 56 characters, 
it's our first "ladder" beginning at 0,1!.

lets decode it!

![Win!](/images/stego75pwnium2014/stego3-ascii3.png)

## Win!


I rather enjoyed this stego challenge, it was short and to the point, when the challenge was released we jumped at it and threw some powerful stego tools
at it, sometimes it's better to look at things at ground level first.

Here is the full solution which will print out the flag, it requires PIL as mentioned.

{% gist mtnmts/34e9dbe09fad8c607e5f %}

See you at the next CTF!,
Matan M. Mates


