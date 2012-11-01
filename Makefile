VERSION:=$(shell python -c 'from Dymo import __version__ as v; print v')
PACKAGE=Dymo-$(VERSION)
TARBALL=$(PACKAGE).tar.gz
DATAPKG=Dymodata-$(VERSION)
DATATAR=$(DATAPKG).tar.gz


# 
# RAW INPUT list of places, init zooms, and populations
#

INPUT_POINT_FILE_WORLD=data/World-all.txt.gz

# Adjust to your machine's cores.
CPU_PROCESSES=6

#
# RUN TIME
# Note: Time in comments should be used for full world. Default time is for test run.
#

TIME_Z4 = 1   # 1
TIME_Z5 = 2   # 4
TIME_Z6 = 4   # 12
TIME_Z7 = 8   # 60
TIME_Z8 = 15  # 120
TIME_Z9 = 30  # 240
TIME_Z10 = 60 # 600


#
# SPATIAL FILTERS
#

#SANFRANCISCO << because Stamen is in SF
FILTER_SANFRANCISCO=-124.1620 36.6332 -120.8661 39.2323

#JERUSALEM << good as it has 3 character sets to test font-set support in final renders
FILTER_JERUSALEM=31.9592 28.9312 38.5510 34.5337
    
# COMPOSITE FILTER (fast!)
SPATIAL_FILTER=  --filter-bounding-box $(FILTER_SANFRANCISCO) --filter-bounding-box $(FILTER_JERUSALEM)
# NO FILTER (slow! If no filter is desired, uncomment line below, comment out line above.)
#SPATIAL_FILTER=

#
# FONTS
#

FONT_TTF="fonts/DejaVuSans.ttf"
FONT_TTF2="fonts/DejaVuSans.ttf"

#
# Fonts here are ordered triplets of min. population, file name, font size.
#

#place-labels[zoom<8][population>=50000] name,
#place-labels[zoom=8][population>=15000] name,
#place-labels[zoom=9][population>=5000] name,
#place-labels[zoom=10][population>=1000] name,
#place-labels[zoom>=11][zoom<15][population>0] name,
#place-labels[zoom>=11][zoom<15][place=city] name,
#place-labels[zoom>=11][zoom<15][place=town] name,

FONTS_Z4=  --font 0 $(FONT_TTF2) 14   --font 500000 $(FONT_TTF2) 16
FONTS_Z5=  --font 0 $(FONT_TTF2) 14   --font 250000 $(FONT_TTF2) 16
FONTS_Z6=  --font 0 $(FONT_TTF2) 14   --font 100000 $(FONT_TTF2) 16   --font 2500000 $(FONT_TTF2) 20
FONTS_Z7=  --font 0 $(FONT_TTF2) 14   --font 100000 $(FONT_TTF2) 16   --font 2500000 $(FONT_TTF2) 20
FONTS_Z8=  --font 0 $(FONT_TTF2) 14   --font 35000 $(FONT_TTF2) 16    --font 100000 $(FONT_TTF2) 20
FONTS_Z9=  --font 0 $(FONT_TTF2) 14   --font 35000 $(FONT_TTF2) 16    --font 100000 $(FONT_TTF2) 20
FONTS_Z10= --font 0 $(FONT_TTF2) 14   --font 35000 $(FONT_TTF2) 16    --font 100000 $(FONT_TTF2) 20
#FONTS_Z11= --font 0 $(FONT_TTF2) 14   --font 35000 $(FONT_TTF2) 16    --font 100000 $(FONT_TTF2) 20

#
# TOWNSPOT SIZES (points), based on population breaks and pixel sizes
#

POINTS_Z4=  --symbol-size -1 5   --symbol-size 500000 7
POINTS_Z5=  --symbol-size -1 5   --symbol-size 250000 7
POINTS_Z6=  --symbol-size -1 5   --symbol-size 250000 7
POINTS_Z7=  --symbol-size -1 5   --symbol-size 250000 7
POINTS_Z8=  --symbol-size -1 5   --symbol-size 100000 7
POINTS_Z9=  --symbol-size -1 5   --symbol-size 100000 7
POINTS_Z10= --symbol-size -1 5   --symbol-size 100000 7
#POINTS_Z11= --symbol-size -1 5   --symbol-size 100000 7

#
# BUFFER: How much "buffer" should the large towns have around them before smaller towns start showing?
# Higher values = faster run time, but less town labels.
#

