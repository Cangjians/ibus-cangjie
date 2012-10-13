pkgpython_PYTHON = \
	__init__.py \
	engine.py \
	$(NULL)
pkgpythondir = $(pythondir)/ibus_cangjie

pkgpython_setup_PYTHON = \
	setup/__init__.py \
	setup/config.py \
	setup/setup.ui \
	$(NULL)
pkgpython_setupdir = $(pythondir)/ibus_cangjie/setup

libexec_SCRIPTS = \
	ibus-engine-cangjie \
	setup/ibus-setup-cangjie \
	$(NULL)

CLEANFILES = \
	*.pyc \
	setup/config.py \
	setup/*.pyc \
	$(NULL)

EXTRA_DIST = \
	ibus-engine-cangjie \
	setup/config.py.in \
	setup/ibus-setup-cangjie \
	$(NULL)

setup/config.py: setup/config.py.in Makefile
	sed -e 's&@SETUP_GETTEXT_PACKAGE@&$(GETTEXT_PACKAGE)&g' \
	    -e 's&@SETUP_LOCALEDIR@&$(localedir)&g' \
	    -e 's&@SETUP_PKGDATADIR@&$(pkgdatadir)&g' \
	    -e 's&@SETUP_PKGLIBDIR@&$(pkglibdir)&g' $< > $@
