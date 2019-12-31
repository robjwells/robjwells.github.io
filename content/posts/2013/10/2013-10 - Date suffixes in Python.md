---
title: Date suffixes in Python
date: 2013-10-07 22:51
tags: ["AppleScript", "Programming", "Python", "TextExpander"]
---

A little while ago I wrote about [using TextExpander to write dates][tedate], the bulk of which was given over to an Applescript that returned a long date complete with date suffixes.

[tedate]: /2013/03/setting-a-date-with-textexpander/

Since I’ve been writing more and more Python, I thought it would be fun to rewrite it to see the difference between the two.

First, here’s my original Applescript:

    applescript:
     1:  set theDate to the day of the (current date)
     2:  set theDay to the weekday of the (current date)
     3:  set theMonth to the month of the (current date)
     4:  set theYear to the year of the (current date)
     5:  
     6:  set lastChar to (the last character of (theDate as string)) as number
     7:  
     8:  if lastChar > 3 or lastChar is 0 or (theDate > 10 and theDate < 21) then
     9:    set theDate to (theDate as string) & "th"
    10:  else
    11:    set theSuffixes to {"st", "nd", "rd"}
    12:    set theDate to (theDate as string) & (item lastChar of theSuffixes)
    13:  end if
    14:  
    15:  return (theDay & ", " & theMonth & " " & theDate & ", " & theYear) as string

And now the Python:

    python3:
     1:  #!/usr/local/bin/python3
     2:  
     3:  from datetime import date
     4:  
     5:  today = date.today()
     6:  date_string = today.strftime('%A, %B #, %Y')
     7:  day = today.day
     8:  
     9:  if (3 < day < 21) or (23 < day < 31):
    10:    day = str(day) + 'th'
    11:  else:
    12:    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    13:    day = str(day) + suffixes[day % 10]
    14:  
    15:  print(date_string.replace('#', day), end='')

<div class="flag">
    <p>
        <strong>Update: <time>2015-01-17</time></strong>
    </p>
    <p>
        <a href="/2015/01/updated-date-suffix-script/">I’ve improved the Python code.</a> Please use the more recent code and not that above.
    </p>
</div>

A date object, kind of similar to Applescript’s `current date`, is constructed on line 5. This is used to build a formatted date on line 6, which is complete bar the day of the month. I swap it out for a # placeholder because both `strftime` options for the day fall short: `%d` is padded with a zero, and `%e` is padded with a space. So instead I pull out the day separately in line 7.

The date-testing logic on line 9 is simpler and more explicit in this version, testing first for any date that takes a -th. Those dates that require a different suffix get dumped to the else clause.

A bit of modulo arithmetic on line 13 reduces the date integer to the units digit, which is used to key into a dictionary holding the suffixes.

The day and its suffix are concatenated, and are inserted into the formatted date on line 15 using the `replace` string method (god I love Python’s string methods) and printed, with `end=''` suppressing the standard newline.

Though the line count is the same between the two, the Python version has about half the characters of the Applescript. I think the Applescript’s verbosity — which I don’t help with that conditional — makes it harder to understand at a glance, while the Python is very clear, excepting the `strftime` format string.

As a side note, I don’t actually use either of these scripts for my long date, having given in to “Weekday month day year” without a suffix or any commas. This can be constructed using TextExpander’s own date macros, which mirror `strftime` formatting: `%A %B %e %Y`. Still, a fun exercise.
