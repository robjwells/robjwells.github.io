---
title: "My email nightmare"
date: 2015-02-25T12:35:00
tags: ["email"]
---

At work we have about 40 employees. A couple of weeks ago I moved our email to a new provider ([FastMail][]). It took a while to get to but most of the activity was extremely concentrated, and that led me to make some mistakes. However, the move was successful, and hopefully my experience can smooth the way for people in a similar situation.

[FastMail]: https://fastmail.com

### Background

From what I can tell, we’d been running our email through cPanel on a [shared host][ukwsd] since 2003. (I was hired in 2010 and this became my responsibility in May 2014.)

It wasn’t really an appropriate choice for a business. We had a small amount of space (9GB) shared between all employees. When users (or the entire account) exceeded their quota, the software would bounce incoming emails and send a shaming email to senders. Lots of simple things (holiday automatic replies) required my involvement.

In addition, our domain’s DNS records were also managed through cPanel, tying the settings for our domain to our host (who were also our registrar at this point, so not totally unreasonable).

The host wasn’t great either.

*   To use SSL encryption, our email clients had to point to their server (not our own domain). This isn't a problem, except that one weekday afternoon in November they moved us to a different server without warning, breaking our email clients.
*   Our contacts, using major webmail services, would sometimes have their provider refuse to send mail to us because our shared server had been placed on a [blackhole list][rbl].
*   Five failed login attempts within two minutes would trigger an IP block. Starting an email client and, wondering why nothing’s happening, pressing the check mail button twice would shut down one of our two office lines. (POP/IMAP & SMTP authentication counted as separate attempts.)

That last one was really fun in combination with the November server move, as I went round the office changing people’s email settings. Their support workers, however, were helpful.

And about two-thirds of our employees were accessing their email over POP, with nothing stored on our server.

We were in a pretty bad state. (Hopefully little of this sounds familiar to you.)

[ukwsd]: https://ukwebsolutionsdirect.co.uk
[rbl]: https://en.wikipedia.org/wiki/DNSBL

### Preparation

The biggest task before the switch itself was to move everyone using POP to access their mail to IMAP, otherwise when it came time to do the migration there’d be nothing to move across. They’d have to keep the old POP account in their client forever to be able to access old mail (one remote worker has had to do this because they couldn’t manage to set up IMAP access to their account in [Entourage][], their version of which is [old and busted][office]).

[Entourage]: https://en.wikipedia.org/wiki/Microsoft_Entourage
[office]: https://en.wikipedia.org/wiki/Microsoft_Office#Microsoft_Office_2001_and_v._X

For machines you can access personally this is fairly straightforward but dull. You generally can’t convert a client account from POP to IMAP, so set up a parallel account in the client and move messages into the IMAP version’s folders. If you have people using Entourage X or 2004 beware that moving messages between accounts will not preserve the original received date. I was moving everyone to Apple Mail — the only OS X client I’m going to support — and had to change the date column to use *date sent*.

With remote workers you’re reliant on their technical skills and your ability to give instructions. For non-technical users think seriously about having them keep a disabled POP account as an archive (as mentioned above) as it may not be worth hours of your time trying to guide them on to IMAP.

Ensure that your DNS settings are in a state where all that’s needed to do is to flip the MX records during the transition. You want to be able to pull the plug on your old provider without the world stopping. In our case, I transferred our domain to [Hover][] and recreated the records. (cPanel stores MX and other records separately.)

[Hover]: https://www.hover.com

You’ll obviously need to draw up a list of accounts that’ll need creating at the new provider, which will give you a chance to rationalise your usage. This is particularly important when moving to a provider that charges per account (as FastMail and seemingly everyone else does). FastMail has a CSV import feature which will let you create many accounts in one step. (I just used regex in BBEdit to transform a simple list into the required format.)

In our case, the biggest change was the ability to create aliases. So instead of five separate arts desk accounts we now have one main account, with aliases filing mail into subfolders. Combined with pruning unnecessary accounts, this meant I was able to almost halve the number we needed.

Aliases also let me clean up our unpredictable account names, so that everyone is now firstnamesurname@, while ensuring that all mail sent to the old addresses ends up in the right place.

