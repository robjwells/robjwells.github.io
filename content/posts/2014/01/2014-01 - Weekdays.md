---
title: "Next and last weekdays"
date: 2014-01-11T16:08:00
tags: ["Python", "Programming", "TextExpander"]
---

I was recently reminded of David Sparks’s [TextExpander date snippets][ds-dates], the most interesting of which use AppleScript to insert the date for the next occurrence of a certain weekday. (And were [written by Ben Waldie][bw].)

[ds-dates]: http://macsparky.com/blog/2013/5/text-expander-snippets-date-and-time
[bw]: http://www.tuaw.com/2013/01/21/mac-productivity-ten-textexpander-date-snippets/

Out of curiosity, I wrote a Python command-line tool called dayshift that does something similar. Its main differences are that it doesn’t have to be set up for specific days like the AppleScript snippets, and that it can find the date for a past weekday (“last Monday”) as well as a future one (“next Monday”).

    python3:
     1:  #!/usr/local/bin/python3
     2:  """
     3:  Print the date of the next or last specified weekday.
     4:  
     5:  Usage:
     6:    dayshift next <weekday> [--format=<fmt> --inline]
     7:    dayshift last <weekday> [--format=<fmt> --inline]
     8:  
     9:  Options:
    10:    --format=<fmt>, -f <fmt>  A strftime format string
    11:                              [default: %Y-%m-%d]
    12:    --inline, -i              Omit trailing newline
    13:  
    14:  """
    15:  from docopt import docopt
    16:  from datetime import date, timedelta
    17:  
    18:  WEEKDAYS = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
    19:              'fri': 4, 'sat': 5, 'sun': 6}
    20:  
    21:  args = docopt(__doc__)
    22:  starting_offset = 2 if args['next'] else -2
    23:  start_date = date.today() + timedelta(starting_offset)
    24:  start_integer = start_date.weekday()
    25:  target_integer = WEEKDAYS[args['<weekday>'][:3].lower()]
    26:  
    27:  if args['next']:
    28:    offset = target_integer - start_integer
    29:  elif args['last']:
    30:    offset = start_integer - target_integer
    31:  
    32:  if offset <= 0:
    33:    offset += 7
    34:  
    35:  if args['last']:
    36:    offset /= -1    # Make the offset negative
    37:  
    38:  target_date = start_date + timedelta(offset)
    39:  ending = '' if args['--inline'] else '\n'
    40:  print(target_date.strftime(args['--format']), end=ending)

<div class="flag" id="update_2014-01-13">
  <p><strong>Update <time>2014-01-13</time></strong></p>
  <p>I’ve added an offset to the starting day (lines 22 & 23) to skip past the two days before and after the current date. The line numbers in the explanation below have been altered to match.</p>
  <p>You might like to look at the <a href="https://gist.github.com/robjwells/8370699">corresponding Gist</a> in case I’ve made any further changes.</p>
</div>

The interface is created by [docopt][] in line 21 from the script’s docstring (lines 2–14).

[docopt]: http://docopt.org

After parsing the arguments we reduce the given weekday to its integer representation in line 25 by getting its first three characters, converting them to lowercase and using that string to key into the `WEEKDAYS` dictionary (lines 18 & 19).

On line 24 we get the integer for a starting date which is offset forward or backward by two days (lines 22 & 23). You can adjust the forward and backward offsets separately, depending on where you draw the line.

Now the `next` and `last` commands come into play, deciding how we compare the two weekday integers (lines 27–30). In both instances we can end up with 0 or a negative number so we add 7 to the offset (line 33).

But surely we want a negative number if we’re after the “last” weekday? Yes, but not just yet — at this point it tells us that we’ve passed the given weekday in the current week (if `next`) or the given weekday is still to come (if `last`). We add 7 to move outside of the current week.

To ensure we go back in time we specifically invert the offset in line 36, before adding it to the starting date in line 38 to reach the target date.

Now the two options shown in the docstring come into play. Line 39 uses the `--inline` flag to determine whether the printed string ends in a newline or not — handy when the script is called by a snippet inserted in the middle of some text.

The other option, `--format`, determines how the date is printed. I use docopt’s ability to have default values (see line 11) to print an [ISO 8601 date][iso] if another format isn’t given. This lets me pass the argument directly to `strftime` in line 40.

[iso]: http://en.wikipedia.org/wiki/ISO_8601

### Using the script in TextExpander

The script works great as a command-line utility:

    $ dayshift next Wednesday
    2014-01-15
    $ dayshift last Wednesday
    2014-01-08

But, returning to the original use case, I recommend two approaches.

You can set up individual snippets to find the next or last occurrence of a certain weekday. Add a new shell script snippet, with code similar to this:
    
    bash:
    #!/bin/bash
    /path/to/dayshift next Monday -i

Or you can use TextExpander’s fill-in feature to let you pick the options on the fly (line breaks inserted for readability):

    bash:
    #!/bin/bash
    /path/to/dayshift %fillpopup:name=Next/Last:default=next:last%
    %fillpopup:name=Weekday:default=Monday:Tuesday:
    Wednesday:Thursday:Friday:Saturday:Sunday% -i

That looks pretty gross there, and it doesn’t look good in use either:

![Screenshot of the dayshift fill-in TextExpander snippet](/images/2014-01-11_weekdaysfillin.png)

But it gives you a lot of control and you can tab between the fields.

<div class="flag" id="update_2014-01-12">
  <p><strong>Update <time>2014-01-12</time></strong></p>
  <p>Shortly after posting this yesterday, <a href="http://leancrew.com/all-this/">Dr Drang</a> sent me a nice email pointing out a <a href="http://www.leancrew.com/all-this/2012/09/eight-days-a-week/#comment-24659">comment by Dave Cross</a> on how to use the <code>date</code> utility in Unix to similar effect, which in its simplest form is <code>date -v+weds</code> (to get next Wednesday’s date).</p>
  <p>I recommend reading <a href="http://www.leancrew.com/all-this/2012/09/eight-days-a-week/">the entire post</a> that comment is in reply to as it addresses a very similar situation to the one above, but with an illuminating look at working with weekdays as integers.</p>
</div>
