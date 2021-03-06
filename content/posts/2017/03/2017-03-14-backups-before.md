---
title: "Backups: before"
date: 2017-03-14T15:00:00
---

At [work][] I’m responsible for our office file server, which is mostly used for storing the InDesign pages and related files we need to produce the paper every day.

[work]: https://www.morningstaronline.co.uk

At the end of 2016 we replaced the server, which was a 2010 or 2011 Mac Mini, with a “current” Mac Mini — the 2014 release. That wasn’t ideal and part of the reason why I hadn’t replaced it sooner was because I was waiting for Apple to at least refresh the specs.

In any case, we got to a point where the machine needed swapping. The final straw for me was being unable to trust that the backups would run reliably.

Ever since I got my current post (in mid-2014) I’d been meaning to overhaul our backup strategy but it was always a case of “I’ll do it when we replace the server.” It’s worth sketching out what we were doing before moving on to what caused concern and what I’ve replaced it with now.

In this, I’m going to include [RAID][] because the redundancy side of things also changes. For context, our working day is roughly 10am-7pm Sunday–Friday:

* Two 500GB drives in the Mini itself, in [RAID 1 (mirrored)][r1].
* [SuperDuper!][sd] copies (newer files) to two drives (in RAID 1) at — if I remember correctly — 9am, 12pm, 3pm, 5pm, 9pm, Sunday–Friday.
* Daily SuperDuper copies (newer files) to two drives (in RAID 1) at about 9pm, Sunday–Friday.
* Weekly SuperDuper erase-and-copy on Saturday to both the three-ish-hourly mirrors and the daily mirrors.
* [Arq][] backups to (old-style) [Glacier][] vaults, once a day.

The SuperDuper copies were done to a set of USB 2 disk enclosures, containing ordinary 3.5″ drives.

[RAID]: https://en.wikipedia.org/wiki/RAID
[r1]: https://en.wikipedia.org/wiki/Standard_RAID_levels#RAID_1
[sd]: http://www.shirt-pocket.com
[Arq]: https://www.arqbackup.com
[Glacier]: https://aws.amazon.com/glacier/

You’ll have noticed some fuzziness in my recollections just there, for an important reason: the machine’s performance was so poor everything bled into each other. It was totally competent serving files over [AFP][] but trying to work on the machine itself was a nightmare.

[AFP]: https://en.wikipedia.org/wiki/Apple_Filing_Protocol

And this is the point where it gets concerning. It wasn’t rare to log in to the server to find a SuperDuper copy having run for 12 hours and still going, or that Arq had hung and needed its agent restarted. Both are solid pieces of software (though it was an older version of Arq, v3 I think) so the blame does lie with the machine.

Which is odd, really, because its only tasks were:

* Serve files on the local network over AFP (to fewer than 25 users).
* Run OS X Server to handle user log-in (for access to files only).
* Host our internal (unloved and little-used) wiki.
* Perform backups (of its own drives).

Hopefully you can spot the problems — both the ones inherent in the strategy and the ones that result from poor performance:

*   Local backups were relatively infrequent and could result in hours of data loss.

    This is a bit dicey when our business relies on getting all pages to the printers by the early evening. Each page takes about an hour of work to create.

*   Local backups may not complete in a timely fashion.

    This exacerbates the point above, and the cause wasn’t readily apparent.

*   Local backups, as copies, don’t allow for the recovery of older versions of a file.

    So if you accidentally erase everything off a page, save it, and it’s backed up, you can’t recover the previous state unless it was picked up by the previous daily backup. (That’s an unlikely event, since most pages are created, finished and published between daily backups.) 

*   Remote backups, because they were stored in Glacier, would take several hours even to reach the point where files could begin to be restored.

    Even if they were hourly (not our case), if you lose a page an hour before deadline and it’s not backed-up locally your only option is to recreate the page because there’s no chance you’ll get it out of Glacier fast enough.

Let’s walk through perhaps the most likely example of data loss during our working day, when a user accidentally deletes a file (taking an InDesign page as our file):

Because of the way deletes work over [AFP][] & [SMB][], the deleted file is removed *immediately*, in contrast to a local delete requiring two steps to complete (usually): the file is moved to the trash, the trash is emptied.

[SMB]: https://en.wikipedia.org/wiki/Server_Message_Block

First, the local backups are checked. In the lucky case, a backup has run recently (and completed timely!), otherwise you could face up to three hours’ data loss, which could be all of the work on that page.

If the page was created on a previous day (uncommon) then you’d also check the daily local backups, hoping that the page was substantially complete at that point.

Then you’d check the remote backups, hoping that (like above) the page was substantially complete at the point that the backup ran and that you have the three-to-five hours needed for the restore to begin.

It’s perhaps clear that the chances of recovering your work are *not good*. It gets even worse when you consider the next common case: that a user modifies a complete page, destroying the original work, and that modified version replaces the original on the more-frequent local backups.

(When I was very new at the Star I did something similar. I was asked to work on a features page for the following day. I opened up the corresponding page for edition to save a copy but for whatever reason didn’t — and began to work *on the “live” page for edition*. When this was noticed — close to deadline! — I was thankfully able to undo my way back to the original state, as I hadn’t closed InDesign since opening it. It was an *incredibly* close call that still makes me feel queasy when I think about it.)

So while we did have a strategy that included both local and remote backups, it was effectively useless. That everything locally was in RAID 1 — meaning that if one drive of a mirror fails, you don’t lose data — I think just shows that when it was set up, the core purpose of backing up our data was misunderstood. 

We had copies of our business-critical data, but constructed in such a way that protection against drive failure was far, far more important that the much more common case of restoring fast-changing files. In this system, you could have five drives die and still have a copy of our server data locally, or all six die (perhaps in a fire) and be able to recover remotely.

To sum up, it was reasonable protection for a rare event but little protection for a common event.

It is, of course, possible to have both. In [my next post][next] I’ll go into what’s changed, why, and what that means for protecting our data in both the common and rare cases.

[next]: https://www.robjwells.com/2017/03/backups-the-change/
