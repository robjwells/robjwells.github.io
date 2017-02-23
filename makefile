NOW = $(shell date +'%Y-%m-%d %H:%M')


define upload-robjwells
rsync -zv -e ssh www.robjwells.com.conf rick@deckard:/srv/www/www.robjwells.com/
rsync -azv -e ssh site/ rick@deckard:/srv/www/www.robjwells.com/html/
endef


define upload-github
cd gh-pages ; git add . ; git commit -m "$(NOW)" ; git push
endef


all: robjwells github

force-all: force-robjwells force-github

robjwells:
	majestic --settings=settings.cfg
	$(upload-robjwells)

force-robjwells:
	majestic --settings=settings.cfg --force-write
	$(upload-robjwells)

github:
	majestic --settings=robjwells.github.io.cfg
	$(upload-github)

force-github:
	majestic --settings=robjwells.github.io.cfg --force-write
	$(upload-github)
