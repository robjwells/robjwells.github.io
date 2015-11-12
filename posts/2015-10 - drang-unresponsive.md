title: Re: Unresponsive
date: 2015-10-06 02:33
tags: Web

[Dr Drang posted recently][drang] about his trouble getting his site to work with the new responsive design mode in Safari 9 (which is very similar to the Firefox feature of the same name). He also detailed the complicated setup he has for providing his current mobile layout to small, portrait screens (ie phones) — media queries in HTML link tags and separate stylesheet files.

[drang]: http://leancrew.com/all-this/2015/10/unresponsive/

(I should also point out, if Dr Drang is reading, that his mobile.css file is missing the rule for `#content iframe`. I’m not sure if this is deliberate.)

Since I’ve fought with responsive design a couple of times, and seemingly have a need to stick my nose into other people’s business, I wondered how difficult it would be to combine the two separate CSS files and get responsive design mode to work.

To give some context to what’s discussed, I’ve put up [a gist containing the combined CSS file and required HTML changes][gist]. In the CSS file you’ll want to look at the end part, [from line 809][l809]. That part contains two media queries, which split out:

1. Rules only for small portrait screens (ie phones).
2. Rules for everyone else (but *not* small portrait screens).

[gist]: https://gist.github.com/robjwells/d1c38b72ddc292ac42e1
[l809]: https://gist.github.com/robjwells/d1c38b72ddc292ac42e1#file-drang-combined-css-L809

The two diffs at the top show the changes from Dr Drang’s mobile.css and style.css. The combined file is based on the main stylesheet, which is why there are more changes in the mobile diff.

Most of the changes that make up the Doc’s mobile style sheet are `font-size` declarations to boost the text size — and these don’t appear in the combined file, which points to the most interesting aspect of this and something that had me confused for not a short while.

Basically, Dr Drang’s mobile style sheet increases the text size to compensate for the mobile browser rendering at “full size” (980px in Safari on iOS). (This is how [the New York Times website looked normal in the first iPhone demo][nyt-demo] in 2007.) The usual technique is to tell the browser to render at “device size” through the use of a `meta` HTML tag:

    xml:
    <meta name="viewport" content="width=device-width, initial-scale=1">

[nyt-demo]: https://youtu.be/vN4U5FqrOdQ?t=2515

It took me a while to work out that this combined with Dr Drang’s larger text to make everything appear massive:

<p>
    <img
        alt="My CSS changes to the And Now It's All This mobile css file caused the text to become huge."
        src="http://img.robjwells.com.s3.amazonaws.com/posts/2015-10-06_massive.png"
        width="320">
</p>

So those rules went, and some new ones to fix the size of the header came in. But otherwise there are no changes to the styles.

The change in approach means that the result isn’t an exact match for the real site:

<p class="pic">
    <img
        alt="A portrait comparison of my CSS changes to the real And Now It's All This site."
        src="http://img.robjwells.com.s3.amazonaws.com/posts/2015-10-06_portrait-comparison.png"
        width="641">
</p>

And in landscape the fixed sizes in the CSS file combine with the use of “device size” to produce a layout that’s larger than the screen width, forcing Safari to resize the viewport until it *just* fits:

<p class="pic">
    <img
        alt="A landscape comparison of my CSS changes to the real And Now It's All This site."
        src="http://img.robjwells.com.s3.amazonaws.com/posts/2015-10-06_landscape-comparison.png"
        width="568">
</p>

The changes mean that responsive design mode in Safari works for portrait mode:

<p class="pic">
    <img
        alt="My CSS changes to And Now It's All This in Safari's responsive design mode in portrait."
        src="http://img.robjwells.com.s3.amazonaws.com/posts/2015-10-06_portrait-rdm.png">
</p>

But landscape mode is not accurate, as there isn’t the viewport-resizing that squeezes the too-large layout to fit on the phone itself:

<p class="pic">
    <img
        alt="My CSS changes to And Now It's All This in Safari's responsive design mode in portrait."
        src="http://img.robjwells.com.s3.amazonaws.com/posts/2015-10-06_landscape-rdm.png">
</p>

Lastly, I’m going to close with my tips for not going completely mad when trying to make a responsive layout:

* Have the main part of the CSS file — before any media queries — produce a usable single-column layout (ie for phones).
* Try to have media queries build on previous rules instead of trying to undo them.
* Use as few media queries, and as few rules within them, as possible.

I’ve recently rewritten this site’s CSS to prepare for [a behind-the-scenes change][majestic]. Compared to the current stylesheet, first written in 2013, it’s much saner — specifically with regards to media queries but also in general.

Here’s [the current stylesheet][current-css] and [the new one][new-css] if you want to take a look. In the new file the main part, before any media queries, creates a small layout, which is finessed by a mid-sized media query, then finally adjusted for larger screens.

[majestic]: https://bitbucket.org/robjwells/majestic/
[current-css]: https://gist.github.com/robjwells/9026d9da9c19c5f24ad7
[new-css]: https://bitbucket.org/robjwells/primaryunit-2015/src/572cbd62d4e5c54804a608398a39aeac3777a88e/css/styles.css
