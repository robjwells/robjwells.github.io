---
title: "Ejecting all disks"
date: 2022-01-09T20:13:21Z
publishDate: 2022-01-09T20:48:27+00:00
---

David Sparks posted this week about [ejecting disks using AppleScript
and Keyboard Maestro][macsparky]. I’m grateful to David for posting
about this — it’s something I’ve needed for a while but hadn’t got
around to doing. Currently I plug my laptop into several external drives
when I’m sat at my desk, and have to eject them before taking it
somewhere more relaxed.

[macsparky]: https://www.macsparky.com/blog/2022/01/using-keyboard-maestro-and-applescript-to-eject-external-drives/

But David’s script didn’t quite work for me in that a blunt `eject the
disks` command to the Finder will attempt to eject all the disks that
are considered “ejectable”. For me, this includes APFS snapshots that
aren’t obviously visible in the user interface, where trying to eject
them pops up a dialog referencing "Macintosh HD – Data@snap…".

My alternative is to filter out any drives that contain "Macintosh HD"
in their displayed name:

```applescript
tell application "Finder"
    eject (every disk where "Macintosh HD" is not in its displayed name)
end tell
```

Note that it’s important to use the _displayed name_ property as the
APFS snapshots have UUIDs as their name property.

I’ve also stripped out David’s error handling, as I find that if there’s
an error ejecting the disk it’s usually communicated by the Finder
itself rather than via an error code visible to AppleScript.

This doesn’t tackle the problem of the Finder refusing to eject a drive
containing opened files, even if those files are opened by (from the
user’s perspective) unimportant background commands. I spent a chunk of
the morning mulling this over (and looking at `lsof`’s inscrutable man
page!), and think I might try to run the output of `lsof -F` through AWK
to enable a prompt-to-terminate interface. This is particularly
important for me as I keep my music and photo libraries on an external
drive; the photo library in particular is often opened by background
system tasks, I think as iCloud syncs across new photos from my phone.
