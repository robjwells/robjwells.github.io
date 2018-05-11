---
Title: Table manipulation with R
Date: 2018-05-08 23:15
---

One of my responsibilities at work is to provide a list of people who our printers should call if there’s ever a problem with the edition. Usually that’s the chief sub, or whoever is covering her.

I also prepare the rota for the journalistic staff, which I use as the source of information for the responsibility list.

This job has largely escaped automation. I do have a Python script that prints a nice template report for the week ahead, complete with BBEdit placeholders, but working out whose name should be attached to each edition is just done by reading the rota across and deleting names from the template list until you’re down to one.

However, I’ve found things of this nature, if not automated, are put off, forgotten, or done wrong. This, because it’s not actually vital to anything, is no exception, particularly when I’m pulled into jobs that actually are vital.

The report looks a little like this, so you get the idea:

    Tue May 08    16pp    Alice Jones
    Wed May 09    16pp    Bob Smith
    Thu May 10    16pp    Rob Wells

And so on, with the pagination in the middle column.

The pagination is consistent (16 in the week, 24 on the weekend) with occasional larger editions. It can either be predicted with total certainty or none at all, as the large editions vary considerably with advertising and feature articles.

The responsibility can’t be predicted because we don’t work fixed patterns (we don’t have enough staff to do so). However, it can be done in advance once the newsroom rota is completed.

So let’s forget the pagination and just focus on pulling together a list of every production day in the completed period and who is the chief sub.

Our newsroom rota is just a spreadsheet, which is actually the best tool I’ve found so far for handling a couple dozen people with intricate job-cover links between them. (The rota used to be laid out in InDesign, which, no matter what you think about spreadsheets or InDesign, was much more difficult.)

It looks a bit like this (the real spreadsheet has proper formatting and so on):

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th></th>
                <th>Sun 6/5</th>
                <th>Mon 7/5</th>
                <th>Tue 8/5</th>
                <th>Wed 9/5</th>
                <th>Thu 10/5</th>
                <th>Fri 11/5</th>
                <th>Sat 12/5</th>
                <th>Lieu add</th>
                <th>Lieu tot</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Rob Wells</td>
                <td>Off</td>
                <td></td>
                <td></td>
                <td>Sport</td>
                <td>Ch Sub</td>
                <td>Sport</td>
                <td></td>
                <td></td>
                <td>10</td>
            </tr>
            <tr>
                <td>Alice Jones</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>Off</td>
                <td></td>
                <td></td>
                <td>0.25</td>
                <td>4.5</td>
            </tr>
        </tbody>
    </table>
</div>

There’s a fair amount of information: names, dates, days off, cover responsibilities, new and accrued [TOIL][]. It’s entirely designed for humans, not computers (and it takes the humans a little while until they’re able to read it).

[TOIL]: https://www.gov.uk/overtime-your-rights/time-off-and-paid-leave

A lot is implicit. If we assume in this example that Alice is the chief sub, she is performing that role on her usual working days (the empty cells). It is only marked for people who have to cover someone else’s job.

This table is not something that you can just chuck into a computer program; it needs cleaning up first.

Thankfully, R (and the [Tidyverse][] particularly) is a great environment in which to wrangle your data, and to do so fairly quickly. All the code below was pulled together in about 30 minutes total (with a good 10 minutes of reading documentation and fixing errors in the original source data). Writing this post has taken much longer.

[Tidyverse]: https://www.tidyverse.org

In our example below we’re going to have four workers who each cover the chief sub at different times. Here we’re going make “Dan Taylor” the chief sub. Congratulations, Dan!

First we’ll pull in our libraries.

    r:
    library(tidyverse)
    library(lubridate)
    library(stringr)

Then we’ll read in the data, which is saved in a TSV file after copying and pasting from the spreadsheet into a text document. We’ll select only the production days and the unnamed first column (named X1 on import), excluding Saturdays and the TOIL columns.

    r:
    wide <- read_tsv('chsub.tsv') %>%
        select(matches('^(Mon|Tue|Wed|Thu|Fri|Sun) |X1')) %>%
        rename(name = X1)

Then we’ll use a [tidyr][] function, [`gather()`][gather], to transform our wide format into a tall one by selecting the date columns. It’s easier to get a feel for `gather()` by looking at the output.

