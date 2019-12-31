---
title: "HTML image dimensions with a CSS border"
date: 2018-05-17 21:00
---

When I use images here, I tend to give ones without any transparency a border, which is done using CSS and applied to `img` tags unless they have a `no-border` class.

Like a good web citizen, I also [specify image dimensions in HTML][html-dims]:

> “The image’s rendered size is given in the width and height attributes, which allows the user agent to allocate space for the image before it is downloaded.”

[html-dims]: http://w3c.github.io/html/semantics-embedded-content.html#example-82f39213

In fact my BBEdit `image` snippet makes it a doddle:

    <p <#* class="full-width"#>>
        <img
            src="/images/#SELECTIONORINSERTION#"
            alt="<#alt text#>"
            <#* class="no-border"#>
            width=<#width#>
            height=<#height#>
            />
    </p>

But this causes a problem, which I’ve spotted in a couple of my recent posts.

If you specify the image dimensions, and use a CSS border, *and* have your CSS `box-sizing` set to `border-box`, then the CSS border shrinks the amount of space available to the image to its specified dimensions − 2 × the border width.

So if you specify your `img` dimensions to match the dimensions of the file, then the image itself will be shrunk within the element.

This animation shows this situation, and what happens when you toggle the CSS border. Watch what happens to the image itself.

<p class="full-width">
    <img
        src="/images/2018-05-17-border-with-dimensions.gif"
        alt="An animation showing an image being squeezed within the space it has been allocated, causing distortion."
        class="no-border"
        width=565
        height=385
        />
</p>

(It’s got a slight offset from the text because it’s a screenshot of this blog and includes some of the background on each side.)

In contrast, this animation shows what happens when the dimensions are not specified, and so the image is free to grow when the border is applied:

<p class="full-width">
    <img
        src="/images/2018-05-17-border-no-dimensions.gif"
        alt="An animation showing an image growing when a CSS border is applied, with no distortion to the image itself."
        class="no-border"
        width=565
        height=385
        />
</p>

Really the culprit here is `box-sizing: border-box`, forcing the border to remain within the size of the `img` element itself. This is a behaviour you actually want, as it solves the old CSS problem of juggling widths, borders and padding within a parent element. Check out [MDN’s `box-sizing` page][mdn] to see what I mean.

[mdn]: https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing

What are my options, then?

*   Change box-sizing.

    I’m not touching this because the potential sizing headaches are not worth it, even just for `img` elements.

*   Apply a border to the image files themselves.

    No, because if I change my mind about the CSS, previously posted images are stuck with the old style forever. CSS borders should also work correctly across high-density displays, whereas a 1px border in the file may not.

*   Don’t specify dimensions in the HTML.

    I don’t like the idea of making pages of this site slower to render, but I think this is the least bad option, particularly given that [this site is already pretty fast][speed].

[speed]: /2017/04/page-speed/

It’s not ideal, but that BBEdit snippet is now just:

    <p <#* class="full-width"#>>
        <img
            src="/images/#SELECTIONORINSERTION#"
            alt="<#alt text#>"
            <#* class="no-border"#>
            />
    </p>

Hey, at least it makes images quicker to include in posts!
