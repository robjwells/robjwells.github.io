---
title: "Blackjack!"
date: 2013-02-25T14:58:00
tags: ["Web"]
---

For the last few months I’ve been working, on and off, on a little web project — [a basic blackjack game you can play in your browser][bj]. It’s not going to win any awards but it was a fun exercise to teach myself some JavaScript, HTML and CSS.

[bj]: http://robjwells.github.com/veintiuno

I got the idea for it after finishing [Codecademy’s original JavaScript course][cjs], where you spend some time working on the basics behind such a game. At the very end of the course, once you’ve put all the pieces together, you’re encouraged to keep working on it to see what you can improve.

[cjs]: http://www.codecademy.com/tracks/javascript-original

One of the leads is to improve the way the players’ hands are displayed by printing a more human-friendly message to the console. But I thought perhaps there was a way to improve the interface further, by breaking the game out of the console and hooking it up to a visual display in the browser proper. And, well, [this is what I’ve got][bj] — and I encourage you to [poke around the code][bjc] as well.

[bjc]: https://github.com/robjwells/veintiuno

The core game logic is more or less the same, though I’ve taken time to improve certain aspects — dealing cards from a depleting deck, having the dealer hit on “soft” 17 (mostly for the challenge), better feedback, hiding the dealer’s hole card, and a few other bits.

Since it hasn’t changed radically, I was surprised to find that the JavaScript file is now over four times longer than what I had when I finished the [Codecademy][] track.

[Codecademy]: http://www.codecademy.com

I think that mirrors my surprise at how much work it actually was to get everything hooked up, working right and looking good enough to put out into the world without me dying of embarrassment. (And most of the extra JavaScript lines are related to connecting with HTML & CSS.)

Man, web design is *hard*. Well, it was hard for me — I guess because what little I did know was all geared towards making “regular” web pages, where you’ve got some text and maybe some images and maybe a list or two and *not* enough moving parts to construct a [Rube Goldberg Machine][rgm].

[rgm]: http://en.wikipedia.org/wiki/Rube_Goldberg_machine

I actually would have been finished a little while ago but I decided to junk my original design, which looked like the layout you get now when using a wider window, because cutting off screens thinner than 800px was just an enormous cop-out and I couldn’t stand it. It was made worse by the fact I’d started reading [Ethan Marcotte’s Responsive Web Design][rwd].

[rwd]: http://www.abookapart.com/products/responsive-web-design

So now you’ll see a “narrow” layout with devices thinner than 800px, and a luxuriously spacious design on anything wider. If you have an iPad you can see both very easily: thin design in portrait, wide in landscape.

Speaking of the iPad, one of my goals was to not use any images that would get pixellated on high-DPI (retina) displays. I also wanted to keep the total file size as low as possible — one of the reasons I didn’t use jQuery and instead wrote my own helper functions.

So step in [SVG][]. The seven images used are all SVG files, weighing in at a whopping 12KB (and just 6KB when compressed).

[SVG]: http://en.wikipedia.org/wiki/Scalable_Vector_Graphics

The biggest file by far is the [League Gothic][lg] web font file, which I like a lot and wouldn’t change but it has caused me some headaches. It can display oddly, appearing overly bold in Chrome for example. And finding a fallback font was basically impossible, though the new designs get around that by not including fragile elements designed around the font’s particular shape and size.

[lg]: http://www.theleagueofmoveabletype.com/league-gothic

The about button, styled as a red casino chip, is the only thing left of those fragile elements. Originally I had [two other chips][chips], with the number on their faces displaying the number of hands won and lost. I liked the look but they were ultimately so fiddly I ditched them for the simpler, clearer text-only counters.

[chips]: /images/2013-02-25_bjchips.png

These also display better in Firefox, as the tabs around the chips’ outside — originally faked using a dashed border — displayed as a solid ring (because of how Firefox handles high border-radius values).

Having said that, compatibility was not a priority for me. That would be stupid in the real world but I think I can get away with it here. This freed me up to use recent CSS features such as transforms, transitions, shadows, animation, new units, etc. (Since I mention animation, the overlays’ bounce effects come from [Daniel Eden’s awesome animate.css][ani].)

[ani]: http://daneden.me/animate/

While this has been liberating, it’s also made clear that there are some oddities in CSS and browsers’ implementations of it that can sometimes trip you up, with problems seemingly coming out of nowhere.

But practice looks to be the best way to clear up any confusion and I’m eager to learn and do more. I’ll probably make my own theme for this blog next, though I’m going to work through [Jennifer Robbins’s Learning Web Design][lwd] first to make sure I have a firm footing.

[lwd]: http://learningwebdesign.com

I think that’s about it, so thanks for reading and if you have any questions or comments I’m [@robjwells on Twitter][tw].

[tw]: http://twitter.com/robjwells
