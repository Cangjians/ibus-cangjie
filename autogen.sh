#!/bin/bash

set -e
set -x

autopoint
libtoolize --automake --copy
intltoolize --copy --force
aclocal -I m4
autoheader
automake --add-missing --copy
autoconf
./configure $*
