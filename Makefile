#

ifndef PIWEB_ROOT_DIR
$(error "YOU MUST DO 'export PIWEB_ROOT_DIR=/absolute/path/to/root/dir/'.")
endif

SRCDIR		:= $(PIWEB_ROOT_DIR)/src
SCRIPTSDIR  := $(PIWEB_ROOT_DIR)/script



all:
	$(MAKE) -C $(SRCDIR)

clean:
	$(MAKE) -C $(SRCDIR) clean

install:
	$(MAKE) -C $(SRCDIR) install

dpkg: clean-dpkg install
	@$(SCRIPTSDIR)/mkdpkg.sh

clean-dpkg :
	@rm -rf dpkg/opt


.PHONY: dpkg clean-dpkg install
