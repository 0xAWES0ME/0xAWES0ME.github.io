---
layout: post
title:  "Rarara - Reversing (Secuinside CTF)"
date:   2014-06-12 21:34:50
categories: writeups
author: Joey Geralnik
tags: reversing, math, crc
---
This is a writeup of the challenge rarara from the secuinside 2014 pre-qual ctf.

This was the probably the hardest challenge in the competition and only one team had managed to solve it a few hours before the competition ended when my team had to leave early.

We had figured out the solution but ran out of time before implementing it. Had we stayed and finished this level and another we likely would have been in the top ten teams, but oh well!

## The challenge
We're given a binary. Running it from a terminal yields

![This program must run in x64 windows](/images/rarara/x64.png)

While the easy solution might be to install 64 bit windows, examining the assembly reveals that the code is actually 32 bit binary. I'm not sure why this check is done, but it's easy enough to patch it (a single jz -> jnz) and allow the binary to run on 32 bit systems.

Next we are presented with a prompt asking for input. Trying a few random inputs, we get the message "Wrong!". It's time to open up IDA and see what this program does!

## Anti-reversing
Once we've identified the important function, we can see a few things. First, the length of the input is checked and compared to 13.

![Length check](/images/rarara/length.png)

Then each of the letters is checked to make sure it is alphanumeric

![Alphanumeric check](/images/rarara/alphanumeric.png)

And then we reach this block at which point IDA's analysis fails us:

![IDA fail](/images/rarara/endingblock.png)

This block is repeated in many different locations throughout the code.

What is this block doing? When we call $+5 it puts our address on the stack. 3E+var3E is 0x3E - 0x3E = 0, so the add instruction adds 5 to the address just placed on the stack. Finally, we return to that address, or just after the retf instruction.

In other words, this whole block is just a compilicated nop that screws with IDA's autoanalysis. By patching the binary to replace all instances of this block (plus some slight variations) with nops, we turn this:

![Messy graph](/images/rarara/messy_graph.png)

into this:

![Clean graph](/images/rarara/clean_graph.png)

So straight and organized! Now we can start working.

## Understanding how the password is checked

After making sure that all of the characters are alphanumeric, the program places the letters into a global array in jumps of 0x14 while keeping track of the sum. The sum is later compared to 0x3E2 giving us our third constraint on the password (the other two being length and alphanumericness).

The global array is then processed in a loop. This was the third challenge in the competition involving CRC's, so we quickly recognized the loop as calculating the crc64 of the global array (of length 0x100) with the letters of our password placed in the indexes as described above.
