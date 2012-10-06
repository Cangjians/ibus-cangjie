# Point to our macro directory and pick up user flags from the environment
ACLOCAL_AMFLAGS  = -I m4 ${ACLOCAL_FLAGS}

SUBDIRS = \
	src \
	po \
	$(NULL)

EXTRA_DIST = \
	autogen.sh \
	$(NULL)

noinst_DIST = \
	$(NULL)


DISTCLEANFILES = \
	po/stamp-it \
	$(NULL)

# Custom targets
superclean:
	rm -fr ABOUT-NLS aclocal.m4 autom4te.cache config.* configure \
	       install-sh ltmain.sh m4 Makefile Makefile.in missing   \
	       py-compile stamp-h1
	
	rm -fr src/cangjie.xml src/cangjie.xml.in src/ibus-engine-cangjie \
	       src/Makefile src/Makefile.in
	
	rm -fr po/Makefile po/Makefile.in po/Makefile.in.in \
	       po/Makevars.template po/POTFILES po/Rules-quot po/*.sed \
	       po/*.header po/*.sin
