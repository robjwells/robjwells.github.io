title: Sunny with a chance of Python
date: 2013-07-23 22:28
tags: Programming, Python

Learning Python is the next goal that I’ve set myself, though I have put it off for a bit while I [improve my maths skills][maths].

[maths]: http://www.cengage.com/cgi-wadsworth/course_products_wp.pl?fid=M20b&product_isbn_issn=9780495826163&discipline_number=10002&template=AISE

But I do have one little Python script that I’ve been playing with for a while, which I first wrote to dip my toe in and see if I liked the language. (I do, very much so).

It’s incredibly basic but complements my [automatic weather script][weatherman], which saves a lot of time and tedium at work, by fetching a text summary of the weather for the entire UK.

[weatherman]: https://github.com/robjwells/weatherman

    python3:
     1:  #!/usr/bin/env python3
     2:  """Get a 3 to 5 day outlook for the UK from the Met Office."""
     3:  
     4:  from urllib.request import urlopen
     5:  from bs4 import BeautifulSoup as bs
     6:  from subprocess import Popen, PIPE
     7:  
     8:  api_url = ("http://datapoint.metoffice.gov.uk/public/" +
     9:             "data/txt/wxfcs/regionalforecast/xml/515")
    10:  api_key = "Your Datapoint API key here"
    11:  
    13:  def get_weather():
    14:    """Retrieve and parse the text summary forecast"""
    15:    raw_xml = urlopen(api_url + "?key=" + api_key)
    16:    outlook = bs(raw_xml).find(id="day3to5").get_text()
    17:    return outlook
    18:  
    19:  if __name__ == "__main__":
    20:    # Encode and pipe outlook to pasteboard
    21:    outlook_bytes = get_weather().encode()
    22:    Popen("pbcopy", stdin=PIPE).communicate(outlook_bytes)


As shown at the top, this is Python 3 code. I have a version written in Python 2 which is very similar. It uses the built-in ElementTree XML parser instead of the nicer Beautiful Soup used in this script as I both wanted to get my head around the interface and for reasons to do with the Python version at work.

Lines 8–10 set up variables needed to access the [Met Office API][datapoint], which is done in the `get_weather` function below.

[datapoint]: http://www.metoffice.gov.uk/datapoint

Beautiful Soup is used to parse the API response in line 16. I love its dead simple method for finding elements, especially compared to ElementTree’s insistence that you provide the XML namespace:

    python3:
    pattern = (".//{www.metoffice.gov.uk/xml/metoRegionalFcst}" +
               "Period[@id='day3to5']")

My favourite part of the script is also the newest. If it is run directly from the command line (line 18) it pipes the forecast to the clipboard using `pbcopy`. I knew Python could start external processes but I was *blown away* by how easy this was. Previously the script printed the forecast and I used a shell alias to send it to the pasteboard. Yuck. This is much better.

The way Python 3 handles strings requires an encoding step in line 21, whereas Python 2 can just send a string through `communicate` — as it’s already bytes. This caught me out at first but otherwise it was incredibly simple to implement.

So, like I said, a trivial program but one that has made me eager to learn more Python.
