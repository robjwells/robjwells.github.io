title: Setting OS X’s environment
date: 2017-03-02 14:30

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

Trying to set a consistent environment in OS X is the single most frustrating thing I’ve ever tried to do on a Mac.

I’ve written three posts ([1][], [2][], [3][]) in the past few years trying to get to the bottom of this but *still* I have problems. (That’s why that giant disclaimer is on the top of this post!)

[1]: /2013/09/get-your-us-ascii-out-of-my-face/
[2]: /2014/12/locale-in-os-x-and-launch-agents/
[3]: /2014/12/locale-in-os-x-whats-the-current-situation/

This bit me again the other day when using a Jupyter notebook to [export from TextExpander][te-lb], with my favourite UnicodeDecodeError. Here’s an example:

[te-lb]: /2017/03/textexpander-to-launchbar-snippets/

<pre><code>-----------------------------------------------------------------
UnicodeEncodeError              Traceback (most recent call last)
&lt;ipython-input-8-c4b3c1d6f2e6&gt; in &lt;module&gt;()
      1 with open('/Users/robjwells/Desktop/testfile', 'w') as f:
----> 2     f.write('☃')

UnicodeEncodeError: 'ascii' codec can't encode character
'\u2603' in position 0: ordinal not in range(128)
</code></pre>

Now, this machine has been upgraded all the way from 10.7 and my understanding is that if you’ve a fresh install of a more recent version than you should be OK as far as the encoding-related environment variables (`LANG`, `LC_CTYPE`, `LC_ALL`). [A recent Python enhancement proposal][pep] includes the paragraph:

[pep]: https://www.python.org/dev/peps/pep-0538/#background

> On Apple platforms (including both Mac OS X and iOS), this [ensuring Python is set to use UTF-8] is straightforward, as Apple guarantees that these [Python start-up] operations will always use UTF-8 to do the conversion.

If you’ve ready my posts linked above, particularly [Locale in OS X and Launch Agents][2], a good question arises: “I thought you’d figured this out!”

Well, yeah, me too! I have a script that runs at start-up designed to set my environment up. But it’s not reliable — I think because it may run after other start-up items (both Launch Agents & Daemons, and the Login Items listed in System Preferences). One of those is my Jupyter notebook server, hence the problem above.

Having the environment script run as the root user doesn’t solve the problem — in fact it means it has no effect at all.

(My way of checking whether a program has inherited my script-set environment variables is to define `RJWENVSET` as well.)

And then there’s the `PATH`, which I used to set in the same script using `launchctl setenv` like my other environment variables. Which doesn’t work. There’s a suggestion on [a GitHub issue for a tool meant to resolve this problem][env-sync] that the following command could reliably set the path:

[env-sync]: https://github.com/ersiner/osx-env-sync/issues/1#issuecomment-230053839

    bash:
    sudo launchctl config user path $PATH

But that doesn’t work for me. You can swap `user` for `system` but I’m wary of doing that.

This problem is ludicrously frustrating. Apple deprecated /etc/launchd.conf “for security considerations” but it means there’s no reliable way of setting variables that will be inherited by your programs, and so no way of having a consistent environment.

What a pain in the arse.

Right now, I’m doing the following:

* I have my environment.sh file set `LANG`, `LC_ALL`, `LC_CTYPE`, `PYTHONPATH`, `RJWENVSET` when it is run at start-up by [Lingon][] (for “all users”, though I’m not sure if this is any more effective than using “me” — I’m the only user on this machine).
* My Lingon start-up items have environment variables and their `PATH` set explicitly.
* I currently restart other start-up items that don’t pick up the variables set by environment.sh — but that doesn’t solve the `PATH` problem so you’ll want to [set that explicitly][drang].

[Lingon]: https://www.peterborgapps.com/lingon/
[drang]: http://leancrew.com/all-this/2017/03/the-keyboard-maestro-scripting-environment/

But for Pete’s sake I wish I could just define variables in ~/.launchd.conf and be done with it.
