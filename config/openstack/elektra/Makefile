SHELL := /bin/sh

# Commands
RUBY := ruby

.PHONY: all clean

GENERATED_YAML_FILES = $(patsubst %.yaml.erb, %.yaml, $(wildcard *.yaml.erb))


all: $(GENERATED_YAML_FILES)

clean:
	rm -f $(GENERATED_YAML_FILES) 

%.yaml: %.yaml.erb vars.rb Makefile
	@echo "# Generated from $<. Do not modify manually!" > $@
	@echo "# Edit $< and run 'make' instead." >> $@
	@echo >> $@
	erb -T - -r ./vars.rb $< >> $@

replace-%: %-rc.yaml
	image=$$(kubectl get rc $* -o jsonpath='{.spec.template.spec.containers[0].image}') && \
				sed "1,/RE/s!image:.*!image: $$image!" $< | kubectl replace -f -
