---
title: "Audio Hijack 3 and scripts"
date: 2015-01-21 21:03
tags: ["Audio Hijack Pro", "Audio Hijack 3"]
---

Rogue Amoeba released [their upgrade to Audio Hijack Pro][ah3] [yesterday][ah3_blog], and it looks superb. I haven’t had a chance to do any recording with it yet, but I just did a quick test to see how it handles [scripted recordings][beeb_hijack].

The short answer is that, if you have Audio Hijack Pro run an AppleScript at the start of a recording or process the finished recording using a script, you won’t be able to easily migrate to Audio Hijack 3.

In Audio Hijack 3, application blocks can be set to open a URL. If you have the path to an AppleScript in that field it’ll treat it as a file to be saved. (So, in my case, Chrome “downloaded” the .scpt file.) There aren’t any blocks that offer more exotic input methods, nor outputs that pass the file off for processing.

I’ve got a good idea for solving the latter (having Hazel watch a directory and run a script when files come in) but providing the right URL to begin with is more tricky. Perhaps a local web server that redirects to the correct URL? I haven’t done any web programming but I imagine that it would be fairly easy to rig up [my existing Python scripts][beeb_hijack] with [Flask][] or [web.py][] or something. Or you could schedule a script to run after Audio Hijack wakes your machine and begins recording that hands the correct address directly to the browser?

Who knows — maybe the removed functionality will be reintroduced down the line? Audio Hijack Pro still works fine so there’s no great rush to get off that and on to Audio Hijack 3.

On a separate but related matter, there’s no AppleScript dictionary for Audio Hijack 3 (as with [Fission][]).

<div class="flag">
  <p>
    <strong>Update: 2015-01-28</strong><br>
    In <a href="http://weblog.rogueamoeba.com/2015/01/28/audio-hijack-3-is-a-hit-and-audio-hijack-3-0-1-is-here/">a new post about Audio Hijack 3’s first week</a>, scripting is explicitly noted as an area that might get some attention.
  </p>
</div>

[ah3]: http://rogueamoeba.com/audiohijack/
[ah3_blog]: http://weblog.rogueamoeba.com/2015/01/20/audio-hijack-3-has-arrived/
[beeb_hijack]: /2014/01/hijacking-the-bbc/
[Flask]: http://flask.pocoo.org
[web.py]: http://webpy.org
[Fission]: http://rogueamoeba.com/fission/
