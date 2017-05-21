library(ggplot2)

trains <- read.csv('collected.csv')
trains$Time <- as.POSIXct(trains$Time, format = '%Y-%m-%dT%H:%M:%S')

p <- ggplot(trains, aes(x = Time, y = Cost))

completed <- p + geom_point(aes(color = Operator)) +
    geom_smooth(data = subset(trains, Operator == 'East Midlands Trains'),
                aes(group = Operator, color = Operator),
                method = 'loess', se = FALSE,
                size = 0.75, show.legend = FALSE) +
    scale_x_datetime(date_breaks = '1 hour',
                     date_labels = '%H:%M') +
    scale_y_continuous(limits = c(0, 100),
                       breaks = seq(10, 100, 10),
                       expand = c(0, 0)) +
    labs(title = paste('Cost of single train tickets',
                       'leaving European\ncapital cities',
                       'on Friday December 23 2016'),
         y = 'Ticket cost (€)',
         color = 'Train operator') +
    theme_bw(base_family = 'Source Sans Pro') +
    theme(plot.title = element_text(hjust = 0.5))

ggsave('plot.svg', plot = completed, device = 'svg',
       width = 8, height = 4, units = 'in')
