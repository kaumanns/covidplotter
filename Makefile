SHELL = /bin/bash
GIT = /usr/bin/git
COVIDPLOTTER = src/covidplotter.py

TITLE = "COVID-19 time series (John Hopkins University): Deaths"
NUM_RECENT_ENTRIES = 20

SUBMODULE_REPOSITORY = https://github.com/CSSEGISandData/COVID-19.git
SUBMODULE_ROOT = COVID-19
CSV_HOME = $(SUBMODULE_ROOT)/csse_covid_19_data/csse_covid_19_time_series
CSV_BASENAME = time_series_covid19_deaths_global

vpath %.csv $(CSV_HOME)
vpath %.json etc

.SECONDEXPANSION:

TARGETS = \
		  $(CSV_BASENAME).png \
		  $(CSV_BASENAME).@log.png \
		  $(CSV_BASENAME).@population.png \
		  $(CSV_BASENAME).@population@log.png \
		  $(CSV_BASENAME).@density.png \
		  $(CSV_BASENAME).@density@log.png

define plot =
	$(COVIDPLOTTER) \
		--input              $(1) \
		--scaling-map        $(2) \
		--output             $(3) \
		--title              $(4) \
		--ylabel             $(5) \
		--precision-factor   $(6) \
		--transformation     $(7) \
		--num-recent-entries $(8)
endef

all: $(SUBMODULE_ROOT).pull
	$(MAKE) $(TARGETS)

$(SUBMODULE_ROOT).submodule_add:
	[[ -e $(SUBMODULE_ROOT) ]] \
		|| $(GIT) add submodule $(SUBMODULE_REPOSITORY) $(SUBMODULE_ROOT)

%.pull: %.add_submodule
	cd $* \
		&& $(GIT) pull

%.png: %.csv locations.json
	$(call plot,$<,$(word 2,$^),$@,$(TITLE),"Count",1.0,identity,$(NUM_RECENT_ENTRIES))

%.@log.png: %.csv locations.json
	$(call plot,$<,$(word 2,$^),$@,$(TITLE),"Log_e(count)",1.0,log,$(NUM_RECENT_ENTRIES))

%.@population.png: %.csv location_to_population_size.json
	$(call plot,$<,$(word 2,$^),$@,$(TITLE),"Count / population size",0.000001,identity,$(NUM_RECENT_ENTRIES))

%.@population@log.png: %.csv location_to_population_size.json
	$(call plot,$<,$(word 2,$^),$@,$(TITLE),"Log_e(count / population size)",0.000001,log,$(NUM_RECENT_ENTRIES))

%.@density.png: %.csv location_to_population_density.json
	$(call plot,$<,$(word 2,$^),$@,$(TITLE),"Count / population density",1.0,identity,$(NUM_RECENT_ENTRIES))

%.@density@log.png: %.csv location_to_population_density.json
	$(call plot,$<,$(word 2,$^),$@,$(TITLE),"Log_e(count / population density)",1.0,log,$(NUM_RECENT_ENTRIES))
