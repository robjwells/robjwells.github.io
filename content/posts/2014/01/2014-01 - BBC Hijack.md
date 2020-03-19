---
title: "Hijacking the BBC"
date: 2014-01-08T15:56:00
tags: ["Audio Hijack Pro", "Programming", "Python"]
---

In December I started using [Audio Hijack Pro][ahp] to record [Jazz on 3][j3], initially from the [Radio 3 live stream][3live]. I soon realised this wasn’t a great idea: live streaming, Flash and an occasionally patchy internet connection don’t make for reliable recording.

[ahp]: http://rogueamoeba.com/audiohijackpro/
[j3]: http://www.bbc.co.uk/programmes/b006tt0y
[3live]: http://www.bbc.co.uk/radio/player/bbc_radio_three

A bit of searching turned up [a blog post][drang] and [GitHub repository][drang-gh] by Dr Drang — who else! His approach was to record programmes from the BBC website after they’ve been broadcast. This is more reliable, allows for repeated tries if the recording fails for any reason, and makes it easier to handle longer-than-usual episodes.

[drang]: http://www.leancrew.com/all-this/2009/07/bbc-radio-2-and-audio-hijack-pro-scripts/
[drang-gh]: https://github.com/drdrang/radio2

The logic is straightforward: find the unique ID for the programme’s most recent episode, use that to construct the player URL, and feed that to Audio Hijack.

Most of the work is done in Python, with Audio Hijack running bridging AppleScripts when a recording starts and finishes — the latter used by Dr Drang to add a track list to the recording’s lyrics field and add the file to iTunes.

This sounded ideal, but I couldn’t use the Doc’s work straight away as the scripts focus on Radio 2, use a player URL that doesn’t work (at least at home in Blighty) and need a few tweaks to fit my Python environment. It gave me an excuse to tinker with the wheel, if not [reinvent it][drang-wheel].

[drang-wheel]: http://www.leancrew.com/all-this/2014/01/reinventing-the-wheel/

If you want to follow along at home, all the code is [in a Bitbucket repository][rjw-bb].

[rjw-bb]: https://bitbucket.org/robjwells/beeb-hijack/src/

Before we dig in, there are two practical things to note:

*   It’s all written for Python 3, but it wouldn’t take much to work on 2.
*   You’ll need to install [Beautiful Soup 4][bs4] and [docopt][].
    (Use [pip][].)

I initially wanted to consolidate the Python scripts into one file but that turned out to be stupid, so I (eventually) settled on having a module similar to Dr Drang’s that did most of the work and another script that acted as the command-line interface.

(That partly explains why [my repo][rjw-bb] has fewer files — the other being that I add the artwork in Audio Hijack’s tags tab, not a script.)

[bs4]: http://www.crummy.com/software/BeautifulSoup/
[docopt]: http://docopt.org
[pip]: http://www.pip-installer.org/en/latest/

### Python module: bbcradio

A look at the programme info dictionaries at the top of our modules reveals the differences in our methods:

```python
# Dr Drang’s
showinfo = {'70s': (6, re.compile(r"Sounds of the '?70s")),
            '60s': (5, re.compile(r"Sounds of the '?60s")),
            'soul':(2, re.compile(r"Trevor Nelson")),
            'at':  (3, re.compile(r"At the BBC"))}
# Mine:
PROG_DICT = {'jazz on 3': 'b006tt0y',
             'jazz line-up': 'b006tnmw'}
```

Each entry in the Doc’s dictionary is a tuple of the weekday as an integer — used to construct a URL for a daily schedule — and a regular expression to pick out the programme from the scraped schedule.

In mine I go after the programmes directly, as they all have a unique ID similar to the ones given to individual episodes. With this ID we can go to [a list of the programme’s available episodes][j3-avail] and pluck out the most recent one.

[j3-avail]: http://www.bbc.co.uk/programmes/b006tt0y/episodes/player

This has two benefits: we don’t need to care about the broadcast day and don’t have to search the schedule page. All you need is the programme ID, which you can grab from the end of [a programme’s home page][j3] URL.

All the work is done in `latest_episode_code` in lines [17–29][epfunc], which fetches the available episodes page and pulls the episode code for the first episode listed.

[epfunc]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/bbcradio.py?at=default#cl-17

For weekly programmes only one episode is listed, but this technique also works for programmes which are broadcast more often — like [Today][], which Dr Drang has [addressed specifically][drang-daily]. In such cases just make sure to record an episode while it’s the most recent on the available episodes page.

[Today]: http://www.bbc.co.uk/programmes/b006qj9z
[drang-daily]: http://www.leancrew.com/all-this/2009/10/adapting-bbc-radio-recording-scripts/

I’ve kept Dr Drang’s [episodeInfo][epinfo-drang] function — used to fetch the episode title, date and track list — [largely intact][epinfo-rjw]. I’ve added the time a track was played (if available — it’s often not) and I use a simpler method to fetch the broadcast date (pulling an [RFC 3339 date][rfc3339] from an attribute).

