---
title: "Give Python’s static typing a go"
date: 2020-07-07T22:42:45+01:00
publishDate: 2020-07-08T06:00:00+01:00
---

While my go-to language is still Python, at [university][birkbeck] I’ve also used Java and C#.
I have to say, there was a huge amount to like — much to my surprise initially!

Previously I’d kind of written off Java as being a [boring language for boring businesspeople][enterprise fizz buzz].
There are certainly elements of that (`package com.robjwells.MyPackage;` in `src/main/java/com/robjwells/MyPackage.java`) but there’s a lot to like.
Streams are great, lambdas are great, the standard library is great (though not without its rough edges, such as the repeated attempts at date and time), and the tooling is great (I have actually come round to really like [IntelliJ IDEA][] — certainly buying a full licence when my academic licence expires).
Plus, it’s really coming along at a clip now with the shorter release cycle.

And C# was an even more pleasant surprise. It’s easy to get the impression that it’s “Microsoft’s Java”, but that’s really selling it short.
[LINQ][] is a joy that makes [comprehensions in Python][trey-comprehensions] (of which I am a huge fan!) seem… just a bit clunky. But C# is full of features, not just LINQ, that make working in it a real pleasure. (I will say, though, that at least on the Mac [Rider][] is a far superior editor than Visual Studio.)

[birkbeck]: https://www.dcs.bbk.ac.uk/
[enterprise fizz buzz]: https://github.com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition
[IntelliJ IDEA]: https://www.jetbrains.com/idea/
[LINQ]: https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/
[trey-comprehensions]: https://www.youtube.com/watch?v=ei71YpmfRX4
[Rider]: https://www.jetbrains.com/rider/

All of this is to say, in a round-about way, that those *weird verbose enterprise-y languages* have a lot going for them — even in the still small-scale things that I’m working on where without this exposure I would just use Python.

Now, I still *am* using Python, but there are things that I miss.
Chief among them in Python is having the type system actively help me out. [Gary Bernhardt writes a bit about this in the context of Ruby and TypeScript][gb-typescript]. (Be warned there are trivial examples ahead.)

Now, I’m using [VSCode][] so actually the editor will step in and help you even if you do nothing to aid it. For instance, in the following situation:

```python
# untyped.py v1
def ultimate_answer():
    return 42

def main():
    u = ultimate_answer()
```

VSCode (using the [Python extension][]) will correctly infer that the type of `u` is `int`. So let’s do something with that:

[Python extension]: https://marketplace.visualstudio.com/items?itemName=ms-python.python

```python
# untyped.py v2
def ultimate_answer():
    return 42

def do_something(n):
    return n - 11

def main():
    u = do_something(ultimate_answer())
```

VSCode still correctly infers `u` to be an `int`. Great! But let’s be clear: this is VSCode doing the work so that it can offer you handy things like code completion.

What happens if we have a change in requirements and we change our API… only we don’t catch everything so we end up with the following:

```python
# untyped.py v3
def ultimate_answer():
    return "42"

def do_something(n):
    return n - 11

def main():
    u = do_something(ultimate_answer())
```

At this point, VSCode gives up: `u` is an `int` or it’s a `str`. In fact it’s neither, because `do_something()` raises a `TypeError` so `u` is never assigned. This is “obvious” to a human reading the code, in this simple example, but it’s easy to imagine a complex system where the types get out of line but the definitions are far apart from each other and the eventual call site.

There are type checkers for Python, the main one being [mypy][] (which is great!). Can mypy help us here?

```
$ mypy untyped.py
Success: no issues found in 1 source file
```

Oh, success! Great.

```
$ python3 untyped.py
Traceback (most recent call last):
  File "untyped.py", line 10, in <module>
    main()
  File "untyped.py", line 8, in main
    u = do_something(ultimate_answer())
  File "untyped.py", line 5, in do_something
    return n - 11
TypeError: unsupported operand type(s) for -: 'str' and 'int'
```

Ah, no, no magic was performed and we still have a `TypeError`. It’s worth pointing out here that mypy is all about gradual typing — adding type annotations to your programs as and when. If there are no annotations, there are no checks performed. It’s not clairvoyant.

If we switch back to VSCode, what if we try [Microsoft’s shiny new Pylance extension][pylance]? In the basic type-checking mode it reports that the type of `u` is unknown which … is a step in the right direction? But no warnings.

If we ratchet up the type-checking mode to strict it reports, with a bunch of red error squiggles, that the return type of `do_something()` is unknown and the type of `u` is unknown. We get a similar result if we pass the `--strict` flag to mypy, which essentially tells the type checker “forget about this gradual business” and attempts to check the whole file. This effectively fails, because we’ve done nothing to help it. Let’s do that now.

In fact, very little is needed before Pylance starts to push you in the right direction, only this:

```python
# typed.py v1 excerpt
def do_something(n: int):
    return n - 11
```

After which we’re rewarded with red squiggles underneath the call to `ultimate_answer()` that provides the argument inline to `do_something()`. The message we get is interesting because it reveals something about the knowledge of the type-checker:

```
Argument of type "Literal['42']" cannot be assigned to
parameter "n" of type "int" in function "do_something"
  "Literal['42']" is incompatible with "int"
```

We haven’t typed `ultimate_answer()`, but it knows that "42" can’t be treated as an `int`. Mypy needs a little more help to get there:

