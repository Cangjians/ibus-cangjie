ibus_cangjie_PYTHON = \
	__init__.py \
	config.py \
	engine.py \
	$(NULL)
ibus_cangjiedir = $(pythondir)/ibus_cangjie

setup_PYTHON = \
	setup/__init__.py \
	$(NULL)
setupdir = $(ibus_cangjiedir)/setup

libexec_SCRIPTS = \
	ibus-engine-cangjie \
	setup/ibus-setup-cangjie \
	$(NULL)

CLEANFILES = \
	*.pyc \
	config.py \
	setup/*.pyc \
	$(NULL)

EXTRA_DIST = \
	config.py.in \
	ibus-engine-cangjie \
	setup/ibus-setup-cangjie \
	$(NULL)

config.py: config.py.in Makefile
	sed -e 's&@CANGJIE_GETTEXT_PACKAGE@&$(GETTEXT_PACKAGE)&g' \
	    -e 's&@LOCALEDIR@&$(localedir)&g' \
	    -e 's&@PKGDATADIR@&$(pkgdatadir)&g' $< > $@
