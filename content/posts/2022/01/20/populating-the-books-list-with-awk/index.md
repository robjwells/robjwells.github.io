---
title: "Populating the books list with AWK"
date: 2022-01-20T19:45:17Z
publishDate: 2022-01-20T20:40:28+00:00
---

I read [48 books][books] last year, which is a lot for me. At least part of
that, I think, was to keep my mind in gear in a fairly healthy way, when I
didn’t feel like engaging with the world (poor mental health — thanks
once-in-a-century pandemic!)

What I did _not_ do, though, is keep the [list of books][books] up to date,
not since spring 2020.

Since I’ve been playing around with AWK a little, and had a big TSV file
containing the details for each of the books, I thought I'd pair the two to
fill out the missing files.

I use [Hugo][] to generate this site, and each book is represented by a
markdown file containing a metadata block with (at least) the title, author’s
name, and the date on which I finished reading it. For example:

```markdown
---
title: "Empire of Pain"
author: "Patrick Radden Keefe"
finish-date: 2022-01-01
---

_Short review to come!_
```

AWK is great for processing lines of text, but it’s missing some of the library
functions you’d like for working with the filesystem. The book files are stored
in this directory structure, where the markdown files are under each year
folder:

```
content/books
├── 2019
├── 2020
├── 2021
└── 2022
```

Those year folders might not exist (_did not_ for 2021 and 2022). I could have
just created them by hand, but then we’d miss out on some yak-shaving.

The path to the markdown file is constructed using the book's title (for the
markdown filename itself) and finish date (for the year directory). We can wrap
the `dirname` Unix utility:

```awk {linenos=true, linenostart=1}
function dirname(path) {
    cmd = "dirname " path
    cmd |& getline result
    close(cmd)
    return result
}
```

The funny `|&` operator on line 3 executes the command in `cmd` and then
`getline` stores the first line of the output (there's just one for `dirname`) in
`result`. We call `close` on the command string to release the associated file
descriptor.

Let’s wrap our wrapper in a function that just makes sure the directory exists,
using `mkdir -p`, to make our lives easier:

```awk {linenos=true, linenostart=8}
function ensure_dir(path) {
    system("mkdir -p " dirname(path))  
}
```

Now we can think about the filename itself. It doesn't have to be anything
particular, but I like to keep mine `really-simple-like-this.md`. We’re using
the title of the books as the filenames, so the key is just to strip out
non-word characters:

```awk {linenos=true, linenostart=12}
function safe_name(string) {
    return remove_non_word_characters( remove_apostrophes( tolower( string ) ) )
}

function remove_apostrophes(string) {
    return gensub(/['’]/, "", "g", string)
}

function remove_non_word_characters(string) {
    return gensub(/\W+/, "-", "g", string)
}
```

The `remove_apostrophes` function is not strictly necessary but ensures titles
such as _Hitler’s Army_ don’t become `hitler-s-army` when they go through
`remove_non_word_characters`.

With that setup done, we can move on to the meat of the file, the lone
pattern-action statement:

```awk {linenos=true, linenostart=24}
/^(2020-(0[6-9]|1[0-2])|202[12])/ {
    path_template = "content/books/%s/%s.md"
    year = substr($1, 0, 4)
    title_for_path = safe_name($2)
    path = sprintf(path_template, year, title_for_path)

    content_template = ( \
        "---\n" \
        "title: \"%s\"\n" \
        "author: \"%s\"\n" \
        "finish-date: %s\n" \
        "---\n" \
        "\n" \
        "_Short review to come!_")
    content = sprintf(content_template, $2, $3, $1)

    ensure_dir(path)
    print content > path
}
```

We match lines that start with dates representing June 2020 (the last update
being in May 2020) through 2022. Next, we pull out the year from the date
(field 1), and munge the book title (field 2), before formatting them into the
path template with the built-in `sprintf` function.

The `content_template` is just the markdown you saw earlier in the post, again
formatted using `sprintf` and this time involving the author name (field 3).

We ensure the directory exists for the target markdown file, and just print the
formatted template via redirection into the file.

So, would I use AWK over Python for things like this in the future? Maybe. The
disadvantage with AWK is that it’s missing built-in tools for working with
the system, and the work done above would be easier with, say, [Python’s
pathlib module][pathlib]. Or, then again, I could have just done `mkdir 2021
2022` — but I wanted to get a feel for calling tools from AWK.

I think this tool is perhaps just on the edge where it could go either way.
Python has more tools available, but AWK is so focussed on text processing that
it does some of that boring work you’d have to do manually in Python.

It was fun, and I look forward to using AWK for more in the future. (I’ve
bought [the book][awk] second-hand.)

[books]: https://www.robjwells.com/books/
[Hugo]: https://gohugo.io
[awk]: https://archive.org/details/pdfy-MgN0H1joIoDVoIC7
[pathlib]: https://docs.python.org/3.10/library/pathlib.html#module-pathlib
