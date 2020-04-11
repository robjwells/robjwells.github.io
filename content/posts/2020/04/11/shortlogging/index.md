---
title: "Shortlogging"
date: 2020-04-11T10:47:05+01:00
---

Back in 2018, I was trying to think of a way where I could record work or personal activities, and what I came up with was to create a daily log file for my life, like you might have from a program with `logger.setLevel(INFO)`.

I set up a [Drafts][] action on my phone, and stuck with it for a couple of months. But there was always a certain amount of friction, more so after I changed jobs to one where I use a fairly locked-down Windows PC for most of the day.

In 2018 I stuck with it for a few months. Now, with the current coronavirus lockdown in Britain, I’m working from home and thought it might be a good idea to revive it. But I had to resolve the problem that caused me to stop in the first place: friction.

I use [Beeminder][] and knew they had something along these lines, called [TagTime][]. But it’s not quite what I was after — it’s more of a time-tracking approach, for which I use [RescueTime][].

RescueTime itself has a [highlights feature][highlights], which is philosophically what I want — record the meaningful things that you did to complement time-tracking — but recording the highlights has the same problem. I actually came to resent RescueTime a bit as I had an alert set (I think it’s one of the suggested ones) that prompts you to enter highlights after a certain amount of “productive” time. The problem was, this alert would activate my web browser and open a new tab on the highlights page, typically while I was in the middle of working on something!

Brett Terpstra has a tool called [doing][], which now that I look at it behaves how I want (recording activities as complete) but it’s very featureful and a bit much for me.

So, obviously, I decided to roll my own.

The core of my setup is a folder which I keep at `~/Dropbox/notes/shortlog/`, in which reside files like `shortlog-2020-04-09.txt`. The contents of these files looks like this:

```
2020-04-09 09:46:36 | Read Kirk Baker’s SVD notes (…)
2020-04-09 10:00:15 | Set up Python environment for NLP coursework 2 (…)
2020-04-09 11:30:07 | Had CND Team Meeting
```

I created a [Keyboard Maestro][] macro to make logging easy ([click to download][macro]):

{{% figure src="shortlog-prompt-kmmacro.png" alt="A screenshot showing the Keyboard Maestro macro I use to enter shortlog entries." link="shortlog-prompt.kmmacros" class="full-width" %}}

When you invoke the macro, you get a pop-up dialog like this:

{{% figure src="shortlog-prompt.png" alt="A screenshot of the shortlog pop-up window prompting for an entry, with a text entry field and buttons labelled “More”, “Cancel” and “Done”." %}}

“More” lets you log more than one entry. For convenience, if the entry field is empty and you choose “Done”, it exits without logging anything.

These entries get prepended with the date and then appended to a file named after the current date.

TagTime randomly polls you at an interval drawn from a Poisson distribution. I didn’t want to get into the weeds on that, so I took their average poll time (45 minutes) and set up another macro to invoke the shortlog entry macro that often during my normal waking hours. This can be a bit annoying if you’re focussed on a particular task, in a similar way to the RescueTime highlight prompt, so I found it useful to create a macro that toggles the automatic prompting (which I invoke through Keyboard Maestro’s find-by-name palette as it doesn’t need its own shortcut).

On my iPhone, I’ve kept the Drafts action ([which is available online][drafts-action]). It’s just a single Dropbox step, with the following attributes:

| Attribute          | Value                                      |
| ------------------ | ------------------------------------------ |
| *fileNameTemplate* | `shortlog-[[date\|%Y-%m-%d]].txt`          |
| *folderTemplate*   | `/notes/shortlog/`                         |
| *template*         | `[[date\|%Y-%m-%d %H:%M:%S]] \| [[draft]]` |
| *writeType*        | `append`                                   |

Drafts writes a newline before the content defined in *template*, which I can’t seem to disable. (Advice greatly appreciated.) I’ve got a simple `sed` command I run occasionally to remove the blank lines if it’s bugging me.

```zsh
sed -i '' -e '/^\s*$/d'
    "/Users/$USER/Dropbox/notes/shortlog/shortlog-$(date +%Y-%m-%d).txt"
```

Lastly, I also wanted these shortlog entries available as RescueTime highlights, as it allows you to review your tracked time with your manual “annotations” alongside. I wrote a fairly short Python script to do this ([repo][], [script itself][py]), which runs each morning and logs the previous days’s entries as highlights by POSTing them to the RescueTime API. It’s nuts-and-bolts so I won’t review the code here.

The one thing that I do want to note is that I have a job set up in [Lingon][] (a friendly interface to `launchd`) to do this each day, and that `launchd` will run jobs missed while asleep (though not those missed if the computer is powered off) at the next opportunity:

> Unlike `cron` which skips job invocations when the computer is asleep, `launchd` will start the job the next time the computer wakes up. If multiple intervals transpire before the computer is woken, those events will be coalesced into one event upon wake from sleep.
> (From `man launchd.plist`)

I don’t believe that you can achieve this with Keyboard Maestro, as the [wiki page for the time of day trigger][km-tod] contains this warning:

> Remember that the Mac must be awake for the trigger to happen, and if the Mac is sleeping the macro will not fire at a later time.

But I’d be very happy to be corrected if there’s a way to achieve the `launchd` behaviour through Keyboard Maestro.

[Drafts]: https://getdrafts.com/
[Beeminder]: https://www.beeminder.com
[TagTime]: https://github.com/tagtime/TagTime
[RescueTime]: https://www.rescuetime.com/
[highlights]: https://blog.rescuetime.com/highlights/
[doing]: https://github.com/ttscoff/doing
[macro]: shortlog-prompt.kmmacros
[Keyboard Maestro]: https://www.keyboardmaestro.com/main/
[shortlog-to-rescuetime]: https://github.com/robjwells/shortlog_to_rescuetime_highlights
[repo]: https://github.com/robjwells/shortlog_to_rescuetime_highlights
[py]: https://github.com/robjwells/shortlog_to_rescuetime_highlights/blob/master/shortlog_to_rescuetime.py
[Lingon]: https://www.peterborgapps.com/lingon/
[km-tod]: https://wiki.keyboardmaestro.com/trigger/Time_of_Day
[drafts-action]: https://actions.getdrafts.com/a/17R
