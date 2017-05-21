library(ggplot2)
library(Cairo)

# 'Open up' an SVG device to record the plots
CairoSVG('plot.svg', width = 8, height = 4, bg = 'transparent')

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
    theme_bw(base_family = 'Source Sans Pro') +
    theme(plot.title = element_text(hjust = 0.5))

# Display the plot and close the SVG device
print(completed)
dev.off()
