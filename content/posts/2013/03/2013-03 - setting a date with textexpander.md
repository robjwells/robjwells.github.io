---
title: "Setting a date with TextExpander"
date: 2013-03-06T10:45:00
tags: ["AppleScript", "TextExpander"]
---

I suck at dates. Badly.

Thankfully, there are a few ways to get around this in software — not least [TextExpander][], Smile’s ace text-substitution program. (I don’t use it nearly enough, but [I’m looking to fix that][tc].)

[TextExpander]: http://smilesoftware.com/TextExpander/index.html
[tc]: http://www.takecontrolbooks.com/textexpander

TextExpander has a lot of date placeholders, so it’s obvious that I’m not the only one that needs help with this — but I may well be the first to be *this* bad. Here’s a list of the snippets in my Time & Date folder:

    ;mdate   ->   March 6 2013
    ;*ddate  ->   Wednesday March 6 2013
    ;ds      ->   _0306_0914
    ;time    ->   09:14
    ;bd      ->   20130306
    ;ldate   ->   March 6, 2013
    ;sdate   ->   06/03/2013
    ;dt      ->   09:14, March 6, 2013

Those eight snippets include *seven* different ways to get the date, and *three* different ways to get the time. The worst part about this is that I can never remember which abbreviation corresponds to which date format.

Ok, let’s fix this. How many formats do I really need? I need a short date, a more human-friendly long date, the time, and the format used at [work][ms].

So that’s four — only half as bad as before!

[ms]: http://www.morningstaronline.co.uk

### Time

I’m sticking with my old `;time` snippet here, a colon-separated 24-hour time. If I need a more human-friendly time, typing 10am or 8pm or whatever is as easy as typing an abbreviation (and TextExpander only does uppercase AM/PM, which I dislike). Here’s the snippet:

    %H:%M   ->    10:23

### Short date

Because, well, [XKCD][], I’m going to use the [ISO 8601 date format][iso] for this. It means I can dump my separate backwards date snippet and avoids any confusion across DD/MM/YY and MM/DD/YY countries.

    %Y-%m-%d    ->  2013-03-06

[XKCD]: http://xkcd.com/1179/
[iso]: http://en.wikipedia.org/wiki/ISO_8601

### Long date

Since this is implicitly not the format to use when you’re counting characters and one that’s explicit enough to avoid confusion, there’s quite a bit of personal freedom here.

This one’s going to be more complicated than the previous two, as I want to use date suffixes (March 2nd, April 21st, etc). But TextExpander doesn't include a suffix placeholder, so let’s take advantage of its script support.

AppleScript’s built-in `current date` command returns an object from which we can extract all the pieces we need to construct a date, like so:

```applescript
set theDate to the day of the (current date)
set theDay to the weekday of the (current date)
set theMonth to the month of the (current date)
set theYear to the year of the (current date)
```

Now to build the suffix. Most dates have the suffix “th”, so we want to focus on the special cases: 1, 2, 3, 21, 22, and 31. We could check for each of these but there’s a smarter way.

We need to pull the date’s **last** character, which determines the suffix, so we can work with both single and double-digit dates:

```applescript
set lastChar to (the last character of (theDate as string)) as number
```

Now we check for the most common situation (“th”) by testing `lastChar` against a range:

```applescript
if lastChar is 0 or lastChar > 3 or (theDate > 10 and¬
 theDate < 21) then
    set theDate to (theDate as string) & "th"
```

If we put the other suffixes in order and in a list, we can use the last character of the date itself to extract the correct suffix:

```applescript
set theSuffixes to {"st", "nd", "rd"}
set theDate to (theDate as string) & (item lastChar of theSuffixes)
```

Now let’s roll it up and `return` a constructed date:

```applescript
set theDate to the day of the (current date)
set theDay to the weekday of the (current date)
set theMonth to the month of the (current date)
set theYear to the year of the (current date)

set lastChar to (the last character of (theDate as string))¬
 as number

if lastChar > 3 or lastChar is 0 or (theDate > 10 and¬
 theDate < 21) then
    set theDate to (theDate as string) & "th"
else
    set theSuffixes to {"st", "nd", "rd"}
    set theDate to (theDate as string) & (item lastChar¬
     of theSuffixes)
end if

return (theDay & ", " & theMonth & " " & theDate & ", " &¬
 theYear) as string
```

### End result

Hey! You made it! I was sure I’d lose everyone in the middle of breaking down that AppleScript.

So, here’s what I’m left with:

    ;iso    ->    2013-03-06
    ;ldt    ->    Wednesday, March 6th, 2013
    ;tm     ->    10:21

Mix in one for work:

    ;*dt    ->    Wednesday March 6 2013

And we’re all set.
