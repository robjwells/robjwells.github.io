title: Gating Hazel with git status
date: 2013-06-25 00:52
tags: Git, Hazel, Shell

The JavaScript and CSS files for this site live on Amazon S3, but getting them up there can be a chore once you consider compression and uploading with the right headers.

That wasn’t too difficult to sort out with AppleScript and Transmit but I wanted to avoid having to start the script manually as well.

[Hazel][], the housekeeper for your Mac, can keep watch and is ideal for this — except when you’re still working on the file. It’s going to get under your feet if you tell it to run its rules once the modification date is after the last match.

[Hazel]: http://www.noodlesoft.com/hazel.php

If the files are under version control the commit status is an ideal way to signal whether or not a file is ready to go. Combine that with Hazel’s ability to use a shell script in its conditions and you end up with something like this:

    bash:
    cd ~/Sites/robjwells
    GITSTATUS=$(git status | head -n 2 | tail -n 1 | grep -o "^nothing")
    if [ "$GITSTATUS" == "nothing" ]; then
        exit 0
    else
        exit 1
    fi

(This is my first time writing about a purely shell script, so please be gentle.)

First it moves into the directory in question, which is a git repo.
Next it calls `git status`, extracts the second line of the output (`head` and `tail`) and checks if it starts with “nothing”. That’s because the status command returns this on a clean repo:

    # On branch master
    nothing to commit, working directory clean

If `grep` finds “nothing” it gets stuck in `$GITSTATUS`, which is compared to the string you would expect from a clean repo. If it matches the script exits with a success status code, which tells Hazel that the file has passed the check.

(The -o flag makes `grep` only return the match, instead of the whole line.)

Initially I did this check in the AppleScript that was applied to the file once it passed date and extension checks. But this meant that Hazel considered it to have matched successfully and would not run the rules on the file until it triggered the date conditions again. The lesson here is that checks must be separate from actions. Thankfully Hazel makes it easy to do that.

If you work with repositories which are rarely “all clear” as in this case, you could improve this snippet by [checking the status tool’s list of uncommitted modified files for the name of the file][update] (provided by Hazel as `$1`).

[update]: http://robjwells.com/post/53871219250
