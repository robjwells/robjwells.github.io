NOW = $(shell date +'%Y-%m-%d %H:%M')
DISTID = $(shell cat cloudfront-distribution-id)


define upload-robjwells
rsync -zv -e ssh www.robjwells.com.conf rick@deckard:/srv/www/www.robjwells.com/
rsync -azv --delete -e ssh site/ rick@deckard:/srv/www/www.robjwells.com/html/
endef


define upload-github
cd gh-pages ; git add . ; git commit -m "$(NOW)" ; git push
endef


define upload-aws
aws s3 sync s3 s3://s3.robjwells.com --delete
endef


all: robjwells github aws

force-all: force-robjwells force-github force-aws

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

aws:
	majestic --settings=s3.robjwells.com.json
	$(upload-aws)

force-aws:
	majestic --settings=s3.robjwells.com.json --force-write
	$(upload-aws)
