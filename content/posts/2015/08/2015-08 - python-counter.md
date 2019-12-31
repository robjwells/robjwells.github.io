---
title: Python Counter gotcha with max
date: 2015-08-07 13:49
tags: ["Python"]
---

<div class="flag">
  <p><strong>Update 2015-08-10</strong></p>
  <p>
    The example given now uses strings as the keys instead of numbers
    to ward off any confusion between the keys and their counts.
  </p>
</div>

Getting the greatest element from a sequence in Python is dead simple: just use the built-in [max][] function.

Storing the frequency of items is also dead easy with [collections.Counter][counter]:

    pycon:
    >>> from collections import Counter
    >>> c = Counter('abracadabra')
    >>> print(c)
    Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

The greatest item in a counter is obviously the most common, so surely we’ll just …

    pycon:
    >>> max(c)
    'r'

*What?* Here’s the gotcha: Python counters are a dictionary subclass. Call `max` with a dictionary and it’ll get the greatest key, because keys are what you get when you iterate over a dictionary. Same deal.

To get the most common element you have to use — surprise! — `Counter.most_common()`. Without arguments this produces a list of tuples (item, count), sorted by count:

    pycon:
    >>> c.most_common()
    [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1)]

So to get the actual most common element, you do:

    pycon:
    >>> c.most_common(1)[0][0]
    'a'

Where the argument `1` limits it to the first tuple.

But what if the counter’s empty? You’ll get an IndexError trying to index into the list returned by `most_common()`:

    pycon:
    >>> d = Counter()
    >>> d.most_common()
    []
    >>> d.most_common()[0][0]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IndexError: list index out of range

In Python 3.4 `max` got the `default` argument, which you can use to get a default value when a sequence is empty. Here’s how to get similar behaviour with Counter:

    python3:
    d.most_common(1)[0][0] if d else None

This takes advantage of the "falsey" nature of an empty dictionary to give you `None` without having to handle an IndexError.

[max]: https://docs.python.org/3/library/functions.html?highlight=max#max
[counter]: https://docs.python.org/3/library/collections.html?highlight=collections.counter#collections.Counter

