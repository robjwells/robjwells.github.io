---
title: "Keyboard Maestro macro to insert images into blog posts"
date: 2020-05-24T09:00:00+01:00
publishDate: 2020-05-30T06:00:00+01:00
draft: true
---

Here’s a quick Keyboard Maestro macro to make it easier to insert images into blog posts, or any other markdown or HTML document really. The details of the macro are set up to create a [Hugo figure shortcode][hugo-figure], but the Hugo-specific bits are just scaffolding and could be swapped out for whatever you need.

[hugo-figure]: https://gohugo.io/content-management/shortcodes/#figure

You can [download the macro file here][macro], but the whole thing ended up being a bit long so I’m not going to include the usual image of the whole macro (which is 1,631 pixels tall). Let’s step through it.

[macro]: insert-hugo-figure.kmlibrary

{{% figure src="macro-1-prompt-and-read.png" alt="A screenshot showing a portion of a Keyboard Maestro macro, prompting the user for a file and then reading it." caption="The first stage of the macro, prompting for the image file and then loading it onto a named clipboard." link="macro-1-prompt-and-read.png" class="full-width no-border" width=551 height=275 %}}

After selecting the image, we need to load it onto a named clipboard because Keyboard Maestro’s image actions generally work on the contents of a clipboard.

{{% figure src="macro-2-store-properties.png" alt="A screenshot showing a portion of a Keyboard Maestro macro, reading image properties into variables." caption="Next we extract needed properties from the image into Keyboard Maestro variables." link="macro-2-store-properties.png" class="full-width no-border" width=551 height=312 %}}
