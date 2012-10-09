setup_cangjie_PYTHON = \
	main.py \
	setup.ui \
	$(NULL)
setup_cangjiedir = $(pkgdatadir)/setup

bin_SCRIPTS = ibus-setup-cangjie

CLEANFILES = \
	ibus-setup-cangjie \
	*.pyc \
	$(NULL)

EXTRA_DIST = \
	ibus-setup-cangjie.in \
	$(NULL)

config.py: config.py.in Makefile
    sed -e 's&@SETUP_GETTEXT_PACKAGE@&$(GETTEXT_PACKAGE)&g' \
        -e 's&@SETUP_LOCALEDIR@&$(localedir)&g' \
        -e 's&@SETUP_PKGDATADIR@&$(pkgdatadir)&g' \
        -e 's&@SETUP_PKGLIBDIR@&$(pkglibdir)&g' $< > $@

test:
	$(ENV) DBUS_DEBUG=true \
	       PYTHONPATH=$(abs_top_srcdir):$(pyexecdir) \
	       $(PYTHON) $(srcdir)/main.py
