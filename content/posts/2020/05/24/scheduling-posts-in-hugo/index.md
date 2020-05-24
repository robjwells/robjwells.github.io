---
title: "Scheduling posts in Hugo"
date: 2020-05-24T09:25:44+01:00
publishDate: 2020-06-06T06:00:00+01:00
---

My enthusiasm for writing posts here tends to come in reasonably short bursts, usually over a weekend, so I’ve taken to scheduling the two or three posts I might write over the following weeks.

It’s reasonably straightforward to schedule publication with [Hugo][] by using the `publishDate` attribute in your post frontmatter. For instance, this is the frontmatter for this post right now:

```yaml
title: "Scheduling posts in Hugo"
date: 2020-05-24T09:25:44+01:00
publishDate: 2020-06-06T06:00:00+01:00
draft: true
```

The `date` attribute is filled in by Hugo when I create the post bundle skeleton. I tend to leave this as a marker for when I started writing a post (though I have changed it for posts that I start, leave for a while, and [finish later][figure-post]).

The `publishDate` attribute controls when the post is actually published. Hugo by default doesn’t build posts with this set in the future.

One important change that I made from the defaults, though, is to define the handling of dates in my site-wide config file (`config.toml`) like so:

```toml
[frontmatter]
date = ["publishDate", "date", ":default"]
```

What this means is that Hugo will prefer the `publishDate` as the date of the post, before falling back to the `date` attribute, and then resuming its default lookup, which is listed [in the Hugo documentation][docs].
(At the moment, the only other thing in the default lookup order is the file modification time, but mostly I include ":default" to be safe if this changes in the future.)

Otherwise, you might end up with a situation where you write “Post Future”, set a publish date in the future, then write “Post Now” and publish immediately, and when “Post Future” is published it will be shown as being published earlier than “Post Now” because its `date` is earlier. Changing the date lookup order in the config will preserve your deliberate schedule.

(Thanks to “n m” on StackOverflow who got me started [with this answer][so].)

Obviously, just having a bunch of files with the dates set properly doesn’t mean your post will actually be published automatically at the right time.
I have a script on my server that cron runs every 15 minutes that pulls from [the GitHub repository][repo] and rebuilds the site.

This set-up is made easy thanks to Hugo being a single binary, so it’s simple to install on the server, whereas [before][majestic] I would generally build the site locally and upload it to my server with rsync.

---

I actually now have a [Beeminder goal][bm] to ensure that I write a post a month — well, I was being lenient with myself so it’s every 31 days. It’s set for a maximum 31 safe days, so I feel that scheduling once a week is enough to tamp down any short-term blog-mania while also not gaming the Beeminder goal too much by scheduling posts at 31-day intervals. (Perhaps this is a sign though that I can set the goal to have a shorter period, but at the moment I have enough commitments that I feel comfortable doing so.)

[Hugo]: https://gohugo.io/
[figure-post]: /2020/05/keyboard-maestro-macro-to-insert-images-into-blog-posts/
[docs]: https://gohugo.io/getting-started/configuration/#configure-dates
[so]: https://stackoverflow.com/questions/59655470/hugo-date-vs-publishdate/59760977#59760977
[repo]: https://github.com/robjwells/primaryunit
[majestic]: https://github.com/robjwells/majestic/
[bm]: https://www.beeminder.com/robjwells/blog
