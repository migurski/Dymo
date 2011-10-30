VERSION:=$(shell cat VERSION)
PACKAGE=Dymo-$(VERSION)
TARBALL=$(PACKAGE).tar.gz

#
# Fonts here are ordered triplets of min. population, file name, font size.
#
FONTS_Z4=  --font 0 fonts/PTN57F.ttf 13   --font 250000 fonts/PTN57F.ttf 18
FONTS_Z5=  --font 0 fonts/PTN57F.ttf 13   --font 2500000 fonts/PTN57F.ttf 18
FONTS_Z6=  --font 0 fonts/PTN57F.ttf 13   --font 250000 fonts/PTN57F.ttf 18   --font 2500000 fonts/PTN57F.ttf 24
FONTS_Z7=  --font 0 fonts/PTN57F.ttf 13   --font 250000 fonts/PTN57F.ttf 18   --font 2500000 fonts/PTN57F.ttf 24
FONTS_Z8=  --font 0 fonts/PTN57F.ttf 13   --font 50000 fonts/PTN57F.ttf 18    --font 250000 fonts/PTN57F.ttf 24
FONTS_Z9=  --font 0 fonts/PTN57F.ttf 13   --font 50000 fonts/PTN57F.ttf 18    --font 250000 fonts/PTN57F.ttf 24
FONTS_Z10= --font 0 fonts/PTN57F.ttf 13   --font 50000 fonts/PTN57F.ttf 18    --font 250000 fonts/PTN57F.ttf 24
FONTS_Z11= --font 0 fonts/PTN57F.ttf 13   --font 50000 fonts/PTN57F.ttf 18    --font 250000 fonts/PTN57F.ttf 24



all: $(TARBALL)

