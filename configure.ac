AC_PREREQ(2.63)
AC_INIT([ibus-cangjie], [0.0.1], [http://no.bug.tracker.com/ibus-cangjie], [ibus-cangjie])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])

AC_SUBST([PACKAGE_NAME], ["$PACKAGE_NAME"])
AC_SUBST([PACKAGE_VERSION], ["$PACKAGE_VERSION"])

AM_INIT_AUTOMAKE([1.11 no-dist-gzip dist-xz tar-ustar foreign])

m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

IT_PROG_INTLTOOL([0.35.0])

# i18n
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION(0.17)

GETTEXT_PACKAGE=ibus-cangjie
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE",
                   [The prefix for our gettext translation domains.])

# check deps
PKG_CHECK_MODULES(IBUS, [ibus-1.0 >= 1.3.0])
AM_PATH_PYTHON([2.5])

# define GETTEXT_* variables
GETTEXT_PACKAGE="$PACKAGE_NAME"
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Define to the read-only architecture-independent data directory.])

# OUTPUT files
AC_CONFIG_FILES([
  Makefile
  data/Makefile
  data/cangjie.xml.in
  data/quick.xml.in
  setup/Makefile
  src/Makefile
  src/ibus-engine-cangjie
  po/Makefile.in
])

AC_OUTPUT
