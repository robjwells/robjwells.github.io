---
title: "Keyboard Maestro macro to insert images into blog posts"
date: 2020-05-24T09:00:00+01:00
publishDate: 2020-05-30T06:00:00+01:00
---

Here’s a quick Keyboard Maestro macro to make it easier to insert images into blog posts, or any other markdown or HTML document really. The details of the macro are set up to create a [Hugo figure shortcode][hugo-figure], but the Hugo-specific bits are just scaffolding and could be swapped out for whatever you need.

[hugo-figure]: https://gohugo.io/content-management/shortcodes/#figure

You can [download the macro file here][macro], but the whole thing ended up being a bit long so I’m not going to include the usual image of the whole macro (which is 1,965 pixels tall). Let’s step through it.

[macro]: insert-hugo-figure.kmlibrary

{{% figure src="macro-1-prompt-and-read.png" alt="A screenshot showing a portion of a Keyboard Maestro macro, prompting the user for a file and then reading it." caption="The first stage of the macro, prompting for the image file and then loading it onto a named clipboard." link="macro-1-prompt-and-read.png" class="full-width no-border" width=551 height=275 %}}

After selecting the image, we need to load it onto a named clipboard because Keyboard Maestro’s image actions generally work on the contents of a clipboard.

{{% figure src="macro-2-store-properties.png" alt="A screenshot showing a portion of a Keyboard Maestro macro, reading image properties into variables." caption="Next we extract needed properties from the image into Keyboard Maestro variables." link="macro-2-store-properties.png" class="full-width no-border" width=551 height=312 %}}

Then we need to prompt the user to confirm the attributes of the figure.

{{% figure src="macro-3-prompt-attributes.png" alt="A screenshot showing a portion of a Keyboard Maestro macro, of a prompt to the user to confirm attributes for the figure to be inserted." caption="The prompt set-up." link="macro-3-prompt-attributes.png" class="full-width no-border" width=551 height=377 %}}

{{% figure src="macro-prompt.png" alt="A screenshot showing a Keyboard Maestro prompt asking for attributes to complete an HTML figure" caption="And the prompt itself." link="macro-prompt.png" class="full-width no-border" width=537 height=267 %}}

Any of these can be empty, so after assembling the shortcode text blank attributes are removed:

{{% figure src="macro-4-assemble-figure.png" alt="A screenshot showing a portion of a Keyboard Maestro macro, creating the figure shortcode from provided attributes and using a regular expression to remove any empty attributes." link="macro-4-assemble-figure.png" class="full-width no-border" width=551 height=631 %}}

And then lastly the figure shortcode text is inserted by pasting, which is handy because it end up on the clipboard if anything goes wrong — like it did when I changed the focus when inserting the previous screenshot!
