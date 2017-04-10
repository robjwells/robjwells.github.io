title: Backups: the change
date: 2017-03-21 01:05

To recount from [last time][before], our backup strategy was a mess. The tools were solid but used in such a way that the common case (fast file restoration) was likely to fail, even if the rare case (complete disk failure) was covered.

[before]: /2017/03/backups-before/

That alone should have made me act sooner than I did. But ultimately the common case was so rare that the pain it caused wasn’t sufficiently motivating. That combined with an already set plan to make the change when the server hardware was changed, a reluctance to spend money that delayed the hardware change, and a near-total lack of time. So it didn’t happen for about 2.5 years after I got the job.

What finally prompted me to overhaul the backups was a nerve-wracking hour late last year when the Mac Mini server became unresponsive and would fail to start up with its external drives attached.

Detaching the drives, booting and then reattaching the drives got us back to normal. (This had happened before; I think it might have been connected to the third-party RAID driver we were using, but I don’t know that for sure.)

As a precaution I checked the server’s backups. None had completed in five days. Understand that there was no monitoring; checking required logging in to the machine and looking at the Arq interface and SuperDuper’s schedule.

The [Arq][] agent had hung and I believe [SuperDuper][SD] had too, just frozen in the middle of a scheduled copy. As I noted [before][], these are both solid pieces of software so I’m very much blaming the machine itself and the way it was set up.

[Arq]: https://www.arqbackup.com
[SD]: http://www.shirt-pocket.com

Shortly after I ordered a replacement Mac Mini (with a 1TB [Fusion][] drive that feels nearly as fast as my SSD at home) and a bunch of new external drives.

[Fusion]: https://support.apple.com/en-gb/HT202574

### Hardware

Previously we had been using various 3.5″ drives in various enclosures.

I don’t know what the professional advice about using internal drives in enclosures versus external drives, but my preference is for “real” external drives, mostly because they’re better-designed when it comes to using several of them, they seem to be better ventilated and quieter, and they’re less hassle.

All of our existing drives were several years old, the newest 2.5 years (and I managed to brick that one through impatience — a separate story), so they all needed replacing.

I bought four [4TB USB3 Toshiba][tosh] drives, which run at 7,200 RPM using drives apparently manufactured by someone else. That [review][tosh] says they’re noisy, but I’ve had all four next to my desk (in an office) since the start of the year, with at least one reading constantly (more on that later), and they’re OK. I might feel differently if I was using one in my quiet bedroom at home, but it’s hard to tell.

Funnily enough, you can no longer buy these drives from the retailer where we got them. But from memory they were about £100 each, maybe a bit less.

[tosh]: http://www.techradar.com/reviews/pc-mac/pc-components/storage/toshiba-4tb-canvio-usb-3-0-external-hard-drive-1261227/review

More recently I bought a 1TB USB3 Toshiba Canvio 2.5″ external drive to serve as a SuperDuper clone. (Not to match the 4TB Toshiba drives, but because it was well reviewed and cheaper than others.)

In sum, here’s our stock of drives:

* 1 in the Mac Mini. (You can’t buy dual-drive Minis anymore.)
* 2 Time Machine drives.
* 1 nightly SuperDuper clone.
* 1 for the 2002-2016 archives.
* 1 for the post-2016 archives.

#### Redundancy

One of the biggest changes is one that’s basically invisible. Beforehand we had loads of drives, not all of which I mentioned last time.

* 2 in the Mac Mini server.
* 2 for daily/3-hourly clones (each drive containing two partitions).
* 2 for the 2002-2011 archives.
* 2 for the post-2011 archives.

All of them were in [RAID 1][r1], where each drive contains a copy of the data. The idea behind this is that one drive can fail and you can keep going.

We were using a third-party RAID driver by a long-standing vendor. I won’t name them because I didn’t get on with the product, but I don’t want to slight it unfairly.

The RAID software frequently cried wolf — including on a new external drive that lasted 2.5 years until I broke it accidentally — so I got to a point where I just didn’t believe any of its warnings.

