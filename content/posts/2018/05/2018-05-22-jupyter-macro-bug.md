---
title: "Jupyter notebook macro bug"
date: 2018-05-22 09:47
---

My post detailing [a Keyboard Maestro macro to open Jupyter notebooks][km-jupyter] had a dumb bug in the second shell pipeline, which fetches the URL of the desired notebook.

[km-jupyter]: /2018/05/open-jupyter-notebooks-with-a-keyboard-maestro-macro/

You’d hit it if:

* You have more than one notebook server running.
* The working directory of one is beneath another.
* The subdirectory server was started more recently.
* You tried to open the parent server with the macro.

The shorter path of the parent would match part of the child’s path.

The original `grep` pattern was:

    sh:
    grep "$KMVAR_dir"

And is now:

    sh:
    grep ":: $KMVAR_dir$"

So that it only matches the exact directory chosen in the list prompt, and not one of its children.

I’ve updated [the Keyboard Maestro macro file][macro-file] too.

[macro-file]: /files/OpenJupyterNotebook.kmmacros
