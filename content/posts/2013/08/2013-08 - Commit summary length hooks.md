---
title: Commit summary length hooks
date: 2013-08-03 13:31
tags: Git, Mercurial, Python
---

Despite planning to take a break from doing computer work in my spare time, I’ve haven’t stopped playing with Mercurial and Git.

Right now I’m learning towards Mercurial (and am using it to track these blog posts) but I will still be using Git, not least because of [GitHub][gh].

[gh]: https://github.com/robjwells

So when I wrote my first commit hook I did it in both flavours. It’s a simple Python script that rejects a commit if the first-line summary is too long (over 50 characters) or too short (10 characters). The idea is to make sure `hg log` and `git log (--oneline|--pretty=short)` are informative but brief.

### Mercurial

    python3:
     1:  #!/usr/bin/env python3
     2:  
     3:  import os
     4:  import sys
     5:  from termtools import colour
     6:  from subprocess import check_output
     7:  
     8:  node = os.environ["HG_NODE"]
     9:  message = check_output(["hg", "log", "-r", node,
    10:                          "--template", "{desc}"]).decode()
    11:  summary_length = len(message.splitlines()[0])
    12:  
    13:  if summary_length > 50:
    14:    print(colour("! Changeset summary is too long (> 50c)", "red"))
    15:    sys.exit(1)
    16:  elif summary_length < 10:
    17:    print(colour("! Changeset summary is too short (< 10c)", "red"))
    18:    sys.exit(1)

Many of [Mercurial’s hook types][hghooks] provide useful data as shell variables. In line 8 we get the node (hash) of the changeset about to be committed and use that on line 9 & 10 to fetch the commit message.

[hghooks]: http://www.selenic.com/mercurial/hgrc.5.html#hooks

The call to check_output on those lines is a little confusing, but it’s essentially the equivalent of this terminal command:

    hg log -r $HG_NODE --template {desc}

Line 11 finds the length of the first line of the commit message, and lines 13–18 checks its length. If the summary is too long or short a warning is printed and the script exits with a non-zero status to tell Mercurial to reject the commit.

The colour function called on lines 14 and 17 is used to turn the warning text red. I’ll explain it below.

### Git

    python3:
     1:  #!/usr/bin/env python3
     2:  
     3:  import sys
     4:  from termtools import colour
     5:  
     6:  message = open(sys.argv[1])
     7:  summary_length = len(message.readline().splitlines()[0])
     8:  
     9:  if summary_length > 50:
    10:    print(colour("! Commit summary is too long (> 50c)", "red"))
    11:    sys.exit(1)
    12:  elif summary_length < 10:
    13:    print(colour("! Commit summary is too short (< 10c)", "red"))
    14:    sys.exit(1)


[Git’s hooks][githooks] include one specifically for the commit message, and when it is called Git feeds it a file containing the message — that’s what we open on line 6.

[githooks]: http://git-scm.com/docs/githooks

We read a single line from the file on line 7, but still use the splitlines method as in the Mercurial version in order to gracefully handle newlines at the end — I don’t want to unconditionally chop the last character in case it’s actually part of the summary.

The if block at the end is almost identical to the Mercurial version, save for the “commit” replacing “changeset”. This is just me trying to avoid blindly using Git terminology when discussing Mercurial.

### Usage

I include the hook in my main Mercurial config file (`~/.hgrc`), which means it applies to all repositories:

    [hooks]
    pretxncommit.summary_length = path/to/hook/file.py

The first part of the second line is the hook type, which sets when the script should be called, and the bit after the dot is a custom name — this lets you have multiple scripts attached to a certain hook type.

With Git things are a little more tricky, as the script (or a link to it) must appear in each repository’s `.git/hooks/` directory. As far as I’m aware there isn’t a built-in way of setting global hooks. I’ve toyed with the idea of writing my own little program to help set up hooks but I’m not sure if I can be bothered. I guess it will come down to how often I use hooks (and Git itself).

(Benjamin Meyer’s [git-hooks][icefox-githooks] tool is designed to help with this, but it’s written as a shell script and I can’t quite get my head round it.)

[icefox-githooks]: https://github.com/icefox/git-hooks


### Terminal colouring

In both scripts the printed warnings are run through a colour function, which is something I whipped up with exactly this situation in mind.

    python3:
     1:  def colour(str, col, background=False):
     2:    COLOURS = {'black': "30",
     3:               'red': "31",
     4:               'green': "32",
     5:               'yellow': "33",
     6:               'blue': "34",
     7:               'magenta': "35",
     8:               'cyan': "36",
     9:               'white': "37"}
    10:    escape = "\x1b"
    11:    reset = escape + "[0m"
    12:    reverse = ";7"
    13:  
    14:    colour_code = COLOURS[col.lower()]
    15:    start = escape + "[" + colour_code
    16:    if background:
    17:      start += reverse
    18:    start += "m"
    19:  
    20:    return (start + str + reset)

It wraps [ANSI colour codes][ansi] around a string and returns it. The action occurs in lines 14-18, where control codes are concatenated with the colour number fetched from the dictionary on lines 2-9. There’s an option to colour the background instead of the text, using the reverse code. The colour codes get stuck on the front of the string and a reset code is put on the end.

[ansi]: http://en.wikipedia.org/wiki/ANSI_escape_code#Colors

You could keep this function in the hook script itself, but I keep it inside a module in Python’s search path (hence the import statements in the hooks).

If you want more features the [termcolor module on PyPI][termcolor] allows for setting different foreground and background colours as well as bold text, underlines, etc.

[termcolor]: https://pypi.python.org/pypi/termcolor

I decided against using termcolor as I wanted to write my own as a test and because most of those options end up looking very ugly or are unnecessary. Coloured and reversed text is enough for me.
