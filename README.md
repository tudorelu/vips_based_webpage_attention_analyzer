About
-----
This is the first version of the Webpage Analyzer program. It will take a webpage (for now a locally saved .html file works better than a URL), It will segment it's content and it will determine which parts are more visible & attractive based on color & size.


Usage
-----

**Ubuntu (Maybe Windows too)**

Open cmd from vips_java folder, then:

`
javac -cp ".:src/:lib/\*" src/org/fit/vips/\*.java"
`

followed by

`
java -cp ".:src/:lib/\*" org/fit/vips/VipsTester \[webpage\]
`

Here, webpage* can be a **local .html file** or an **URL** (tis way might not work properly).

If everything goes well (after some time - it can take up to 20 minutes, & maybe more) the program will produce a folder with some images - **blocks1.png, blocks3.png, page.png** etc. Each 'blocksN.png' is a different segmentation of the webpage - the bigger the N, the smaller the segments. 

*Next*, you copy from there **page.png** + your desired segmentation image (for example **blocks8.png**) into a folder, together with the **create_heatmap.py** script. Open the script and change the *Block_Image* variable to be the name of the segmentation image (for example **blocks8.png**) that you copied. 

And finally...

Make sure you have PIL installed (the Python Image Library). You can install it via pip.
Then, open a terminal and CD in that directory, then run 

`python create_heatmap.py`

After a few seconds, the result should appear as a png image (named **results_blocks8.png** in this example)


Credits
------

Implementation of Vision Based Page Segmentation (VIPS) algorithm in Java taken from
here:
[https://github.com/tpopela/vips_java](https://github.com/tpopela/vips_java "") 


