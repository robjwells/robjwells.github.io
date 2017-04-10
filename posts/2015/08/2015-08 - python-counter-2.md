title: Python’s Counter class, again
date: 2015-08-10 22:34
tags: Python


I made a mistake in [my recent post about Python’s Counter class][post] by using numbers in the example rather than strings. It meant it wasn’t clear what I actually wanted out of the counter. (While I was writing it, I was getting confused between the keys and their counts myself. I should have taken the hint.) That post’s now been updated.

I had a lovely email from [Jacob Söndergaard][js] that prompted me into clarifying things, and also started me thinking about ways you can still use `max` on the counter to get the most common item. Here’s what I’ve got:

    python3:
    from collections import Counter
    c = Counter('abracadabra')
    most_common = max(c.items(), key=lambda t: t[1])[0]

Here `max` gets a sequence of tuples (key, count) from `c.items()` and the custom `key` function tells it to choose the greatest element based on the count. The `[0]` index at the end ensures you just get the key, not the count.

But should you do this? No. Please don’t. At this point you’re effectively duplicating the way that Counter implements `.most_common()` internally. (Here’s [the Python source for the method][most_common].) That’s at best too — the implementation does something more complicated if you only want the top n most-common elements.

Also: [Abracadabra][].

[post]: /2015/08/python-counter-gotcha-with-max/
[js]: http://jacobsondergaard.com
[most_common]: https://hg.python.org/cpython/file/tip/Lib/collections/__init__.py#l530
[Abracadabra]: https://www.youtube.com/watch?v=fH850qp85Zk
