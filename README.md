# UCWC:  Unnamed Cheapo Weather Client

It's a pretty boring weather client.  It more or less works.  It's more experiment than application.  It's pretty hideous.

## Why?

After many years of excusively using the National Weather Service data for hour-by-hour weather forecasts, I have started looking at [Open Weather Map](http://openweathermap.org) as well.

They have an [API](http://openweathermap.org/API).  So, when I decided I wanted to take Python for a spin (I haven't used it in years), a quick client to show the current conditions and forecast seemed like a reasonable project.

## What?

It's painfully procedural code using *httplib*, *xml.dom.minidom*, *ConfigParser*, and *Tkinter*.  I'll say this for Python:  If nothing else, there's at least a decent library for just about anything.

But otherwise, it's all pretty straightforward linear, procedural code.  The only way it might be remarkable is in its tedium.  It's egregious filling in all the UI elements.  It gets the job done, though.

And the code is so blindingly simple that I'm pretty sure nobody is going to need comments.  The most complicated thing in there is teasing out which libraries to import and what XML attributes to grab where.

## How?

To make this work, you need two pieces of information, put into the configuration files, and a little bit of work.

* Sign up for an account at [Open Weather Map](http://openweathermap.org) to get an API Key/Application ID.  Copy it as the value of the "user" key in the configuration file.

* Search for your town/city to get the city ID.  Copy it as the value of the "city" key in the configuration file.

* Grab the [weather icons](http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes) and convert them to GIF files.  I also cropped my copies.  With ImageMagick, it looks something like `convert $file -trim -bordercolor Transparent -border 5x1 +repage cropped_$(basename $file .png).gif`.  Why not pack them up here?  They do look like the Oxygen Project's icons, but I'd be unhappy if they turned out not to be public-licensed.  Why not find [definitely-public-licensed equivalents](https://commons.wikimedia.org/wiki/Tango_icons#Weather)?  No reason other than not wanting to over-complicate this.

* Accept the fact that, since I only wrote this for myself, this is totally ethnocentric and chauvenist.  English, degrees Fahrenheit, miles, and whatever else I could find.

Go!

Oh, right.  If there's a problem connecting to the server on either HTTP request, the program bombs out with the error status.

## What's Left?

Are you kidding?  It does only what I needed it to do, so there's pretty much an unending supply of possible enhancements.  A sampling?

* The text color is pretty hideous.  It contrasts with most of the images, but that's about it.

* Improved error handling.

* Input and caching of cities.

* Metric/imperial and language settings.

* Refactor the code.  Like, a lot.

* Don't trash the entire layout to refresh the data, since just about everything is going to be identical or at worst parallel.

* Cache recent results and don't hammer the servers, since the short-term forecasts aren't going to change second-by-second.

* Put the layout into the configuration file.

You get the idea.  It's just a toy.  This wasn't much more than a couple of hours of tinkering, and it absolutely shows.  The list is what I'd want to do first, if I considered this a serious project for other people to use.

# License

That all said, if anybody can get any use out of the thing, I license this under the terms of the GPLv3.  Of course, that's the public license.  "Negotiation" for a private license under more liberal terms is basically going to be confused with "asking."  Do you really think I'm going to fuss over two hundred lines of uncommented code in a language I don't routinely use?
