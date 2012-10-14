ibus_cangjie_PYTHON = \
	__init__.py \
	config.py \
	engine.py \
	$(NULL)
ibus_cangjiedir = $(pythondir)/ibus_cangjie

setup_PYTHON = \
	setup/__init__.py \
	setup/setup.ui \
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
	sed -e 's&@SETUP_GETTEXT_PACKAGE@&$(GETTEXT_PACKAGE)&g' \
	    -e 's&@SETUP_LOCALEDIR@&$(localedir)&g' \
	    -e 's&@SETUP_PKGDATADIR@&$(pkgdatadir)&g' \
	    -e 's&@SETUP_PKGLIBDIR@&$(pkglibdir)&g' $< > $@
