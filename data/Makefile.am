component_DATA = \
	cangjie.xml \
	quick.xml \
	$(NULL)
componentdir = $(datadir)/ibus/component

desktop_in_files = \
	ibus-setup-cangjie.desktop.in \
	ibus-setup-quick.desktop.in \
	$(NULL)
desktop_DATA = \
	ibus-setup-cangjie.desktop \
	ibus-setup-quick.desktop \
	$(NULL)
desktopdir = $(datadir)/applications
@INTLTOOL_DESKTOP_RULE@

CLEANFILES = \
	cangjie.xml \
	cangjie.xml.in \
	quick.xml \
	quick.xml.in \
	ibus-setup-cangjie.desktop \
	ibus-setup-cangjie.desktop.in \
	ibus-setup-quick.desktop \
	ibus-setup-quick.desktop.in \
	$(NULL)

EXTRA_DIST = \
	cangjie.xml.in.in \
	quick.xml.in.in \
	ibus-setup-cangjie.desktop.in.in \
	ibus-setup-quick.desktop.in.in \
	$(NULL)

%.xml: %.xml.in
	$(AM_V_GEN) \
	( \
		libexecdir=${libexecdir}; \
		pkgdatadir=${pkgdatadir}; \
		s=`cat $<`; \
		eval "echo \"$${s}\""; \
	) > $@

%.desktop.in: %.desktop.in.in
	$(AM_V_GEN) \
	( \
		libexecdir=${libexecdir}; \
		pkgdatadir=${pkgdatadir}; \
		s=`cat $<`; \
		eval "echo \"$${s}\""; \
	) > $@

test:
	echo "TODO: run desktop-file-validate"
