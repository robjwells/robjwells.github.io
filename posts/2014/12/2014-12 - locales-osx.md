title: Locale in OS X and Launch Agents
date: 2014-12-20 15:46
tags: OS X


I really dislike [last year’s post about ASCII and UTF-8][rjw-ascii]. It’s one of those posts that, when you look back, reveals how little you know about a topic. The stuff in there isn’t all wrong but as a whole it’s not correct.

[rjw-ascii]: /2013/09/get-your-us-ascii-out-of-my-face/

Towards the end I say that the way to make sure that the locale isn’t `C` is to export `LANG` in a bunch of profile/rc files. But that doesn’t work if those files aren’t sourced — quite common when scripts get run on your behalf.

At some point I got bitten again and fixed it using [launchd][]. By modifying the /etc/launchd.conf configuration file (as suggested [here][conf_1] and [here][conf_2]), you could make launchd set environment variables at startup:

    bash:
    # /etc/launchd.conf
    setenv LANG en_GB.UTF-8

[launchd]: http://en.wikipedia.org/wiki/Launchd
[conf_1]: http://www.digitaledgesw.com/node/31
[conf_2]: http://stackoverflow.com/questions/135688/setting-environment-variables-in-os-x/

Dead simple, and ensures that `LANG` is always correct. But unfortunately useless in Yosemite. From the launchctl man page:

> The /etc/launchd.conf file is no longer consulted for subcommands to run during early boot time; this functionality was removed for security considerations.

(I should note that I don’t have a clean install of Yosemite, so maybe Apple has fixed the default locale to something `*.UTF-8` and my carried-over files have got in the way. But I don’t think so: the guest account defaults to the `C` locale.)

There’s a [thread on Stack Overflow][so-yosemite] containing some discussion about how to handle the change. It’s a bit of a muddle, but the common theme is to use a real launchd job to set environment variables on startup.

[so-yosemite]: http://stackoverflow.com/questions/25385934/setting-environment-variables-via-launchd-conf-no-longer-works-in-os-x-yosemite

Launchd agents are registered using .plist files (XML), which are a pain to work with by hand, so I recommend [Lingon][] (nicer to use) or [LaunchControl][] (exposes more settings). The most basic setup is to call launchctl directly:

![Lingon set to run launchctl at startup with the arguments 'setenv LANG en_GB.UTF-8'](/images/2014-12-19_locales-lingon-basic.png)

[Lingon]: https://www.peterborgapps.com/lingon/
[LaunchControl]: http://www.soma-zone.com/LaunchControl/

That’ll save a .plist file in ~/Library/LaunchAgents/ — a job that gets run by launchd when you log in (for your user only). And we’re done!

Setting the locale in this way means that it will be set correctly for any process that follows (even something like `do shell script` in AppleScript).

## But wait

Since we’re mucking around with Launch Agents and using launchctl at boot, we can set up the environment however we like. Rather than use launchctl directly, I run my own script that does several things:

    bash:
     1:  # Launch Agent to set environment variables on boot
     2:  
     3:  set -e
     4:  
     5:  date=$(date +"%Y-%m-%d %H:%M:%S")
     6:  echo -e "$date\tSetting environment variables with $0"
     7:  
     8:  # Locale
     9:  launchctl setenv LANG en_GB.UTF-8
    10:  launchctl setenv LC_ALL en_GB.UTF-8
    11:  
    12:  # Python
    13:  launchctl setenv PYTHONPATH "/Users/robjwells/Dropbox/bin"
    14:  
    15:  # Path
    16:  if [ -x /usr/libexec/path_helper ]; then
    17:    export PATH=""
    18:    eval $(/usr/libexec/path_helper -s)
    19:    launchctl setenv PATH $PATH
    20:  fi

It’s largely straightforward: setting the locale correctly, then `PYTHONPATH` (searched for Python modules), then something more involved for the `PATH`.

By default, OS X sets `PATH` to something that’s pretty sparse:

    /usr/bin:/bin:/usr/sbin:/sbin

(You can check this with `do shell script "echo $PATH"` in AppleScript.)

That can make some things pretty difficult, particularly if you want to use scripts you’ve written through some kind of intermediary that doesn’t source your setup files.

[path_helper][] constructs a path from the contents of /etc/paths and files in /etc/paths.d — giving you a much more expansive path than by default (and one you can add to by placing a file of your own in the latter directory). And again, by setting this at boot through launchctl it’s available widely afterwards.

[path_helper]: https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/path_helper.8.html

Not everywhere, though. For instance, [TextExpander][] [ensures UTF-8 support][te-help] by setting `LANG`, but `PATH` is still restricted to the short one listed above. I get the feeling TextExpander is doing more than just inheriting the environment and tweaking `LANG`.

[TextExpander]: http://smilesoftware.com/TextExpander/index.html
[te-help]: http://www.smilesoftware.com/help/TextExpander/applescript.html

## ‘Legacy subcommands’

The language in the launchctl man page refers to “the previous implementation of launchd” and Yosemite brings with it a new (painful) interface, with the previous interface listed under the heading “legacy subcommands”. Some of the commands listed there don’t have equivalents in the new interface — including the vital `setenv`.

I don’t know whether to be worried by the “legacy” description. If these commands go away without similar ones being introduced we could be left without a way to set vital environment variables (fixing Apple’s oversights). But it sounds that launchd has undergone major surgery, so reimplementing the previous interface does suggest some kind of commitment to it, at least in the interim.
