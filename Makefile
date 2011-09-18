#
# Fonts here are ordered triplets of min. population, file name, font size.
#
FONTS_Z4=  0 fonts/Arial.ttf 10   250000 fonts/Arial.ttf 12
FONTS_Z5=  0 fonts/Arial.ttf 10   2500000 fonts/Arial.ttf 12
FONTS_Z6=  0 fonts/Arial.ttf 10   250000 fonts/Arial.ttf 13   2500000 fonts/Arial.ttf 18
FONTS_Z7=  0 fonts/Arial.ttf 10   250000 fonts/Arial.ttf 13   2500000 fonts/Arial.ttf 18
FONTS_Z8=  0 fonts/Arial.ttf 10   50000 fonts/Arial.ttf 13    250000 fonts/Arial.ttf 18
FONTS_Z9=  0 fonts/Arial.ttf 10   50000 fonts/Arial.ttf 13    250000 fonts/Arial.ttf 18
FONTS_Z10= 0 fonts/Arial.ttf 10   50000 fonts/Arial.ttf 13    250000 fonts/Arial.ttf 18
FONTS_Z11= 0 fonts/Arial.ttf 10   50000 fonts/Arial.ttf 13    250000 fonts/Arial.ttf 18



all: data

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




data/North-America-z4.txt: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z4) 4 $@

data/North-America-z5.txt: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z5) 5 $@

data/North-America-z6.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z6) 6 $@

data/North-America-z7.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z7) 7 $@

data/North-America-z8.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z8) 8 $@

data/North-America-z9.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z9) 9 $@

data/North-America-z10.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z10) 10 $@

data/North-America-z11.txt.gz: data/North-America-all.txt.gz
	python dymo-prepare-places.py data/North-America-all.txt.gz $(FONTS_Z11) 11 $@



data/Europe-z4.txt: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z4) 4 $@

data/Europe-z5.txt: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z5) 5 $@

data/Europe-z6.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z6) 6 $@

data/Europe-z7.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z7) 7 $@

data/Europe-z8.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z8) 8 $@

data/Europe-z9.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z9) 9 $@

data/Europe-z10.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z10) 10 $@

data/Europe-z11.txt.gz: data/Europe-all.txt.gz
	python dymo-prepare-places.py data/Europe-all.txt.gz $(FONTS_Z11) 11 $@



data/South-America-z4.txt: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z4) 4 $@

data/South-America-z5.txt: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z5) 5 $@

data/South-America-z6.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z6) 6 $@

data/South-America-z7.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z7) 7 $@

data/South-America-z8.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z8) 8 $@

data/South-America-z9.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z9) 9 $@

data/South-America-z10.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z10) 10 $@

data/South-America-z11.txt.gz: data/South-America-all.txt.gz
	python dymo-prepare-places.py data/South-America-all.txt.gz $(FONTS_Z11) 11 $@



data/Asia-z4.txt: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z4) 4 $@

data/Asia-z5.txt: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z5) 5 $@

data/Asia-z6.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z6) 6 $@

data/Asia-z7.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z7) 7 $@

data/Asia-z8.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z8) 8 $@

data/Asia-z9.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z9) 9 $@

data/Asia-z10.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z10) 10 $@

data/Asia-z11.txt.gz: data/Asia-all.txt.gz
	python dymo-prepare-places.py data/Asia-all.txt.gz $(FONTS_Z11) 11 $@



data/Africa-z4.txt: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z4) 4 $@

data/Africa-z5.txt: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z5) 5 $@

data/Africa-z6.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z6) 6 $@

data/Africa-z7.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z7) 7 $@

data/Africa-z8.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z8) 8 $@

data/Africa-z9.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z9) 9 $@

data/Africa-z10.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z10) 10 $@

data/Africa-z11.txt.gz: data/Africa-all.txt.gz
	python dymo-prepare-places.py data/Africa-all.txt.gz $(FONTS_Z11) 11 $@



data/Australia-New-Zealand-z4.txt: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z4) 4 $@

data/Australia-New-Zealand-z5.txt: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z5) 5 $@

data/Australia-New-Zealand-z6.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z6) 6 $@

data/Australia-New-Zealand-z7.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z7) 7 $@

data/Australia-New-Zealand-z8.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z8) 8 $@

data/Australia-New-Zealand-z9.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z9) 9 $@

data/Australia-New-Zealand-z10.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z10) 10 $@

data/Australia-New-Zealand-z11.txt.gz: data/Australia-New-Zealand-all.txt.gz
	python dymo-prepare-places.py data/Australia-New-Zealand-all.txt.gz $(FONTS_Z11) 11 $@
