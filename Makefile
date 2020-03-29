SHELL = /bin/bash
GIT = /usr/bin/git
COVIDPLOTTER = src/covidplotter.py

NUM_RECENT_ENTRIES = 30
SCALE_MAP = scale_map.json

SUBMODULE_ROOT = COVID-19
CSV_HOME = $(SUBMODULE_ROOT)/csse_covid_19_data/csse_covid_19_time_series

vpath %.csv $(CSV_HOME)
vpath %.json etc

csv_basename = time_series_covid19_$(1)_global

targets = $(addprefix out/$(call csv_basename,$(1)),.png .@log.png .@population.png .@population@log.png .@density.png .@density@log.png)

define plot =
	$(COVIDPLOTTER) \
		--input              $(1) \
		--scale-map          $(2) \
		$(if $(3),--scale-key $(3)) \
		--output             $(4) \
		--title              $(5) \
		--scale-factor       $(6) \
		$(if $(7),--transformation $(7)) \
		--num-recent-entries $(8) \
		--xlabel 			 Date \
		--ylabel             Count
endef

.SECONDEXPANSION:

all: $(SUBMODULE_ROOT).pull
	$(MAKE) $(call targets,confirmed) $(call targets,deaths) $(call targets,recovered)

clean:
	rm out/*.png

%.pull:
	cd $* \
		&& $(GIT) pull

%.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),,$@,$(notdir $*),1.0,,$(NUM_RECENT_ENTRIES))

%.@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),,$@,$(notdir $*),1.0,log,$(NUM_RECENT_ENTRIES))

%.@population.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_size,$@,$(notdir $*),0.000001,,$(NUM_RECENT_ENTRIES))

%.@population@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_size,$@,$(notdir $*),0.000001,log,$(NUM_RECENT_ENTRIES))

%.@density.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_density_per_sqkm,$@,$(notdir $*),1.0,,$(NUM_RECENT_ENTRIES))

%.@density@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_density_per_sqkm,$@,$(notdir $*),1.0,log,$(NUM_RECENT_ENTRIES))