$(TARBALL): data
	mkdir $(PACKAGE)
	ln setup.py $(PACKAGE)/
	ln VERSION $(PACKAGE)/
	ln dymo-*.py $(PACKAGE)/

	mkdir $(PACKAGE)/Dymo
	ln Dymo/*.py $(PACKAGE)/Dymo/

	rm $(PACKAGE)/Dymo/__init__.py
	cp Dymo/__init__.py $(PACKAGE)/Dymo/__init__.py
	perl -pi -e 's#\bN\.N\.N\b#$(VERSION)#' $(PACKAGE)/Dymo/__init__.py

	mkdir $(PACKAGE)/data
	ln data/Africa-*.* $(PACKAGE)/data/
	ln data/Asia-*.* $(PACKAGE)/data/
	ln data/Australia-New-Zealand-*.* $(PACKAGE)/data/
	ln data/Europe-*.* $(PACKAGE)/data/
	ln data/North-America-*.* $(PACKAGE)/data/
	ln data/South-America-*.* $(PACKAGE)/data/
	ln data/US-*.* $(PACKAGE)/data/

	mkdir $(PACKAGE)/fonts
	ln fonts/*.ttf $(PACKAGE)/fonts/

	tar -czf $(TARBALL) $(PACKAGE)
	rm -rf $(PACKAGE)

data: \
	data/North-America-z4.txt data/North-America-z5.txt \
	data/North-America-z6.txt.gz data/North-America-z7.txt.gz \
	data/North-America-z8.txt.gz data/North-America-z9.txt.gz \
	data/North-America-z10.txt.gz data/North-America-z11.txt.gz \
	data/Europe-z4.txt data/Europe-z5.txt data/Europe-z6.txt.gz \
	data/Europe-z7.txt.gz data/Europe-z8.txt.gz data/Europe-z9.txt.gz \
	data/Europe-z10.txt.gz data/Europe-z11.txt.gz \
	data/South-America-z4.txt data/South-America-z5.txt \
	data/South-America-z6.txt.gz data/South-America-z7.txt.gz \
	data/South-America-z8.txt.gz data/South-America-z9.txt.gz \
	data/South-America-z10.txt.gz data/South-America-z11.txt.gz \
	data/Asia-z4.txt data/Asia-z5.txt data/Asia-z6.txt.gz data/Asia-z7.txt.gz \
	data/Asia-z8.txt.gz data/Asia-z9.txt.gz data/Asia-z10.txt.gz \
	data/Asia-z11.txt.gz \
	data/Africa-z4.txt data/Africa-z5.txt data/Africa-z6.txt.gz \
	data/Africa-z7.txt.gz data/Africa-z8.txt.gz data/Africa-z9.txt.gz \
	data/Africa-z10.txt.gz data/Africa-z11.txt.gz \
	data/Australia-New-Zealand-z4.txt data/Australia-New-Zealand-z5.txt \
	data/Australia-New-Zealand-z6.txt.gz data/Australia-New-Zealand-z7.txt.gz \
	data/Australia-New-Zealand-z8.txt.gz data/Australia-New-Zealand-z9.txt.gz \
	data/Australia-New-Zealand-z10.txt.gz data/Australia-New-Zealand-z11.txt.gz

clean:
	find Dymo -name '*.pyc' -delete
	rm -rf $(TARBALL)




data/North-America-z4.txt: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z4) --zoom 4 data/North-America-all.txt.gz $@

data/North-America-z5.txt: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z5) --zoom 5 data/North-America-all.txt.gz $@

data/North-America-z6.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z6) --zoom 6 data/North-America-all.txt.gz $@

data/North-America-z7.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z7) --zoom 7 data/North-America-all.txt.gz $@

data/North-America-z8.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z8) --zoom 8 data/North-America-all.txt.gz $@

data/North-America-z9.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z9) --zoom 9 data/North-America-all.txt.gz $@

data/North-America-z10.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z10) --zoom 10 data/North-America-all.txt.gz $@

data/North-America-z11.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z11) --zoom 11 data/North-America-all.txt.gz $@



data/Europe-z4.txt: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z4) --zoom 4 data/Europe-all.txt.gz $@

data/Europe-z5.txt: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z5) --zoom 5 data/Europe-all.txt.gz $@

data/Europe-z6.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z6) --zoom 6 data/Europe-all.txt.gz $@

data/Europe-z7.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z7) --zoom 7 data/Europe-all.txt.gz $@

data/Europe-z8.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z8) --zoom 8 data/Europe-all.txt.gz $@

data/Europe-z9.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z9) --zoom 9 data/Europe-all.txt.gz $@

data/Europe-z10.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z10) --zoom 10 data/Europe-all.txt.gz $@

data/Europe-z11.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z11) --zoom 11 data/Europe-all.txt.gz $@



data/South-America-z4.txt: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z4) --zoom 4 data/South-America-all.txt.gz $@

data/South-America-z5.txt: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z5) --zoom 5 data/South-America-all.txt.gz $@

data/South-America-z6.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z6) --zoom 6 data/South-America-all.txt.gz $@

data/South-America-z7.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z7) --zoom 7 data/South-America-all.txt.gz $@

data/South-America-z8.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z8) --zoom 8 data/South-America-all.txt.gz $@

data/South-America-z9.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z9) --zoom 9 data/South-America-all.txt.gz $@

data/South-America-z10.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z10) --zoom 10 data/South-America-all.txt.gz $@

data/South-America-z11.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z11) --zoom 11 data/South-America-all.txt.gz $@



data/Asia-z4.txt: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z4) --zoom 4 data/Asia-all.txt.gz $@

data/Asia-z5.txt: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z5) --zoom 5 data/Asia-all.txt.gz $@

data/Asia-z6.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z6) --zoom 6 data/Asia-all.txt.gz $@

data/Asia-z7.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z7) --zoom 7 data/Asia-all.txt.gz $@

data/Asia-z8.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z8) --zoom 8 data/Asia-all.txt.gz $@

data/Asia-z9.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z9) --zoom 9 data/Asia-all.txt.gz $@

data/Asia-z10.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z10) --zoom 10 data/Asia-all.txt.gz $@

data/Asia-z11.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z11) --zoom 11 data/Asia-all.txt.gz $@



data/Africa-z4.txt: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z4) --zoom 4 data/Africa-all.txt.gz $@

data/Africa-z5.txt: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z5) --zoom 5 data/Africa-all.txt.gz $@

data/Africa-z6.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z6) --zoom 6 data/Africa-all.txt.gz $@

data/Africa-z7.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z7) --zoom 7 data/Africa-all.txt.gz $@

data/Africa-z8.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z8) --zoom 8 data/Africa-all.txt.gz $@

data/Africa-z9.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z9) --zoom 9 data/Africa-all.txt.gz $@

data/Africa-z10.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z10) --zoom 10 data/Africa-all.txt.gz $@

data/Africa-z11.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z11) --zoom 11 data/Africa-all.txt.gz $@



data/Australia-New-Zealand-z4.txt: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z4) --zoom 4 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z5.txt: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z5) --zoom 5 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z6.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z6) --zoom 6 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z7.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z7) --zoom 7 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z8.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z8) --zoom 8 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z9.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z9) --zoom 9 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z10.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z10) --zoom 10 data/Australia-New-Zealand-all.txt.gz $@

data/Australia-New-Zealand-z11.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py $(FONTS_Z11) --zoom 11 data/Australia-New-Zealand-all.txt.gz $@
