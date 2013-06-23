Dymo
====

Dymo is a placement script for map labels, isolated from the purpose-built code in
[GeoIQ’s Acetate](https://github.com/fortiusone/acetate). Dymo resolves positions for
densely-packed point labels, and results in layouts make your maps look like they’ve been
[touched by a cartographer](http://www.flickr.com/photos/mmigurski/5194528400/sizes/l/in/photostream/).

Dymo uses [Simulated Annealing](http://en.wikipedia.org/wiki/Simulated_annealing)
to derive an acceptable global label set, described in Steven Wouderberg’s
[October 2007 presentation](http://www.cs.uu.nl/docs/vakken/gd/steven2.pdf)
at Utrecht University. See an animation of the process over time in these two
videos of U.S. and European place names:

<p>
    <a href="http://vimeo.com/migurski/dymo-n-america"><img src="https://github.com/migurski/Dymo/raw/master/images/us-video-still.jpg" width="440" height="219"></a>
    <a href="http://vimeo.com/migurski/dymo-europe"><img src="https://github.com/migurski/Dymo/raw/master/images/europe-video-still.jpg" width="440" height="219"></a>
</p>

QUICK START
----------

**Demo area:** Run `make geojson` to anneal labels for San Francisco and Israel sample areas from zooms 4 to 10. This will automatically build the data files, too (eg: `make data`). Should run in less than an hour.

**World:** Annealing the entire world will take several days to several weeks and will require lots of RAM and many processor cores. Modify the `Makefile` to remove the spatial filter as below:

    # COMPOSITE FILTER (fast!)
    # SPATIAL_FILTER=  --filter-bounding-box $(FILTER_SANFRANCISCO) --filter-bounding-box $(FILTER_JERUSALEM)
    # NO FILTER (slow! If no filter is desired, uncomment line below, comment out line above.)
    SPATIAL_FILTER=

You can change the fonts and population steps in the Makefile, too.

DETAILS
----------

```dymo-label.py``` is a script that converts lists of cities with included font
information to GeoJSON point and label files suitable for use in geographic
rendering.

Mamata Akella at the National Park Service has written [a detailed tutorial on Dymo and Tile Mill](http://www.nps.gov/npmap/blog/improving-park-label-placement-with-dymo-and-tilemill.html), to “avoid label overlaps and improve the overall legibility of park names dramatically.”
The tutorial shows how to prepare data for Dymo using ArcGIS Desktop.

###Label Usage

Place U.S. city labels at zoom 6 for two minutes:

    python dymo-label.py -z 6 --minutes 2 --labels-file labels.json --places-file points.json data/US-z6.csv.gz

Place U.S. city labels at zoom 5 over a 10000-iteration 10.0 - 0.01 temperature range:

    python dymo-label.py -z 5 --steps 10000 --max-temp 10 --min-temp 0.01 -l labels.json -p points.json data/US-z5.csv

Both examples will result in a pair of GeoJSON files, ```labels.json``` and
```points.json.``` The first will contain rectangular label areas, the second
will contain center points of places successfully positioned by Dymo. Because
labels will collide in different ways depending on map scale, labels must be
placed separately for each zoom level:

![U.S. Labels](http://farm5.static.flickr.com/4123/5413923643_be14a6b13b_b.jpg)

For larger datasets, it’s almost always faster to run `dymo-label.py` with the
`--minutes` option instead of `--min-temp`/`--max-temp`, because Dymo will
automatically partition labels based on mutual overlaps and perform many small
annealing processes.

Data Included
-------------

Look in ```data/``` for a list of zoom-by-zoom city locations, organized by
continent and selected by Justin O’Bierne. Data is distributed separately from
code, see [downloads](https://github.com/migurski/Dymo/downloads) for a link.

To prepare your own city lists or modify fonts and font sizes in input lists,
Use ```dymo-prepare-places.py``` to apply population-specific font choices to
an in-bound list.

###Prepare-Places Usage

    python dymo-prepare-places.py --font 0 fonts/Arial.ttf 10 --font 1000000 fonts/Arial.ttf 12 --zoom 5 data/North-America-all.txt.gz data/North-America-z5.txt

Sample Output
-------------

These sample images were created during the development of Acetate, and show
the results of town placement.

[Central Japan](http://www.flickr.com/photos/mmigurski/5194528400/):

![Central Japan](http://farm5.static.flickr.com/4148/5194528400_abf78d0c09_b.jpg)

[Western Europe](http://www.flickr.com/photos/mmigurski/5193928891/):

![Western Europe](http://farm5.static.flickr.com/4111/5193928891_25ae4e213c_b.jpg)

[Northen Appalachians](http://www.flickr.com/photos/mmigurski/5194532290/):

![Northen Appalachians](http://farm5.static.flickr.com/4092/5194532290_96776a8241_b.jpg)

Advanced Options
----------------

###Dymo Prepare Places

* `-z ZOOM, --zoom=ZOOM` - Maximum zoom level. _Default value is `4`._
* `--zoom-field=ZOOM_FIELD` - Field to use for limiting selection by zoom. _Default field is `zoom start`._
* `-f FONTS, --font=FONTS` - Additional font, in the form of three values: minimum population number (or other font field), font file path, font size. Can be specified multiple times.
* `-r RADIUS, --radius=RADIUS` - Pixel buffer around each place. _Default value is `0`._
* `--font-field=FONT_FIELD` - Field to use for font selection. _Default field is `population`._
* `--filter-field=FILTER_FIELD` - Field to use for limiting selection by theme and the value to limit by. _Default is no filter._
* `--symbol-size=SYMBOL_SIZE` - Size in pixels for implied townspot symbol width/height in pixels. _Default size is `8`._
* `--symbol-size-field=SYMBOL_SIZE_FIELD` - Field to use for sizing the implied townspot symbol width/height in pixels. _No default._

###Dymo Label

* `-m MINUTES, --minutes=MINUTES` - Number of minutes to run annealer. Longer run times generally give better results, to a point. _Default value is `2.0`._
* `-z ZOOM, --zoom=ZOOM` -  Map zoom level. Conflicts with `--scale` and `--projection` options. _Default value is `18`._
* `-l LABELS_FILE, --labels-file=LABELS_FILE` - _Optional: name of labels file to generate._
* `-p PLACES_FILE, --places-file=PLACES_FILE` - _Optional: name of place points file to generate._
* `-r REGISTRATIONS_FILE, --registrations-file=REGISTRATIONS_FILE` - _Optional: name of registration points file to generate._ This file will have an additional "justified" field with values "left", "center", or "right".
* `--min-temp=TEMP_MIN` - Optional: Minimum annealing temperature, for more precise control than specifying --minutes.
* `--max-temp=TEMP_MAX` - Optional: Maximum annealing temperature, for more precise control than specifying --minutes.
* `--steps=STEPS` - Number of annealing steps, for more precise control than specifying --minutes.
* `--include-overlaps` - Include lower-priority places when they overlap higher-priority places. _Default behavior is to skip the overlapping cities._
* `--output-projected` - Optional: output projected coordinates.
* `--projection=PROJECTION` - Optional: PROJ.4 string to use instead of default web spherical mercator.
* `--blobs` - Load input as blobs rather than points, placing labels on top of locations instead of near them.
* `--scale=SCALE` - Scale to use with --projection. Equivalent to +to_meter PROJ.4 parameter, which is not used internally due to not quite working in pyproj. Conflicts with --zoom option. _Default value is `1`._
* `--dump-file=DUMP_FILE` - Optional: filename for a sequential dump of pickled annealer states. This all has to be stored in memory, so for a large job specifying this option could use up all available RAM.
* `--dump-skip=DUMP_SKIP` - Optional: number of states to skip for each state in the dump file.
* `--name-field=NAME_FIELD` - Name of column for labels to name themselves. _Default value is `name`._
* `--placement-field=PLACEMENT_FIELD` - Optional: name of column for point placement. Default value is `preferred placement`.

###Advanced Prepare Places Usage

* Use larger or smaller townspot symbol sizes: `--symbol-size`

        python dymo-prepare-places.py --symbol-size 6 --font 0 fonts/Arial.ttf 10 --font 1000000 fonts/Arial.ttf 12 --zoom 5 data/North-America-all.txt.gz data/North-America-z5.txt

* Use custom townspot symbol size per feature: `--symbol-size-field`

        python dymo-prepare-places.py --symbol-size-field spotsize --font 0 fonts/Arial.ttf 10 --font 1000000 fonts/Arial.ttf 12 --zoom 5 data/North-America-all.txt.gz data/North-America-z5.txt

* Use a custom 'population' attribute to size grade the text labels: `--font-field`

        python dymo-prepare-places.py --font-field rank --font 0 fonts/Arial.ttf 10 --font 1000000 fonts/Arial.ttf 12 --zoom 5 data/North-America-all.txt.gz data/North-America-z5.txt

* Limit the initial visibility of a feature to a specific zoom: `--zoom-field`

        python dymo-prepare-places.py --zoom-field init_zoom --font 0 fonts/Arial.ttf 10 --font 1000000 fonts/Arial.ttf 12 --zoom 5 data/North-America-all.txt.gz data/North-America-z5.txt

* Subselect features based on a simple filter: `--filter-field`

        python dymo-prepare-places.py --filter-field city_type capital_city --font 0 fonts/Arial.ttf 10 --font 1000000 fonts/Arial.ttf 12 --zoom 5 data/North-America-all.txt.gz data/North-America-z5.txt

* Combo:

        python dymo-prepare-places.py -z 6 --radius 1 --font 0 "fonts/Arial.ttf" 14 --font 4 "fonts/Arial Bold.ttf" 18 --font-field "sizeclass" master_data_file.tsv --zoom-field "zoom_start" --symbol-size-field "symbol_size" --filter-field region west west-labels-z6.txt


###Advanced Label Usage

* Run longer, look prettier: adjust `--minutes`, `--min-temp`, `--max-temp`, and `--steps`
* Use a custom `name` field: specify a custom `--name-field`

        python dymo-label.py --name-field name_ascii -z 6 --minutes 2 --labels-file labels.json --places-file points.json data/North-America-z5.txt

* Output multiple label, places, registration outputs: Use `--labels-file`, `--places-file`, and `--registrations-file`.

        python dymo-label.py --registrations-file registrations.json -z 6 --minutes 2 --labels-file labels.json --places-file points.json data/North-America-z5.txt

* Provide label hints to the auto-label algorithm: Use `--placement-field`.

        python dymo-label.py --placement-field hint -z 6 --minutes 2 --labels-file labels.json --places-file points.json data/North-America-z5.txt

* Manually troubleshoot overlaps in QGIS: Use `--include-overlaps` and open in QGIS and fine tune output.

        python dymo-label.py --include-overlaps -z 6 --minutes 2 --labels-file labels.json --places-file points.json data/North-America-z5.txt

* Use a custom map projection: Use `--output-projected`, `--projection`, and `--scale`

    For an Albers map of the USA, but saved in WGS84 geographic coodinates:

        python dymo-label.py --projection "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=38.0 +lon_0=-98.0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" --scale 2377 --steps 50000 --max-temp 230 --min-temp 0.0001 --labels-file northeast-labels.json east-labels-z3.txt --name-field "label" --placement-field "preferred_z3"
        
    For an Albers map of the USA, saved in that projection:

        python dymo-label.py --projection "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=38.0 +lon_0=-98.0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" --output-projected --scale 2377 --steps 50000 --max-temp 230 --min-temp 0.0001 --labels-file northeast-labels.json east-labels-z3.txt --name-field "label" --placement-field "preferred_z3"

Dependencies
-----------
Some of the advanced options, such as custom map projections, will require the following libraries: 

* Modest Maps
* Shapely
* Pyproj

For projection-specific inputs, see this [projections transform list](http://www.remotesensing.org/geotiff/proj_list/).

Tips
----

* **Converting to Esri Shapefile format:** Use [GDAL/OGR's]() `ogr2ogr` tool to convert the GeoJSON Dymo output. [QGIS](), a free desktop GIS application, will also convert the files to SHP. 

		ogr2ogr -f 'Esri Shapefile' -lco=UTF8 output.shp input.json
		
    If you have OGR 1.9+ (for the UTF8 layer creation option to preserve the unicode place names), run `make shp` from the Dymo directory and the SHP versions will be automatically created.

* **Reduce the file size** of the GeoJSON output using [Lil'JSON](https://github.com/migurski/LilJSON/):

        python LilJSON.py --precision 3 input.json output.json


Who
---

Copyright 2010-2012 Michal Migurski, Nathaniel V. Kelso, and GeoIQ, offered under the [BSD license](http://www.opensource.org/licenses/bsd-license.php). Uses Richard J. Wagner’s [Python annealing library](http://www-personal.umich.edu/~wagnerr/PythonAnneal.html).

We’re not affiliated with [Dymo Corporation](http://dymo.com).
