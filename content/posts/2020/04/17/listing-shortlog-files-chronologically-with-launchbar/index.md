---
title: "Listing shortlog files chronologically with LaunchBar"
date: 2020-04-17T12:40:52+01:00
publishDate: 2020-04-25T06:00:00+01:00
---

Building on [my introductory post about maintaining “shortlog” diary files][shortlogging], I quite often want to have a look at recent shortlog files.

I have my shortlog folder indexed by [LaunchBar][lb], so I can browse the files that way. By default these are listed in lexicographically ascending order. You can reverse this by holding down command when navigating into the folder in LaunchBar.

However, that doesn’t resolve the problem that it’s not always easy to realise that 2020-04-13 is “Monday”.

So I thought I would write a [LaunchBar action][lb-action] to do both.

Despite being my first, it was really very easy. I wrote it in JavaScript as the documentation leads you that way, and you don’t have to serialise to JSON and write to stdout to return values. LaunchBar provides some additional tools to make interacting with the system straightforward from JavaScript. (And, to be clear, this isn’t [JXA][] either.)

[shortlogging]: https://www.robjwells.com/2020/04/shortlogging/
[lb]: https://www.obdev.at/products/launchbar/index.html
[lb-action]: https://developer.obdev.at/launchbar-developer-documentation/#/actions-overview
[JXA]: https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/index.html

Here are the settings in the scripts pane in LaunchBar’s Action Editor:

{{% figure src="action-editor-script-settings.png" alt="A screenshot of the scripts pane settings in LaunchBar’s action editor for a default script, showing the default settings except that it returns an Item" link="action-editor-script-settings.png" class="full-width" width=510 height=250 %}}

This is a default script, taking no input. One thing to note is that it returns a result of type “Item” — an array of JavaScript objects with particular keys. You can read about the properties items can have [in the LaunchBar action developer documentation][lb-action].

And here’s the code:

```JavaScript {linenos = true}
function run(argument) {
  const shortlogDir = "~/Dropbox/notes/shortlog/"
  return File.getDirectoryContents(
    shortlogDir
  ).filter(fileName =>
    /^shortlog-20\d{2}-\d{2}-\d{2}.txt$/.test(fileName)
  ).map(fileName => {
    const isoString = fileName.substring(9, 19)
    const dateString = LaunchBar.formatDate(
      new Date(isoString),
      {
        timeStyle: "none",
        dateStyle: "full",
        relativeDateFormatting: true
      }
    )
    return {
      title: dateString,
      path: shortlogDir + fileName,
      /* Use the ISO string as LaunchBar rejects returned objects
         containing types other than strings, numbers, arrays
         and objects (dictionaries) */
      date: isoString
    }
  }).sort(
    /* Note this is a string comparison, but it’s OK as
       we’re comparing ISO date strings. */
    (first, second) => first.date > second.date ? -1 : 1
  )
}
```

This is just a “default script”, and while `run` takes an argument, it’s ignored.

We treat this as a simple pipeline of transformations on data:

*   reading the contents of a directory (lines 3 & 4)
*   keeping only those whose filenames match dated shortlog files (lines 5 & 6)
*   creating an object containing a human-readable date, the path to the file, and an ISO-format date string (lines 7–24)
*   sorting those objects on the ISO date string, newest to oldest (lines 25–29).

In line 3, we make use of the `File` object, which is provided by LaunchBar. And in lines 9–12 we use the `formatDate` function on the `LaunchBar` object, which gives us access to the system’s date formatting, which is both locale-aware and respects the user’s date & time preferences.

{{% figure src="shortlogs-action-result.png" alt="A screenshot showing the resulting list of files in reverse date order in LaunchBar" link="shortlogs-action-result.png" class="pull-right" width=310 height=459 %}}

By providing the path in the result object, LaunchBar treats each entry in the list as a file, so you can press return to open it, or press the right arrow to inspect its details.

One oddity: I did try to store a JavaScript `Date` in the result objects, to use in the final sorting, but LaunchBar displays an error if a `Date` in the returned items. You could strip out any of your custom properties, but here I just use the ISO-format date string from the filename as it works just as well for the sorting comparison.

(Another oddity: I initially created the `Date` (now in line 10) manually with the date components extracted from the ISO-format date string. I learned that the constructor doesn’t take a `month` argument but instead a `monthIndex`, in the range 0–11. [Some background on why this is][so-jsdate].)

[so-jsdate]: https://stackoverflow.com/questions/2552483/why-does-the-month-argument-range-from-0-to-11-in-javascripts-date-constructor
