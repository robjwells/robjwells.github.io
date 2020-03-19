---
title: "Hop aboard the R train"
date: 2017-05-21T16:27:00
---

I quite enjoy turning out little plots for posts on here. Admittedly I’m not great at it, but I like to have a go.

However, [matplotlib][] really is not my favourite. It feels like there’s a lot of boilerplate to write and a lot of work to do before you get make something reasonably approaching what you had envisioned in your head.

[matplotlib]: https://matplotlib.org

So I thought I’d give [R][] a try, and learn some things about visualisation along the way with [Kieran Healey’s data visualisation course notes][vissoc], which was fun.

[R]: https://www.r-project.org
[vissoc]: http://vissoc.co

But mostly in this post I wanted to show how ludicrously straightforward using [ggplot2][] can be compared with what you have to do in matplotlib. Let’s pick on [my plot of train ticket prices][trains-post] from just before Christmas.

[ggplot2]: http://ggplot2.tidyverse.org
[trains-post]: https://www.robjwells.com/2016/12/trains-home-and-away/

The Python code for that is quite long so I’m not going to include it, but [it is available to view online][trains-github]. I’m not being completely fair because part of that involves getting the data into shape, and I’m sure there’s things I could’ve done to cut out a few lines.

[trains-github]: https://github.com/robjwells/primaryunit/blob/master/posts/2016/12/2016-12-23-trains/plot_trains.py

That said, it took me a while to figure out exactly how to go about doing the plot in matplotlib, exactly how to, say, parse the dates and label the axis.

There was some of that with R and ggplot2, but mostly me looking things up in the documentation as I’ve not used them much. But mostly it was pretty straightforward to figure out how to build up the plot.

Anyway, here’s the plot:

<p class="full-width">
    <a href="/images/2017-05-21-r-trains.svg">
        <img alt="A chart showing single train fares for selected journeys in England, France, Germany and the Netherlands on Friday December 23. This plot was made with R and ggplot2 instead of matplotlib."
             src="/images/2017-05-21-r-trains.svg"
             class="no-border"
             width=720>
    </a>
</p>

And here’s the code that produced it:

```r
library(ggplot2)

# Read in and convert string times to datetimes
trains <- read.csv('collected.csv')
trains$Time <- as.POSIXct(trains$Time, format = '%Y-%m-%dT%H:%M:%S')

# Get the data onto the plot
p <- ggplot(trains, aes(x = Time, y = Cost))

# 'Reveal' the data with points and show the
# East Mids price trend with a smoother
completed <- p + geom_point(aes(color = Operator)) +
  geom_smooth(data = subset(trains, Operator == 'East Midlands Trains'),
              aes(group = Operator, color = Operator),
              method = 'loess', se = FALSE,
              size = 0.75, show.legend = FALSE) +

  # Let's adjust the scales
  scale_x_datetime(date_breaks = '1 hour',
                   date_labels = '%H:%M') +
  scale_y_continuous(limits = c(0, 100),
                     breaks = seq(10, 100, 10),
                     expand = c(0, 0)) +

  # Set some labels and adjust the look
  labs(title = paste('Cost of single train tickets',
                     'leaving European\ncapital cities',
                     'on Friday December 23 2016'),
       y = 'Ticket cost (€)',
       color = 'Train operator') +
  theme_bw(base_family = 'Trebuchet MS') +
  theme(plot.title = element_text(hjust = 0.5))

ggsave('plot.svg', plot = completed, device = 'svg',
     width = 8, height = 4, units = 'in')
```

I’m still figuring things out with R and ggplot so I’m not exactly blazing through. (I still haven’t figured out how to export transparent SVGs without editing them by hand.)

But I love the way that plots are built up out of individual pieces, which makes far more sense to me than trying to wrangle matplotlib’s figures and axes.