RADIUS= 6



# 
# MAIN LOGIC
#

all: $(TARBALL) $(DATATAR)

$(TARBALL):
	mkdir $(PACKAGE)
	ln setup.py $(PACKAGE)/
	ln dymo-*.py $(PACKAGE)/

	mkdir $(PACKAGE)/Dymo
	ln Dymo/*.py $(PACKAGE)/Dymo/

	rm $(PACKAGE)/Dymo/__init__.py
	ln Dymo/__init__.py $(PACKAGE)/Dymo/__init__.py

	tar -czf $(TARBALL) $(PACKAGE)
	rm -rf $(PACKAGE)

$(DATATAR): data
	mkdir $(DATAPKG)

	mkdir $(DATAPKG)/data
	ln data/World-*.* $(DATAPKG)/data/

	mkdir $(DATAPKG)/geojson
	ln data/World-*.* $(DATAPKG)/geojson/

	mkdir $(DATAPKG)/shp
	ln data/World-*.* $(DATAPKG)/shp/

	mkdir $(DATAPKG)/fonts
	ln fonts/*.ttf $(DATAPKG)/fonts/

	tar -czf $(DATATAR) $(DATAPKG)
	rm -rf $(DATAPKG)

data: data/World-z4.txt \
	  data/World-z5.txt \
	  data/World-z6.txt.gz \
	  data/World-z7.txt.gz \
	  data/World-z8.txt.gz \
	  data/World-z9-North-America.txt.gz \
	  data/World-z9-South-America.txt.gz \
	  data/World-z9-Europe.txt.gz \
	  data/World-z9-Asia.txt.gz \
	  data/World-z9-Africa.txt.gz \
	  data/World-z9-Oceania.txt.gz \
	  data/World-z10-North-America.txt.gz \
	  data/World-z10-South-America.txt.gz \
	  data/World-z10-Europe.txt.gz \
	  data/World-z10-Asia.txt.gz \
	  data/World-z10-Africa.txt.gz \
	  data/World-z10-Oceania.txt.gz
	
	touch data

clean:
	find Dymo -name '*.pyc' -delete
	rm -rf $(TARBALL)
	rm -rf $(DATATAR)


clean-data:
	rm -f geojson/*.geojson
	rm -rf shp
	mkdir -p geojson
	mkdir -p shp
	


#
# DATA FILES
# Quick to run, see GEOJSON section below for actual annealing bits
#

data/World-z4.txt: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 4 --radius $(RADIUS) $(FONTS_Z4) $(POINTS_Z4) $(SPATIAL_FILTER) data/World-all.txt.gz $@

data/World-z5.txt: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 5 --radius $(RADIUS) $(FONTS_Z5) $(POINTS_Z5) $(SPATIAL_FILTER) data/World-all.txt.gz $@

data/World-z6.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 6 --radius $(RADIUS) $(FONTS_Z6) $(POINTS_Z6) $(SPATIAL_FILTER) data/World-all.txt.gz $@

data/World-z7.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 7 --radius $(RADIUS) $(FONTS_Z7) $(POINTS_Z7) $(SPATIAL_FILTER) data/World-all.txt.gz $@

data/World-z8.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 8 --radius $(RADIUS) $(FONTS_Z8) $(POINTS_Z8) $(SPATIAL_FILTER) data/World-all.txt.gz $@


# Zoom 9

data/World-z9-North-America.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 9 --radius $(RADIUS) $(FONTS_Z9) $(POINTS_Z9) $(SPATIAL_FILTER) --filter-field continent "North America" data/World-all.txt.gz $@
	
data/World-z9-South-America.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 9 --radius $(RADIUS) $(FONTS_Z9) $(POINTS_Z9) $(SPATIAL_FILTER) --filter-field continent "South America" data/World-all.txt.gz $@
	
data/World-z9-Europe.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 9 --radius $(RADIUS) $(FONTS_Z9) $(POINTS_Z9) $(SPATIAL_FILTER) --filter-field continent "Europe" data/World-all.txt.gz $@
	
data/World-z9-Asia.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 9 --radius $(RADIUS) $(FONTS_Z9) $(POINTS_Z9) $(SPATIAL_FILTER) --filter-field continent "Asia" data/World-all.txt.gz $@
	
data/World-z9-Africa.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 9 --radius $(RADIUS) $(FONTS_Z9) $(POINTS_Z9) $(SPATIAL_FILTER) --filter-field continent "Africa" data/World-all.txt.gz $@
	
data/World-z9-Oceania.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 9 --radius $(RADIUS) $(FONTS_Z9) $(POINTS_Z9) $(SPATIAL_FILTER) --filter-field continent "Oceania" data/World-all.txt.gz $@


# Zoom 10

data/World-z10-North-America.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 10 --radius $(RADIUS) $(FONTS_Z10) $(POINTS_Z10) $(SPATIAL_FILTER) --filter-field continent "North America" data/World-all.txt.gz $@
	
data/World-z10-South-America.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 10 --radius $(RADIUS) $(FONTS_Z10) $(POINTS_Z10) $(SPATIAL_FILTER) --filter-field continent "South America" data/World-all.txt.gz $@
	
data/World-z10-Europe.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 10 --radius $(RADIUS) $(FONTS_Z10) $(POINTS_Z10) $(SPATIAL_FILTER) --filter-field continent "Europe" data/World-all.txt.gz $@
	
data/World-z10-Asia.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 10 --radius $(RADIUS) $(FONTS_Z10) $(POINTS_Z10) $(SPATIAL_FILTER) --filter-field continent "Asia" data/World-all.txt.gz $@
	
data/World-z10-Africa.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 10 --radius $(RADIUS) $(FONTS_Z10) $(POINTS_Z10) $(SPATIAL_FILTER) --filter-field continent "Africa" data/World-all.txt.gz $@
	
data/World-z10-Oceania.txt.gz: data/World-all.txt.gz
	python dymo-prepare-places.py --zoom 10 --radius $(RADIUS) $(FONTS_Z10) $(POINTS_Z10) $(SPATIAL_FILTER) --filter-field continent "Oceania" data/World-all.txt.gz $@
	

#
# GEOJSON
#
# This is the meat of Dymo where the actual simulated annealing processes are called
# It is not made by default, takes a while to chug thru
#

geojson: geojson/world-labels-z4.json \
	 geojson/world-labels-z5.json \
	 geojson/world-labels-z6.json \
	 geojson/world-labels-z7.json \
	 geojson/world-labels-z8.json \
	 geojson/world-labels-z9.json \
	 geojson/world-labels-z10.json
	 
	 touch geojson


geojson/world-labels-z4.json: data/World-z4.txt
	python dymo-label.py -z 4 --minutes $(TIME_Z4) -P $(CPU_PROCESSES) --labels-file geojson/world-labels-z4.json --places-file geojson/world-townspots-z4.json data/World-z4.txt

geojson/world-labels-z5.json: data/World-z5.txt
	python dymo-label.py -z 5 --minutes $(TIME_Z5) -P $(CPU_PROCESSES) --labels-file geojson/world-labels-z5.json --places-file geojson/world-townspots-z5.json data/World-z5.txt

geojson/world-labels-z6.json: data/World-z6.txt.gz
	python dymo-label.py -z 6 --minutes $(TIME_Z6) -P $(CPU_PROCESSES) --labels-file geojson/world-labels-z6.json --places-file geojson/world-townspots-z6.json data/World-z6.txt.gz

geojson/world-labels-z7.json: data/World-z7.txt.gz
	python dymo-label.py -z 7 --minutes $(TIME_Z7) -P $(CPU_PROCESSES) --labels-file geojson/world-labels-z7.json --places-file geojson/world-townspots-z7.json data/World-z7.txt.gz

geojson/world-labels-z8.json: data/World-z8.txt.gz
	python dymo-label.py -z 8  --minutes $(TIME_Z8) -P $(CPU_PROCESSES) --labels-file geojson/world-labels-z8.json --places-file geojson/world-townspots-z8.json data/World-z8.txt.gz

geojson/world-labels-z9.json: \
	data/World-z9-North-America.txt.gz \
	data/World-z9-South-America.txt.gz \
	data/World-z9-Europe.txt.gz \
	data/World-z9-Asia.txt.gz \
	data/World-z9-Africa.txt.gz \
	data/World-z9-Oceania.txt.gz
	python dymo-label.py -z 9  --minutes $(TIME_Z9) -P $(CPU_PROCESSES) --blobs --labels-file geojson/world-labels-z9.json --places-file geojson/world-townspots-z9.json data/World-z9-North-America.txt.gz
	python dymo-label.py -z 9  --minutes $(TIME_Z9) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z9.json --places-file geojson/world-townspots-z9.json data/World-z9-South-America.txt.gz
	python dymo-label.py -z 9  --minutes $(TIME_Z9) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z9.json --places-file geojson/world-townspots-z9.json data/World-z9-Europe.txt.gz
	python dymo-label.py -z 9  --minutes $(TIME_Z9) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z9.json --places-file geojson/world-townspots-z9.json data/World-z9-Asia.txt.gz
	python dymo-label.py -z 9  --minutes $(TIME_Z9) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z9.json --places-file geojson/world-townspots-z9.json data/World-z9-Africa.txt.gz
	python dymo-label.py -z 9  --minutes $(TIME_Z9) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z9.json --places-file geojson/world-townspots-z9.json data/World-z9-Oceania.txt.gz

geojson/world-labels-z10.json: \
	data/World-z10-North-America.txt.gz \
	data/World-z10-South-America.txt.gz \
	data/World-z10-Europe.txt.gz \
	data/World-z10-Asia.txt.gz \
	data/World-z10-Africa.txt.gz \
	data/World-z10-Oceania.txt.gz
	python dymo-label.py -z 10  --minutes $(TIME_Z10) -P $(CPU_PROCESSES) --blobs --labels-file geojson/world-labels-z10.json --places-file geojson/world-townspots-z10.json data/World-z10-North-America.txt.gz
	python dymo-label.py -z 10  --minutes $(TIME_Z10) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z10.json --places-file geojson/world-townspots-z10.json data/World-z10-South-America.txt.gz
	python dymo-label.py -z 10  --minutes $(TIME_Z10) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z10.json --places-file geojson/world-townspots-z10.json data/World-z10-Europe.txt.gz
	python dymo-label.py -z 10  --minutes $(TIME_Z10) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z10.json --places-file geojson/world-townspots-z10.json data/World-z10-Asia.txt.gz
	python dymo-label.py -z 10  --minutes $(TIME_Z10) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z10.json --places-file geojson/world-townspots-z10.json data/World-z10-Africa.txt.gz
	python dymo-label.py -z 10  --minutes $(TIME_Z10) -P $(CPU_PROCESSES) --blobs --append --labels-file geojson/world-labels-z10.json --places-file geojson/world-townspots-z10.json data/World-z10-Oceania.txt.gz



#
# SHAPEFILES
# ¡Optional!
# Warning: Requires ogr2ogr via GDAL 1.9+
# Sometimes it's nice to have SHP files instead of GeoJSON.
#

shp: geojson
			   
	rm -f shp/world_city_labels_z4.*
	rm -f shp/world_city_labels_z5.*
	rm -f shp/world_city_labels_z6.*
	rm -f shp/world_city_labels_z7.*
	rm -f shp/world_city_labels_z8.*
	rm -f shp/world_city_labels_z9.*
	rm -f shp/world_city_labels_z10.*

	rm -f shp/world_city_townspots_z4.*
	rm -f shp/world_city_townspots_z5.*
	rm -f shp/world_city_townspots_z6.*
	rm -f shp/world_city_townspots_z7.*
	rm -f shp/world_city_townspots_z8.*
	rm -f shp/world_city_townspots_z9.*
	rm -f shp/world_city_townspots_z10.*

	rm -fr shp
	mkdir shp
		
    #Important to keep the -lco else bad conversion from UTF8 original to Latin1 type
		
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z4.shp geojson/world-labels-z4.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z5.shp geojson/world-labels-z5.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z6.shp geojson/world-labels-z6.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z7.shp geojson/world-labels-z7.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z8.shp geojson/world-labels-z8.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z9.shp geojson/world-labels-z9.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_labels_z10.shp geojson/world-labels-z10.json
	
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z4.shp geojson/world-townspots-z4.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z5.shp geojson/world-townspots-z5.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z6.shp geojson/world-townspots-z6.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z7.shp geojson/world-townspots-z7.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z8.shp geojson/world-townspots-z8.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z9.shp geojson/world-townspots-z9.json
	ogr2ogr -f "ESRI Shapefile" -overwrite -lco ENCODING=UTF8 shp/world_city_townspots_z10.shp geojson/world-townspots-z10.json

	touch shp