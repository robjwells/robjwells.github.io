title: Updated date suffix script
date: 2015-01-17 18:56
tags: Python, Programming

One of my favourite scripts is [a snippet of Python that produces a date with an ordinal suffix][suffixes]. It’s [short, simple][good_code], and was probably the first thing I did in Python that made me sit back and smile.

[suffixes]: /2013/10/date-suffixes-in-python/
[good_code]: http://stilldrinking.org/programming-sucks

But it contains a hack to prevent the day of the month from being prefixed with a zero (`%d`) or a space (`%e`). I recently [discovered][drang] that you can use a hyphen in the format specifier to prevent this: `%-d`.

[drang]: http://www.leancrew.com/all-this/2013/02/new-flexible-timestamps-in-drafts/

Also, the method of inserting the suffixed day just uses `str.replace` to replace a hash mark. But what if you need a hash mark in your date string? Not ideal, and easily solved with Python’s `str.format`.

Here’s the new code:

    python3:
     1:  from datetime import date
     2:  
     3:  def ordinal_suffix(day):
     4:    if 3 < day < 21 or 23 < day < 31:
     5:      return 'th'
     6:    else:
     7:      return {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]
     8:  
     9:  today = date.today()
    10:  date_string = today.strftime('%A, %B %-d{suffix}, %Y')
    11:  print(date_string.format(suffix=ordinal_suffix(today.day)))

Starting with the date string on line 10, `%-d` surpasses the prefix, and we include a replacement field (`{suffix}`). That gets formatted with the output of the `ordinal_suffix` function.

The logic there is largely the same as [before][suffixes] <del datetime="2015-01-17">except that I’m treating the 1x numbers as a special case in line 4 (which I appreciate is a bit silly given the range 1-31, but 0x, 2x and 3x days all conform)</del>. <ins datetime="2015-01-17">Given a bit more thought, it makes sense to handle all `th` suffixes in the True part of the conditional.</ins> Everything else, as before, gets reduced to the final digit and is used to index into the dictionary in line 7 <del datetime="2015-01-17">— using `get` to supply `th` as a default</del>.

It may seem silly to revisit this — this may as well be [fizzbuzz][] — but I really don’t like leaving blog posts that I *know* are incorrect in some way. I hate the idea that someone may stumble across a post and take away an idea that isn’t the best that I could provide them. And really this is a learning process for me: I think something is one way, write about it, come to a better conclusion, and write about it again.

[fizzbuzz]: https://en.wikipedia.org/wiki/Fizz_buzz
