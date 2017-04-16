---
title: Padding regex groups in Name Mangler
date: 2016-10-21 22:45
---

I’m a big fan of [Name Mangler by Many Tricks][nm], an interactive file renaming application for everything from simple operations to really quite complex and powerful ones, with a comfortable and straightforward interface.

[nm]: http://manytricks.com/namemangler/

I don’t use it particularly often but it’s nice to have in the toolbox for things that might otherwise be frustrating.

One of my most common tasks for Name Mangler is converting the filename convention used internally at work for naming page files to a more general format we use for our external partners.

Here’s what they look like:

    # Internal
    1_Front_221016.pdf
    # External
    MS_2016_10_22_001.pdf

Normally this is done automatically with a scheduled script, but occasionally that script fails (at a different stage) and it has to be done by hand. Now obviously this involves a regular expression, and the page number group (at the start of the internal name, end of the external) is zero-padded so it’s three digits long.

So, in Name Mangler’s advanced renaming syntax that becomes:

    [pad
        "$1"
        to "-3"
        with "0"
    ]

right?

Well, no. What happens is interesting. The literal string `$1` is zero-padded until it’s three digits long: `0$1` (one extra zero). But after that the regex replacement is made, so page #1 becomes `01`: 1 with one zero on the front.

To Many Tricks’s great credit, they responded to the support ticket I raised with example code in less than a day, along with an explanation of what’s happening by the developer.

The trick is, instead of providing the group name as the argument to pad, to perform the regex search in-line:

    [pad
        [findRegularExpression
            "^(\d+)_.*$"
            in <name>
            replace with "$1"
        ]
        to "-3"
        with "0"
    ]

This means that when `pad` gets its arguments, it’s exactly what you want to pad.

By necessity this uses regexes twice: one for parsing the date and constructing most of the name, and this for finding and padding the page number. Perhaps the reason why I missed this approach by myself is that in the Python code, the regex search is performed once and the groups placed in this format string:

    MS_{date:%Y}_{date:%m}_{date:%d}_{page:03}.pdf

Which takes care of the padding with no fuss. (At this point, the date has been parsed for completeness’s sake, hence the strftime codes.)

That might lead to a question about why I don’t just use Python to do this. And the answer is that, once you’ve got a recipe that works for you, Name Mangler is painless and flexible. Really, [check it out][nm].
