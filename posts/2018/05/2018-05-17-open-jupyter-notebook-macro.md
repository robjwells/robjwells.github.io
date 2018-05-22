---
title: Open Jupyter notebooks with a Keyboard Maestro macro
date: 2018-05-17 19:45
---

I have a startup item that launches a Jupyter notebook so that the server is always running in the background. It’s an attempt to reduce the friction of using the notebooks.

By default, Jupyter starts the server on port 8888 on localhost, but expects a token (a long hexadecimal string) before it’ll let you in. If you list the currently running servers in the terminal you can see the token and also the server’s working directory.
    
    zsh:
    % jupyter-notebook list
    Currently running servers:
    http://localhost:8889/?token=…hex… :: /Users/robjwells
    http://localhost:8888/?token=…hex… :: /Users/robjwells/jupyter-notebooks

We can use this to make finding and opening the particular notebook server you want a bit easier, using Keyboard Maestro.

<p>
    <img
        src="/images/2018-05-17-macro-overview.png"
        alt="A screenshot showing the (minimised) Keyboard Maestro steps"
        />
</p>

The macro uses the `jupyter-notebook` command, so that’ll need to be in your `$PATH` as Keyboard Maestro sees it.

The first and third steps both execute `jupyter-notebook list` and use Unix tools to extract parts from it.

In between, if there’s more than one notebook server running, the macro prompts the user to choose one from a list of their working directories.

<p>
    <img
        src="/images/2018-05-17-notebook-list.png"
        alt="A Keyboard Maestro list selection dialogue"
        class="no-border"
        width=534
        height=464
        />
</p>


Here’s the first step, where we fetch the list of working directories.

    zsh:
    jupyter-notebook list | tail -n +2 | awk '{print $3}'

Our +2 argument to `tail` gets the output from the second line, chopping off the “Currently running servers:” bit. Then `awk` prints the third field, which contains the directory. (The first is the URL, the second the double-colon separator.)

The third step fetches the corresponding URL for a directory:

    zsh:
    jupyter-notebook list | grep ":: $KMVAR_dir$" | awk '{ print $1 }'

Since the user has specified a directory already, we use `grep` with the Keyboard Maestro variable to find just that one line, and use `awk` again to extract the URL field.

<div class="flag" id="update-20180522">
  <p><strong>Update: <time>2018-05-22</time></strong></p>
  <p>There was a bug in the original version of this snippet of shell script, where a parent path could match a child path (as it was only looking for the path itself without an anchor on either side). It was only luck that had me miss this with my example, with the more recently started home directory notebook server being listed ahead of one in a subdirectory, which <code>grep</code> would have also matched. The code above and the macro file have been fixed.</p>
</div>

Obviously, this won’t work if you have more than one notebook server running from the same directory. (But you wouldn’t do that, right?)

[Here’s the macro file][macro] if you’d like to try it out.

[macro]: /files/OpenJupyterNotebook.kmmacros
