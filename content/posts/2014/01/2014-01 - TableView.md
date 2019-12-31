---
title: "Misbehaving single-column NSTableView"
date: 2014-01-26T19:24:00
tags: ["Cocoa", "Programming", "Xcode"]
---

This is mostly a note for myself, as I was ready to pull my hair out earlier.

Interface Builder can get in your way when you want to create a single-column `NSTableView` where the column fills the entire width available.

Setting the column count to 1 doesn’t automatically resize it, and extending the column using its resize handle or by setting its width to the width of the view can cause a horizontal scrollbar to appear.

The solution is to **resize the view itself** — so that you eat into the space occupied by the single column, and then expand back to your desired width. It is incredibly stupid. Here’s a video:

<video src="/images/2014-01-26_tableview.m4v" poster="/images/2014-01-26_tableview_poster.png" controls preload="metadata">
  Sorry if you can’t see it. <a href="/images/2014-01-26_tableview.m4v">Here’s a link to the file itself.</a>
</video>

There’s a [Stack Overflow question][so] where the accepted answer recommends this method. Handily I misread it — only realising what it was saying after I’d stumbled across the resizing trick myself (after trying many other things).

[so]: http://stackoverflow.com/questions/7545490/how-can-i-have-the-only-column-of-my-nstableview-take-all-the-width-of-the-table

In related news, I’m almost done with the excellent [Big Nerd Ranch Cocoa book][bnr] after getting sidetracked for two months.

[bnr]: http://www.bignerdranch.com/book/cocoa_programming_for_mac_os_x_th_edition_
