title: Easy branch comparison with Mercurial
date: 2013-07-27 20:33
tags: Git, Mercurial

I’ve spent a lot of time recently learning [Git][] and [Mercurial][], and trying to decide which one I prefer and want to keep using.
Both are nice, but one thing I like about Git is how easy it is to quickly see which commits are on one branch but not another.

[Git]: http://git-scm.com
[Mercurial]: http://mercurial.selenic.com

The commands below show commits on the feature branch that aren’t present on master, and are all equivalent:

    git log feature ^master
    git log ^master feature
    git log master..feature

Unfortunately doing the same with Mercurial requires a lot more typing:

    hg log -r "ancestors('feature') and not ancestors('master')"
    hg log -r "::'feature' and not ::'master'"

Which is a shame, and a bit odd since Mercurial has the incoming and outgoing commands to see which commits are coming in from (or going out to) a remote repository.
I like to think of the comparison above as a local equivalent, to see which commits are going to be pulled across branches in a merge.

Thankfully this can be put right with a quick alias in your .hgrc file. This is what I’ve got in mine:

    [alias]
    compare = log -r "ancestors('$1') and not ancestors('$2')"

It’s general enough to allow comparisons between any two commits. Named branches and bookmarks both work fine, as do revision numbers and commit hashes.

What’s nice about this alias is that any `hg log` options you’d like to use can just be stuck on the end as usual, since it’s just a shortcut to that command. For example these work as you’d expect:

    hg compare feature master
    hg compare feature master --graph
    hg compare feature master -l 20 -p
