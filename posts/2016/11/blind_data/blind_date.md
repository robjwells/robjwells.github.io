title: Blind data
date: 2016-11-05 01:00

The [Guardian’s Blind Date column][blind-date] has been going for over seven and a half years now, but I always struggled to read it. There was something missing — I didn’t just want to peer into these people’s lives and be left feeling bad for them if things hadn’t gone well.

[blind-date]: https://www.theguardian.com/lifeandstyle/series/blind-date

Well the missing thing was [The Guyliner’s sort-of reviews][guyliner], which are brilliant. I only found out about his blog recently and binged a bit on them.

[guyliner]: https://impeccabletablemanners.theguyliner.com

One thing I find interesting is the way the daters’ scores for each other, which are meant to be out of 10, are stuck in a limited range between 7 and 9. (7 being “[a gentleman’s one][g1]”.)

[g1]: https://impeccabletablemanners.theguyliner.com/2016/06/18/aidan-and-padraig/

In [a recent entry][tom-emily] — which mentions a letter to the Guardian about the limited range of scores used — the two seem to get on really well, want to see each other again but the scores are 7.5 and 8.

[tom-emily]: https://impeccabletablemanners.theguyliner.com/2016/10/29/tom-and-emily/

To get a bit of perspective on the scoring I went through all of the Blind Date columns from January 31 2009 through October 31 2016. The [Guardian’s API][gapi] makes this easy, although what wasn’t immediately obvious is that you can use subsection paths (such as Blind Date at `lifeandstyle/series/blind-date`) as an alternative to an imprecise search for the same articles. Use the [interactive explorer][exp] to see for yourself.

[gapi]: http://open-platform.theguardian.com
[exp]: http://open-platform.theguardian.com/explore/

I used a bit of Python to grab all the articles, save them to disk and pull out two things: the score each dater gave their opposite number and whether or not they wanted to see them again.

The data needed cleaning up by hand, usually to parse whether a person wanted to see their opposite number again. This often required a bit of judgement on my part, so it’s not perfect. “Just as friends” counts as a No: only seeming romantic interest gets a Yes. I excluded people who in whatever way refused to answer the scoring question. (This includes “The food was a 10” etc.) I was left with 637 individual responses.

I want to stress two things: the scores are the scorer’s judgement on their date and don’t reflect mutual agreement; answers to the “Would you meet again?” question might be swayed by their partner’s reaction. So, for example, a person might rate their date a 9 but say No to the latter question if their date didn’t seem interested. I wouldn’t worry too much about this for our purposes, but I’m also not claiming this is rigorous work.

So, how frequently do the scores come up?

<p class="full-width">
    <a href="/images/2016-11-05-score_distribution.svg">
        <img alt="A bar chart showing the distribution of scores in the Guardian’s Blind Date column."
             src="/images/2016-11-05-score_distribution.svg"
             class="no-border">
    </a>
</p>

Dominating the scoring are 8 and 7, with 9 a distant third. 6 and 10 get a look in but only that.

Very few people award less than a 6 — in fact, you’re more likely to get a half-point score between 7 and 9 than a 5.

Overlaid on the grey total bars are red bars, which are daters who would like to meet their partner again. The way 8 dominates the scoring, it’s not surprising that there are more Yes answers to the “meet again” question for 8-awarding daters than any other score.

But what happens when we look at how likely a person wants to see their date again for the score given?

<p class="full-width">
    <a href="/images/2016-11-05-interest_rate.svg">
        <img alt="A bar chart showing percentage of people giving a certain score who would like to meet their date again."
             src="/images/2016-11-05-interest_rate.svg"
             class="no-border">
    </a>
</p>

Because no-one’s ever awarded less than a 6 and also wanted to see their date again, I’ve limited this plot to scores 6–10. It’s seriously unlikely that someone who awards a 6 wants to see their date again; at 7 it’s not hugely better at about one in four.

7.5 is an interesting score. I was initially tempted to round half-scores but I’m glad I didn’t (though I did round silly scores like [8.9][lougeorge] to the nearest integer). If someone awards a 7.5 they are much more likely to want to see their date again than a straight 7, at just under half the time, but still noticeably less than the rate for 8.

[lougeorge]: https://impeccabletablemanners.theguyliner.com/2016/07/23/lou-and-george/

The same can’t be said about 8.5, though, which really is a cautious 9. Someone who gives an 8.5 or 9 is pretty likely to want to see their date again.

More so actually than 10, but I’ve got a theory here: 10 is the refuge for a certain group of people who had a good time but didn’t feel anything for their date. Given the relative rarity of 10, I think it’s enough to bring down the Yes percentage to beneath that for 8.5 & 9.

(We can ignore the 100% Yes rate for 9.5, a score which has only been awarded twice.)

Lessons, then. The real scoring range is 6 to 10, but within that there are only real differences in the fundamental question — Would you meet again? — up to 8.5, after which things level off.

That’s it. I did pick up a few scoring bugbears while doing this, though:

*   “Cute” scores. 6.1, 7.4, 7.75 (twice!). These come up not often but enough that people really should resist.
*   Not answering the scoring question. My favourite was:
    
    > What is this, a baking competition? All I’ll say is “top marks”
    
    If you can award a numerical score to a cake you can award one to a date.

*   People who say they won’t answer the scoring question because they’re above it but who actually do answer the scoring question:

    > That seems rather ungentlemanly, but since you insist, 7.
    > 
    > The date? 7. Jo? I wouldn't be so vulgar…
    
    It’s men that do this. Please stop.

And lastly, our favourite fairly common sort of cop-out answer: spark.

<p>
    <video
        src="/images/2016-11-05-spark.mp4"
        poster="/images/2016-11-05-spark.jpg"
        width="480"
        height="270"
        controls loop muted
        >
    </video>
</p>

Across the 357 articles I downloaded (a handful of which aren’t actual Blind Date columns), spark is mentioned 45 separate times — about once every eight articles, which is much less frequently than I expected.
