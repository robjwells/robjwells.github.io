title: Tube crowding
date: 2017-03-13 23:10

Last week [TfL released some data about crowding on Tube trains][data]. There’s a good write-up by [Diamond Geezer][dg].

[data]: https://blog.tfl.gov.uk/2017/03/09/new-tube-customer-volumes-and-movements-data/
[dg]: http://diamondgeezer.blogspot.co.uk/2017/03/tubesquash.html

Basically, TfL give each 15-minute slot on each line in each direction a rating from 1 (quiet) to 6 (stuffed). I thought I’d have a go at turning that data into some heatmaps, so you can pick out the busiest times more easily.

Now, this was my first time trying to make heatmaps, my first time using [Seaborn][] and my first time using [Pandas][]. The plots are not great. I basically got to the end of my tether trying to sort the code out and ended up spending a chunk of time polishing the resulting images. Even then…

[Seaborn]: http://seaborn.pydata.org
[Pandas]: http://pandas.pydata.org

Before we go any further, all the plots are linked to the SVG files if you want to have a closer look as the labels appear quite small. Also, I’m only going to describe the oddities in the plots, not draw conclusions from them — others can do that if they’re interested.

Let’s start with the [Waterloo & City][Waterloo] line because it’s simplest:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-WC.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-WC.svg"
        alt="Tube crowding on the Waterloo & City line"
        class="no-border"
        width=720
        height=80
        />
    </a>
</p>

Hopefully you can pick out the labels on the left showing the source and destination stations, the times (5am to 2am) and the change in colour showing how crowded the trains are. It’s quiet easy to pick out the peaks here: Waterloo to Bank around 8 and 9am, Bank to Waterloo around 5 and 6pm.

Now, in alphabetical order, let’s go through the rest. [Bakerloo][]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Bakerloo.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Bakerloo.svg"
        alt="Tube crowding on the Bakerloo line"
        class="no-border"
        width=720
        height=360
        />
    </a>
</p>

Note here something that applies to the rest: not all pairs of stations are listed as I was having trouble making them legible. I tend to leave out every other pair so, above, it’s implied that after *Harrow & Wealdstone → Kenton* and before *South Kenton → North Wembley* there is *Kenton → South Kenton*. But, as we’ll see, this isn’t always the case.

Looking at the early morning services in Kenton and Wembley it is pretty obvious, as [Diamond Geezer pointed out][dg], that someone has been mucking about with the data.

Next, [Central][]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Central.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Central.svg"
        alt="Tube crowding on the Central line"
        class="no-border"
        width=720
        height=720
        />
    </a>
</p>

This was one of the first plots I “tidied” which is why the scale is missing. Note here the apparent disappearance of lots of travellers in the top-left and bottom-right of each plot. This is because of branching lines. I’ve tried to keep in the first station for each branch for each direction but it isn’t always the case. You may want to read these alongside [the Tube map][map].

[map]: https://tfl.gov.uk/maps/track/tube

[Circle][]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Circle.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Circle.svg"
        alt="Tube crowding on the Circle line"
        class="no-border"
        width=720
        height=360
        />
    </a>
</p>

Not this is only the “Outer Rail” and “Inner Rail” — clockwise and anti-clockwise — sections of the Circle line, starting at Edgware Road. I left off the “jug handle” between Paddington and Hammersmith, which was pretty quiet anyway. In fact the whole line is fairly quiet — something DG pointed out — so the data is a bit suspect.

[District][]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-District.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-District.svg"
        alt="Tube crowding on the District line"
        class="no-border"
        width=720
        height=700
        />
    </a>
</p>

All those cut-off bits are because of the five branches in west London. [It’s a weird line][District] for historical reasons. Again I’m sceptical about the data because the District is the busiest sub-surface line, but the plots show that to be the [Hammersmith & City][HC]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-HC.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-HC.svg"
        alt="Tube crowding on the Hammersmith & City line"
        class="no-border"
        width=720
        height=380
        />
    </a>
</p>

No branches. Hurrah. Next.

[Jubilee][]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Jubilee.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Jubilee.svg"
        alt="Tube crowding on the Jubilee line"
        class="no-border"
        width=720
        height=360
        />
    </a>
</p>

I love how Canary Wharf slices across these charts.

Let’s sod off to [Metro-land][metro]:

[metro]: /images/2017-03-13-metro-land.jpg

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Metropolitan.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Metropolitan.svg"
        alt="Tube crowding on the Metropolitan line"
        class="no-border"
        width=720
        height=430
        />
    </a>
</p>

The [Metropolitan][] line appears to be weirdly spacious in the evenings given how rammed it is in the morning. I’ve no idea if either is true to life.

More branching fun with the [Northern][] line:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Northern.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Northern.svg"
        alt="Tube crowding on the Northern line"
        class="no-border"
        width=720
        height=620
        />
    </a>
</p>

I know, it’s weird, I should have done separate charts or something but TfL need to get on with it and [split it up][split].

[split]: http://www.standard.co.uk/news/northern-line-service-divided-in-312m-bid-to-end-overcrowding-6468560.html

[Piccadilly][]:

<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Piccadilly.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Piccadilly.svg"
        alt="Tube crowding on the Piccadilly line"
        class="no-border"
        width=720
        height=630
        />
    </a>
</p>

Strange pattern there, but it’s another strange line. Thankfully the last one is straightforward, the [Victoria][]:


<p class="full-width">
    <a href="/images/2017-03-13-Tube-Crowding-Victoria.svg">
        <img
        src="/images/2017-03-13-Tube-Crowding-Victoria.svg"
        alt="Tube crowding on the Victoria line"
        class="no-border"
        width=720
        height=240
        />
    </a>
</p>

Doesn’t look too bad, that one.

Sorry the charts were so poor, do let me know what I should’ve done differently, or just whinge — I’m just glad this is over.

[Bakerloo]: https://en.wikipedia.org/wiki/Bakerloo_line
[Central]: https://en.wikipedia.org/wiki/Central_line_(London_Underground)
[Circle]: https://en.wikipedia.org/wiki/Circle_line_(London_Underground)
[District]: https://en.wikipedia.org/wiki/District_line
[HC]: https://en.wikipedia.org/wiki/Hammersmith_%26_City_line
[Jubilee]: https://en.wikipedia.org/wiki/Jubilee_line
[Metropolitan]: https://en.wikipedia.org/wiki/Metropolitan_line
[Northern]: https://en.wikipedia.org/wiki/Northern_line
[Piccadilly]: https://en.wikipedia.org/wiki/Piccadilly_line
[Victoria]: https://en.wikipedia.org/wiki/Victoria_line
[Waterloo]: https://en.wikipedia.org/wiki/Waterloo_%26_City_line
