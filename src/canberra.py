# Copyright (c) 2012-2013 - The IBus Cangjie authors
#
# This file is part of ibus-cangjie, the IBus Cangjie input method engine.
#
# ibus-cangjie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-cangjie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-cangjie.  If not, see <http://www.gnu.org/licenses/>.


try:
    from pycanberra import (Canberra as _Canberra,
                            CA_PROP_EVENT_ID, CA_PROP_MEDIA_ROLE)

except ImportError:
    # pycanberra is optional, make it all noops if it's not installed
    class _Canberra:
        def play(self, *args, **kwargs):
            pass

    CA_PROP_EVENT_ID = None
    CA_PROP_MEDIA_ROLE = None


class Canberra:
    def __init__(self):
        self.__canberra = _Canberra()

    def play_error(self):
        self.__canberra.play(1, CA_PROP_EVENT_ID, "dialog-error",
                             CA_PROP_MEDIA_ROLE, "error", None)
