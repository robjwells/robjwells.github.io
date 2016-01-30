#!/usr/bin/env python

from datetime import datetime

details = [
  [
    "Thursday, 4 December 2014 at 00:01:37",
    "Solving boredom with four languages",
    "Shell,AppleScript,JavaScript,Python"
  ],
  [
    "Thursday, 18 December 2014 at 00:34:31",
    "Start and end of line shortcuts in BBEdit",
    "applescript,bbedit"
  ],
  [
    "Saturday, 20 December 2014 at 15:46:49",
    "Locale in OS X and Launch Agents",
    "OSX"
  ],
  [
    "Monday, 22 December 2014 at 10:16:17",
    "Locale in OS X \u2014 what\u2019s the current situation?",
    "OSX"
  ],
  [
    "Saturday, 17 January 2015 at 18:56:53",
    "Updated date suffix script",
    "Python,Programming"
  ],
  [
    "Saturday, 17 January 2015 at 22:13:38",
    "Interruptions",
    "work"
  ],
  [
    "Wednesday, 21 January 2015 at 21:03:12",
    "Audio Hijack 3 and scripts",
    "Audio Hijack Pro,Audio Hijack 3"
  ],
  [
    "Wednesday, 25 February 2015 at 12:35:56",
    "My email nightmare",
    "email"
  ],
  [
    "Friday, 26 June 2015 at 12:05:12",
    "AppleScript list gotchas",
    "applescript"
  ],
  [
    "Tuesday, 30 June 2015 at 12:21:12",
    "You should be using docopt",
    "Python,Programming"
  ],
  [
    "Thursday, 2 July 2015 at 13:19:16",
    "The automation paradox at work",
    "work"
  ],
  [
    "Sunday, 5 July 2015 at 16:52:41",
    "A scripting mess",
    "AppleScript"
  ],
  [
    "Wednesday, 15 July 2015 at 23:40:37",
    "Historical dollars",
    "Python,Programming"
  ],
  [
    "Tuesday, 4 August 2015 at 10:04:44",
    "Corbyn",
    "politics"
  ],
  [
    "Wednesday, 5 August 2015 at 20:04:20",
    "Yeah!",
    "music,JavaScript"
  ],
  [
    "Friday, 7 August 2015 at 13:49:34",
    "Python Counter gotcha with max",
    "Python"
  ],
  [
    "Monday, 10 August 2015 at 22:34:21",
    "Python\u2019s Counter class, again",
    "Python"
  ],
  [
    "Monday, 21 September 2015 at 20:42:49",
    "Cameron & Ashcroft",
    "politics"
  ],
  [
    "Tuesday, 6 October 2015 at 02:33:35",
    "Re: Unresponsive",
    "Web"
  ],
  [
    "Sunday, 15 January 2012 at 16:22:00",
    "Netflix Roulette",
    "Web"
  ],
  [
    "Wednesday, 1 February 2012 at 15:18:00",
    "Endnotes: The Call of the Weird",
    "Books"
  ],
  [
    "Tuesday, 17 July 2012 at 09:00:00",
    "Restarting in Bootcamp the easy way",
    "AppleScript"
  ],
  [
    "Friday, 7 September 2012 at 14:25:45",
    "Update: Restart in Windows",
    "AppleScript"
  ],
  [
    "Sunday, 9 September 2012 at 02:00:31",
    "I\u2019m on GitHub",
    "Personal"
  ],
  [
    "Tuesday, 18 September 2012 at 18:23:14",
    "Everyday automation",
    "AppleScript"
  ],
  [
    "Friday, 5 October 2012 at 00:00:00",
    "What\u2019s in the box!?",
    "AppleScript"
  ],
  [
    "Saturday, 6 October 2012 at 18:14:11",
    "Restart in Windows: Revenge of the Script",
    "AppleScript"
  ],
  [
    "Sunday, 14 October 2012 at 16:20:00",
    "Dishonored by the numbers",
    "Games"
  ],
  [
    "Monday, 25 February 2013 at 14:58:18",
    "Blackjack!",
    "Web"
  ],
  [
    "Wednesday, 6 March 2013 at 10:45:41",
    "Setting a date with TextExpander",
    "AppleScript,TextExpander"
  ],
  [
    "Saturday, 25 May 2013 at 17:47:00",
    "Restart in Windows: The script strikes back",
    "AppleScript"
  ],
  [
    "Monday, 24 June 2013 at 17:36:28",
    "A new look and name",
    "Personal"
  ],
  [
    "Tuesday, 25 June 2013 at 00:52:45",
    "Gating Hazel with git status",
    "Hazel,Shell,Git"
  ],
  [
    "Tuesday, 25 June 2013 at 22:18:03",
    "More precise git status gating",
    "Hazel,Shell,Git"
  ],
  [
    "Saturday, 29 June 2013 at 12:05:45",
    "First brush with modulo speed",
    "Programming"
  ],
  [
    "Saturday, 6 July 2013 at 18:54:56",
    "Five different kinds of grey",
    "Personal,Web"
  ],
  [
    "Tuesday, 23 July 2013 at 22:28:06",
    "Sunny with a chance of Python",
    "Programming,Python"
  ],
  [
    "Saturday, 27 July 2013 at 20:33:39",
    "Easy branch comparison with Mercurial",
    "Git,Mercurial"
  ],
  [
    "Wednesday, 31 July 2013 at 23:16:53",
    "Hazel gating with Mercurial",
    "Mercurial,Hazel,Shell"
  ],
  [
    "Saturday, 3 August 2013 at 13:31:52",
    "Commit summary length hooks",
    "Mercurial,Git,Python"
  ],
  [
    "Saturday, 17 August 2013 at 14:36:37",
    "Terminal countdown",
    "Python,Shell,Programming"
  ],
  [
    "Saturday, 24 August 2013 at 13:04:40",
    "Promptless Mercurial",
    "Mercurial"
  ],
  [
    "Friday, 13 September 2013 at 20:39:50",
    "Solo diff",
    "Python,Programming,Copy editing,BBEdit"
  ],
  [
    "Saturday, 14 September 2013 at 14:05:42",
    "Get your US-ASCII out of my face",
    "OSX,Shell,Programming,Python"
  ],
  [
    "Tuesday, 17 September 2013 at 23:16:23",
    "Quit to Linux",
    "Games"
  ],
  [
    "Monday, 7 October 2013 at 22:51:22",
    "Date suffixes in Python",
    "AppleScript,Programming,Python,TextExpander"
  ],
  [
    "Monday, 18 November 2013 at 13:15:04",
    "Die, bookmarks bar, die",
    "AppleScript,Launchbar"
  ],
  [
    "Wednesday, 8 January 2014 at 15:56:59",
    "Hijacking the BBC",
    "Audio Hijack Pro,Programming,Python"
  ],
  [
    "Saturday, 11 January 2014 at 16:08:55",
    "Next and last weekdays",
    "Python,Programming,TextExpander"
  ],
  [
    "Thursday, 16 January 2014 at 12:25:25",
    "My one iOS 7 problem",
    "iOS"
  ],
  [
    "Wednesday, 22 January 2014 at 13:32:38",
    "Scraping Entourage",
    "Programming,Python,AppleScript"
  ],
  [
    "Sunday, 26 January 2014 at 19:24:53",
    "Misbehaving single-column NSTableView",
    "Programming,Cocoa,Xcode"
  ],
  [
    "Sunday, 13 April 2014 at 09:03:24",
    "Manhandled",
    "Shell"
  ],
  [
    "Sunday, 13 April 2014 at 09:37:39",
    "Broken Mercurial dummy cacerts",
    "Mercurial"
  ],
  [
    "Monday, 14 April 2014 at 23:09:30",
    "Mano-al-teclado",
    "Shell"
  ]
]

details = [[datetime.strptime(d, '%A, %d %B %Y at %H:%M:%S'),
           ti, ', '.join(ts.split(','))] for d, ti, ts in details]
details.sort(key=lambda l: l[0])

for sub_list in details:
    sub_list[0] = sub_list[0].strftime('%Y-%m-%d %H:%M')
    print('\n'.join(sub_list) + '\n\n')
