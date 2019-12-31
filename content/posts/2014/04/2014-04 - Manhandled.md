---
title: Manhandled
date: 2014-04-13 09:03
tags: Shell
---

[Dr Drang][] and [Nathan][] have both written recently about bringing up a man page for reference while typing a command in the terminal. I’ve two approaches to share, but unlike Nathan I can’t claim that they’re superior — just alternatives.

[Dr Drang]: http://www.leancrew.com/all-this/2014/04/oh-man/
[Nathan]: http://nathangrigg.net/2014/04/zsh-push-line-or-edit/

I prefer them over the right-click method because I don’t like to take my hands off the keyboard unless absolutely necessary, and moving to Zsh is a bit much for me right now.

First is [LaunchBar’s][lb] built-in man page search (found under UTF-8 search templates in the index), which uses the `x-man-page://` URL scheme to bring up a new Terminal window. Here’s what you type:

[lb]: http://www.obdev.at/products/launchbar/index.html

    ⌘-Space man Space `command` ↩

The second approach layers the wonderful [Dash][] on top of LaunchBar, bringing up the man page in Dash’s interface instead of the Terminal.

[Dash]: http://kapeli.com/dash

    ⌘-Space dash Space `command` ↩

This gives you all the usual Dash goodies, including a section list and inline links to other man pages (if you decide, after all, to take your hands off the keyboard).

You can prepend `man:` to the command name to restrict the search to man pages only, or even add a search template of the form `dash://man:*` to LaunchBar’s index — in place of the first man page search if you like.