The worst was a pop-up once a day warning that one of the drives inside the Mini was likely to fail within the next few weeks. I got that message for over two years. I’d only infrequently log in to the Mini, so I’d have to click through weeks of pop-ups. The drive still hasn’t died.

As I’ve made clear, the machine itself was a pain to work with and that may have been the root problem. But I won’t be using the RAID driver again.

[r1]: https://en.wikipedia.org/wiki/Standard_RAID_levels#RAID_1

That experience didn’t encourage me to carry over the RAID setup, but the main factor in deciding against using RAID was cost. As we openly admit in the paper, our place isn’t flush with cash so we try to make the best use of what we’ve got.

The demise of the dual-drive Mini means that the internal drive isn’t mirrored, and that would have been the obvious candidate. So if I were to buy extra drives for a RAID mirror, it might be for the external archive drives. They are backed up but if either drive were to snuff it most of their contents would be unavailable for a period.

But buying mirror drives means that money isn’t available for other, more pressing needs.

### Backup strategy

OK, with that out of the way, let’s talk about what we *are* doing now. In short:

* Time Machine backups every 20 minutes, rotated between two drives.
* Nightly SuperDuper clones to a dedicated external drive.
* Arq backups once an hour.
* “Continuous” [Backblaze][] backups.

[Backblaze]: https://www.backblaze.com

#### Time Machine

I’m a big fan of Time Machine; I’ve been using it for years and very rarely had problems. But Time Machine [does have][mjt] [problems][jk]. I wouldn’t recommend using Time Machine by itself, particularly not if you’ve just got a single external disk.

[mjt]: http://mjtsai.com/blog/tag/timemachine/
[jk]: https://joeontech.net//why-i-dont-rely-on-time-machine.html

There are a couple of reasons for using two drives for Time Machine:

* Keep backup history if one drive dies.
* Perform backups frequently without unduly stressing a drive.
* Potentially a better chance of withstanding [a Time Machine problem][jk]. (Perhaps? Fortunately this hasn’t happened to me yet.)

Because of the nature of our work in the newsroom, a lot can change with a page or an article in a very short span of time, yet as we approach deadline there may not be any time to recreate lost work. So I run Time Machine every 20 minutes via a script.

It started off life as [a shell script by Nathan Grigg][ng], which I was first attracted to because at home my Time Machine drives sit next to my iMac — so between backups I wanted them unmounted and not making any noise. I’ve since recreated it in Python and expanded its logging.

[ng]: https://nathangrigg.com/2014/03/automounting-time-machine

