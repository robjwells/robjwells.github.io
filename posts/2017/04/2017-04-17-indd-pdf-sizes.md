---
title: InDesign PDF metastasis
date: 2017-04-17 22:25
---

At work we deal a lot with PDFs, both press quality and low-quality for viewing on screen. Over time I’ve automated a fair amount of the creation for both types, but one thing that I haven’t yet done is automate file-size reductions for the low-quality PDFs.

(We still use InDesign CS4 at work, so bear in mind that some or all of the below may not apply to more recent versions.)

It’s interesting to look at exactly what is making the files large enough to require slimming down in the first place. All our low-quality PDFs are exported from InDesign with the built-in “Smallest file size” preset, but the sizes are usually around 700kB for single tabloid-sized, image-sparse pages.

<img src="/images/2017-04-17-arts-full.jpg"
     class="pull-right"
     alt="A low-quality image of a Morning Star arts page.">

Let’s take Tuesday’s arts page as our example. It’s pretty basic: two small images and a medium-sized one, two drop shadows, one transparency and a fair amount of text. (That line of undermatter in the lead article was corrected before we went to print.)

But exporting using InDesign’s lowest-quality PDF preset creates a 715kB file. The images are small and rendered at a low DPI, so they’re not inflating the file.

Thankfully you can have a poke around PDF files with your favourite text editor ([BBEdit][], obviously). You’ll find a lot of “garbage” text, which I imagine is chunks of binary data, but there’s plenty of plain text you can read. The big chunks tend to be metadata. Here’s part of the first metadata block in the PDF file for the arts page:

[BBEdit]: http://www.barebones.com/products/bbedit/

    xml:
    <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP […]">
     <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
        xmlns:xmp="http://ns.adobe.com/xap/1.0/"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
        … Blah blah blah exif data etc …
      </rdf:Description>
     </rdf:RDF>
    </x:xmpmeta>

Which is the none-too-exciting block for one of the images, a Photoshop file. There’s two more like this, roughly 50–100 lines each. Then we hit a chunk which describes the InDesign file itself, with this giveaway line:

    xml:
    <xmp:CreatorTool>Adobe InDesign CS4 (6.0.6)</xmp:CreatorTool>

So what, right? InDesign includes some document and image metadata when it exports a PDF. Sure, yeah. I mean, the metadata blocks for the images weren’t too long, and this is just about their container.

Except this InDesign metadata block is 53,895 lines long in a file that’s 86,585 lines long. 574,543 characters of the document’s 714,626 — 80% of the file.

I think it’s safe to say we’ve found our culprit. But what’s going on in those 54,000 lines? Well, mostly this:

    xml:
    <xmpMM:History>
       <rdf:Seq>
          <rdf:li rdf:parseType="Resource">
             <stEvt:action>created</stEvt:action>
             <stEvt:instanceID>xmp.iid:[… hex ID …]</stEvt:instanceID>
             <stEvt:when>2012-05-22T12:55:27+01:00</stEvt:when>
             <stEvt:softwareAgent>Adobe InDesign 6.0</stEvt:softwareAgent>
          </rdf:li>
          <rdf:li rdf:parseType="Resource">
             <stEvt:action>saved</stEvt:action>
             <stEvt:instanceID>xmp.iid:[… hex ID …]</stEvt:instanceID>
             <stEvt:when>2012-05-22T12:55:54+01:00</stEvt:when>
             <stEvt:softwareAgent>Adobe InDesign 6.0</stEvt:softwareAgent>
             <stEvt:changed>/</stEvt:changed>
          </rdf:li>
        <!--  1,287 more list items  -->
       </rdf:Seq>
    </xmpMM:History>

It’s effectively a record of every time the document was saved. But if you look at the `stEvt:when` tag you’ll notice the first items are from 2012 — when our “master” InDesign file from which we derive our edition files was first created. So, the whole record of that master file is included in every InDesign file we use, and the PDFs we create from them.

Can we remove this metadata from InDesign? You can see it in <span class="osx-menu">File ▸ File Info… ▸ Advanced</span>, select it and press the rubbish bin icon. Save, quit, reopen and… it’s still there.

Thankfully Acrobat can remove this stuff from your final PDF, by going through the “PDF Optimizer” or “Save Optimized PDF” or whatever menu item it’s hiding under these days. (In the “Audit Space Usage” window it corresponds to the “Document Overhead”.)

Unfortunately Acrobat’s AppleScript support has always been poor — I’ve no idea what it’s like now, remember we’re talking CS4 — and I’ve no time nor desire to dive into Adobe’s JavaScript interface. So while you can (and we do) automate the PDF exports, you can’t slim these files down automatically with Acrobat.

Our solution at work has been to cut the cruft from the PDF using Acrobat when we use it to combine our separate page PDFs by hand. But ultimately I want to automate the whole process of exporting the PDFs, stitching them together in order, and reducing the file size.

After using [ghostscript][] for our [automatic barcode creation][barcode], I twigged that it would be useful for processing the PDFs after creation, and sure enough you can use it to slim down PDFs. Here’s an example command:

[ghostscript]: https://ghostscript.com
[barcode]: https://github.com/ppps/ms-barcode

    gs -sDEVICE=pdfwrite \
       -dPDFSETTINGS=/screen \
       -dCompatibilityLevel=1.5 \
       -dNOPAUSE -dQUIET -dBATCH \
       -sOutputFile="11_Books_180417-smaller.pdf" \
       "11_Books_180417.pdf"

Most of that is ghostscript boilerplate (it’s not exactly the friendliest tool to use), but the important option is `-dPDFSETTINGS=/screen` which, according to [one page of the sprawling docs][pdfsettings], is a predefined Adobe Distiller setting.

[pdfsettings]: https://ghostscript.com/doc/9.14/Ps2pdf.htm#Options

Using it on our 715kB example spits out an 123kB PDF that is visually identical apart from mangling the drop shadows (which I think can be solved by changing the transparency flattening settings when the PDF is exported from InDesign).
