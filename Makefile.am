# Point to our macro directory and pick up user flags from the environment
ACLOCAL_AMFLAGS  = -I m4 ${ACLOCAL_FLAGS}

# Keep recursive, the tools depend on it
SUBDIRS = po


# -- data/ ---------------------------
ibus_cangjie_data_DATA = \
	data/setup.ui \
	$(NULL)
ibus_cangjie_datadir = $(pkgdatadir)

component_DATA = \
	data/cangjie.xml \
	data/quick.xml \
	$(NULL)
componentdir = $(datadir)/ibus/component

desktop_in_files = \
	data/ibus-setup-cangjie.desktop.in \
	data/ibus-setup-quick.desktop.in \
	$(NULL)
desktop_DATA = \
	data/ibus-setup-cangjie.desktop \
	data/ibus-setup-quick.desktop \
	$(NULL)
desktopdir = $(datadir)/applications
@INTLTOOL_DESKTOP_RULE@

%.xml: %.xml.in
	$(AM_V_GEN) \
	( \
		libexecdir=${libexecdir}; \
		s=`cat $<`; \
		eval "echo \"$${s}\""; \
	) > $@

%.desktop.in: %.desktop.in.in
	$(AM_V_GEN) \
	( \
		libexecdir=${libexecdir}; \
		s=`cat $<`; \
		eval "echo \"$${s}\""; \
	) > $@


# -- src/ ----------------------------
ibus_cangjie_PYTHON = \
	src/__init__.py \
	src/engine.py \
        src/pycanberra.py \
	$(NULL)
ibus_cangjiedir = $(pythondir)/ibus_cangjie
nodist_ibus_cangjie_PYTHON = src/config.py

ibus_cangjie_setup_PYTHON = \
	src/setup/__init__.py \
	$(NULL)
ibus_cangjie_setupdir = $(ibus_cangjiedir)/setup

libexec_SCRIPTS = \
	scripts/ibus-engine-cangjie \
	scripts/ibus-setup-cangjie \
	$(NULL)

src/config.py: src/config.py.in Makefile
	$(MKDIR_P) src
	sed -e 's&@CANGJIE_GETTEXT_PACKAGE@&$(GETTEXT_PACKAGE)&g' \
	    -e 's&@LOCALEDIR@&$(localedir)&g' \
	    -e 's&@PKGDATADIR@&$(pkgdatadir)&g' $< > $@

BUILT_SOURCES = src/config.py

# -- Common --------------------------
CLEANFILES = \
	data/cangjie.xml \
	data/cangjie.xml.in \
	data/quick.xml \
	data/quick.xml.in \
	data/ibus-setup-cangjie.desktop \
	data/ibus-setup-cangjie.desktop.in \
	data/ibus-setup-quick.desktop \
	data/ibus-setup-quick.desktop.in \
	scripts/ibus-engine-cangjie \
	scripts/ibus-setup-cangjie \
	src/*.pyc \
	src/config.py \
	src/setup/*.pyc \
	$(NULL)

EXTRA_DIST = \
	autogen.sh \
	data/setup.ui \
	data/ibus-setup-cangjie.desktop.in.in \
	data/ibus-setup-quick.desktop.in.in \
	src/config.py.in \
	$(NULL)

# Custom targets
superclean:
	rm -fr ABOUT-NLS aclocal.m4 autom4te.cache config.* configure \
	       install-sh ltmain.sh m4 Makefile Makefile.in missing   \
	       py-compile stamp-h1
	
	rm -fr po/Makefile po/Makefile.in po/Makefile.in.in \
	       po/Makevars.template po/POTFILES po/Rules-quot po/*.sed \
	       po/*.header po/*.sin po/stamp-it po/.intltool-merge-cache
