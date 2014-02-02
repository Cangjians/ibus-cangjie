AC_PREREQ(2.63)
AC_INIT([ibus-cangjie], [2.1], [https://github.com/Cangjians/ibus-cangjie/issues], [ibus-cangjie], [https://github.com/Cangjians/ibus-cangjie])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])

AC_SUBST([PACKAGE_NAME], ["$PACKAGE_NAME"])
AC_SUBST([PACKAGE_VERSION], ["$PACKAGE_VERSION"])

AM_INIT_AUTOMAKE([1.11 no-dist-gzip dist-xz tar-ustar foreign])
AC_PROG_MKDIR_P

m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

IT_PROG_INTLTOOL([0.35.0])

# i18n
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION(0.17)

# Note: If you change GETTEXT_PACKAGE below, you will also need to change it
#       in src/config.py, or find a way to de-hardcode it there.
GETTEXT_PACKAGE=ibus-cangjie
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE",
                   [The prefix for our gettext translation domains.])

# check for Python
AM_PATH_PYTHON([3.2.3])

# check for the cangjie Python module
AC_MSG_CHECKING([the cangjie Python module])
FOUND_PY_CANGJIE=$($PYTHON -c 'import cangjie' 2>/dev/null; echo $?)
AS_IF([test "$FOUND_PY_CANGJIE" != 0], [AC_MSG_RESULT([no]); AC_MSG_ERROR([Please install the cangjie Python module])])
AC_MSG_RESULT([yes])

# check for IBus
PKG_CHECK_MODULES(IBus, [ibus-1.0 >= 1.4.1])
AC_MSG_CHECKING(for IBus component dir)
IBUS_COMPONENT_DIR="`$PKG_CONFIG --variable=pkgdatadir ibus-1.0`/component"
AC_MSG_RESULT($IBUS_COMPONENT_DIR)

# check for the IBus bindings
AC_MSG_CHECKING([the IBus introspection-based bindings])
FOUND_PY_IBUS=$($PYTHON -c 'from gi.repository import IBus' 2>/dev/null; echo $?)
AS_IF([test "$FOUND_PY_IBUS" != 0], [AC_MSG_RESULT([no]); AC_MSG_ERROR([Please install the IBus introspection-based bindings])])
AC_MSG_RESULT([yes])

COMPONENT_DIR="${datadir}/ibus/component"
AC_SUBST(COMPONENT_DIR)

EXPANDED_COMPONENT_DIR=`eval echo $COMPONENT_DIR`

GLIB_GSETTINGS

# OUTPUT files
AC_CONFIG_FILES([
  Makefile
  po/Makefile.in
])

AC_OUTPUT

dnl ==========================================================================
echo "

    $PACKAGE $VERSION
    ==================

    python version: ${PYTHON_VERSION}
    prefix:         ${prefix}
    component dir:  ${EXPANDED_COMPONENT_DIR}

    Remember: IBus finds its engines only in $IBUS_COMPONENT_DIR by default.

    Now type 'make' to build $PACKAGE
"
