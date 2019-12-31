---
title: "Restart in Windows: Revenge of the Script"
date: 2012-10-06 18:14
tags: ["AppleScript"]
---

<div class="flag">
<strong>UPDATE 2013-05-25</strong>
<p>I’ve changed the script to fix the fiddliness on Leopard. Please <a href="/2013/05/restart-in-windows-the-script-strikes-back/">see my new post</a> for details. I’ve left the rest of this post mainly intact, but please bear in mind that the code has changed slightly.</p>
</div>

Want to quickly restart your Mac in your Windows Bootcamp partition, without having to hold down option/alt as the computer starts?

<del>Click this link</del>, which will open an AppleScript in your default editor, and replace “YourBootcampPartition” in the first line with your Windows partition’s actual name (making sure that is exactly the same, as it’s case sensitive). Then save it as a .scpt file in your user scripts folder, which you can access through the system-wide script menu (which is turned on in AppleScript Editor’s preferences).

Then, to restart, just pick it from that script menu.

### Extra, extra

<del>*Using Leopard (10.5) or earlier?* You’ll have to change the first line as “diskutil info” doesn’t work with volume names. Try this:</del>

    applescript:
    set deviceID to (do shell script "diskutil list | ¬
      grep YourBootcampPartition | awk '{print $8}'")

<del>That should return something like "disk0s4". If it doesn’t change “print $8” to a different number, probably 7. (I recommend you try this in the Terminal until you’ve got it right, then adjust the AppleScript. The number refers to the column of the information.)</del>

<ins>The above isn’t true anymore. <a href="/2013/05/restart-in-windows-the-script-strikes-back/">Please see my latest post about it.</a></ins>

*Don’t want to have to type your password in every time?* Add “password "YourPassword" ” after “ -nextonly" ” on the second line, then save your script as run-only. **I do not recommend this.** Your password will not be encrypted. It is only slightly less insecure than keeping your password in a text file. Please, *do not do this*.

### Using it

I’ve got it saved to my ~/Library/Scripts folder, and have [Launchbar][lb] set to index that folder so I can just type "Restart in Windows" into the prompt, hit enter, type my password and then I’m set.

You could also use [FastScripts][fs], a really nice replacement for the system script menu that you can use to give the script a keyboard shortcut.

I don’t recommend that you save it as an application, which would let you add it to your dock. I did that once and got stuck in a restart loop, thanks to Lion’s ability to re-open applications that were running when you restarted. You can disable that feature in Mountain Lion, but I still strongly advise that you keep it as a plain old script file.

[fs]:   http://www.red-sweater.com/fastscripts/
[lb]:   http://www.obdev.at/products/launchbar/index.html

### The code

    applescript:
    set deviceID to (do shell script "diskutil info ¬
    YourBootcampPartition | grep Identifier | awk '{print $3}'")

    do shell script "bless -device /dev/" & deviceID & ¬
    " -legacy -setBoot -nextonly" with administrator privileges

    tell application "Finder" to restart


### The story

Basically, holding down option on my keyboard was unreliable because the computer had booted up too fast for the Bluetooth connection. I’d been using [Bootchamp][], a menubar utility, for a while but you couldn’t trigger a restart from Launchbar and had to mount the partition first.

[Bootchamp]:    http://www.kainjow.com

The first version relied on the disk identifier never changing. You can’t rely on a partition having the same identifier after a restart, so the script would silently fail.

The next version relied on the disk identifier being in a certain character position, which (aside from being a dirty hack) was also unreliable if you had more than 10 disks connected.

The most recent (and probably final) version uses grep and awk on the command line to fetch the disk identifier after pulling up the information for the partition. (In Leopard it has to get the identifier from the list of every partition, as “diskutil info [PartitionName]” only works in Snow Leopard and later. As such it’s a little less reliable and needs a bit more tweaking by users.)

For such a simple script (three whole lines!) this has taken more work than I originally anticipated. But it’s also taught me a fair bit about the command line and how to retrieve information from it.

So, yeah. I think it’s done now. If you have any questions or comments please [message me on Twitter][tw] or add a comment to [the script’s gist][gist].

[tw]:   http://www.twitter.com/robjwells
[gist]: https://gist.github.com/3681949