[epinfo-drang]: https://github.com/drdrang/radio2/blob/master/radio2.py#L37
[epinfo-rjw]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/bbcradio.py?at=default#cl-38
[rfc3339]: http://tools.ietf.org/html/rfc3339#section-5.8

But there is one important difference: the use of Beautiful Soup’s `select` function, which allows for a liberal search for multiple class names, instead of `find_all`, which only returns elements which *exactly* match a given class string. This is important because every other track listing has an `alt` class.

### Command-line interface: beebhijack

By itself bbcradio is inert, with the moving parts contained in [a single interface script][bb-beebhijack] that has two modes which return an episode’s streaming URL or its details and track list. (Originally these were separate scripts, but there was a lot of duplicate code.)

[bb-beebhijack]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/beebhijack?at=default

At the command line you just pick a mode and supply a programme name. Here’s the help message:

```
$ beebhijack -h
Usage:
    beebhijack url <programme>
    beebhijack details [--clean] <programme>

Options:
    --clean     Use two newlines instead of a pipe
                to separate the episode details

Accepted programmes:
    jazz on 3
    jazz line-up
```

And, because I’m still blown away how simple [docopt][] is, here’s all the code needed to produce that interface:

```python {linenos=true, linenostart=7}
programmes = '''\
Accepted programmes:
    {}'''.format('\n    '.join(bbcradio.PROG_DICT.keys()))

usage = '''\
Usage:
    {name} url <programme>
    {name} details [--clean] <programme>

Options:
    --clean     Use two newlines instead of a pipe
                to separate the episode details

{prog_list}'''.format(name='beebhijack', prog_list=programmes)

args = docopt(usage)
```

If you haven’t used it before, take 20 minutes to watch the [docopt video][docopt]. It’s wonderful: give it a usage message and it hands you back a dictionary. Mine above is a little complicated because it tacks the list of accepted programmes onto the end of the usage message, in case you need a reminder at the command line. (I also print the list if you ask for a programme that’s not in the dictionary, in lines [24–27][wrongprog]).

[wrongprog]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/beebhijack#cl-24

In the dictionary docopt returns, commands (url, details) get a boolean value, so the mode switch is a simple if-else if.

Unless given the `--clean` argument, the details mode prints the three parts of the tuple it gets from `episode_details` separated by pipes, which you can split up in AppleScript by changing the text item delimiters.

It’s important to note that I don’t exactly `print` the details — instead I encode the string into UTF-8 and [write it as bytes][wb] to `sys.stdout.buffer`. ([Dr Drang’s script does something similar][drang-tracklist].) The shell invoked by AppleScript’s `do shell script` command defaults to [`US-ASCII`][ascii], causing a UnicodeEncodeError if you try to `print` a string containing non-Ascii characters.

[wb]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/beebhijack#cl-38
[drang-tracklist]: https://github.com/drdrang/radio2/blob/master/radio2-tracklist#L44
[ascii]: /2013/09/get-your-us-ascii-out-of-my-face/

Generally, I think the key distinction between beebhijack and Dr Drang’s four scripts is that I keep all of the “real work” in the module.

For example, we both fetch the episode ID in our modules, but I also construct the streaming URL there (lines [32–35][epurl-func]) while the Doc does that in [a separate script][drang-stream].

[epurl-func]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/bbcradio.py#cl-32
[drang-stream]: https://github.com/drdrang/radio2/blob/master/radio2-stream

This isn’t a big deal either way but I think it reveals my thinking about the beebhijack script: it’s a bridge between what you want to achieve and the program that actually does the work. The heaviest lifting done by beebhijack (joining the details) controls how the information is output, not what the information is.

### Putting it all together

With the Python code sorted, all that’s left to do is to create individual pre- and post-recording AppleScripts that you get Audio Hijack to run (on the input and recording tabs, respectively).

The [pre-recording script][rjw-pre] just calls beebhijack’s url mode and pass a programme name. I’ve copied Dr Drang’s, but separated out the programme name and path to the script into properties to make them easier to spot and change.

[rjw-pre]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/Jazz%20Line-Up%20URL.applescript

The same applies to [the post-recording script][rjw-post], which I stole off the Doc, who adapted one by Rogue Amoeba.

[rjw-post]: https://bitbucket.org/robjwells/beeb-hijack/src/06686071d912f817b898b3c21bb88f3dc2d30ae6/Process%20Jazz%20Line-Up.applescript

The biggest change I made was to use text-item delimiters to split up the episode date, title and track list as I don’t just put them all into the lyrics field, instead using the title and date to rename the track. (The date is necessary because, although I have Audio Hijack name the files with the date, the recording takes place at least the day after the broadcast day.)

I also don’t use a try block to handle errors fetching the episode details, because I prefer have an error message in the morning to prompt me to sort out the recording by hand.

Once you’ve got the scripts in place, just set an appropriate schedule in Audio Hijack. I have it set to record for much longer than the usual episode length, just in case a longer episode airs that I don’t expect. This doesn’t inflate the file size, because Audio Hijack doesn’t add silence when nothing is output from your source.
