SHELL = /bin/bash
GIT = /usr/bin/git
COVIDPLOTTER = src/covidplotter.py

NUM_RECENT_ENTRIES = 20

SUBMODULE_ROOT = COVID-19
CSV_HOME = $(SUBMODULE_ROOT)/csse_covid_19_data/csse_covid_19_time_series

vpath %.csv $(CSV_HOME)
vpath %.json etc

csv_basename = time_series_covid19_$(1)_global

targets = $(addprefix out/$(call csv_basename,$(1)),.png .@log.png .@population.png .@population@log.png .@density.png .@density@log.png)

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

.SECONDEXPANSION:

all: $(SUBMODULE_ROOT).pull
	$(MAKE) $(call targets,confirmed) $(call targets,deaths) $(call targets,recovered)

clean:
	rm out/*.png

%.pull:
	cd $* \
		&& $(GIT) pull

%.png: $$(notdir $$*).csv locations.json
	$(call plot,$<,$(word 2,$^),$@,$(notdir $*),"Count",1.0,identity,$(NUM_RECENT_ENTRIES))

%.@log.png: $$(notdir $$*).csv locations.json
	$(call plot,$<,$(word 2,$^),$@,$(notdir $*),"Log_e(count)",1.0,log,$(NUM_RECENT_ENTRIES))

%.@population.png: $$(notdir $$*).csv location_to_population_size.json
	$(call plot,$<,$(word 2,$^),$@,$(notdir $*),"Count / population size",0.000001,identity,$(NUM_RECENT_ENTRIES))

%.@population@log.png: $$(notdir $$*).csv location_to_population_size.json
	$(call plot,$<,$(word 2,$^),$@,$(notdir $*),"Log_e(count / population size)",0.000001,log,$(NUM_RECENT_ENTRIES))

%.@density.png: $$(notdir $$*).csv location_to_population_density.json
	$(call plot,$<,$(word 2,$^),$@,$(notdir $*),"Count / population density",1.0,identity,$(NUM_RECENT_ENTRIES))

%.@density@log.png: $$(notdir $$*).csv location_to_population_density.json
	$(call plot,$<,$(word 2,$^),$@,$(notdir $*),"Log_e(count / population density)",1.0,log,$(NUM_RECENT_ENTRIES))
