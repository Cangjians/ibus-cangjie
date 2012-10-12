engine_cangjie_PYTHON = \
	engine.py \
	main.py \
	$(NULL)
engine_cangjiedir = $(datadir)/ibus-cangjie

libexec_SCRIPTS = ibus-engine-cangjie

CLEANFILES = \
	*.pyc \
	$(NULL)

EXTRA_DIST = \
	ibus-engine-cangjie.in \
	$(NULL)

test:
	$(ENV) \
		LANG=en_US \
		PYTHONPATH=$(top_srcdir) \
		$(PYTHON) $(srcdir)/main.py
