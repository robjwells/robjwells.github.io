---
title: The automation paradox at work
date: 2015-07-02 13:19
tags: ["Work"]
---

A couple of great recent episodes of [99% invisible][99pi] ([one][99pi_1], [two][99pi_2]) tackle the "automation paradox", where the increased use of automation leaves people unable to perform the task themselves.

[99pi]: http://99percentinvisible.org/
[99pi_1]: http://99percentinvisible.org/episode/children-of-the-magenta-automation-paradox-pt-1/
[99pi_2]: http://99percentinvisible.org/episode/johnnycab-automation-paradox-pt-2/

The [first episode][99pi_1] uses the [Air France Flight 447 crash][crash] as a hook to investigate the phenomenon:

> The automated system suddenly shut off, and the pilots were left surprised, confused and ultimately unable to fly their own plane.

[crash]: https://en.wikipedia.org/wiki/Air_France_Flight_447?wprov=sfti1

In a much less serious way, it got me thinking about the tools I've made for work. Nothing is so critical that its failure will dump the paper into the ocean but there are things that we rely on to get the paper out every day, including scripts to:

* [Make the InDesign page files][generators]
* [Set the weather forecast][weather]
* [Fix common problems in reporters' copy][cleaner]
* [Scrape football match listings and results][matches]
* [Format phone numbers][phone]
* [Export files ready for the printers and the web][pdf]
* Automatically upload a day's worth of PDFs to our archive contractor

[generators]: https://github.com/robjwells/feral-four
[weather]: https://bitbucket.org/robjwells/ms-python-weather/src/
[cleaner]: https://gist.github.com/robjwells/5032356
[matches]: https://bitbucket.org/robjwells/matchday/src
[phone]: https://gist.github.com/robjwells/d601a0aad80f487014d9
[pdf]: https://github.com/robjwells/ms-pdf-export

Most of this stuff could be done by hand. Most of it is pretty straightforward. The risk isn't really in the automation breaking, but in the automation breaking and having no-one to fix it.

We don't hire for the skills to do these things, and the complexity of our workflow has changed with the technical ability of individual staff members.

I don't know how best to cope with this. If, say, I get hit by a bus tomorrow, what do other people need to know? What things wouldn't even occur to them that they need to know about?

Should I draw up emergency guides, some kind of [Plan R][]? What about the code itself needs changing? (God help me, no-one else should be exposed to the horrible mess that is the [page generator script][generator-core].)

[Plan R]: https://upload.wikimedia.org/wikipedia/commons/f/fc/Dr._Strangelove_-_Wing_Attack_Plan_R.png
[generator-core]: https://github.com/robjwells/feral-four/blob/Illadelph/core.applescript
