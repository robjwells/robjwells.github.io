---
title: "Get your US-ASCII out of my face"
date: 2013-09-14T14:05:00
tags: ["OS X", "Programming", "Python", "Shell"]
---

<div class="flag">
  <p><strong>Warning: The contents of this post may not be up to date!</strong></p>
  <p>Sorry, but if you’re searching for answers about why you can’t reliably set environment variables in OS X (particularly <code>PATH</code>), the information below may be out of date.</p>
  <p>Apple has changed the system so many times in so many different ways it’s difficult to find <em>anything</em> on the internet about this that is correct and up-to-date, so I’ve placed this warning on the top of every post I’ve written about it.</p>
  <p>As of 2017-03-02 it appears that the best collection of information is <a href="https://github.com/ersiner/osx-env-sync">the osx-env-sync project on GitHub</a> and its associated issues.</p>
  <p>Be wary of anything that you find on StackOverflow: the answers there may well have been correct at the time but incorrect now.</p>
  <p>For reference, my own posts on this problem (newest first) are:</p>
  <ul>
    <li><a href="/2017/03/setting-os-xs-environment/">Setting OS X’s environment</a></li>
    <li><a href="/2014/12/locale-in-os-x-whats-the-current-situation/">Locale in OS X — what’s the current situation?</a></li>
    <li><a href="/2014/12/locale-in-os-x-and-launch-agents/">Locale in OS X and Launch Agents</a></li>
    <li><a href="/2013/09/get-your-us-ascii-out-of-my-face/">Get your US-ASCII out of my face</a></li>
  </ul>
</div>

When I was writing the script in [yesterday’s post][solo-diff] I came across this bizarre text encoding problem:

    UnicodeDecodeError: 'ascii' codec can't decode byte
    0xe2 in position 5: ordinal not in range(128)

Ascii what? We’re all Unicode now, don’t you know? If I’m taking in UTF-8 text, keeping it in a Unicode string, and then writing it out to UTF-8 encoded text files where is goddamn Ascii creeping in?

[solo-diff]: /2013/09/solo-diff/

This first occurred at work, while I was *trying to work*, so my horrendous hack solution was to switch the temporary files into binary mode and encode the two strings into UTF-8 before writing them out. (This was when the script was still a text filter, so the problem was only on the back end.)

That’s a horrible hack. Bytes! Yuck! So in my next attempt I explicitly opened the files with a UTF-8 encoding. Which was still gross. And totally unnecessary. This is Python 3, everything’s Unicode, all the defaults are UTF-8, why am I having to specify the encoding at every point?

This was the point at which I found [a relevant Stack Overflow question][so]. Unfortunately the answer there was to tinker with Python’s start-up files in a way that was always discouraged and had since been removed from Python 3.

[so]: http://stackoverflow.com/questions/5981570/encoding-errors-running-python-from-within-bbedit?rq=1

Hm. But what’s this about `sys.setdefaultencoding`? So I started poking around with this terrible little script:

    python3:
    #!/usr/bin/env python3
    import os
    import sys
    import locale
    entire_file = open(os.environ['BB_DOC_PATH'], 'r')
    print(os.environ)
    print(entire_file.encoding)
    print(sys.getdefaultencoding())
    print(locale.getpreferredencoding())

For the last three lines, which print the encodings used, I got:

    US-ASCII    # File encoding
    utf-8       # sys.getdefaultencoding
    US-ASCII    # locale.getpreferredencoding

So the system setting wasn’t the culprit. But why is the system encoding different to the locale, which seems to determine the default encoding with which files are opened?

Locale refers to the environment variables in my Terminal, but when I try `echo $LANG` it’s set to `en_GB.UTF-8` — surely that’s not the problem?

### WRONG.

As [this thread][lang] eventually made me realise, I didn’t actually have `$LANG` set to anything — it was all smoke and mirrors that cleared away when I ran the script through BBEdit. (I also had a similar problem with Applescript’s `do shell script` and it looks like [Sublime Text users][sublime] have also run into it.) Checking the `os.environ` output from the script above confirmed it: no `$LANG`.

[lang]: http://www.velocityreviews.com/forums/t695885-print-and-unicode-strings-python-3-1-a.html
[sublime]: http://www.sublimetext.com/forum/viewtopic.php?t=13753

The root of the problem is that if a locale isn’t set it defaults to the C locale — meaning US-ASCII in OS&nbsp;X. **The solution is to explicitly set $LANG in your .bash_profile**:

    bash:
    export LANG="en_GB.UTF-8"

I’ve also got that line in ~/.bashrc for safety, but do bear in mind that *some shells will ignore both* ~/.bash_profile and ~/.bashrc.

You could set the other `LC_*` keywords as well, if you like, but `$LANG` should be enough according to [the man page for `locale`][manlang]:

    LANG         Used as a substitute for any unset LC_* variable.  If LANG
                 is unset, it will act as if set to "C".  If any of LANG or
                 LC_* are set to invalid values, locale acts as if they are
                 all unset.

[manlang]: https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/locale.1.html

<div class="flag">
  <p><strong>Update 2013-09-21</strong></p>
  <p>I’ve just re-watched <a href="http://nedbatchelder.com/text/unipain.html">Ned Batchelder’s great Pragmatic Unicode video</a> and while setting the <code>$LANG</code> environment variable is a handy solution on your own machines, it’s not a good fit when you’re writing a program that will run on systems where you can’t control the default encoding.</p>
  <p>In such cases it makes sense to adopt his “Unicode sandwich” approach of explicitly decoding I/O and then working on the resulting Unicode.</p>
</div>
