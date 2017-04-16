---
title: Promptless Mercurial
date: 2013-08-24 13:04
tags: Mercurial
---

My time-wasting with Git and Mercurial continues apace — although I think I’m largely done learning how to use each — and I’m at the point where I start fussing over trivial details.

This time it’s prompts. I’ve had [Git’s status][git-prompt] in my prompt for quite a while, since it comes bundled, but as I’ve been spending so much time mucking about with Mercurial I decided to give Steve Losh’s [hg-prompt][] a try.

[git-prompt]: https://raw.github.com/git/git/master/contrib/completion/git-prompt.sh
[hg-prompt]: https://bitbucket.org/sjl/hg-prompt/src

It’s nice and you use it in a similar way to [Mercurial’s own templates][templates], which are very powerful. But it does introduce a slight delay at the command line, which I haven’t noticed with the Git prompt. Maybe I’ll decide this isn’t a big deal and change my mind in the future, but at the moment it was just enough to put me off.

[templates]: http://selenic.com/hg/help/templates

I also like to keep my prompt nice and short. Right now it’s just the basename of the working directory and the dollar sign (or hash if root). The prompt in my home directory is just:

    ~ $

So I’ve decided to go promptless and ditch the additions for both Git and Mercurial. This should help get me in the habit of checking each kind of repository in a similar way, instead of glancing at the prompt for Git and typing commands for Mercurial.

If you use the `-sb` options with Git’s `status` command it gives you a short status with the current branch on top, which is adequate for my needs.

By default there isn’t a Mercurial command to do this, but it’s trivial to create one using an alias — and one that’s superior to `git status -sb`. Here’s what I’ve got in my .hgrc file (line breaks added for clarity):

    now = !$HG log -r . --template
          "{label('log.changeset', rev)}
          {label('branches.active', '    {branch}')}
          {label('bookmarks.current', '    {bookmarks}')}\n" ; $HG status

The exclamation mark at the start tells Mercurial to interpret it as a shell alias — this lets us call `hg status` at the end. The alias calls `hg log` for the parent of the working directory (the commit you currently have checked out).

Using the template system we ask for that changeset’s revision number, branch and any bookmarks associated with it. The `label` stuff surrounding `rev`, `branch` and `bookmarks` colours the output — you can otherwise ignore it.

[Revision numbers][revs] are a convenient but *strictly local* way of referring to changesets. I include the branch name and bookmarks because you can use either (or both) to branch your work; there’s no point just printing the named branch if you’re using bookmarks, and vice versa.

[revs]: http://mercurial.selenic.com/wiki/RevisionNumber

When called inside a repository, `hg now` prints something like this:

    hgrepo $ hg now
    20    experimental    super-duper

If there are any changes in the working directory that’s followed by the usual output of `hg status`, like so:

<img src="/images/2013-08-24_hgnow.png" alt="Image of the output of hg now when there are changes in the working directory.">
