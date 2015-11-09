title: AppleScript list gotchas
date: 2015-06-26 12:05
tags: AppleScript

At work recently I ran into two subtle AppleScript oddities that tripped me up when modifying one of our production scripts.

## Return value could be a string or a list

This may be specific to InDesign but I'd be surprised (I haven't checked). When asking for:

	applescript:
	get the contents of text frame frame_name of page page_num

you could receive a string (if there's just one frame with that name) or a list of strings (if there are several).

This causes a problem when you want to compare the result to another string, because AppleScript will silently concatenate the list items and your comparison will fail.

The solution is to cast the result to a list, using `as list`. If it's already a list it's unchanged, if it's a lone string it's just wrapped in a list.

## AppleScript's for-in may not give you the value

AppleScript lets you do the following:

	applescript:
	repeat with element in the_list

which assigns (sort of) the elements of the list to the given variable name. Sort of because in some cases you don't get the value represented by `element`, you get a kind of pointer to the nth item of the list:

	applescript:
	item n of {...}

If you have a list of strings, comparing another string to the loop variable will fail, because it's not really a string. The solution is to ask for `the contents of element` or `element as string`.
