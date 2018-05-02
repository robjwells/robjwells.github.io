#!/usr/local/bin/python3

import fileinput
import re

block_boundary = re.compile(r'^~~~~(?: (\S+))?$')
indent = ' ' * 4

new_lines = []
in_block = False


for line in fileinput.input():
    if in_block and block_boundary.match(line):
        in_block = False
        new_lines.append('\n<!-- Comment to separate R code and output -->\n')
        continue

    if block_boundary.match(line):
        in_block = True
        new_lines.append(
            block_boundary.sub(indent + '\g<1>:', line))
        continue

    if in_block:
        new_lines.append(indent + line)
        continue

    new_lines.append(line)


image_html = '''\
<p class="full-width">
    <img
        src="/images/{date}-{fn}"
        alt="<#alt text#>"
        class="no-border"
        width=720
        />
</p>
'''


date_lines = [l[6:16] for l in new_lines if l.startswith('date: ')]
if not date_lines:
    date_prefix = ''
else:
    date_prefix = date_lines[0]


# Rewrite images
for idx, line in enumerate(new_lines):
    if line.startswith('![]('):
        fn = line.rstrip()[:-1].rsplit('/', maxsplit=1)[-1]
        new_lines[idx] = image_html.format(date=date_prefix, fn=fn)


print(''.join(new_lines))
