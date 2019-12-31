---
title: "Broken Mercurial dummy cacerts"
date: 2014-04-13 09:37
tags: ["Mercurial"]
---

When I tried to push [my last post][manhandled] to Bitbucket I received this ugly error:

    abort: error: _ssl.c:507: error:14090086:SSL
    routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed

[manhandled]: /2014/04/manhandled/

Gross as it is, the message is straightforward: the SSL certificate failed to verify. I imagine the root cause is the whole [OpenSSL mess][heartbleed] and everyone reissuing their certificates, but it posed an immediate practical local problem: I couldn’t push to my source control.

[heartbleed]: http://heartbleed.com

Git(hub) seemed to be fine, but any Mercurial commands involving the network — either trying to connect to Bitbucket or Kiln — would fail.

The culprit turned out to be this line in my `~/.hgrc`:

    [web]
    cacerts = /etc/hg-dummy-cert.pem

Which, as dumb as it looks, is the [recommended way][hgwiki] to enable certificate checking through the system keychain.

[hgwiki]: http://mercurial.selenic.com/wiki/CACertificates#Mac_OS_X_10.6_and_higher

Regenerating the permissions file didn’t help. Maybe this approach will work again in the future, once the wave of reissued certificates has broken, but for now there’s a straightforward solution:

1.  Remove the `cacerts` line from your `hgrc`;
2.  Use a Mercurial command such as `hg incoming` that causes it to wail about
    a server’s certificate not being verified;
3.  Using the details from that message, add a [`hostfingerprints`][hfp]
    section to your `hgrc`;
4.  Repeat with each server you connect to.
    
[hfp]: http://www.selenic.com/mercurial/hgrc.5.html#hostfingerprints

You should end up with something like this:

    [hostfingerprints]
    bitbucket.org = 45:AD:AE:1A:CF:0E:73:47…
    robjwells.kilnhg.com = c3:83:2c:5a:2d:0…

See [Bitbucket’s post][bbssl] for a few more details.

[bbssl]: http://blog.bitbucket.org/2014/04/08/bitbuckets-ssl-certificates-are-changing/
