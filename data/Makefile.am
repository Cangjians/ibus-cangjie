component_DATA = cangjie.xml
componentdir = $(datadir)/ibus/component

CLEANFILES = \
	$(NULL)

EXTRA_DIST = \
	cangjie.xml.in.in \
	$(NULL)

cangjie.xml: cangjie.xml.in
	$(AM_V_GEN) \
	( \
		libexecdir=${libexecdir}; \
		pkgdatadir=${pkgdatadir}; \
		s=`cat $<`; \
		eval "echo \"$${s}\""; \
	) > $@

test:
	echo "TODO: run desktop-file-validate"
