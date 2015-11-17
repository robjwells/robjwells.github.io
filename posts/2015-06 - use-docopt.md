title: You should be using docopt
date: 2015-06-30 12:21
tags: Python, Programming

If you write any command-line tools that have a need for a help message, then you should really try [docopt][], which gets you out of having to write argument-parsing code yourself. I’ve mentioned it before, [briefly][], and I wouldn’t want to be without it.

[docopt]: http://docopt.org
[briefly]: http://robjwells.com/2014/01/hijacking-the-bbc/

For an example I’m going to pick on Dr Drang, who was unfortunate enough to [post such a script recently][drang]. Sorry!

[drang]: http://leancrew.com/all-this/2015/06/weather-history-without-the-web/

Take a look at his original help message, and then check out the following:

    Return NCDC weather report for the given date.

    Usage: ncdc [options] DATE

    Options:
        -a, --ascii        : return ASCII file instead of HTML
        -d, --daily        : return daily summary instead of hourly reports
        -m, --month        : entire month, not just a single day
        -p, --precip       : precipitation (hourly only, overrides -d)
        -s, --station STA  : the station abbreviation [default: ORD]
                             O'Hare     ORD
                             Midway     MDW
                             Palwaukee  PWK
                             Aurora     ARR
                             Waukegan   UGN
                             Lewis      LOT
                             DuPage     DPA
                             Lansing    IGQ
                             Joliet     JOT
                             Kankakee   IKK
                             Gary       GYY
        -h, --help         : print this message

It’s essentially the same, but with a couple of minor changes:

*   The description of the script comes before the usage.
*   The date argument is now in upper case.
*   I've added long options to make things a little more readable.
*   The description of the station option gains `[default: ORD]`,
    which specifies — shocker — the default value for that option.

And here’s the new argument-handling code, to replace lines 54–87 in his script (there’s also the new line `from docopt import docopt` earlier on):

    python:
    # Handle options.
    args = docopt(help)
    sta = args['--station'].upper()
    ascii = args['--ascii']
    month = args['--month']
    precip = args['--precip']
    daily = False if precip else args['--daily']

    d = parse(args['DATE'], dayfirst=False)

Provide `docopt` with your help message and you get back a dictionary. Options that take an argument give you back the argument, the default or None (if you don’t set a default). The switch-type options are booleans, being False if they’re not used.

Calling the script incorrectly prints the basic usage pattern, and `docopt` gives you the help options for free. (You don’t have to include them in the help message, even, but you should.)
