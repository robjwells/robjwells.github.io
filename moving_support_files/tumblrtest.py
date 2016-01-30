#!/usr/local/bin/python3

import requests

urls = map(str.split, '''\
130587511574 /2015/10/re-unresponsive/
129586295999 /2015/09/cameron-ashcroft/
126368607134 /2015/08/pythons-counter-class-again/
126091701894 /2015/08/python-counter-gotcha-with-max/
125947006604 /2015/08/yeah/
125831941749 /2015/08/corbyn/
124189849869 /2015/07/historical-dollars/
123287249414 /2015/07/a-scripting-mess/
123026389999 /2015/07/the-automation-paradox-at-work/
122845967089 /2015/06/you-should-be-using-docopt/
122496405324 /2015/06/applescript-list-gotchas/
112039873059 /2015/02/my-email-nightmare/
108761821499 /2015/01/audio-hijack-3-and-scripts/
108366697214 /2015/01/updated-date-suffix-script/
108382504259 /2015/01/interruptions/
105859135434 /2014/12/locale-in-os-x-whats-the-current-situation/
105693102839 /2014/12/locale-in-os-x-and-launch-agents/
105480268234 /2014/12/start-and-end-of-line-shortcuts-in-bbedit/
104282032029 /2014/12/solving-boredom-with-four-languages/
82726757818  /2014/04/mano-al-teclado/
82561579583  /2014/04/manhandled/
82563133206  /2014/04/broken-mercurial-dummy-cacerts/
74634491422  /2014/01/misbehaving-single-column-nstableview/
74167330488  /2014/01/scraping-entourage/
73506147999  /2014/01/my-one-ios-7-problem/
72982090824  /2014/01/next-and-last-weekdays/
72667571379  /2014/01/hijacking-the-bbc/
67363133765  /2013/11/die-bookmarks-bar-die/
63406927107  /2013/10/date-suffixes-in-python/
61532712822  /2013/09/quit-to-linux/
61198832297  /2013/09/get-your-us-ascii-out-of-my-face/
61132555301  /2013/09/solo-diff/
59190736990  /2013/08/promptless-mercurial/
58506696571  /2013/08/terminal-countdown/
57241647827  /2013/08/commit-summary-length-hooks/
57006269554  /2013/07/hazel-gating-with-mercurial/
56625083307  /2013/07/easy-branch-comparison-with-mercurial/
56271189166  /2013/07/sunny-with-a-chance-of-python/
54764697875  /2013/07/five-different-kinds-of-grey/
54173300695  /2013/06/first-brush-with-modulo-speed/
53797469484  /2013/06/gating-hazel-with-git-status/
53871219250  /2013/06/more-precise-git-status-gating/
53765836190  /2013/06/a-new-look-and-name/
51312006146  /2013/05/restart-in-windows-the-script-strikes-back/
44699403276  /2013/03/setting-a-date-with-textexpander/
43984440715  /2013/02/blackjack/
33569049552  /2012/10/dishonored-by-the-numbers/
33015505284  /2012/10/restart-in-windows-revenge-of-the-script/
32899874477  /2012/10/whats-in-the-box/
31802717329  /2012/09/everyday-automation/
16865232551  /2012/02/the-call-of-the-weird/\
'''.split('\n'))

for tumblr_id, new_path in urls:
    response = requests.request(
        method='GET',
        url='http://deckard.robjwells.com/post/{id}/andsomegarbage'.format(id=tumblr_id),
        allow_redirects=False)
    print(
        '\t'.join([
            str(response.status_code), str(response.status_code == 301),
            response.headers['Location'],
            str(new_path in response.headers['Location'])
            ]))
