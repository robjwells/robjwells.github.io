title: First brush with modulo speed
date: 2013-06-29 12:05
tags: Programming

I had read that the modulo operator (remainder after integer division) was slow but had never had a chance to try to break it myself, until a couple of days ago. I was distracted from my [current project][dip] by [Project Euler][pe], after searching for a way to test and improve my programming and maths skills.

[dip]: http://getpython3.com/diveintopython3/
[pe]: http://projecteuler.net

Project Euler is a collection of problems designed to exercise those skills and its first, simplest task is to add up the multiples of 3 and 5 below 1,000, which I first solved with a fairly typical “brute-force” approach:

    python3:
    sum = 0
    for x in range(1, 1000):
        if x % 3 == 0 or x % 5 == 0:
            sum += x

This iterates over the numbers 1 through 999, checking to see if there’s a remainder after dividing by 3 or 5. After finishing, I read on the problem’s forum thread of a way of achieving the result with a little more maths and without using the modulo.

I tried it out for fun and to be honest wasn’t impressed — when timed with the Unix `time` command both methods took around 0.025 seconds.

So I decided to kick the limit up a bit, from 999 to 999,999,999.

The modulo method took 4 minutes and 24.506 seconds (264.506s) while the more mathematical approach held steady at 0.026 seconds. Over 10,000 times as fast. Yes, I double-checked the results.

The modulo code was similar to that above while the other method was written like so:

    python3:
    def sum_series(multiple, top_limit):
        mult_max = top_limit // multiple
        return multiple * (mult_max * (mult_max + 1)) / 2

    print(sum_series(3, 999)
            + sum_series(5, 999)
            - sum_series(15, 999))

The `sum_series` function works out how many multiples of a given number there are between 0 and `top_limit` and adds them up.

But you can avoid iterating over them because of the interesting fact that the sum of all [natural numbers][natn] through *x* is *x × (x + 1) ÷ 2*. It took me a while of head-scratching before I [read an explanation][gauss] (two, actually) that made sense.

[natn]: http://en.wikipedia.org/wiki/Natural_numbers
[gauss]: http://mathandmultimedia.com/2010/09/15/sum-first-n-positive-integers/

The function does that for the *number* of multiples, and then multiplies the result by the number in question to actually *make* them multiples. For example, 1 + 2 + 3 through 333 become 3 + 6 + 9 through 999.

Repeat with 5, then subtract the results for 15 (to remove the double-counted multiples of both 3 and 5) and you’re done.
