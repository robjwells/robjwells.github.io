NOW = $(shell date +'%Y-%m-%d %H:%M')


define upload-robjwells
rsync -zv -e ssh www.robjwells.com.conf rick@deckard:/srv/www/www.robjwells.com/
rsync -azv --delete -e ssh site/ rick@deckard:/srv/www/www.robjwells.com/html/
endef


define upload-github
cd gh-pages ; git add . ; git commit -m "$(NOW)" ; git push
endef


define upload-s3
aws s3 sync s3 s3://s3.robjwells.com --delete
endef


all: robjwells github s3

force-all: force-robjwells force-github force-s3

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

s3:
	majestic --settings=s3.robjwells.com.json
	$(upload-s3)

force-s3:
	majestic --settings=s3.robjwells.com.json --force-write
	$(upload-s3)
