################################################################################
# Configuration

SHELL = /bin/bash
GIT = /usr/bin/git
TABLEPLOTTER = tableplotter/tableplotter.py

CONFIRMED_KEY = confirmed
DEATHS_KEY = deaths
RECOVERED_KEY = recovered

PIP_DEPENDENCIES = dateparser

NUM_RECENT_ENTRIES = 60
SCALE_MAP = scale_map.json

SUBMODULE_ROOT = COVID-19
CSV_HOME = $(SUBMODULE_ROOT)/csse_covid_19_data/csse_covid_19_time_series

vpath %.csv $(CSV_HOME) $(CONFIRMED_KEY) $(DEATHS_KEY) $(RECOVERED_KEY)

csv_basename = time_series_covid19_$(1)

targets = $(addprefix $(1)/$(call csv_basename,$(1)),.png .@log.png .@population.png .@population@log.png .@density.png .@density@log.png .@age.png .@age@log.png .@land.png .@land@log.png)

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

define CSV_template
$(1)/time_series_covid19_$(1).csv: time_series_covid19_$(1)_global.csv $(if $(4),time_series_covid19_$(1)_US.csv)
	./merge_csse_time_series.py \
		--primary-input $$(word 1,$$^) \
		--primary-key-fields $(2) \
		--primary-value-fields-begin $(3) \
		$(if $(4),--secondary-input $$(word 2,$$^)) \
		$(if $(4),--secondary-key-fields $(4)) \
		$(if $(4),--secondary-value-fields-begin $(5)) \
		--output $$@
endef
$(eval $(call CSV_template,$(DEATHS_KEY),1 0, 4,7 6,12))
$(eval $(call CSV_template,$(CONFIRMED_KEY),1 0,4,7 6,11))
$(eval $(call CSV_template,$(RECOVERED_KEY),1 0,4))

################################################################################
# File targets

define plot
	$(TABLEPLOTTER) \
		--input $(1) \
		--scale-map $(2) \
		$(if $(3),--scale-key $(3)) \
		--output $(4) \
		--title $(5) \
		$(if $(6),--scale-factor $(6)) \
		$(if $(7),--yscale $(7)) \
		--num-recent-columns $(8) \
		--xlabel Date \
		--ylabel Count
endef

%.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),,$@,$(notdir $*),,,$(NUM_RECENT_ENTRIES))

%.@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),,$@,$(notdir $*),,log,$(NUM_RECENT_ENTRIES))

%.@population.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_size,$@,$(notdir $*),0.000001,,$(NUM_RECENT_ENTRIES))

%.@population@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_size,$@,$(notdir $*),0.000001,log,$(NUM_RECENT_ENTRIES))

%.@density.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_density_per_sqkm,$@,$(notdir $*),,,$(NUM_RECENT_ENTRIES))

%.@density@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),population_density_per_sqkm,$@,$(notdir $*),,log,$(NUM_RECENT_ENTRIES))

%.@age.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),median_age,$@,$(notdir $*),,,$(NUM_RECENT_ENTRIES))

%.@age@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),median_age,$@,$(notdir $*),,log,$(NUM_RECENT_ENTRIES))

%.@land.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),land_area_in_sqkm,$@,$(notdir $*),0.0001,,$(NUM_RECENT_ENTRIES))

%.@land@log.png: $$(notdir $$*).csv $(SCALE_MAP)
	$(call plot,$<,$(word 2,$^),land_area_in_sqkm,$@,$(notdir $*),0.0001,log,$(NUM_RECENT_ENTRIES))

