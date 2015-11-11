# thegreatdictation

### contacts

lohse (--at--) cl.uni-heidelberg.de

tobygoebel (--at--) web.de

uni (--at--) dboth.de

uni (--at--) tonioweidler.de

### explanation of what i just did in code/

Created a little backend gerüst. 
I wanted to divide the backend as good as possible from the frontend.
That means: No php code in design files. that just messes things up and creates php apps à la php-cliché.
For this to achieve we needed a template engine that I just wrote.

A call to the website like example.org?p=PAGENAME shows the page PAGENAME. There is a default page if there is no p specified.

For each page there are three settings: *template, page and vars*. The template is the html file for the structure of the whole page containing the complete html template for the page, but with a placeholder for the content. This placeholder is `<tgd_body>`. The placeholder gets replaced by the content of the file specified by page. A page is a html snippet. templates are located in `frontend/`, pages in `frontend/page/`. 

So the workflow would be: Create and design the website in a template. Create a view inside a page.

For the title of a page or for other variables that should not be hardcoded in the page (like action urls of forms etc.) variables can be created in the vars array. Each occurence of `<tgd_varname>` gets replaced by vars[varname]. (Todo: expand this also to javascripts, to use varnames in ajax calls etc)

At least there is a translation engine. If strings that should be translated are used in a page or template, use the translate tag like the following: `<tgd_translate>Text to be translated</tgd_translate>`

~~The python part only works with mod_python installed, there is a `webconnector.py` that gets the requests~~ There is a index.php that takes requests adds metadata and just gives them to the `TheGreatDictator` class which later should contain the analysis. This should word on every testsystem if `tgd.py` is executable.

For questions or objections just ask me :)
