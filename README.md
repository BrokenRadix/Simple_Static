Simple Static
=========

A script to help make generating static sites super simple.

Description
-----
Simple Static was created to help create simple websites, without the need for installing anything but some basic python modules.

Using Simple Static should be... well, simple; as there are a few concepts that one needs to understand:

- Running Simple Static in an empty directory creates two directories:
    - "source" and "build"
- By default, Simple Static will backup your "build" directory if it exists
    - This can be disabled with: ``` $ python simple_static.py -db ```
- The directory where you will do all your editing is the "source" directory. It has three sub directories:
    - "assets" --> your media/css/js/etc
    - "elements" --> these files will be injected into your pages
        - these are likely your global code (header/footer/ads/etc)
    - "pages" --> these are your unique pages in which you will place your tags, which inject the content of the elements files
        - the default tag is ```#### element_name ####```
            - (four hashtags + space + name of element + space + four hashtags)


How It Works
-----
Simple Static works by scanning all the files in the "pages" directory, looking for specifically tagged references to files in the "elements" directory.

For example, if you have the following in your "source/pages/index.html",
```
#### header ####
<div>Home Page</div>
```
and you have the following in "elements/header.html",
```
<script>console.log("That IS simple!")</script>
```
after you run,
```
$ python simple_static
```
you will have the following in "build/index.html",
```
<script>console.log("That IS simple!")</script>
<div>Home Page</div>
```
Usage
-----
To use Simple Static, you can either:
- use the included "example_source" by renaming it to "source" and running Simple Static
- run Simple Static in an empty directory and create the site from scratch (see below)
    - the script will create the minimum require files for you

Example run, in an empty directory, with verbose messages:
```
$ python simple_static.py -v
DEBUG:root:No './source' directory, creating one at: ./source
DEBUG:root:No './source/assets' directory, creating one at: ./source/assets
DEBUG:root:No './source/elements' directory, creating one at: ./source/elements
DEBUG:root:No './source/pages' directory, creating one at: ./source/pages
DEBUG:root:No './source/elements/header.html' file, creating one at: ./source/elements/header.html
DEBUG:root:No './source/elements/footer.html' file, creating one at: ./source/elements/footer.html
DEBUG:root:No './source/pages/index.html' file, creating one at: ./source/pages/index.html
DEBUG:root:Done: created ./build
```
```
$ python simple_static.py -v
DEBUG:root:Moving ./build to ./build.20150720_212322.bak
DEBUG:root:Done: created ./build
```
Example of disabling the default backups:
```
$ python simple_static.py -v -db
DEBUG:root:Removing ./build
DEBUG:root:Done: created ./build
```
