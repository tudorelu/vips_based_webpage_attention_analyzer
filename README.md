About
-----
This is the first part of the Webpage Analyzer program. This part will segment a webpage and extract the main areas from it.


Usage
-----

**Windows**

`
javac -cp ".:src/:lib/\*" src/org/fit/vips/\*.java"
`

then

`
java -cp ".:src/:lib/\*" org/fit/vips/VipsTester \[webpage\]
`

Here, webpage* can be a **local .html file** (but it will take a while - around 20 minutes to run) or an **URL** (unless you have very fast internet, the page will not load completely & the analysis will occur on the partially loaded page).

Credits
------

Implementation of Vision Based Page Segmentation algorithm in Java taken from
here:
[https://github.com/tpopela/vips_java](https://github.com/tpopela/vips_java "") 

The implementation utilizes CSSBox (X)HTML/CSS rendering engine written
by Radek Burget.

*Description of VIPS and **tpopela's** implementation in his master's thesis (in Czech)*

[http://www.fit.vutbr.cz/study/DP/DP.php?id=14163&file=t](http://www.fit.vutbr.cz/study/DP/DP.php?id=14163&file=t "")

*Original work by Microsoft*

[http://www.cad.zju.edu.cn/home/dengcai/VIPS/VIPS_July-2004.pdf](http://www.cad.zju.edu.cn/home/dengcai/VIPS/VIPS_July-2004.pdf "")

*CSSBox*

[http://cssbox.sourceforge.net](http://cssbox.sourceforge.net "")