```python
# typed.py v2 excerpt
def ultimate_answer() -> str:
    return "42"

def do_something(n: int):
    return n - 11
```

So, at this point we’ve said that `ultimate_answer()` returns a string and that `do_something()` takes an integer. What does mypy think?

```
> $ mypy typed.py
Success: no issues found in 1 source file

> $ mypy --strict typed.py
[…snip…]
typed.py:8: error: Argument 1 to "do_something" has
    incompatible type "str"; expected "int"
[…snip…]
```

This is an interesting situation because "normal" mode mypy reports that this is fine, no problems here. Strict mode complains — among other things — that the types don’t match. Finally, this is what we want.

But why doesn’t “normal” mode mypy not see the problem? I think this is to do with what is considered a “typed context”. By using `--strict` we force everything to be a typed context, so we get a lot more warnings and errors from mypy. But without this, `main()` is not a typed context — it has no typed arguments, and no explicit return type, so “normal” mode mypy just skips over it.

The strength of gradual typing is that if you don’t want to or aren’t ready to add type information, you don’t. But even in this toy example, the standard Python type-checker under its default settings does not pick up this “obvious” (to us!) type error. In [Dustin Ingram’s Pycon talk about static typing][ingram] he says you should use static typing everywhere — for a few reasons, but here we can see that failing to do so leaves a clear error undetected..

It doesn’t take much to rectify that for mypy, just a return type on `main()`, yielding the following:

```python
# typed.py v3
def ultimate_answer() -> str:
    return "42"

def do_something(n: int):
    return n - 11

def main() -> None:
    u = do_something(ultimate_answer())
```

And now `mypy typed.py` gives the same error that strict mode did for the previous example. Adding the explicit return type to `main()` is honestly pretty useless, but now it opens up the definition of `main()` to be type checked, at which point the error is spotted.

* * *

I wrote the title of this blog post before I really knew where I was going (I have a Beeminder deadline to hit!) so at this point it feels to me like I haven’t quite delivered on (why you should) “Give Python’s static typing a go”. Really we’re at “If you decide to use Python’s static typing you need to go all-in.” Which actually is something I do believe! I think the strictest settings are the most useful, but leaving something untyped leaves a hole for type errors to sneak through.

But it is useful in itself. It’s unfamiliar and, honestly, a bit clunky in Python. (The dance for declaring a `TypeVar` for a generic function taking some type `T` is … Not Good and looks worse once you run your code through a formatter, with it then two lines away.)

But thinking about types is thinking about design, and thinking about the contract that you’re willing to offer to the outside world. I’ve found that in Java and C# sometimes I’m ready to bound straight into defining a function … only to stop after realising that I haven’t really clarified what expectations I have of the outside world (parameter types) and what expectations the outside world has of me (return type).

Here’s a dead-obvious example from a simple exercise on [Exercism][] (sorry for any spoilers but I should hope this one is straightforward to anyone with any knowledge of the `datetime` module!):

```python
from datetime import datetime, timedelta

GIGASECOND = timedelta(seconds=1_000_000_000)


def add(moment: datetime) -> datetime:
    return moment + GIGASECOND
```

Now, `add()` is a bad name in general but fine in this confined case, but it’s the simple addition of the `datetime` annotations that make it clear what we’re handling here. You give a datetime, receive a datetime. Nothing fancy, but compare with the following signature:

```python
def add(moment): ...
```

It’s concise, sure, but is the cost in understanding worth it? Explicitly annotating the types forces you to consider what the interface is and, in return, tools like mypy will give you a hand in finding bugs.

Anyway, give [Dustin Ingram’s talk][ingram] a watch (check out those t-shirts!) as it’s informative, straightforward and short. Do check out the [mypy documentation][mypy-docs], as there’s plenty of descriptive information in there beyond the interface to the command line tool and the `typing` module. [Jukka Lehtosalo and David Fisher spoke in some detail at Pycon 2017 about mypy][jh-df], and I highly recommend [Jukka’s article on the Dropbox tech blog that looks at the history and practical aspects of mypy][jh-dropbox].

It’s clear also that this is the direction of travel for Python — there is a lot on the horizon that will make life easier (see [the list of PEPs][peps]), and I’m particularly looking forward to seeing what becomes of [PEP 622][] as at the moment it looks like it will bring with it [sum types][], even if it is a year or two off at this point.

[gb-typescript]: https://www.executeprogram.com/blog/porting-to-typescript-solved-our-api-woes
[mypy]: http://www.mypy-lang.org/
[pylance]: https://devblogs.microsoft.com/python/announcing-pylance-fast-feature-rich-language-support-for-python-in-visual-studio-code/
[VSCode]: https://code.visualstudio.com/
[ingram]: https://www.youtube.com/watch?v=ST33zDM9vOE&feature=youtu.be
[Exercism]: https://exercism.io/
[mypy-docs]: https://mypy.readthedocs.io/en/stable/index.html
[peps]: https://www.python.org/dev/peps/
[PEP 622]: https://www.python.org/dev/peps/pep-0622/
[sum types]: https://fsharpforfunandprofit.com/posts/discriminated-unions/
[jh-df]: https://www.youtube.com/watch?v=7ZbwZgrXnwY
[jh-dropbox]: https://dropbox.tech/application/our-journey-to-type-checking-4-million-lines-of-python
