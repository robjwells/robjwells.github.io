---
title: Terminal countdown
date: 2013-08-17 14:36
tags: ["Python", "Programming", "Shell"]
---

I’ve got some annual leave booked for the very end of September, which is pretty far away still — but I wanted to know exactly how many days I have to go before my break.

Usually I would just query [Wolfram Alpha][wa] but, since I’ve been spending a fair amount of time at the command line, I wondered if `date` in Unix could give me the answer.

[wa]: http://www.wolframalpha.com/input/?i=Days+until+December+25+2013

It’s easy to ask `date` to add or subtract an amount of time:

    bash:
    $ date -v +2w   # Now plus two weeks
    Sat 31 Aug 2013 13:14:20 BST

However there’s no built-in way to find the difference between two dates. So I wrote one. Now originally I was going to walk through that shell script but there were enough problems that I rewrote it in Python this morning.

But before I get to the Python code I want to discuss the shell script.

It took a date in [ISO format][iso] ([because][xkcd]) and ran it through `date` to get back a [Unix timestamp][unix]. This was then subtracted from the timestamp for the current date and divided by the number of seconds in a day to give the number of days difference.

[iso]: http://en.wikipedia.org/wiki/ISO_8601
[xkcd]: http://www.xkcd.com/1179/
[unix]: http://en.wikipedia.org/wiki/Unix_time

Unfortunately writing the script gave me a few headaches:

*   Unix timestamps can break.
    Passing a date before 1902 caused `date` to choke on my machine, and this varies from system to system.
*   Commands you expect to be reliable can differ wildly between systems.
    I used `egrep` to check the format of the provided date and used `\d` as the digit wildcard. But on my work machine, which runs Mac OS 10.6, you can only use `\d` with `grep -P`. That breaks `grep` on 10.8 at home.
    The nasty solution was to use an explicit range: `[0-9]`. Gross.
*   The bash scripting syntax is insane.
    Want to check if stdin is connected to an interactive terminal, so you know you won’t be getting data on stdin? Use `-t 0`.
    Meanwhile in Python: `sys.stdin.isatty()`.

The timestamp problem is an edge case as days aren’t a useful measure of time past a certain, short distance, so it was mainly the reliability and syntax complaints that pushed me to rewrite the script. I don’t consider `\d` to be exotic and with the removal of the `-P` option in newer versions of `grep` how can you expect to use it in portable code?

As for the syntax, while I was pleased I’d managed to lump together enough parts to make a working program, it’s not clear by any means — and this is just a 45-line wrapper around `date`! String comparisons in bash get to use `!=` and `==` but numbers are stuck with `-ne` and `-eq`? Oh god it’s *horrible*.

Anyway, let’s move on to the Python script:

    python3:
     1:  #!/usr/bin/env python3
     2:  
     3:  from __future__ import print_function
     4:  import sys
     5:  import os
     6:  import re
     7:  from datetime import datetime
     8:  
     9:  if len(sys.argv) == 2:
    10:    date = sys.argv[1]
    11:  elif not sys.stdin.isatty():
    12:    # Called in a pipeline
    13:    date = sys.stdin.read().rstrip('\n')
    14:  else:
    15:    # Print usage message if no date is supplied
    16:    script = os.path.basename(sys.argv[0])
    17:    print('Usage:  {0} YYYY-MM-DD\n'
    18:          '        prints number of days until or since the given date'
    19:          .format(script))
    20:    sys.exit(64)
    21:  
    22:  if not re.match(r'\d{4}-\d{2}-\d{2}', date):
    23:    print('Abort:  your date is not in YYYY-MM-DD format')
    24:    sys.exit(65)
    25:  else:
    26:    then = datetime.strptime(date, '%Y-%m-%d').date()
    27:  now = datetime.now().date()
    28:  days = (then - now).days
    29:  
    30:  if days == 0:
    31:    print("That's today!")
    32:    sys.exit(0)
    33:  
    34:  msg = str(days) + ' day'
    35:  if days not in [1, -1]:
    36:    msg += 's'
    37:  
    38:  if days < 0:
    39:    msg = msg.lstrip('-') + ' ago'
    40:  else:
    41:    msg += ' ahead'
    42:  print(msg)

It works in much the same way as the shell script. (In case anyone’s wondering, the `print_function` import is for Python 2 compatibility — just change the shebang line to plain `python`.)

Lines 9–13 handle input from an argument or stdin, and a usage message is printed (lines 14–20) if nothing is passed.

Next is the regular expression to check the date’s format (using `\d`! Yes!).
A warning is printed and the script exits if it doesn’t match, otherwise a datetime object is created using a `strptime` format string in the same way you would with `date` at the terminal. `date()` is immediately called on the object (line 26) because we want to work with full days only.

One nice thing about Python’s datetime module is timedelta, which lets you subtract one date from another and returns the difference — we do that in line 28 and extract the `days` attribute.

From here we’re just constructing the message printed to the user, with a check for the current date and then whether “days” should be plural. If the date is in the past we trim the minus sign in line 39, then stick on an appropriate adverb and print.

All told, we end up with this:

    $ days 2013-12-25
    130 days ahead
    $ days 2013-01-01
    228 days ago

I’ve posted both the [Python and shell versions as a gist][gist] if you’d like to compare the two.

[gist]: https://gist.github.com/robjwells/6256540
