Dependencies
============

To build IBus Cangjie, you will need the following:

* Python >= 3.2
* the Python 3 GObject bindings
* IBus >= 1.4.1 (note that its GObject-Introspection bindings must be enabled)
* pycangjie
* pycanberra: this is **optional**, only needed to play event sounds,
  especially to give feedback to the user on incorrect inputs. IBus Cangjie
  will fail gracefully if pycanberra is not available though, and just won't
  play any sound.

.. note::

    If you do want the event sounds, we require a Python 3 version of
    pycanberra, as can be found in `this (yet-unmerged) pull request`_.

.. _this (yet-unmerged) pull request: https://github.com/psykoyiko/pycanberra/pull/2

Install from a release tarball
==============================

.. note:: There are no release tarballs at this point.

From the root folder of the unpacked tarball, do the usual Autotools dance::

    $ ./configure
    $ make
    # make install

Install from a git snapshot
===========================

From the root folder of your Git clone::

    $ ./autogen.sh
    $ make
    # make install