Here’s the version I use at home:

    python3:
     1:  #!/usr/local/bin/python3
     2:  """Automatically start TimeMachine backups, with rotation"""
     3:  
     4:  from enum import Enum
     5:  import logging
     6:  from pathlib import Path
     7:  import subprocess
     8:  
     9:  logging.basicConfig(
    10:    level=logging.INFO,
    11:    style='{',
    12:    format='{asctime}  {levelname}  {message}',
    13:    datefmt='%Y-%m-%d %H:%M'
    14:  )
    15:  
    16:  TM_DRIVE_NAMES = [
    17:    'HG',
    18:    'Orson-A',
    19:    'Orson-B',
    20:    ]
    21:  
    22:  DiskutilAction = Enum('DiskutilAction', 'mount unmount')
    23:  
    24:  
    25:  def _diskutil_interface(drive_name: str, action: DiskutilAction) -> bool:
    26:    """Run diskutil through subprocess interface
    27:  
    28:    This is abstracted out because other the two (un)mounting functions
    29:    would duplicate much of their code.
    30:  
    31:    Returns True if the return code is 0 (success), False on failure
    32:    """
    33:    args = ['diskutil', 'quiet', action.name] + [drive_name]
    34:    return subprocess.run(args).returncode == 0
    35:  
    36:  
    37:  def mount_drive(drive_name):
    38:    """Try to mount drive using diskutil and return status code"""
    39:    return _diskutil_interface(drive_name, DiskutilAction.mount)
    40:  
    41:  
    42:  def unmount_drive(drive_name):
    43:    """Try to unmount drive using diskutil and return status code"""
    44:    return _diskutil_interface(drive_name, DiskutilAction.unmount)
    45:  
    46:  
    47:  def begin_backup():
    48:    """Back up using tmutil and return backup summary"""
    49:    args = ['tmutil', 'startbackup', '--auto', '--rotation', '--block']
    50:    result = subprocess.run(
    51:      args,
    52:      stdout=subprocess.PIPE,
    53:      stderr=subprocess.PIPE
    54:      )
    55:    if result.returncode == 0:
    56:      return (result.returncode, result.stdout.decode('utf-8'))
    57:    else:
    58:      return (result.returncode, result.stderr.decode('utf-8'))
    59:  
    60:  
    61:  def main():
    62:    drives_to_eject = []
    63:  
    64:    for drive_name in TM_DRIVE_NAMES:
    65:      if Path('/Volumes', drive_name).exists():
    66:        continue
    67:      elif mount_drive(drive_name):
    68:        drives_to_eject.append(drive_name)
    69:      else:
    70:        logging.warning(f'Failed to mount {drive_name}')
    71:  
    72:    logging.info('Beginning backup')
    73:    return_code, log_messages = begin_backup()
    74:    log_func = logging.info if return_code == 0 else logging.warning
    75:    for line in log_messages.splitlines():
    76:      log_func(line)
    77:    logging.info('Backup finished')
    78:  
    79:    for drive_name in drives_to_eject:
    80:      if not unmount_drive(drive_name):
    81:        logging.warning(f'Failed to unmount {drive_name}, trying again…')
    82:        if not unmount_drive(drive_name):
    83:          logging.warning(
    84:            f'Failed to unmount {drive_name} on second attempt')
    85:  
    86:  if __name__ == '__main__':
    87:    main()


The basic idea is the same: mount the backup drives if they’re not already, perform the backup using `tmutil`, and eject the drives that were mounted by the script afterwards. There’s nothing tricky in the script, except maybe the enum on line 22 — that’s to replace strings and risking a typo.

The arguments to `tmutil` on line 49 get Time Machine to behave as if it were running its ordinary, automatic hourly backups. The [`tmutil` online man page][tmutil] is out of date but does contain information on those options.

[tmutil]: https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man8/tmutil.8.html

The version at work is the same except that it contains some code to skip backups overnight:

    python3:
    TIME_LIMITS = (8, 23)
    
    def check_time(time, limits=TIME_LIMITS):
      """Return True if backup should proceed based on time of day"""
      early_limit, late_limit = limits
      return early_limit <= time <= late_limit

    # And called like so:
    check_time(datetime.now().hour)
    
This was written pretty late at night so it’s not the best, but it does work.

#### SuperDuper!

[SuperDuper][SD] is great, if you use it as it’s meant to be used. It runs after everyone’s gone home each evening.

I don’t look forward to booting from the 2.5″ clone drive but an external SSD was too expensive. In any case, should the Mini’s internal drive die the emergency plan is just to set up file sharing on one of our two SSD-equipped iMacs, copy over as many files as needed, and finish off the paper.

We’ve done this before when our internal network went down (a dead rack switch) and when a fire (at a nearby premises) forced us to produce the paper from a staff member’s kitchen. If such a thing happens again and the Mini is still functioning, I’d move that too as it’s not dog-slow like the old one.

In an ideal world we’d have a spare Mini ready to go, but that’s money we don’t have.

#### Arq

The Mini’s internal drive is backed up to S3. The [infrequent access][ia] storage class is used to keep the costs down, but using S3 over Glacier means we can restore files quickly.

[ia]: https://aws.amazon.com/s3/storage-classes/#Infrequent_Access

The current year’s archive and last year’s are also kept in S3, because if the archive drives die we’re more likely to need more recent editions.

All of the archives are kept in [Glacier][], but the modern storage class rather than the legacy vaults. This includes the years that are kept in S3, so that we don’t suddenly have to upload 350GB of stuff as we remove them from the more expensive storage.

