---
title: "A scripting mess"
date: 2015-07-05 16:52
tags: ["AppleScript"]
---

I was thinking about redoing the [page generator script][] for work again this morning, wondering if the newly widespread support for JavaScript in Cocoa applications and JavaScript for Automation would simplify some of the work I started on a Cocoa page-generating application.

[page generator script]: https://github.com/robjwells/feral-four/blob/Illadelph/core.applescript

The short answer is No. In fact I’m more disheartened at the state of inter-application scripting now than I was a year ago.

I began working on the application in January 2014, but hadn’t touched the project since last June. I got a bit bogged down with it, and it was by far too big a project to start with; I’d just finished the Big Nerd Ranch [Objective-C][bnr_objc] and [Cocoa][bnr_cocoa] books and while they were very good, and I learnt loads, I should’ve made some toy applications by myself before tackling it.

[bnr_objc]: https://www.bignerdranch.com/we-write/objective-c-programming/
[bnr_cocoa]: https://www.bignerdranch.com/we-write/cocoa-programming/

In short, it would have been a GUI application that created both preset and custom batches of InDesign documents and changed certain elements on those pages (dates, page numbers), with the user having the ability to change those presets.

One of the biggest hurdles was working with AppleScript from Cocoa. I had to [define a category on NSAppleScript][category] to make bearable calling AppleScript handlers (from a compiled `.scpt` file used as a library). And this was my first attempt at a Cocoa programme without the help of the BNR books! It was a mess (that category is a mess, but it does work) and I got discouraged.

[category]: https://gist.github.com/robjwells/9d1480e4b7a1a8312eca

But when I come back to it, that will be the way I’ll do it, because the other options are so poor.

A “native” Cocoa option is Scripting Bridge. It [hasn’t been updated since 10.6][sb_release_notes], but so what? If it works, it works. It doesn’t work. The generated header for InDesign is 10MB and Xcode hangs when you try to open it. The thousands of enums, typedefs, interfaces, methods and properties even bring BBEdit to its knees when you try to use the function menu or “Named Symbol…” browser.

[sb_release_notes]: https://developer.apple.com/library/mac/releasenotes/ScriptingAutomation/RN-ScriptingBridge/

Well, OK, let’s settle for not being able to properly browse the header, and just include it and poke around. Nope! Xcode won’t compile with it included (because of about 20 errors, mostly “duplicate” definitions that come from flattening InDesign’s enormous scripting dictionary).

Now let’s look at the two JavaScript options: InDesign’s built-in JavaScript interpreter and JavaScript for Automation, introduced at last year’s WWDC. Both Adobe’s ExtendScript Toolkit and Script Editor don’t provide the kind of support you need to navigate the complex object model. We also have the problem of trying to pass arguments to the built-in JavaScript interpreter from Cocoa.

JavaScript for Automation meanwhile has poor documentation. It’s not clear to me how to achieve the same results I do in AppleScript with JavaScript. (What’s `.get()` all about?) There’s no interface to call such scripts from Cocoa. And the [preliminary change notes for OS X 10.11][jxa_1011] don’t contain any significant changes.

[jxa_1011]: https://developer.apple.com/library/prerelease/mac/releasenotes/InterapplicationCommunication/RN-JavaScriptForAutomation/Articles/OSX10-11.html

What a mess. Automation is crucial for our work, and solves so many of our problems. But the existing technologies have so many sharp edges and the “new” one, JavaScript for Automation, is not anything close to the fresh start that might reinvigorate things.

This year’s WWDC talk on automation was [Supporting the Enterprise with OS X Automation][wwdc_2015]. At the start, Sal Soghoian — Mr Automation at Apple — says:

> Some days I feel like I’m a dinosaur looking for a tar pit

[wwdc_2015]: https://developer.apple.com/videos/wwdc/2015/?id=306

It’s not looking good.
