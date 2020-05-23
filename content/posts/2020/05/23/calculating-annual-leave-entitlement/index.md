---
title: "Calculating annual leave entitlement"
date: 2020-05-23T14:21:02+01:00
publishDate: 2020-05-24T06:00:00+01:00
draft: true
---

In my current job, and for much of my last job, I induct new employees and make some of the arrangements for leaving employees.
Part of that is working out how much annual leave they’re entitled to.
Unfortunately people tend not to start exactly at the beginning of the leave year and leave exactly at the end of the leave year.

Many years ago I wrote a simple Python script to do this for me — it asks for the start and end dates, and prints out how much annual leave the person would accrue over that period.

You can [run the calculator in your browser at Repl.it][calc].
(It has an odd name in the URL because originally the script only handled new starts, not leavers, and I don’t want to break the URL for my old colleagues who use it.)

[calc]: https://annualleavecalculator-end-date.robjwells.repl.run/

I’ve cleaned it up today after seeing that [Repl.it can publish new repos to GitHub][gh-announce] (though that feature has some [rough edges][gh-bug]).

[gh-announce]: https://repl.it/talk/announcements/Feedback-for-git-support-the-new-GitHub-integration/21631
[gh-bug]: https://repl.it/talk/announcements/1-to-this-feature-thanks-but-I-came/21631/175353

You can [find the code on GitHub][repo].
Mostly it’s uninteresting, the first 40 lines being the module docstring and the last 30 being mostly wrappers around `input()`, so here’s the meat of it:

[repo]: https://github.com/robjwells/annual_leave_calculator/blob/master/main.py

```python {linenos=true}
# Modify these constants to suit your circumstances
DEFAULT_AL_YEAR_START = date.today().replace(month=1, day=1)
DEFAULT_AL = 28
RESULT_DECIMAL_PLACES = 2


def main() -> None:
    al_for_full_year = prompt_for_al_amount()

    al_year_start = prompt_for_date(
        "Leave year start",
        default=DEFAULT_AL_YEAR_START
    )
    al_year_end = al_year_start.replace(
        year=al_year_start.year + 1
    ) - timedelta(days=1)

    start_date = prompt_for_date("Employee start", default=al_year_start)
    end_date = prompt_for_date("Employee finish", default=al_year_end)

    al_year_days = (al_year_end - al_year_start).days + 1
    employed_days = (end_date - start_date).days + 1
    # +1 as we assume, eg, starting and leaving on Jan 1 accrues
    # 1 day's worth of leave, not zero

    proportion_of_al_year_worked = employed_days / al_year_days
    al_days_available = al_for_full_year * proportion_of_al_year_worked
    print(
        round(al_days_available, RESULT_DECIMAL_PLACES),
        "days annual leave"
    )
```

One thing to state up front is that this only considers leave accrual within a single annual leave year.
Crossing a leave-year boundary isn’t as simple as adding additional leave, as it’ll typically involve some limit on how much leave can be carried across (which may be zero).

There’s also little error-handling, so if you enter something that parses but is nonsensical (negative amount of leave, an end date earlier than the start date) then the result will be nonsensical.

Until I refactored the script today, I’d made assumptions about the leave year that meant you’d have to edit the script more than a little to use leave years that don’t match the calendar years.
I changed that today by prompting the user for the start of the leave year (defaulting the January 1) and calculating the leave year end with some basic date manipulation in lines 14-16.
(This was to fix a regression I introduced, not the result of any great foresight!)

This manipulation isn’t completely robust, but if you say your leave year starts on February 29 then that’s your responsibility.

Lines 21 & 22 are noteworthy for the `+ 1`, so that you get an inclusive range of days, with the assumption being that the person works on the “start day” and also on the “finish day”.
There’s some redundancy between lines 16 and 21, calculating the leave year by subtracting a day and adding it back later, but that’s to fit my mental model that the leave year runs eg from January 1 to December 31.

The rest of the script just works out the proportion of the leave year worked against the length of the full leave year, and computes the same proportion of the total number of leave days available for the full year.

Nothing really tricky, but I work in a small company so it’s easy to misremember the process when you only do it a couple of times a year.

Here’s an example session:

```
How many days annual leave for the full year? [28] 30
Leave year start date [2020-01-01]: 2020-04-01
Employee start date [2020-04-01]:
Employee finish date [2021-03-31]: 2020-06-05
5.42 days annual leave
```

It’s a bit awkward to put in a “start date” for employees who have been employed since before the start of the leave year, and similar for employees who (you hope!) will continue past the end of the leave year, but the prompting helpers take a default value which you can accept by pressing return.
