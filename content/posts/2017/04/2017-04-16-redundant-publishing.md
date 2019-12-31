---
title: "Redundant publishing"
date: 2017-04-16T22:39:00
---

In my previous post about [page speed][ps], I mentioned that I’d written [my own site generator][Majestic]. I’m not quite ready to talk specifically about it — I want to write some documentation first — and really I doubt that anyone but me *should* be using it.

[ps]: /2017/04/page-speed/
[Majestic]: https://github.com/robjwells/majestic

But, having set up [publishing to Amazon S3][s3] today, I wanted to write up how I publish this blog to multiple places so that it’ll be around whatever (within reason) might happen.

[s3]: https://s3.robjwells.com

[Majestic][]’s configuration files are set up in such a way that you have have a default settings file in a directory — `settings.json` — and you can specify others that make adjustments to that.

In my case the main settings file contains the configuration for publishing to my own server (hosted at Linode) — not the nitty gritty of how to get it on to the server, but what the URLs, site title, etc should be. (It’s online if you want to [have a nose around][settings].)

[settings]: https://github.com/robjwells/primaryunit/blob/master/settings.json

Then I have two extra JSON files: `robjwells.github.io.json` and `s3.robjwells.com.json`, which contain the customisations for publishing for those domains. Here’s the config for GitHub in full:

    json:
    {
      "site": {
        "url": "https://robjwells.github.io",
        "title": "Primary Unit mirror on GitHub",
        "description": "A mirror of https://www.robjwells.com hosted on GitHub"
      },

      "paths": {
        "output root": "gh-pages"
      }
    }

Setting `site.url` is important because of the way my templates render article links (though my markdown source contains only relative links that work anywhere). And `paths.output root` just specifies the build directory where the HTML files get written.

All the moving parts are contained in [a makefile][make] which can build all three of my destinations. Here it is in full:

[make]: https://github.com/robjwells/primaryunit/blob/master/makefile

    makefile:
    NOW = $(shell date +'%Y-%m-%d %H:%M')
    DISTID = $(shell cat cloudfront-distribution-id)


    define upload-robjwells
    rsync -zv -e ssh www.robjwells.com.conf
        rick@deckard:/srv/www/www.robjwells.com/
    rsync -azv --delete -e ssh site/
        rick@deckard:/srv/www/www.robjwells.com/html/
    endef


    define upload-github
    cd gh-pages ; git add . ; git commit -m "$(NOW)" ; git push
    endef


    define upload-aws
    aws s3 sync s3 s3://s3.robjwells.com --delete
    aws cloudfront create-invalidation
        --distribution-id="$(DISTID)" --paths=/index.html
    endef


    all: robjwells github aws

    force-all: force-robjwells force-github force-aws

    robjwells:
      majestic
      $(upload-robjwells)

    force-robjwells:
      majestic --force-write
      $(upload-robjwells)

    github:
      majestic --settings=robjwells.github.io.json
      $(upload-github)

    force-github:
      majestic --settings=robjwells.github.io.json --force-write
      $(upload-github)

    aws:
      majestic --settings=s3.robjwells.com.json
      $(upload-aws)

    force-aws:
      majestic --settings=s3.robjwells.com.json --force-write
      $(upload-aws)

(The `force-*` options rebuild the whole site, not just files which have changed.)

And, really, that’s all it takes to publish to multiple hosts (once you’re set up at each one, of course).

My own server is just a vanilla rsync command, with an extra one because I keep my Nginx server config locally too.

For GitHub pages the `gh-pages` folder is a git repository, so `make github` regenerates the site into that folder, commits the changes with a timestamp as the message, and pushes the changes to GitHub. (It’s all on the same line with semicolons because the `cd` into the directory doesn’t hold across lines in the makefile.) Because the GitHub repository is set up to publish, the rest is sorted out on their end.

And for S3 I just use the official AWS tool (`brew install awscli` if you’re on macOS) — the CloudFront line is because I use it to speed up the S3 version and I want to make sure an updated front page is available reasonably quickly, if not anything else.

There’s a bit of overhead setting all of these up but once you do it doesn’t have to be any more work to keep each host updated. For me it’s just a `make all` away.
