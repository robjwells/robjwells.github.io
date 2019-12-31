---
title: "Working with R Markdown"
date: 2018-05-05T23:55:00
---

I’ve just published an update to [my recent Tube travel post][tube-2], fixing a few small mistakes, a bigger one (an error in a station name that nonetheless didn’t affect the plot involved) and adding an update to the last section which goes a bit deeper into the fare and duration difference between the two periods.

I didn’t fix the mistake in the title, as I felt it was too late, but of course it’s 3⅔ years, not 3.75, since September 2014.

<p>
    <video src="/images/2018-05-05-naked-gun-realise-that-now.mp4"
        poster="/images/2018-05-05-naked-gun-realise-that-now.jpg"
        controls
        muted>
        <img
        src="/images/2018-05-05-naked-gun-realise-that-now.jpg"
        alt="“I realise that, now…” from the film Naked Gun">
    </video>
</p>

[tube-2]: https://www.robjwells.com/2018/05/3-75-years-on-the-tube/

In that post I mentioned how pleasant it is working in [R Studio][] in a [R Markdown][] document. It really is, and I find the R Markdown way of mixing prose and code much more natural and fluid than [Jupyter notebooks][jupyter], which I like the idea of but find the block-based method a bit awkward.

[R Studio]: https://www.rstudio.com/products/RStudio/ 
[R Markdown]: https://rmarkdown.rstudio.com
[jupyter]: https://jupyter.org

The biggest problem with R Markdown was fitting it into my, admittedly arcane, [blogging system][majestic]. To do so, I’ve cooked up [a short Python script][script] to transform the Markdown output from R Studio and [knitr][].

[majestic]: https://github.com/robjwells/majestic
[script]: https://github.com/robjwells/primaryunit/blob/3be7c91007f10946e60fecb3c2007f85080d3950/posts/2018/04/decode_blocks.py
[knitr]: https://yihui.name/knitr/

Right now, I’ve settled on this set of output options in the YAML front-matter:

    yaml:
    md_document:
        variant: markdown_strict+fenced_code_blocks
        preserve_yaml: true
        fig_width: 7.5
        fig_height: 5
        dev: svg
        pandoc_args: [
            "--wrap", "preserve"
        ]

Now I don’t actually use fenced (`~~~~`) code blocks in Markdown, instead I just use regular Markdown indented code blocks with a header line (`python:`) at the top. But I include that extension in the Markdown variant to make it easier to transform code blocks later.

But why? Well, if your output just uses indented code blocks, it’s difficult to tell which of those are your R code and which are the R code’s output. Fencing the blocks makes it easier to insert empty comments after each block, keeping code and output separate.

The [YAML][] front matter is preserved as I use a similar thing in my own posts and this gets passed through to my blogging system without a problem, with unknown settings ignored. (I do remove the quoting that the template file includes around strings.)

[YAML]: https://en.wikipedia.org/wiki/YAML

The other important option above is supplying the `--wrap` argument to [Pandoc][], preserving the line breaks as they are in the source file instead of breaking them. By default Pandoc hard-wraps the lines, which I’d be fine with, except that it hard wraps the alt text for images (plots).

That makes it more difficult to pick out later. This is necessary as I always use HTML to include images in my posts (so I can set classes, allow for full-width etc).

I say more difficult as I’m working line-wise. It’d be possible to apply a regex to the joined lines and make the transformation, but then again I don’t hard-wrap my own posts so it’s not something I care about keeping.

[Pandoc]: http://pandoc.org

The option I would like to use is to keep my Markdown reference links intact, instead of having Pandoc put everything inline. But this makes the images into reference links, making rewriting more difficult again.

So, I knit the document together from R Studio, then apply [the script][script], and pipe the output into the for-real .md file. This is the one that gets checked into the [Mercurial][] repository, fed into my blog generator and ultimately published.

[Mercurial]: https://www.mercurial-scm.org

I could probably get away with doing less, or handling things differently — such as allowing for fenced code on the generator’s side.

But I want the transformed output to resemble as closely as possible something that I’d written in [BBEdit][] because I actually attach some importance to the contents of the Markdown files outside their use as raw material with which to create HTML.

They should be able to tell the post’s story without needing to be processed further, to interpret R code or make the raw source readable. I’m not quite at the point of having totally pure, completely readable plain text files (note those dummy comments mentioned above) but I want to be as close as I can.

[BBEdit]: https://www.barebones.com/products/bbedit/