[Glacier]: https://aws.amazon.com/s3/storage-classes/#Amazon_Glacier

I’m slowly removing the legacy Glacier vaults, but it takes forever. You first have to empty the vault, then wait some time so you can actually remove the vault from the list in the management console. I use [Leeroy Brun’s glacier-vault-remove][gvr] tool, to which I had to make a minor change for it to work with Python 3.6 but it was straightforward to get running. (I think it was a missing `str.encode()` or something. Yes, I know, I should submit a pull request. But it was a one-second job.)

Depending on the size of your vaults, be prepared to have the script run for a long time — this is because of the way that Glacier works (slowly). It took a couple of days for me to remove a 1.5TB-ish vault, followed by a little wait (because the vault had been “recently accessed” — to create the inventory for deletion).

[gvr]: https://github.com/leeroybrun/glacier-vault-remove

Arq’s ability to set hours during which backups should be paused is great — I could easily ensure our internet connection was fully available during the busiest part of the day.

These are set per-destination (good!) but if one destination is mid-backup and paused, your backups to other destinations won’t run. Consider this case:

* Our archive is being backed up to Glacier.
* Archive backup is paused between 3pm and 7pm.
* Backups of the server’s internal drive won’t run during 3pm to 7pm because the archive backup is “ongoing” — even if it is paused.

What that meant in practice is that the internal drive wasn’t being backed up to S3 hourly during the (weeks-long) archive backup, except if “Stop backup” is pressed during the pause interval to allow other destinations to backup.

Ideally, paused backups would be put to one side during that window of time and other destinations allowed to run.

#### Backblaze

Our initial 3.5TB [Backblaze][bb] (Star affiliate link) backup is still ongoing, at about 50GB a day over one of our two 17mbps-up fibre lines. In all it’ll have taken a couple of months, compared to a couple of weeks for Arq to S3 & Glacier.

One thing I’ve noticed from personal use at home is that Arq has no qualms about using your entire bandwidth, whereas Backblaze does seem to try not to clog your whole connection. That’s fine at home, but at work with more than one line it matters less.

I was hesitant to write this post up before we’re all set with Backblaze, but it’s got about a week to run still.

I’m interested in seeing what “continuous” backups means in practice, but the [scheduling help page][bb-sched] says: “For most computers, this results in roughly 1 backup per hour.” The important thing for me is having an additional regular remote backup separate to Arq (mostly paranoia).

[bb]: https://secure.backblaze.com/r/010t3l
[bb-sched]: https://help.backblaze.com/hc/en-us/articles/217666288-Schedule-Settings-Mac-

### Enhancements?

Were money no object, I have some ideas for improvements.

First would be to add [Google Cloud Storage][gcs] as an Arq backup destination, replicating our S3-IA/Glacier split with Google’s [Nearline/Coldline][nlcl] storage. It would “just” give us an additional Arq backup, not dependent on AWS.

A big reason why I added Backblaze is to have a remote backup that neither relied on AWS nor Arq. (That’s really not to say that I don’t trust Arq, it’s an eggs-in-one-basket thing.)

[gcs]: https://cloud.google.com/storage/
[nlcl]: https://cloud.google.com/storage/archival/

Next I’d add an additional Time Machine drive (for a total of three). Running every 20 minutes means that the load on each drive is 50% higher over two hours than the ordinary one backup per hour. Adding a third drive would mean that each drive is being backed up only once per hour. And it would also mean that there is backup history stored on *two* drives should one fail.

An external SSD to hold a SuperDuper clone is tempting, for the speed and because it might mean that we could continue to use the Mini as usual until we could get the internal drive replaced. (Though that might well be a bad idea.) Our server contains nowhere near its 1TB capacity, so we might get away with a smaller SSD.

And, maybe, instead of extra drives for RAID mirrors (as discussed above), a network-attached storage (NAS) device. But I have no experience with them nor any idea about how best to make use of one. And they seem to be a bit of a black box to me, and a major goal for our setup (Mac Mini, external drives, GUI backup programs) is to be reasonably understandable to any member of production staff — after all, we’re all journalists, not IT workers.
