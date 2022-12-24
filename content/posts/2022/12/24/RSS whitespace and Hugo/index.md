---
title: "RSS Whitespace and Hugo"
date: 2022-12-24T13:09:00Z
---

One thing I noticed about [yesterday's post][y] was that the code formatting in
the RSS feed was off. This was due to building the site with [Hugo's `--minify`
option][min], which "reached into" the `<description>` item for the post and
squished the whitespace without regard to whether it was in a `<pre>` block.

This was a simple fix: in Hugo's settings there are a bunch of [options for
`minify`][min-config], one of which is `disableXML`. Add that to your config
file, rebuild, and you're done:

```toml
[minify]
disableXML = true
```

[y]: /2022/12/sunrise-and-sunset-database/
[min]: https://gohugo.io/hugo-pipes/minification/
[min-config]: https://gohugo.io/getting-started/configuration/#configure-minify