You can get started on this list at any point, and it was one of the first things that I did after getting approval. But as you approach D-Day you need to *make sure that the list is up to date*. I failed to do this and, while it didn't cause major problems, it caused me to panic a bit as I scrambled to get the missing accounts up and running.

### Transition

It will benefit you greatly if you draw up a plan for the transition. That includes choosing a D-Day, and detailing what actions you are going to perform and in which order. My biggest mistake was to let a worsening of the problems detailed above force my hand and act hastily. Do everything you can to avoid this and work according to plan.

Your D-Day list should include:

1. Business sign-up and payment. (You may be ready but is the person with the company card?)
2. User account creation. (Double-check you're not missing any.)
3. User migration and client settings switch. (You can’t split these.)
4. MX record switch.

1 & 2 are straightforward, although after the second you may want to spend some time cleaning up autofilled names for non-personal accounts (Ms Acme C Department) and corresponding global address book entries.

You’ll need to decide on a migration strategy. [The FastMail help][migration] for this is very good. For any sizeable number of accounts you’ll want the second option: set up the accounts then for each user set up forwarding at the old provider, migrate existing mail and then change the user’s settings.

As soon as you enable forwarding for a user the clock is ticking for you to change the user’s settings. Perform the IMAP migration and the clock ticks faster. The longer you wait the more the user’s new account will diverge from the old one.

This is where I made *by far my biggest mistake*, one which forced me to work through the night to complete the switchover. I set up forwarding for and migrated each user in one block, without changing any client settings. If I hadn’t then spent hours changing everyone’s client settings I would have had to purge the accounts and start over with the IMAP migration. That’s a pain because after each import  for each account you’ll probably have to do some housekeeping (moving sent mail into FastMail’s sent folder, junk to junk, and so on).

Note the order of actions on [the FastMail help page][migration]:

1. Forward the user’s new mail,
2. Migrate the user’s existing mail,
3. Change the user’s settings,
4. Then *and only then* move on to the next user.

Completely moving a user allows you to take as long as you need to complete the whole transition. Given other pressures on me at work, it’s likely that it would’ve taken weeks to move everyone. Making this mistake at least forced me to complete the entire thing quickly, even if it meant working a 19-hour shift. (I started working on the emails in earnest after a full day working on edition.)

If you have remote workers you’ll need a strategy for them too. Mine was to send them all emails (to their personal accounts) containing a warning that their mail clients would be broken, new settings if they felt comfortable enough changing them, and instructions on how to access the web interface.

Once you’ve got everyone moved over, flip the switch on the MX records so that new mail flows directly to the new provider.

[migration]: https://www.fastmail.com/help/business/migrate.html

#### Aside: hosting your DNS with FastMail

FastMail encourages you to host your DNS with them. I haven’t done it for `robjwells.com` or work because I feel that there should be a separation there (DNS settings stay with [the registrar][Hover]) and I’m not intimidated by DNS records (although they’re a massive pain).

But if, say, [my stepdad][dave] wanted email for [his business][dave] I’d tell him to let FastMail handle his DNS settings. If I leave the Star I may switch the DNS to FastMail if there’s no-one sufficiently technical to take over from me.

[dave]: http://daveplummer.net

I did briefly switch work to use FastMail’s DNS two nights ago, to see if it enabled automatic configuration in Apple Mail or Thunderbird. No difference. (Our domain publishes SRV records that are meant to help with this and I thought I might have made a mistake, but no dice with either. Outlook may be a different story, but as we’re a mostly Mac office who cares?)

### Afterwards

The actual change in email provider should largely be invisible to your users. Your biggest problem is going to be what I’ll call user education. Some of this will be straightforward. In our case, an example was to get people to check their spam folder (we previously had daily quarantine emails).

But some will be more personal and political. That you won’t set up or support their [terrible email client][Entourage]. That email aliases really do work. That, no, their emails are not mysteriously disappearing.

A nice bonus for me is that I’m now not responsible for fixing whole categories of problems, and I’m [very confident in the FastMail staff][advent].

But frankly this whole thing has been a nightmare (including writing this damn post, which has taken forever) and it’s a huge relief to have it sorted.

[advent]: http://blog.fastmail.com/2014/12/01/fastmail-advent-2014/
