engine_cangjie_PYTHON = \
	engine.py \
	factory.py \
	main.py \
	$(NULL)
engine_cangjiedir = $(datadir)/ibus-cangjie

bin_SCRIPTS = ibus-engine-cangjie

component_DATA = cangjie.xml
componentdir = $(datadir)/ibus/component

CLEANFILES = \
	*.pyc \
	$(NULL)

EXTRA_DIST = \
	ibus-engine-cangjie.in \
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
	$(ENV) \
		LANG=en_US \
		PYTHONPATH=$(top_srcdir) \
		$(PYTHON) $(srcdir)/main.py
