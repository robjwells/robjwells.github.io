NOW = $(shell date +'%Y-%m-%d %H:%M')

all: robjwells github

robjwells:
	majestic --settings=settings.cfg
	rsync -zv -e ssh www.robjwells.com.conf rick@deckard:/srv/www/www.robjwells.com/www.robjwells.com.conf
	rsync -azv -e ssh site/ rick@deckard:/srv/www/www.robjwells.com/html

github:
	majestic --settings=robjwells.github.io.cfg
	cd gh-pages; git add . ; git commit -m "$(NOW)"; git push
