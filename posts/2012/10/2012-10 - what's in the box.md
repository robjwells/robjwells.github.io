title: What’s in the box!?
date: 2012-10-05 00:00
tags: AppleScript

<p class="pic"><img src="http://f.cl.ly/items/1H130B292f363D1h442Z/SevenBox.jpg" alt="Become vengeance, David. Become wrath."></p>

### Accessing AppleScript records using a variable

AppleScript gets a lot of stick for being a rubbish language. And it is. But before last night there wasn’t anything that really threw me and made me think “wow, that’s incredibly, impressively, mind-meltingly dumb”. (Admittedly, I’m not a programmer.)

But it happened. Here’s the example code:

    applescript:
    set myRecords to {Abc:"1", Def:"2", Ghi:"3"}
    set myVar to "Abc"
    get myVar of myRecords

Try that and you’ll get a big fat error message. Why? Because there’s no property in myRecords that’s literally called myVar.

“But it’s a variable,” I hear you sob quietly into [Script Debugger][SD]. I know, I know. You were after the value of property “Abc”. Unfortunately AppleScript doesn’t let you access records in this way. If you want to access that property you need to refer to its “real” name directly in the code.

[SD]: http://www.latenightsw.com

Even to me this is ridiculous. I’ve learnt a little JavaScript with [Codecademy][] recently and you can do this very easily:

    javascript:
    var theRecords = {
        Abc: 1,
        Def: 2,
        Ghi: 3
    };
    var theVar = "Abc";
    console.log(theRecords[theVar]);

[Codecademy]:   http://www.codecademy.com/

This becomes important when you want to do something else and then refer back to the record.

What I wanted to do is store a simple name for a more complex string, and then later pass the simple name to the record and have it return the longer, hard-to-remember string. But there was no way I could hard-code the property name without defeating the entire purpose of the script I was writing. I just wanted to pass a variable containing the simple name string.

But no. Not in AppleScript.

Well, not quite. The language does not support doing this, true. But the language does let you contain a script within a script — which allows us to get past the “no variables to records” rubbish.

Thanks go to the heroic [jobu on the MacScripter forums][ms], who posted this code in 2006. (Despite being so long ago, this technique doesn’t seem to have gotten much attention, as looking at many, many forum posts about this issue has shown.)

[ms]: http://macscripter.net/viewtopic.php?pid=64151#p64151

Let’s have a look:

    applescript:
    set myRecords to {Abc:"1", Def:"2", Ghi:"3"}
    set myVar to "Abc"

    return (searchRecord(myVar, myRecords))

    to searchRecord(theKey, theRecord)
        run script "on run{theKey,theRecord}
            return (" & theKey & " of theRecord )
            end" with parameters {theKey, theRecord}
    end searchRecord

The important thing to note is that when the variable (in this case, myVar) is passed to the `run script` code, the variable’s contents are passed. That’s what you’d expect it to do, but what that means is that the variable is essentially hard-coded into this new script — you’re not recreating myVar, you’re just passing along myVar’s contents.

Boom. A regular “get value of property x of the record.” And that data is then returned from the internal script to the parent, containing script. You can then call this as you would a subroutine handler, whenever you need to get a value for an unknown-at-compile-time property.

Essentially, the shopkeeper won’t sell to you in person, but if you step outside and ring him then you’re set.

Yeah. It’s a hack. Thankfully a short, understandable one, but a hack nonetheless. It’s crazy and this should be built into the language. Here’s JavaScript’s way again, for reference:

    javascript:
    objectName[myVariable];

Why is this missing? God knows.

I’m pretty sympathetic towards AppleScript. It’s the first language I’ve ever done any kind of programming in, and it’s been — and continues to be — useful at home and essential at work. I do like it, and there’s things you can’t do without it — for better and for worse.

I plan to learn Python at some point so I may end up leaning towards “for worse” quite heavily in the future, but at the moment I’m happy using AppleScript to accomplish the (mostly work-related) things I need to do, even with all of its oddities.

(My “favourite” weird things are:

<ul>
    <li>
        <p>Getting the wrong tell target (generally)</p>
        <p>In BBEdit (for example) do I target “text window 1” or “text of text window 1”? It seems to be “text of” but I’m sure there are situations where the other is needed. The reasons why they’re two separate things aren’t clear.</p>
    </li>
    <li>
        <p>Bizarrely-scoped InDesign properties</p>
        <p>Did you know that “page range,” used when you export a .pdf, is an application-wide setting that you have to specify beforehand, not when you <em>actually export the .pdf</em>? Yeah.</p>
    </li>
    <li>
        <p>Setting page-item InDesign properties</p>
        <p>Let’s create a new frame. When we make it we can give it a bunch of properties, such as its position, size, stroke, fill, layer. How about object style? It’s listed in the options! Let’s set it alongside the position and size. Nope! It fails silently and you’re left with an unstyled frame. The way around this is to assign your new frame to a variable, and then apply the object style after you create it.</p>
    </li>
</ul>


There’s a bunch more, like slash-separated paths being treated differently from colon-separated paths — often requiring a line of code to convert them, because in many cases you can only get one type. But whatever. I’m a little worried that “proper” programming languages won’t be masochistic enough.)

<p class="pic"><img src="http://f.cl.ly/items/232I3S0E2H2V3k3v143q/SevenEnd.jpg" alt="Jesus Christ. Somebody call somebody. Call somebody."></p>
