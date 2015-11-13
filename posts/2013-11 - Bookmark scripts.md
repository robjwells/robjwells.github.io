title: Die, bookmarks bar, die
date: 2013-11-18 13:15
tags: AppleScript, Launchbar

I hate the bookmarks bar. This thing:

<p class="pic no-squish">
    <img src="/images/2013-11-18_bookmarksbar.png" alt="The bookmarks bar in Safari" class="no-border">
</p>

It’s all about the mouse here. Keyboard access is through `⌘1` for the first entry and so on, which often leaves me counting along to find which number I need.

>   What’s the number for Pinboard: Unread? One… two… three… four!

That’s gross and slow. It’s exactly the same reason why I use InDesign’s [quick apply panel][idqap] at work and don’t even try to remember the per-style keyboard shortcuts (which, handily, only work with the number pad).

[idqap]: http://help.adobe.com/en_US/indesign/cs/using/WSa285fff53dea4f8617383751001ea8cb3f-6e68a.html#WSE4179F8F-7053-48b4-BFDC-2102D5F27789

It also applies to keyboard shortcuts more generally — if you don’t use them often enough you’ll forget what the shortcut is, annoying you later and often taking more time that it would to grab the mouse.

Assigning less-arbitrary shortcuts can be helpful, but again only if you use them fairly regularly.

Back to that horrid bookmark bar, though. How do we construct a [Launchbar][lb]-style, search-based panel to get at those bookmarks? We’ll use Launchbar itself. (I guess you can do this in Quicksilver or Alfred, but I haven’t tried.)

[lb]: http://www.obdev.at/products/launchbar/index.html

Safari’s AppleScript support is fairly poor — it doesn’t expose your bookmarks to scripts. But it does have a handy `do JavaScript` command, which is all that those bookmarklets do: run JavaScript.

Grab the code (stored as the bookmark’s address) and — importantly — [decode][url] it to turn entities such as `%7B` into `{`. Lop off the leading `javascript:` and insert it into this tiny AppleScript:

    applescript:
    tell application "Safari"
      set bookmarklet to "your_bookmarklet_code_here"
      set current_tab to the current tab of the front window
      do JavaScript bookmarklet in current_tab
    end tell

[url]: http://meyerweb.com/eric/tools/dencoder/

Save that script into a new folder — mine’s in `~/Library/Scripts/Applications/Safari/Bookmarklets/`

Lastly [add that new folder to Launchbar’s index][lbindex]. I have my entry set to access on sub-search only, so to get to the bookmarklet scripts I type `bookm →` and I end up with this panel:

<p class="pic">
    <img src="/images/2013-11-18_launchbarpanel.png" alt="Launchbar’s list of my Safari bookmarklet scripts" class="no-border">
</p>

[lbindex]: /images/2013-11-18_launchbarindex.png

And we’re set: a quick, searchable, keyboard-friendly list. If, like me, you *only* use the bookmarks bar for JavaScript bookmarklets you can go ahead and hide it as an added bonus.
