---
title: "Hazel gating with Mercurial"
date: 2013-07-31T23:16:00
tags: ["Hazel", "Mercurial", "Shell"]
---

Since I’ve been playing around with Mercurial I thought it would only be fair to write another version of [my Hazel gating snippet][gitgate].

[gitgate]: /2013/06/more-precise-git-status-gating/

The basic mechanism is the same (parsing the status output) and the code is barely changed:

```bash
#!/bin/bash

cd $(dirname $1)
FILENAME=$(basename $1)
HGSTATUS=$(hg status -c "$FILENAME")
if [ "$HGSTATUS" == "" ]; then
  exit 1 # Dirty
else
  exit 0 # Clean
fi
```

An important difference to note is that this script checks that the file is clean (through the `-c` flag on line 5), not that the file is *not dirty* as the Git version does. This requires the conditional to be reversed as an empty string means that the file has been modified in some way.

As I mentioned previously in my post about [branch comparison][hgb], I’ve spent some time recently to learn more about Git and Mercurial. This was both to improve my pretty basic Git skills and see why [Daniel Jalkut][] keeps [banging on about Mercurial][podcast] (go to the 28-minute mark).

[hgb]: /2013/07/easy-branch-comparison-with-mercurial/
[Daniel Jalkut]: http://www.red-sweater.com
[podcast]: https://learn.thoughtbot.com/giantrobots/32

When I learnt about hooks ([Mercurial][hghook], [Git][githook]) I was a little worried they would invalidate the time I’d spent writing the status gating snippet. But while hooks are very handy and powerful, there’s plenty off actions that [Hazel][] is more suited to or more convenient for — this just acts as a nice safety check so it doesn’t step on your toes while you’re working.

[githook]: http://git-scm.com/book/en/Customizing-Git-Git-Hooks
[hghook]: http://mercurial.selenic.com/wiki/Hook
[Hazel]: http://www.noodlesoft.com
