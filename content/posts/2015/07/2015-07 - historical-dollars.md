---
title: "Historical dollars"
date: 2015-07-15T23:40:00
tags: ["Python", "Programming"]
---

I’ve read [a][zinn] [few][chandler] [books][allen] recently where references were made to dollar amounts from many years ago. However, I often find it difficult to understand the context of, say, $10,000 in 1829.

But Wolfram Alpha [can give you a rough approximation][wa] by applying inflation data. This isn’t perfect but is useful to get a general idea of what a similar amount might be today. (There isn’t all the context needed for a more accurate determination, and the underlying basket for inflation measures can be misleading.)

Handily, there’s a [Wolfram Alpha API][wa-api] we can use to get this information programmatically. I originally wrote this script as a command-line tool, but how often do you read at your computer with a terminal window open? So the one in this post uses [Pythonista][] and its `ui` module to make things more practical.

The code to get the new amount is pretty trivial:

```python {linenos=true}
from __future__ import division

from datetime import date
from xml.etree import ElementTree
import requests
import ui


def calculate_amount(sender):
  """Convert given dollar amount for given year to current dollars"""
  amount = view['amount'].text
  year = view['year'].text

  if not (amount and year):
    return

  api_key = 'YOUR API KEY IN HERE'
  api_url = 'http://api.wolframalpha.com/v2/query'
  query_template = '${amount} ({past_year} US dollars) in {current_year}'
  query = query_template.format(amount=amount,
                                past_year=year,
                                current_year=date.today().year)
  parameters = {'appid': api_key,
                'input': query,
                'format': 'plaintext',
                'podtitle': 'Result'}
  response = requests.get(api_url, params=parameters)
  xml_soup = ElementTree.fromstring(response.content)
  new_amount = xml_soup.find('pod/subpod/plaintext').text.splitlines()[0]
  view['result'].text = new_amount
```

The `calculate_amount` function above is called on a button press (hence the `sender` argument) and fetches the text from a couple of UI elements (all that `view` subscripting), bailing out if either the amount or year is missing.

The query template (line 19) is how Wolfram Alpha parses historical dollar calculations (shown as “Input interpretation” on the website) so we can skip as much parsing time as possible.

Requests makes sending the query a doddle, and we use an exact XPath expression to get at the result in the response. There’s an [API explorer][wa-api-explorer] so you can get a handle on the structure. (Normally I’d use Beautiful Soup, but Pythonista doesn’t include lxml, so BS parses it as HTML and there’s really no point in risking — however slightly — that causing some problem. ElementTree isn’t bad if you’re doing something simple, anyway.)

Lastly we update another UI element to show the result. Pretty simple.

With the UI, you’ve got two choices: make it in code or use Pythonista’s UI editor. I chose to do it in code, because the UI editor saves a `.pyui` JSON file that [takes a little work to share][pyui].

But now I would recommend people use the editor, as actually getting the code to work was a bit of a headache too. For the record: Ole Zorn has done an *incredible* job with Pythonista and the UI tools are incredible. However: the `ui` module seems to expose the Cocoa way of making GUIs, so unless you’ve got an understanding of that you may be in for some bumps. Helpfully, you can [view the `ui` module documentation online][ui-docs] Here’s the rest of the code:

```python {linenos=true, linenostart=33}
def setup_view():
    view = ui.View()
    view.name = 'Historical Dollars'
    view.background_color = 'white'
    view.width, view.height = ui.get_screen_size()

    amount_field = ui.TextField()
    amount_field.name = 'amount'
    amount_field.keyboard_type = ui.KEYBOARD_DECIMAL_PAD
    amount_field.placeholder = 'Dollar amount'
    amount_field.width *= 2
    amount_field.height /= 2

    year_field = ui.TextField()
    year_field.name = 'year'
    year_field.keyboard_type = ui.KEYBOARD_NUMBER_PAD
    year_field.placeholder = 'Year'
    year_field.width *= 2
    year_field.height /= 2

    button = ui.Button(title='Calculate')
    button.action = calculate_amount

    result_label = ui.Label()
    result_label.name = 'result'
    result_label.width = view.width
    result_label.alignment = ui.ALIGN_CENTER

    horizontal_centre = view.width * 0.5
    field_spacing = amount_field.height * 1.5
    amount_field.center = (horizontal_centre, amount_field.height)
    year_field.center = (horizontal_centre,
                         amount_field.center[1] + field_spacing)
    button.center = (horizontal_centre,
                     year_field.center[1] + field_spacing * 0.75)
    result_label.center = (horizontal_centre,
                           button.centre[1] + field_spacing * 0.75)

    view.add_subview(amount_field)
    view.add_subview(year_field)
    view.add_subview(button)
    view.add_subview(result_label)

    return view


view = setup_view()
view.present('sheet')
```

And here’s what it looks like in action:

<img src="/images/2015-07-15_historical-dollars.png" alt="A screenshot of the historical dollars script run in Pythonista on an iPhone.">

The thing that really tripped me up was `.flex` on views, for resizing the element based on its containing view. In the code above this isn’t used. I initially followed the example code from the documentation and had all sorts of fun trying to work out why the view spacing was screwed up.

Another problem was expecting the 'master', containing view (instantiated on line 34) to have the same size as the screen, when it seems to act kind of like HTML elements do when they’re full of floated elements (they collapse). That’s why I set the containing view’s size on line 37. (`get_screen_size` also seems to always return the portrait size.) All sorts of headaches resulted from this (centring elements based on the view’s centre particularly).

Otherwise, it’s so straightforward and repetitive that I’m not going to explain most of the lines. It works well enough on an iPhone 5-sized screen in portrait mode (elements are off-centre in landscape) but for smaller screens you may want to shift things about a bit vertically.

There are a couple of things to note. The names you give to elements are how you pick them out later (check out lines 11 and 40). Setting the button’s action (line 54) is obviously key, and you just give it a function object. And specifying the keyboard type for the two text fields relieves the need to do input validation (though the decimal keyboard lets you type multiple points), but frankly anyone who might use this should understand that it’ll break if you type in something funky.

I’ve put [the whole file online][gist] if that’s easier for anyone. You just need to paste it into an empty script in Pythonista and run it. 


[zinn]: https://en.wikipedia.org/wiki/A_People%27s_History_of_the_United_States
[chandler]: https://en.wikipedia.org/wiki/The_Big_Sleep
[allen]: http://www.haymarketbooks.org/hc/People-Wasnt-Made-to-Burn
[wa]: http://www.wolframalpha.com/input/?i=$10,000+(1829+US+dollars)+in+2015
[wa-api]: http://products.wolframalpha.com/api/
[Pythonista]: http://omz-software.com/pythonista/index.html
[wa-api-explorer]: http://products.wolframalpha.com/api/explorer.html
[pyui]: https://omz-forums.appspot.com/pythonista/post/5254558653612032
[ui-docs]: http://omz-software.com/pythonista/docs/ios/ui.html
[gist]: https://gist.github.com/robjwells/9bcdb0cac8d234d1ab7e
