---
title: "More precise git status gating"
date: 2013-06-25 22:18
tags: ["Hazel", "Git", "Shell"]
---

At the end of my post about having [Hazel][] [check a file’s commit status][post] before running rules on it, I suggested that the script could be made better by not requiring the entire repository be committed and clean:

> If you work with repositories which are rarely
> “all clear” as in this case, you could improve
> this snippet by checking the status tool’s list
> of uncommitted modified files for the name of
> the file (provided by Hazel as `$1`).

[Hazel]: http://www.noodlesoft.com
[post]: /2013/06/gating-hazel-with-git-status/

It has been on my mind all day, so I decided to have a crack at it:

    bash:
    1:  cd $(dirname $1)
    2:  FILENAME=$(basename $1)
    3:  GITSTATUS=$(git status -s "$FILENAME")
    4:  if [ "$GITSTATUS" == "" ]; then
    5:    exit 0 # Clean
    6:  else
    7:    exit 1 # Dirty
    8:  fi

<div class="flag">
    <strong>Update 2013-06-27</strong>
    <p>I’ve slightly revised the code and have rewritten the explanation to be clearer.</p>
    <strong>Update 2013-07-31</strong>
    <p>I’ve tweaked the script to make it simpler and more reliable, with the explanation below rewritten again. There is now also <a href="/2013/07/hazel-gating-with-mercurial/">a version for Mercurial users</a>.</p>
</div>

The script is largely the same [as in my original post][post], but with a few tweaks and a different method of action.

In line 1 the directory is not hard-coded as it was before, instead using the built-in `dirname` command to extract it from the path Hazel hands off as `$1`.

Next the script grabs the filename from `$1` and provides it to the short form of `git status`, which returns a single line of output if the file is modified in any way. By moving into the file’s directory on the first line we can reliably avoid modified identically-named files in subfolders causing false negatives.

Older versions of the script parsed the long `git status` output with a regular expression, which wasn’t ideal: a false negative could result if a file had the same name as a branch or the last word on a line of boilerplate output.

Lastly the script checks if `git status` returned anything. An empty string counts as success since it would only contain characters if the file was dirty.

The two exit lines tell Hazel whether the file passed the script’s check (`exit 0`) or failed (`exit 1`).
