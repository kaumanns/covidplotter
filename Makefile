SHELL = /bin/bash
PYTHON = /usr/bin/python3
COVIDPLOTTER = src/covidplotter.py

TITLE_PREFIX = COVID-19 time series (John Hopkins)
NUM_RECENT_ENTRIES = 20

# CSV_BASENAME = time_series_covid19_deaths_global
CSV_BASENAME = time_series_19-covid-Deaths
CSV_URL = https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/$(CSV_BASENAME).csv

vpath %.json etc

TARGETS = \
		  $(CSV_BASENAME).png \
		  $(CSV_BASENAME).@log.png \
		  $(CSV_BASENAME).@population.png \
		  $(CSV_BASENAME).@population@log.png \
		  $(CSV_BASENAME).@density.png \
		  $(CSV_BASENAME).@density@log.png

all: $(TARGETS)

$(CSV_BASENAME).csv:
	curl $(CSV_URL) --output $@

%.png: %.csv locations.json $(COVIDPLOTTER)
	$(PYTHON) $(word 3,$^) \
		--input $(word 1,$^) \
		--denominators $(word 2,$^) \
		--title "$(TITLE_PREFIX)" \
		--num-recent-entries $(NUM_RECENT_ENTRIES) \
		--transformation identity \
		--output $@

%.@log.png: %.csv locations.json $(COVIDPLOTTER)
	$(PYTHON) $(word 3,$^) \
		--input $(word 1,$^) \
		--denominators $(word 2,$^) \
		--title "$(TITLE_PREFIX)" \
		--num-recent-entries $(NUM_RECENT_ENTRIES) \
		--transformation log \
		--output $@

%.@population.png: %.csv location_to_population_size.json $(COVIDPLOTTER)
	$(PYTHON) $(word 3,$^) \
		--input $(word 1,$^) \
		--denominators $(word 2,$^) \
		--title "$(TITLE_PREFIX) scaled by population size" \
		--num-recent-entries $(NUM_RECENT_ENTRIES) \
		--transformation identity \
		--output $@

%.@population@log.png: %.csv location_to_population_size.json $(COVIDPLOTTER)
	$(PYTHON) $(word 3,$^) \
		--input $(word 1,$^) \
		--denominators $(word 2,$^) \
		--title "$(TITLE_PREFIX) scaled by population size" \
		--num-recent-entries $(NUM_RECENT_ENTRIES) \
		--transformation log \
		--output $@

%.@density.png: %.csv location_to_population_density.json $(COVIDPLOTTER)
	$(PYTHON) $(word 3,$^) \
		--input $(word 1,$^) \
		--denominators $(word 2,$^) \
		--title "$(TITLE_PREFIX) scaled by population density" \
		--num-recent-entries $(NUM_RECENT_ENTRIES) \
		--transformation identity \
		--output $@

%.@density@log.png: %.csv location_to_population_density.json $(COVIDPLOTTER)
	$(PYTHON) $(word 3,$^) \
		--input $(word 1,$^) \
		--denominators $(word 2,$^) \
		--title "$(TITLE_PREFIX) scaled by population density" \
		--num-recent-entries $(NUM_RECENT_ENTRIES) \
		--transformation log \
		--output $@

