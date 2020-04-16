################################################################################
# User configuration

SHELL = /bin/bash
GIT = /usr/bin/git

TABLEPLOTTER = tableplotter/tableplotter.py
MERGE_CSSE_TIME_SERIES = ./merge_csse_time_series.py

DEATHS_KEY = deaths
CONFIRMED_KEY = confirmed
RECOVERED_KEY = recovered

AGE_KEY = median_age
AREA_KEY = land_area_in_sqkm
DENSITY_KEY = population_density_per_sqkm
POPULATION_KEY = population_size

NUM_RECENT_ENTRIES = 60
SCALE_MAP = scale_map.json

################################################################################
# Internal configuration

PIP_DEPENDENCIES = dateparser

SUBMODULE_ROOT = COVID-19
CSV_HOME = $(SUBMODULE_ROOT)/csse_covid_19_data/csse_covid_19_time_series

vpath %.csv $(CSV_HOME) $(CONFIRMED_KEY) $(DEATHS_KEY) $(RECOVERED_KEY)

csv_basename = time_series_covid19_$(1)

targets = $(addprefix $(1)/$(call csv_basename,$(1)),.png @log.png @$(POPULATION_KEY).png @$(POPULATION_KEY)@log.png @$(DENSITY_KEY).png @$(DENSITY_KEY)@log.png @$(AGE_KEY).png @$(AGE_KEY)@log.png @$(AREA_KEY).png @$(AREA_KEY)@log.png)

################################################################################
# Helper targets

.PHONY: default update dependencies clean
.SECONDARY:
.SECONDEXPANSION:

default: all

all: $(call targets,$(CONFIRMED_KEY)) $(call targets,$(DEATHS_KEY)) $(call targets,$(RECOVERED_KEY)) | $(CONFIRMED_KEY).mkdir $(DEATHS_KEY).mkdir $(RECOVERED_KEY).mkdir

update: | $(SUBMODULE_ROOT).pull
	$(MAKE) default

dependencies:
	pip3 install --user $(PIP_DEPENDENCIES)

clean:
	rm -rf ./$(CONFIRMED_KEY)/*.{png,csv} ./$(DEATHS_KEY)/*.{png,csv} ./$(RECOVERED_KEY)/*.{png,csv}

%.mkdir:
	mkdir -p $*

%.pull:
	$(GIT) -C "$*" pull

################################################################################
# Templates

define CSV_template
$(1)/time_series_covid19_$(1).csv: time_series_covid19_$(1)_global.csv $(if $(4),time_series_covid19_$(1)_US.csv)
	$(MERGE_CSSE_TIME_SERIES) \
		--primary-input $$(word 1,$$^) \
		--primary-key-fields $(2) \
		--primary-value-fields-begin $(3) \
		$(if $(4),--secondary-input $$(word 2,$$^)) \
		$(if $(4),--secondary-key-fields $(4)) \
		$(if $(4),--secondary-value-fields-begin $(5)) \
		--output $$@
endef

define PNG_template
%$(if $(1),@$(1))$(if $(3),@$(3)).png: $$$$(notdir $$$$*).csv $(SCALE_MAP)
	$(TABLEPLOTTER) \
		--input $$(word 1,$$^) \
		--scale-map $$(word 2,$$^) \
		--title $$(notdir $$*) \
		--output $$@ \
		--xlabel Date \
		--ylabel Count \
		--num-recent-columns $(NUM_RECENT_ENTRIES) \
		$(if $(1),--scale-key $(1)) \
		$(if $(2),--scale-factor $(2)) \
		$(if $(3),--yscale $(3))
endef

################################################################################
# File targets

$(eval $(call CSV_template,$(DEATHS_KEY),1 0, 4,7 6,12))
$(eval $(call CSV_template,$(CONFIRMED_KEY),1 0,4,7 6,11))
$(eval $(call CSV_template,$(RECOVERED_KEY),1 0,4))

$(eval $(call PNG_template,,,,))
$(eval $(call PNG_template,,,log))

$(eval $(call PNG_template,$(POPULATION_KEY),0.000001,))
$(eval $(call PNG_template,$(POPULATION_KEY),0.000001,log))

$(eval $(call PNG_template,$(DENSITY_KEY),,))
$(eval $(call PNG_template,$(DENSITY_KEY),,log))

$(eval $(call PNG_template,$(AGE_KEY),,))
$(eval $(call PNG_template,$(AGE_KEY),,log))

$(eval $(call PNG_template,$(AREA_KEY),0.0001,))
$(eval $(call PNG_template,$(AREA_KEY),0.0001,log))