[tidyr]: http://tidyr.tidyverse.org
[gather]: http://tidyr.tidyverse.org/reference/gather.html

    r:
    tidy <- wide %>%
        gather(matches('^(Mon|Tue|Wed|Thu|Fri|Sun) '),
               key = date,
               value = status)
    head(tidy)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 3
    ##   name           date     status
    ##   <chr>          <chr>    <chr>
    ## 1 Alice Jones    Sun 29/4 Off
    ## 2 Bob Smith      Sun 29/4 Sick
    ## 3 Carol Williams Sun 29/4 Booked
    ## 4 Dan Taylor     Sun 29/4 <NA>
    ## 5 Alice Jones    Mon 30/4 <NA>
    ## 6 Bob Smith      Mon 30/4 Off

We now have a row for each person for each day, along with their “status” for the day.

But Dan doesn’t have his chief sub days marked, as it would be nearly every day. Let’s split out Dan’s rows and replace the empty cells with `Ch Sub`, the same status string used by everyone else. Then we’ll combine the filled-out Dan rows with all the non-Dan rows from the original data frame.

    r:
    dan_replaced <- tidy %>%
        filter(name == 'Dan Taylor') %>%
        replace_na(list(status = 'Ch Sub'))

    all <- tidy %>%
        filter(name != 'Dan Taylor') %>%
        rbind(dan_replaced)

    tail(all)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 3
    ##   name       date      status
    ##   <chr>      <chr>     <chr>
    ## 1 Dan Taylor Sun 30/12 Ch Sub
    ## 2 Dan Taylor Mon 31/12 Ch Sub
    ## 3 Dan Taylor Tue 1/1   Ch Sub
    ## 4 Dan Taylor Wed 2/1   Ch Sub
    ## 5 Dan Taylor Thu 3/1   Ch Sub
    ## 6 Dan Taylor Fri 4/1   Ch Sub

Great. But poor Dan, he’s working every day over New Year 2018-2019. In reality, I haven’t done that far on the rota, just up to October. We’ll convert all those dates now, and filter out all the newly missing entries where the month was outside our range.

    r:
    dated <- all %>%
        mutate(
            date = dmy(str_c(str_extract(date, '\\d+/[4-9]'), '/2018'))
        ) %>%
        filter(!is.na(date))

Let’s get only the chief sub-related rows and sort them by date.

    r:
    chsub <- dated %>%
        filter(str_detect(status, 'Ch Sub')) %>%
        arrange(date) %>%
        select(date, chief_sub = name)
    head(chsub)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 2
    ##   date       chief_sub
    ##   <date>     <chr>
    ## 1 2018-04-29 Dan Taylor
    ## 2 2018-04-30 Dan Taylor
    ## 3 2018-05-01 Dan Taylor
    ## 4 2018-05-02 Bob Smith
    ## 5 2018-05-03 Dan Taylor
    ## 6 2018-05-04 Carol Williams

Exactly what we want. Now time for a bit of formatting to make this giant list somewhat acceptable for other people. This is also where my knowledge of R runs out.

    r:
    formatted <- str_c(
        format(chsub$date, '%a %Y-%m-%d'),
               chsub$chief_sub,
               sep = '  ')

    fd <- file('output.txt')
    writeLines(formatted, fd)
    close(fd)

So we’ll switch to Python, printing a blank line between each production week (of six days).

    python3:
    with open('output.txt') as f:
        for idx, line in enumerate(f.readlines()):
            if idx % 6 == 0:
                print()
            print(line, end='')

<!-- Comment to separate R code and output -->

    Sun 2018-08-19  Carol Williams
    Mon 2018-08-20  Carol Williams
    Tue 2018-08-21  Alice Jones
    Wed 2018-08-22  Carol Williams
    Thu 2018-08-23  Carol Williams
    Fri 2018-08-24  Carol Williams

    Sun 2018-08-26  Carol Williams
    Mon 2018-08-27  Carol Williams
    Tue 2018-08-28  Carol Williams
    Wed 2018-08-29  Dan Taylor
    Thu 2018-08-30  Dan Taylor
    Fri 2018-08-31  Dan Taylor

Perfect. And ready for whenever I get time to update the rota again.
