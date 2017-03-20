title: Backups: the change
date: 2017-03-15 10:00
draft
What prompted me to overhaul work’s [previous backup strategy][before] was a nerve-wracking hour late last year when the Mac Mini server became unresponsive and would fail to reboot with its external drives attached.

Detaching the drives, booting and then reattaching the drives got us back to normal. (This had happened before; I think it might have been connected to the third-party RAID driver we were using, but I don't know that for sure.) 

As a precaution I checked the server's backups. None had completed in five days. Understand that there was no monitoring; checking required logging in to the machine and looking at the Arq interface and SuperDuper's schedule.

The Arq agent had hung and I believe SuperDuper had too, just frozen in the middle of a scheduled copy. As I noted [last time][before], these are both solid pieces of software so I'm very much blaming the machine itself and the way it was set up.

Shortly after I ordered a replacement Mac Mini and a bunch of new external drives.

### Hardware

Previously we had been using various different 3.5 drives in various different enclosures.

I don't know what the professional advice about using internal drives in enclosures versus external drives, but my preference is for "real" external drives, mostly because they're better-designed when it comes to using several of them, they seem to be better ventilated and quieter, and obviously they're less hassle.

All of our existing drives were several years old, the newest 2.5 years (and I managed to brick that one through impatience — a separate story), so they all needed replacing.

I bought four [4TB USB3 Toshiba][tosh] drives, which run at 7,200 RPM using drives apparently manufactured by someone else. That [review][tosh] says they’re noisy, but I’ve had all four next to my desk (in an office) since the start of the year, with at least one reading constantly (more on that later), and they're OK. I might feel 
