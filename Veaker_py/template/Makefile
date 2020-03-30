# Variable
## Commands
VIVADO_HLS := $(shell python3 -c "import os, toml, pathlib; print(pathlib.Path(toml.load(os.path.expanduser('~/.alchemist/config.toml'))['path_to_vivado'])/'bin'/'vivado_hls')")

## Files
export HLS_TARGET   := {{TARGET}}
export HLS_SOLUTION := {{SOLUTION}}
HLS_HEADER          := $(wildcard include/*) $(wildcard test/include/*)
export HLS_SOURCE   := $(wildcard src/*)
export HLS_TEST     := $(wildcard test/src/*)

## Products
IP    = $(HLS_TARGET)/$(HLS_SOLUTION)/impl
COSIM = $(HLS_TARGET)/$(HLS_SOLUTION)/sim
HDL   = $(HLS_TARGET)/$(HLS_SOLUTION)/syn
CSIM  = $(HLS_TARGET)/$(HLS_SOLUTION)/csim

##### targets and commands #####

.PHONY: all
all: $(IP)

$(IP): $(HDL)
	$(VIVADO_HLS) script/export.tcl
	touch $@

$(HDL): $(HLS_TARGET) $(HLS_HEADER) $(HLS_SOURCE) $(HLS_TEST)
	$(VIVADO_HLS) script/csynth.tcl
	touch $@

.PHONY: csim
csim: $(HLS_TARGET)
	$(VIVADO_HLS) script/csim.tcl

$(HLS_TARGET):
	$(VIVADO_HLS) script/init.tcl

.PHONY: clean
clean:
	rm -rf $(HLS_TARGET) *.log
