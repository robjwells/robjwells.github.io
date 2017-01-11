title: Locale in OS X — what’s the current situation?
date: 2014-12-22 10:16
tags: OS X

One thing that I didn’t but meant to mention in [my post about setting the locale correctly in OS X][locales-osx] is a [recent post by Python core developer Nick Coghlan][coghlan], where he talks generally about locales and languages.

[locales-osx]: /2014/12/locale-in-os-x-and-launch-agents/
[coghlan]: http://www.curiousefficiency.org/posts/2014/08/multilingual-programming.html

One of the points he makes is about getting OS vendors to transition to using Unicode. Nick writes:

> For POSIX systems, there are still a lot of systems that don’t use UTF-8 as the preferred encoding and the assumption of ASCII as the preferred encoding in the default `C` locale is positively archaic.

Which has been my experience with OS X (see [my recent locales post][locales-osx] and also parts of [last year’s][ascii-utf8]). But then he writes (emphasis mine):

> Mac OS X is the platform most tightly controlled by any one entity (Apple), and they’re actually in the best position out of all of the current major platforms when it comes to handling multilingual computing correctly.
> 
> They’ve been one of the major drivers of Unicode since the beginning … and *were able to force the necessary configuration changes on all their systems*

[ascii-utf8]: /2013/09/get-your-us-ascii-out-of-my-face/

Which brings me back to something I noted in my last post: *I don’t have a clean install of OS X*. It’s been upgraded from 10.7 up through 10.10. Same story with the machines at work (which are even older).

So is Apple correctly setting the locale now? If any readers have a new machine or a clean install of OS X, could you please check and let me know? (A quick way to test would be to open Script Editor and run `do shell script "locale"`.)
