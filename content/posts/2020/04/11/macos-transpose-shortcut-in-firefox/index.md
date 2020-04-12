---
title: "macOS transpose shortcut in Firefox"
date: 2020-04-11T19:25:51+01:00
publishDate: 2020-04-18T06:00:00+01:00
---

macOS has a built-in shortcut to transpose characters, ⌃T, which is really handy. Sadly, Firefox doesn’t support it. This has been the case for at least the past seven years, as I remember telling a colleague at my previous job about useful macOS shortcuts, only for him to immediately try and find it “didn’t work.”

Firefox is my main browser at the moment (because of [the changes to content-blocking in Safari](https://github.com/el1t/uBlock-Safari/issues/158)), so this has become a bit of an irritation.

Here’s a Keyboard Maestro macro to poorly replicate ⌃T in Firefox:

{{% figure src="transpose-macro.png" alt="A screenshot of a Keyboard Maestro macro to transpose characters in Firefox on macOS." link="transpose-macro.kmmacros" width=473 height=471 %}}

“Poorly” because it’s slower than ⌃T usually is in supporting applications, and it makes no attempt to clean up your clipboard history.

If you’re interested, you’d probably want to implement some clipboard-repair, but I use LaunchBar’s clipboard history and I can’t find a way of using the [Delete Past Clipboard][dpc] action in a way that doesn’t put additional unwanted items into my clipboard history. Keyboard Maestro has its own clipboard history manager, so if you’re using that (or not using one at all) then you should be well served by Delete Past Clipboard.

[dpc]: https://wiki.keyboardmaestro.com/action/Delete_Past_Clipboard
