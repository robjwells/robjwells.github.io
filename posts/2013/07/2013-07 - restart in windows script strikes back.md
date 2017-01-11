title: Restart in Windows: The script strikes back
date: 2013-05-25 17:47
tags: AppleScript

A quick and hopefully final update on my short AppleScript to restart from Mac OS X into your Bootcamp partition.

[The last time we looked at this][1] I had cobbled together some AppleScript, `grep` and `awk` for a fairly reliable script, but it required some fiddling if you were still using Leopard (10.5).

I’ve revised the script again, this time relying on the `$NF` variable in `awk` to extract the last field. That makes using `diskutil list` easy, and so I now recommend the following for all users, including those on Leopard or Tiger:

    applescript:
    set deviceID to (do shell script "diskutil list ¬
      | awk '/YourBootcampPartition/ {print $NF}'")
    do shell script "bless -device /dev/" & deviceID & ¬
      " -legacy -setBoot -nextonly" ¬
      with administrator privileges
    tell application "Finder" to restart

[1]: /2012/10/restart-in-windows-revenge-of-the-script/

Here’s the shell part to get the identifier on its own:

    bash:
    diskutil list | awk '/YourBootcampPartition/ {print $NF}'

To be clear, the name of the partition **must go between the two slashes**.

Aside from making it a purely shell script, which causes problems with prompting for the user’s credentials, I can’t see how this can get any simpler and so I fully expect this to be the last time I write about it.

I’ve uploaded [the script as a Gist][2], if you’d like to star or fork it.

[2]: https://gist.github.com/robjwells/3681949
