---
title: 3.75 years on the Tube
author: Rob Wells
date: 2018-05-03 01:00
output:
    md_document:
        variant: markdown_strict+fenced_code_blocks
        preserve_yaml: true
        fig_width: 7.5
        fig_height: 5
        dev: svg
    html_document:
        dpi: 200
        fig_width: 7.5
        fig_height: 5
        dev: svg
---

A couple of years ago, shortly after I moved house, I wrote [a post
analysing my Tube travel](/2016/09/two-years-on-the-tube/). It was my
first real attempt to do that kind of analysis, and the first time I’d
done anything with [Matplotlib](https://matplotlib.org) of any level of
complexity.

I thought I’d have another crack at it now, looking at the changes in my
travel patterns since the move, and also changing from Python and
Matplotlib to R and ggplot2.

Why now? There’s no great immediate reason, though for a time I was
thinking about stopping to use my Oyster card in favour of a contactless
bank card. You don’t have the option to be emailed CSV journey history
files with a bank card, and the main advantage of weekly capping
wouldn’t affect me, so I’ll be sticking with the Oyster card for the
moment.

But, as I noted in the introduction to the previous post, my travel
habits have changed considerably. Before I would commute by train twice
a day, whereas now I’m within a short cycle of work. I’m expecting this
to have a significant effect in what we observe below.

And why the switch in environment? Python is still the language that
fits my brain the best, but Matplotlib feels like hard work. R is a
pretty odd language in many ways, but the ggplot2 way of building plots
makes a great deal of sense to me, and has allowed me to play with plots
quickly in ways that I feel that wouldn’t be available if I was trying
to contort to fit Matplotlib’s preferences. I freely admit that I don’t
have a great deal of experience with Matplotlib, so it’s entirely
possible that’s the reason why I find it a struggle, but that barrier
just isn’t there with ggplot2.

I’m writing this post in
[RStudio](https://www.rstudio.com/products/RStudio/) in a [R
Markdown](https://rmarkdown.rstudio.com) document, but it’s actually my
second go at this. The first was invaluable in getting myself acquainted
with the process and playing around with ideas, but it kind of spiralled
out of control so it’s not presentable. Hopefully this is something
approaching readable.

### Setup

To start with we’re going to load some libraries to make our life
easier. The [Tidyverse](https://www.tidyverse.org) wraps up several
helpful packages; lubridate has some handy date-handling functions;
stringr is helpful for, er, strings; patchwork allows you to easily
combine plots into one figure; ggalt provides an extra geom
(`geom_encircle()`) that we’ll use in a bit. Forgive me for not making
clear where functions come from below as, like Swift, R imports into the
global namespace.

Not shown is my customised ggplot2 theme, which you can find if you
[look at the original .Rmd source
file](https://github.com/robjwells/primaryunit/tree/master/posts/2018/04).

    r:
    library(tidyverse)
    library(lubridate)
    library(stringr)
    library(patchwork)
    library(ggalt)
    
    # Moving average function from https://stackoverflow.com/a/4862334/1845155
    mav <- function(x, n = 5) {
        stats::filter(x, rep(1/n, n), sides = 1)
    }

<!-- Comment to separate R code and output -->

### Data import

I keep all the CSV files as received, just dating the filenames with the
date I got them. (Sorry, I won’t be sharing the data.) Let’s load all
the files:

    r:
    oyster_filenames <- dir(
        '~/Documents/Oyster card/Journey history CSVs/',
        pattern = '*.csv',
        full.names = TRUE)

<!-- Comment to separate R code and output -->

There are 109 CSV files that we need to open, load, and combine.

    r:
    oyster_data <- oyster_filenames %>%
        map(~ read_csv(., skip = 1)) %>%
        reduce(rbind)

<!-- Comment to separate R code and output -->

Here we’re piping `oyster_filenames` through `map`, where we use an R
formula to supply arguments to `read_csv` to skip the header line in
each file. Finally we `reduce` the 109 data frames by binding them by
row.

### Poking around the data

We can take a look at the data to get an idea of its structure:

    r:
    head(oyster_data)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 8
    ##   Date   `Start Time` `End Time` `Journey/Action`    Charge Credit Balance
    ##   <chr>  <time>       <time>     <chr>                <dbl> <chr>    <dbl>
    ## 1 31-Oc… 23:22        23:50      North Greenwich to…    1.5 <NA>     26.0 
    ## 2 31-Oc… 18:39        18:59      Woolwich Arsenal D…    1.6 <NA>     27.6 
    ## 3 31-Oc… 18:39           NA      Auto top-up, Woolw…   NA   20       29.2 
    ## 4 31-Oc… 17:10        17:37      Stratford to Woolw…    1.6 <NA>      9.15
    ## 5 31-Oc… 16:26        16:53      Woolwich Arsenal D…    1.6 <NA>     10.8 
    ## 6 30-Oc… 22:03        22:39      Pudding Mill Lane …    1.5 <NA>     12.4 
    ## # ... with 1 more variable: Note <chr>

It’s clearly in need of a clean-up. The journey history file appears to
be a record of every action involving the card. It’s interesting to note
that the Oyster card isn’t just a “key” to pass through the ticket
barriers, but a core part of how the account is managed (note that
having an online account is entirely optional).

Actions taken “outside” of the card need to be “picked up” by the card
by tapping on an Oyster card reader. Here we can see a balance increase
being collected, mixed in with the journey details. (Funnily enough, TfL
accidentally cancelled my automatic top-up a couple of months ago, but
that was never applied to my account as I didn’t use the card before the
action expired.)

But we’re only interested in rail journeys, one station to another, with
a start and finish time.

Let’s see if the notes field can give us any guidance of what we may
need to exclude.

    r:
    oyster_data %>%
        filter(!is.na(Note)) %>%
        count(Note, sort = TRUE)

<!-- Comment to separate R code and output -->

    ## # A tibble: 5 x 2
    ##   Note                                                                   n
    ##   <chr>                                                              <int>
    ## 1 The fare for this journey was capped as you reached the daily cha…    18
    ## 2 We are not able to show where you touched out during this journey      6
    ## 3 This incomplete journey has been updated to show the <station> yo…     1
    ## 4 We are not able to show where you touched in during this journey       1
    ## 5 You have not been charged for this journey as it is viewed as a c…     1

OK, not much here, but there are some troublesome rail journeys missing
either a starting or finishing station. The "incomplete journey" line
also hints at something to be aware of:

    r:
    oyster_data %>%
        filter(str_detect(Note, 'This incomplete journey')) %>%
        select(`Journey/Action`) %>%
        first()

<!-- Comment to separate R code and output -->

    ## [1] "Woolwich Arsenal DLR to <Blackheath [National Rail]>"

Note the angle brackets surrounding the substituted station. We’ll come
back this later.

A missing start or finish time is a giveaway for oddities, which
overlaps somewhat but not completely with Journey/Action fields that
don’t match the pattern of `{station} to {station}`. Let’s fish those
out and have a look at the abbreviated descriptions:

    r:
    stations_regex <- '^<?([^>]+)>? to <?([^>]+)>?$'
    
    oyster_data %>%
        filter(
            is.na(`Start Time`) |
            is.na(`End Time`) |
            !str_detect(`Journey/Action`, stations_regex)) %>%
        mutate(abbr = str_extract(`Journey/Action`, '^[^,]+')) %>%
        count(abbr, sort = TRUE)

<!-- Comment to separate R code and output -->

    ## # A tibble: 11 x 2
    ##    abbr                                              n
    ##    <chr>                                         <int>
    ##  1 Auto top-up                                      84
    ##  2 Bus journey                                      26
    ##  3 Automated Refund                                  7
    ##  4 Woolwich Arsenal DLR to [No touch-out]            3
    ##  5 Oyster helpline refund                            2
    ##  6 Unknown transaction                               2
    ##  7 [No touch-in] to Woolwich Arsenal DLR             1
    ##  8 Entered and exited Woolwich Arsenal DLR           1
    ##  9 Monument to [No touch-out]                        1
    ## 10 Stratford International DLR to [No touch-out]     1
    ## 11 Stratford to [No touch-out]                       1

### Tidying the data

All these should be filtered out of the data for analysis. (The two
unknown transactions appear to be two halves of my old commute.
Strange.)

    r:
    rail_journeys <- oyster_data %>%
        # Note the !() below to invert the earlier filter
        filter(!(
            is.na(`Start Time`) |
            is.na(`End Time`) |
            !str_detect(`Journey/Action`, stations_regex)))

<!-- Comment to separate R code and output -->

That leaves us with 993 rail journeys to have a look at.

But there’s more tidying-up to do:

-   Journey dates and times are stored separately. Finish times may be
    after midnight (and so on the day after the date they’re
    associated with).
-   Start and finish stations need to be separated. (And don’t forget
    that set of angle brackets.)
-   All money-related fields should be dropped except for “charge” (the
    journey fare).

Let’s have a crack at it, proceeding in that order:

    r:
    tidy_journeys <- rail_journeys %>%
        mutate(
            start = dmy_hms(
                str_c(Date, `Start Time`, sep=' '),
                tz = 'Europe/London'),
            end = dmy_hms(
                str_c(Date, `End Time`, sep=' '),
                tz = 'Europe/London') +
                # Add an extra day if the journey ends “earlier” than the start
                days(1 * (`End Time` < `Start Time`)),
            # Let’s add a duration to make our lives easier
            duration = end - start,
    
            enter = str_match(`Journey/Action`, stations_regex)[,2],
            exit = str_match(`Journey/Action`, stations_regex)[,3]
        ) %>%
        select(
            start, end, duration,
            enter, exit,
            fare = Charge
        ) %>%
        # Sorting solely to correct the slightly odd example output
        arrange(start)
    head(tidy_journeys)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 6
    ##   start               end                 duration enter    exit      fare
    ##   <dttm>              <dttm>              <time>   <chr>    <chr>    <dbl>
    ## 1 2014-09-06 13:14:00 2014-09-06 13:42:00 28       Woolwic… Stratfo…   1.5
    ## 2 2014-09-06 13:59:00 2014-09-06 14:08:00 9        Stratfo… Hackney…   1.5
    ## 3 2014-09-06 20:47:00 2014-09-06 21:02:00 15       Hackney… Highbur…   1.5
    ## 4 2014-09-06 23:22:00 2014-09-07 00:10:00 48       Highbur… Woolwic…   2.7
    ## 5 2014-09-07 10:00:00 2014-09-07 10:30:00 30       Woolwic… Pudding…   1.5
    ## 6 2014-09-07 20:43:00 2014-09-07 21:15:00 32       Pudding… Woolwic…   1.5

Great. The duration variable isn’t strictly necessary but it’ll make
things a tad clearer later on.

### Weekly totals

For a start, let’s try to remake the first plot from [my previous
post](/2016/09/two-years-on-the-tube/), a plot of weekly spending with a
moving average. Looking back at that plot, it’s not tremendously
helpful, but it’s a starting point. (In addition, while that plot is
labelled as showing a six-week average, the code computes [an eight-week
average](https://github.com/robjwells/primaryunit/blob/master/posts/2016/09/analyse_journey_history.py#L168),
and a quick count of the points on the plot confirms it.)

First, though, a problem with the data: they record journeys made, not
the absence of any journeys (obviously). If we’re to accurately plot
weekly spending, we need to include weeks where no journeys were made
and no money spent.

First, let’s make a data frame containing every [ISO
week](https://en.wikipedia.org/wiki/ISO_week_date) from the earliest
journey in our data to the most recent.

    r:
    blank_weeks <- seq(min(tidy_journeys$start),
        max(tidy_journeys$end),
        by = '1 week') %>%
        tibble(
            start = .,
            week = format(., '%G-W%V')
        )
    head(blank_weeks)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 2
    ##   start               week    
    ##   <dttm>              <chr>   
    ## 1 2014-09-06 13:14:00 2014-W36
    ## 2 2014-09-13 13:14:00 2014-W37
    ## 3 2014-09-20 13:14:00 2014-W38
    ## 4 2014-09-27 13:14:00 2014-W39
    ## 5 2014-10-04 13:14:00 2014-W40
    ## 6 2014-10-11 13:14:00 2014-W41

The format string uses the ISO week year (%G) and the ISO week number
(%V), which made differ from what you might intuitively expect. I’ve
included a somewhat arbitrary start time to make plotting a little
easier later.

Now we need to summarise our actual journey data, collecting the total
fare for each ISO week. We’ll use `group_by()` and `summarise()` — two
tools that took me a few tries to get a handle on. Here `summarise()`
works group-wise based on the result of `group_by()`, you don’t have to
pass the group into the `summarise()` call, just the value you want
summarised and how.

    r:
    real_week_totals <- tidy_journeys %>%
        group_by(week = format(start, '%G-W%V')) %>%
        summarise(total = sum(fare))

<!-- Comment to separate R code and output -->

That done, we can use an SQL-like join operation to take every week in
our giant list and match it against the week summaries from our real
data. The join leaves missing values (`NA`) in the total column for
weeks where no journeys were made (and so weren’t present in the data to
summarise) so we replace them with zero.

    r:
    complete_week_totals <- left_join(blank_weeks,
                                      real_week_totals,
                                      by = 'week') %>%
        replace_na(list(total = 0))
    tail(complete_week_totals)

<!-- Comment to separate R code and output -->

    ## # A tibble: 6 x 3
    ##   start               week     total
    ##   <dttm>              <chr>    <dbl>
    ## 1 2018-03-17 12:14:00 2018-W11   0  
    ## 2 2018-03-24 12:14:00 2018-W12   0  
    ## 3 2018-03-31 13:14:00 2018-W13  21.1
    ## 4 2018-04-07 13:14:00 2018-W14   9.5
    ## 5 2018-04-14 13:14:00 2018-W15   0  
    ## 6 2018-04-21 13:14:00 2018-W16   7.8

With this summary frame assembled, we can now plot the totals. I’m also
going to mark roughly when I moved house so we can try to see if there’s
any particular shift.

    r:
    house_move <- as.POSIXct('2016-08-01')
    pound_scale <- scales::dollar_format(prefix = '£')
    
    weeks_for_avg <- 8
    
    ggplot(data = complete_week_totals,
           mapping = aes(x = start, y = total)) +
        geom_vline(xintercept = house_move,
                   colour = rjw_grey,
                   alpha = 0.75) +
        geom_point(
            colour = rjw_blue,
            size = 0.75) +
        geom_line(
            mapping = aes(y = mav(complete_week_totals$total,
                                  weeks_for_avg)),
            colour = rjw_red) +
    
        labs(
            title = str_glue(
                'Weekly transport spending and {weeks_for_avg}',
                '-week moving average'),
            subtitle = (
                'September 2014 to May 2018, vertical bar marks house move'),
            x = NULL, y = NULL) +
    
        scale_x_datetime(
            date_breaks = '6 months',
            date_labels = '%b ’%y') +
        scale_y_continuous(
            labels = pound_scale)

<!-- Comment to separate R code and output -->

<p class="full-width">
    <img
        src="/images/2018-05-03-weekly-spending-1.svg"
        alt="A plot showing my weekly Oyster card spending, September 2014 to May 2018"
        class="no-border"
        width=720
        />
</p>

It’s pretty clear that there is a marked difference before and after the
house move. But I’m not sure this plot is the best way to show it. (Nor
the best way to show anything.)

That said, the code for this plot is a pretty great example of what I
like about ggplot2: you create a plot, add geoms to it, customise the
labels and scales, piece by piece until you’re happy. It’s fairly
straightforward to discover things (especially with RStudio’s
completion), and you change things by adding on top of the basics
instead of hunting around in the properties of figures or axes or
whatever.

### Cumulative spending

The first plot showed a change in my average weekly spending. What does
that look like when we plot the cumulative spending over this period?

    r:
    ggplot(data = tidy_journeys,
           mapping = aes(x = start,
                         y = cumsum(fare),
                         colour = start > house_move)) +
        geom_line(
            size = 1) +
    
        labs(
            title = 'Cumulative Oyster card spending',
            subtitle = 'September 2014 to May 2018',
            x = NULL, y = NULL,
            colour = 'House move') +
        scale_y_continuous(
            labels = pound_scale,
            breaks = c(0, 500, 1000, 1400, 1650)) +
        scale_color_brewer(
            labels = c('Before', 'After'),
            palette = 'Set2') +
        theme(
            legend.position = 'bottom')

<!-- Comment to separate R code and output -->

<p class="full-width">
    <img
        src="/images/2018-05-03-cumulative-spending-1.svg"
        alt="A plot showing my cumulative Oyster card spending, September 2014 to May 2018"
        class="no-border"
        width=720
        />
</p>

The difference in slope is quite clear; at one point I fitted a linear
smoother to the two periods but it overlapped so tightly with the data
that it was difficult to read either. I’ve also monkeyed around with the
y-axis breaks to highlight the difference; what before took three to six
months to spend has taken about 21 months since the house move.

### Zero-spending weeks

One thing that shows up in the first plot, and likely underlies the drop
in average spending, is the number of weeks where I don’t travel using
my Oyster card at all. Let’s pull together a one-dimensional plot
showing just that.

    r:
    ggplot(complete_week_totals,
           aes(x = start,
               y = 1,
               fill = total == 0)) +
        geom_col(
            width = 60 * 60 * 24 * 7) +  # Datetime width handled as seconds
        geom_vline(
            xintercept = as.POSIXct(house_move),
            colour = rjw_red) +
    
        scale_fill_manual(
            values = c(str_c(rjw_grey, '20'), rjw_grey),
            labels = c('Some', 'None')) +
        scale_x_datetime(
            limits = c(min(complete_week_totals$start),
                       max(complete_week_totals$start)),
            expand = c(0, 0)) +
        scale_y_continuous(
            breaks = c()) +
        labs(
            title = 'Weeks with zero Oyster card spending',
            subtitle = 'September 2014 to May 2018, red line marks house move',
            x = NULL, y = NULL,
            fill = 'Spending') +
        theme(
            legend.position = 'bottom')

<!-- Comment to separate R code and output -->

<p class="full-width">
    <img
        src="/images/2018-05-03-zero-spending-weeks-1.svg"
        alt="A plot showing weeks where I made no journeys using my Oyster card"
        class="no-border"
        width=720
        />
</p>

The change here after I moved house is stark, nearly an inversion of the
previous pattern of zero/no-zero spending weeks. (Almost looks like [a
barcode](https://www.robjwells.com/2018/02/british-newspaper-barcodes-explained-and-automated/)!)

My apologies for the thin lines between columns, which is an SVG
artefact. The inspiration for this was a plot of games/non-games in the
App Store top charts that [Dr Drang](http://leancrew.com/all-this/)
included at the bottom of one of his posts and, for the life of me, I
can’t find now.

### Changes in journey properties

So it’s clear that I travel less on the Tube network, and that I spend
less. But what has happened to the sort of journeys that I make? Are
they longer? Shorter? Less expensive? More?

Let’s have a look at how the average fare and average journey length
change over time.

    r:
    n_journey_avg <- 10
    
    common_vline <- geom_vline(
        xintercept = house_move,
        colour = rjw_red)
    common_point <- geom_point(size = .5)
    
    fares_over_time <- ggplot(tidy_journeys,
                              aes(x = start,
                                  y = mav(fare, n_journey_avg))) +
        scale_x_datetime(
            labels = NULL) +
        scale_y_continuous(
            labels = pound_scale) +
        labs(
            y = 'Fare',
            title = 'More expensive, shorter journeys',
            subtitle = str_glue('{n_journey_avg}-journey average, ',
                                'vertical line marks house move'))
    
    duration_over_time <- ggplot(tidy_journeys,
                                 aes(x = start,
                                     y = mav(duration, n_journey_avg))) +
        scale_y_continuous() +
        labs(
            y = 'Duration (mins)')
    
    (fares_over_time / duration_over_time) &  # Patchwork is magic
        common_vline &
        common_point &
        labs(x = NULL)

<!-- Comment to separate R code and output -->

<p class="full-width">
    <img
        src="/images/2018-05-03-fare-duration-averages-1.svg"
        alt="A plot of average fares and journey durations over time"
        class="no-border"
        width=720
        />
</p>

There’s a tendency for journeys to become shorter and more expensive
after the house move. How distinct in this regard are pre- and post-move
journeys? What is driving the averages? I have a hunch so let me rush on
ahead with this plot.

    r:
    commute_stations <- c('Woolwich Arsenal DLR', 'Stratford International DLR',
                          'Stratford', 'Pudding Mill Lane')
    
    commute_journeys <- tidy_journeys %>%
        filter(
            enter %in% commute_stations,
            exit %in% commute_stations)
    
    high_speed_journeys <- tidy_journeys %>%
        filter(
            str_detect(enter, 'HS1'),
            str_detect(exit, 'HS1'))
    
    ggplot(tidy_journeys,
           aes(x = fare,
               y = duration,
               colour = start > house_move)) +
        geom_jitter(
            width = 0.05,  # 5p
            height = 0.5,  # 30 seconds
            alpha = 0.5) +
        geom_encircle(
            data = commute_journeys,
            size = 1.5) +
        geom_encircle(
            data = high_speed_journeys,
            size = 1.5) +
    
        scale_color_brewer(
            palette = 'Set2',
            labels = c('Before', 'After')) +
        scale_x_continuous(
            labels = pound_scale) +
        scale_y_continuous(
            limits = c(0, 80)) +
        labs(
            title = 'Pre- and post-move averages driven by two groups',
            subtitle = str_c('Old commute and high-speed journeys circled,',
                             ' positions not exact'),
            x = 'Fare',
            y = 'Duration (mins)',
            colour = 'House move'
        )

<!-- Comment to separate R code and output -->

<p class="full-width">
    <img
        src="/images/2018-05-03-fare-against-duration_scatter.svg"
        alt="A plot of journey fare against distance, grouped by whether the journeys were before or after I moved house"
        class="no-border"
        width=720
        />
</p>

We can see in the lower central section that there’s some overlap.
Remember also that there are far fewer post-move journeys, so it’s not
surprising that earlier ones dominate this plot. (I added jitter to the
points to make things a little easier to see — `geom_jitter()` is a
wrapper around `geom_point()`.)

But what is crucial to understanding the averages are the two rough
groups circled: journeys between stations that I used for my old commute
(on the left in green), and journeys involving travel on the [High Speed
1](https://en.wikipedia.org/wiki/High_Speed_1) (HS1) rail line (on the
right in orange).

My old commute was low-cost, each way either £1.50 or £1 (with an
off-peak railcard discount, applied for part of the pre-move period).
There are a lot of these journeys (nearly 500). It was a fairly
predictable 30ish-minute journey.

On the other hand, trips involving the HS1 line are expensive and very
short. A single off-peak fare is currently £3.90 and peak £5.60, while
the journey time between Stratford International and St Pancras is just
seven minutes, with a bit of waiting inside the gateline.

### Last thoughts

If you made it this far, well done, and thanks for reading. There’s a
lot of R code in this post, probably too much. But there are two reasons
for that: as a reference for myself, and to show that there’s not any
magic going on behind the curtain, and very little hard work. (In my
code at least, there’s plenty of both in the libraries!)

Working in R with ggplot2 and the other packages really is a pleasure;
it doesn’t take very long to grasp how the different tools fit together
into nice, composable pieces, and to assemble them in ways that produce
something that matches what you have pictured in your mind.

