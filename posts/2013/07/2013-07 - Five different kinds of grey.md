title: Five different kinds of grey
date: 2013-07-06 18:54
tags: Personal, Web

My post from a couple of weeks ago [about the changes to this site][newlook] briefly mentioned that despite having this domain for about five years I’d never been satisfied with its design.

[newlook]: /2013/06/a-new-look-and-name/

I’ve actually lost count of the number of times I’ve switched themes but, spread across Blogger, WordPress and Tumblr, it must be at least 10. None of them stuck.

[bm]: http://basicmaths.subtraction.com/demo/

Part of that is likely that I never stuck at it, never put in the effort to make the posts worthwhile. But maybe one of the reasons why is because I knew I wasn’t going to be happy with how the results looked.

But I *am* happy with the design now. Having put in the time to learn HTML and CSS (with [some help][lwd]), it wasn’t too hard to make something that I’m at least a little proud of. And now I’d like to share some of the thinking behind it.

[lwd]: http://learningwebdesign.com

It’s pretty simple — largely because I can handle this kind of simplicity well with my limited skills. But it’s just a personal blog and I don’t want to overcomplicate matters.

I took a lot of cues from [Dr Drang][drang], [Marco Arment][marco] and [John Gruber][df], all of whom have great sites with top work framed with a straightforward design.

[drang]: http://www.leancrew.com/all-this/
[marco]: http://www.marco.org
[df]: http://daringfireball.net

I’d love to claim some kind of inspiration but, when it came down to it, I made a fairly arbitrary decision to stick the meta stuff on the left, the content in a big long column on the right and then call it a day. On smaller screens the meta column sits on top of the content and the social links disappear entirely on particularly thin screens (phones) as they’re not essential. My earlier sketches had elements boxed or ruled off, but a few technical difficulties pulling this off convinced me to mostly just use whitespace.

All text is set in [Rooney][]. A while ago I had got obsessed with [Tisa][] and had initially planned to use that. But I eventually had trouble reading long Instapaper articles in it — the vertical strokes tended to run together when I was tired. After searching the Typekit library for a while I settled on Rooney, which is similar in many ways to Tisa — but with enough subtle differences and little quirks to avoid the problem I had with Tisa. Also as lovely as Tisa is it can be a bit cold and clinical, while I find that Rooney feels more warm and welcoming.

[Rooney]: https://typekit.com/fonts/rooney-web
[Tisa]: https://typekit.com/fonts/ff-tisa-web-pro

Paragraphs are limited to roughly 65 characters (about 12 words) a line, though I’m still tweaking the exact length. I had initially had an idea to accommodate margin notes in the extra space but technical hurdles, a lack of anything to put there and fear of looking incredibly pompous made me decide against it. A remnant of this can be seen in the blockquotes, code blocks and coloured boxes I use, which all stretch the full width of the column. Code blocks are the only element that make use the extra space, but the others get it because I like how their background colours can help break up long columns of text.

<div class="flag">
    <p>The coloured boxes I mentioned above I call “flags” and came about when I decided I wanted a way to <em>flag</em> updates to posts. (Again, an influence of Dr Drang: <a href="http://www.leancrew.com/all-this/2012/07/some-safari-6-stuff/">see the updates in this post</a>.) I then generalised the style to be applicable to a range of things, such as flagging download links and warnings.</p>
</div>

The flags use icons from [Symbolset’s Standard font][ssstandard], which I use in a few places on the site — probably not enough to justify the weight of an extra web font but I like the font a lot and had been itching to use it for months. Similarly, the social icons in the sidebar use [Symbolset’s Social font][sssocial]. I use the circular version to give them an even appearance.

[ssstandard]: http://symbolset.com/icons/standard
[sssocial]: http://symbolset.com/icons/social-circle

It took me a long time to pick out the dark blue used as the left-hand border of the flag above, which is also the primary link colour. Generally, I’m not great at picking colours but [Spectrum][] helps enormously. Before using Spectrum I’d end up with a murky mess, but now I’m actually very pleased with the palette I have created. It’s mostly blue and grey, with splashes of green and red where appropriate.

[Spectrum]: http://www.eigenlogik.com/spectrum/mac

The image below shows all the colours used on the site, apart from those used for code. (The two oranges are only used for the RSS link.)

<p class="full-width"><img src="/images/2013-07-06_Spectrum.png" alt="The 14 colours used on robjwells.com"></p>

The syntax highlighting for code is another thing I lifted from Dr Drang, which is to say it is [highlight.js][hljs] combined with [the Doc’s script to conditionally invoke][drangsyntax] the highlight functions and add line numbers.

[hljs]: http://softwaremaniacs.org/soft/highlight/en/
[drangsyntax]: http://www.leancrew.com/all-this/2010/12/new-syntax-highlighting-for-markdown/

I’ve uploaded [my slightly rewritten code][syntaxgist] as a GitHub gist. The two main changes are the introduction of the module pattern (using the RJW global variable as a container) and removing the dependency on JQuery. The syntax colour scheme is based on [my custom one for BBEdit][rjwlight].

[syntaxgist]: https://gist.github.com/robjwells/5940383
[rjwlight]: https://gist.github.com/robjwells/5940537

Speaking of JQuery, nothing in my design requires it. But it’s one of those things Tumblr injects into your blog anyway. This is a bit of a shame, as I’d tried to keep page weight down (*five* web font files notwithstanding). The three largest downloads on this page are all things injected by Tumblr — the fourth is my 135KB Typekit CSS file.

While this doesn’t bother me a huge amount, it does add another reason for me to move away from Tumblr — almost certainly to a static system of some kind. (I have a fantasy of learning enough Python to write my own.) While I imagine that’s quite a while off, it should be a fairly easy transition — there are no dynamic elements to move over and the “Tumblrised” HTML file I have would be simple to switch to another template system.

I haven’t spent much time on Tumblr-specific features, either. The only post types I accommodate are text, links and photos. I did the work for the latter two largely because I already have posts of that type that I wish to keep, not because I plan to make more of them in the future. Again, making it easier to switch away at some point in the future.

It’s not that I dislike Tumblr, just that [I’m not a great fit for Tumblr][hazeltweet] and Tumblr’s not a great fit for me and the kind of site that I want to run.

[hazeltweet]: https://twitter.com/robjwells/statuses/349479449093341188

Right, we’re over 1,000 words now so it’s time to wrap it up. If you’ve made it this far, thanks! If you have any comments or questions be sure to send me a message on [Twitter][] or [App.net][adn].

[Twitter]: https://twitter.com/robjwells
[adn]: https://alpha.app.net/robjwells
