---
title: Start and end of line shortcuts in BBEdit
date: 2014-12-18 00:34
tags: ["AppleScript", "BBEdit"]
---

I keep BBEdit's option to emulate Emacs key bindings disabled, because I don't know most of them and some of those combinations I want to use for other things.

However, I've been doing more work on the command line recently, and not having ⌃A and ⌃E to move to the start and end of the current line was starting to grate. The cursor keys are just too far away!

So I whipped up some scripts to give me back those shortcuts while keeping the rest of the Emacs stuff disabled.

### Start of line

    applescript:
    set line_start to the characterOffset of line (startLine of the selection)
    select insertion point before character line_start

### End of line

    applescript:
    set current_line to line (startLine of the selection)
    set end_of_line to ((characterOffset of current_line) + (length of current_line))
    select insertion point before character end_of_line

Wrap both of those in:

    applescript:
    tell application "BBEdit"
        tell the front text window
            …
        end
    end

(omitted above to reduce the amount of scrolling), dump them in ~/Library/Application Support/BBEdit/Scripts/, assign them the ⌃A and ⌃E shortcuts in BBEdit's preferences, and you're all set.
