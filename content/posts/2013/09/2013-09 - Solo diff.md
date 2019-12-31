---
title: "Solo diff"
date: 2013-09-13T20:39:00
tags: ["Python", "Programming", "Copy editing", "BBEdit"]
---

At work we edit the reporters’ copy in plain text files using [TextWrangler][], duplicating their original at the bottom of the file before we start subbing.
It’s a nice, quick way of having something to refer back to without the hassle of using (and training people to use) a real [VCS][].

[TextWrangler]: http://barebones.com/products/textwrangler/
[VCS]: http://en.wikipedia.org/wiki/Revision_control

It began as a loose convention, with different people having their own way of marking off the original copy. To make it completely painless, and to bring in a standard method, I wrote this short Python script a couple of months ago:

    python3:
    #!/usr/bin/env python3
    from sys import stdin
    orig = stdin.read()
    dupe = "{0}\n\n\n\n#### Original Copy ####\n\n\n\n{0}".format(orig)
    print(dupe)

I installed it to everyone’s text filters folder — TextWrangler provides the document’s text (or the selection) to text filters via stdin — and people tend to use it.

We hired two new subs over the summer and I got into the habit of using the “Compare Two Front Windows” command to check their subbed copy against the original, so I could offer them specific advice.

But manually creating two new windows and pasting in the text can be a pain — you end up juggling lots of windows and it’s easy to mix up the copy so that the “older” pane is showing the subbed text.

Thankfully both of the new people use the duplication script consistently, so it’s easy to use a regular expression to split the file into original and subbed versions. Armed with this knowledge, I wrote a script to automate the comparison, using TextWrangler’s `twdiff` command-line tool.

<div class="flag">
    <p>The code below is written for BBEdit, which I use at home. Except for <code>BB_DOC_PATH</code>, I swap out <code>bb</code> for <code>tw</code> in the script used at work.</p>
</div>

    python3:
     1:  #!/usr/bin/env python3
     2:  
     3:  import os
     4:  import re
     5:  import subprocess
     6:  
     7:  os.chdir('/tmp')
     8:  with open(os.environ['BB_DOC_PATH']) as full_file:
     9:    sub_copy, orig_copy = re.split(r'#{2,} original copy #{2,}',
    10:                                   full_file.read(), flags=re.I)
    11:  
    12:  with open('bb_orig_copy', 'w') as orig_file:
    13:    orig_copy = orig_copy.strip() + '\n'
    14:    orig_file.write(orig_copy)
    15:  
    16:  with open('bb_subbed_copy', 'w') as sub_file:
    17:    sub_copy = sub_copy.strip() + '\n'
    18:    sub_file.write(sub_copy)
    19:  
    20:  subprocess.call(['bbdiff', 'bb_orig_copy', 'bb_subbed_copy'])

The entire file is split into subbed and original sections in lines 9 & 10, and on lines 14 & 18 each of those is written to a file (in `/tmp` — line 7). The leading and trailing whitespace is stripped from each and a newline added in order to clean up the comparison.

The regex on lines 9 & 10 uses a variable number of hash marks and the case-insensitivity flag because on occasion I forget to duplicate the copy first, edit the story, and then go back and fill in the separator by hand.

All of the file interaction is handled in `with` blocks (context managers), which automatically close the files once the block’s statements are executed. Not a big issue in a script this size, but good practice.

Finally we call the diff utility with the names of the two temporary files.

I’ve got this saved in TextWrangler’s scripts folder. Initially I wrote it as a text filter, splitting the contents provided on stdin. But since filters replace the document (or selection) the text had to be written to stdout at the end of the script so that TextWrangler didn’t delete everything.

And it’s also *not a filter*, so I was pleased to find out that several environment variables are set when a script is invoked, one of which is the path to the file that the script was called on.

I’ve tested the script with Python 2.7.5 and it seems to work fine, but with the differences in its Unicode handling I can’t say for certain that some nasty encoding gremlin won’t raise its head.
