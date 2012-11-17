#!/bin/bash

set -e
set -x

autopoint
intltoolize --copy --force
aclocal -I m4
autoheader
automake --add-missing --copy
autoconf
./configure $*
