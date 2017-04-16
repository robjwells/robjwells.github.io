---
title: Solving boredom with four languages
date: 2014-12-04 00:01
tags: Shell, AppleScript, JavaScript, Python
---

At work one of the most tedious jobs is putting all of the stories that appear in the paper onto our website. We're still working from text files (which works very well) as for a number of reasons we haven't yet changed to use the site's CMS as the central location where copy is stored.

So towards the end of the day we have to go through nearly all the pages, strip out the headlines, standfirsts and copy, and input them into the site's backend. It's mindless, slow and frankly demoralising.

A perfect candidate for automation then!

Let's start with taking the text from the InDesign files, with an AppleScript I run through [FastScripts][]:

[FastScripts]: http://www.red-sweater.com/fastscripts/

    applescript:
     1:  tell application "Adobe InDesign CS5.5"
     2:    tell the front document
     3:      set the_text to get the contents of the selection
     4:    end tell
     5:  end tell
     6:  
     7:  repeat with an_item in the_text
     8:    do shell script ("echo '" & an_item & "' >> ~/Desktop/web_strip.txt")
     9:  end repeat
    10:  
    11:  do shell script ("echo '\\n\\n\\n\\n' >> ~/Desktop/web_strip.txt")

Here we take the content of the selected InDesign frames and use a shell script snippet to append it to a file on the desktop, followed by a bunch of newlines to separate the appended text.

It's straightforward, but `the contents of the selection` in line 3 could return anything: more than one selected frame and you get a list, just one and you get whatever data is in the frame. So, instead of iterating over several pieces of text in line 7, you iterate over each character in one piece of text. Bonus points: InDesign CS4 (which we use at work) doesn't preserve the order in which you select frames, meaning you have to go one-by-one (and use a different script — I'm showing the one I use at home here).

Ok, now we've got a text file with all the copy in. Once that's been cleaned up — any unnoticed mistakes corrected, print-focussed formatting removed — it's time to enter it into the CMS.

For ages, this is where the automation stopped. The editor used in the CMS interprets pasted text oddly, requiring people to paste the plain text into (shock horror) TextEdit in rich-text mode, and from there into the field in the CMS. Lots of copying and pasting. Lots of boredom. Gross.

But these are just fields on a web page. And, of course, the page uses jQuery. And Safari lets you `do JavaScript` through AppleScript. This should be trivial. (Chrome also lets you execute JavaScript through AppleScript, but it threw up a weird error that I couldn't be bothered to dig into.)

A bit of poking around in the inspector revealed that most of the interesting fields could be set through a simple `.val(foo)` on the element, while the body of the article could be set through `.html('bar')` — and wrapping paragraphs in `<p>` tags ensured that the text displayed correctly.

But how to get the text from a file in BBEdit into the fields? We need to use AppleScript to tell Safari to execute JavaScript, but you do not want to do any kind of text processing in AppleScript — nor do you really want to do it by hand for tens of articles.

I decided on a Python text filter. Not entirely appropriate — we don't transform and return the text — but it's a dead simple way of working with the selection and removing it once we're done.

Using Python lets us do all sorts of wonderful things too other than just preparing the InDesign text to be entered into the fields. Here's the code, before I dive in any further:

    python3:
     1:  #!/usr/local/bin/python3
     2:  
     3:  import sys
     4:  import subprocess
     5:  
     6:  names = {'Morning Star': 4,
     7:           ...
     8:           'A Reporter': 1002,
     9:           }
    10:  
    11:  
    12:  length_lambdas = {'lead': {'func': lambda l: 300 <= l < 400,
    13:                             'id': 1},
    14:                    '2ndlead': {'func': lambda l: 200 <= l < 300,
    15:                                'id': 2},
    16:                    '150word': {'func': lambda l: 0 < l < 200,
    17:                                'id': 4},
    18:                    'inbrief': {'func': lambda l: False,
    19:                                'id': 5},
    20:                    'splash': {'func': lambda l: 400 <= l,
    21:                               'id': 6},
    22:                    }
    23:  
    24:  # Dr Drang's asrun function
    25:  # http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/
    26:  def asrun(ascript):
    27:    "Run the given AppleScript and return the standard output and error."
    28:    osa = subprocess.Popen(['osascript', '-'],
    29:                            stdin=subprocess.PIPE,
    30:                            stdout=subprocess.PIPE,
    31:                            stderr=subprocess.DEVNULL)
    32:    return osa.communicate(ascript.encode())[0]
    33:  
    34:  
    35:  text = sys.stdin.read().strip()
    36:  head, standfirst, author, body = text.split('\n', maxsplit=3)
    37:  if not standfirst:
    38:    standfirst = ' '           # Required. Don't ask
    39:  if not author.strip():
    40:    author = 'Morning Star'
    41:  else:
    42:    author = author.split('by ', maxsplit=1)[-1]
    43:  name_id = names.get(author, 4)
    44:  words = len(body.split())
    45:  for v in length_lambdas.values():
    46:    if v['func'](words):
    47:      length_id = (v['id'])
    48:  
    49:  wrapped_body = '<p>' + '</p><p>'.join(body.splitlines()) + '</p>'
    50:  
    51:  
    52:  script = """
    53:  tell application "Safari"
    54:    tell the front document
    55:      set js_head to "$('#articleInputTitle').val('{head}')"
    56:      set js_standfirst to "$('#articleTextareaSummery').val('{standfirst}')"
    57:      set js_body to "$('#articleTextareaContent_ifr').contents().find('#tinymce').html('{body}')"
    58:      set js_length to "$('#articleSelectPosition').val({length})"
    59:      set js_author to "$('#articleSelectAuthor').val({author})"
    60:      do JavaScript js_head
    61:      do JavaScript js_standfirst
    62:      do JavaScript js_body
    63:      do JavaScript js_length
    64:      do JavaScript js_author
    65:    end tell
    66:  end tell
    67:  """.format(head=head, standfirst=standfirst, body=wrapped_body,
    68:             length=length_id, author=name_id)
    69:  
    70:  asrun(script)
    71:  print('', end='')

I like to put data at the top of my scripts and the code beneath, so let's start on line 35, where we read in the text from BBEdit. Line 36 breaks that text apart: I use a four-part structure, where the first line is the headline, then the standfirst and byline (both of which can be blank) and then any remaining lines form the body.

In line 43 we index into the names dictionary (abbreviated to protect the guilty, lines 6–9) using the cleaned-up byline, with 4 the value for the default author. This and the story type stuff below are presented as drop-down menus, which is where the integers come from.

Next we crudely count the words in the body to work out the story type, which are roughly differentiated by length. I iterate over a dictionary of lambdas instead of a lengthy `if-elif` block, mostly because it lets me use the dictionary keys to store the strings associated with the values. (You could do the same with comments in the `if-else`. I don't think there's a big advantage to either method.)

Note that the lambda for the 'inbrief' type just returns False. We collect all of the brief stories into a single article on the web, with the total length anything from 100 words to over 600, and I couldn't think of an easy way to pick them out. I set the type for briefs by hand.

The last processing step is to wrap each line of the body with paragraph tags. (It's basic but it works!)

Then we format a string containing the AppleScript, which runs the JavaScript, and pass it to Dr Drang's [asrun function][drang] for execution.

[drang]: http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/

And finally we print an empty string to delete the current selection in BBEdit — time to move on to the next story.

By using this script and opening up a dozen or two 'new article' tabs in Safari, moving between each one and using the text filter to populate the fields, I can effectively do work in parallel instead of one task at a time — filling in new articles while I wait for the website to catch up and show the publishing time options. And no more copy & paste from TextEdit.
