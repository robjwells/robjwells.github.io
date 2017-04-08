NOW = $(shell date +'%Y-%m-%d %H:%M')


define upload-robjwells
rsync -zv -e ssh www.robjwells.com.conf rick@deckard:/srv/www/www.robjwells.com/
rsync -azv --delete -e ssh site/ rick@deckard:/srv/www/www.robjwells.com/html/
endef


define upload-github
cd gh-pages ; git add . ; git commit -m "$(NOW)" ; git push
endef


all: robjwells github

force-all: force-robjwells force-github

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
