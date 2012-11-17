#!/bin/bash

set -e
set -x

autopoint --force
intltoolize --force --copy --automake
aclocal -I m4
autoheader
automake --add-missing --copy
autoconf
./configure $*
