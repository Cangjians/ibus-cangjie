##########################################################################
# pycanberra.py: simple wrapper around most of the libcanberra public api
# Author: Dave Barry <dave@psax.org>
# License: LGPL 2.1
##########################################################################
from ctypes import *
import time

# This is inspired by the six module: http://pypi.python.org/pypi/six
import sys
if sys.version_info.major == 3:
    string_types = str,
    def b(s):
        return s.encode("latin-1")
else:
    string_types = basestring,
    def b(s):
        return s


# /**
#  * CA_PROP_MEDIA_NAME:
#  *
#  * A name describing the media being played. Localized if possible and applicable.
#  */
CA_PROP_MEDIA_NAME = "media.name"

# /**
#  * CA_PROP_MEDIA_TITLE:
#  *
#  * A (song) title describing the media being played. Localized if possible and applicable.
#  */
CA_PROP_MEDIA_TITLE = "media.title"

# /**
#  * CA_PROP_MEDIA_ARTIST:
#  *
#  * The artist of this media. Localized if possible and applicable.
#  */
CA_PROP_MEDIA_ARTIST = "media.artist"

# /**
#  * CA_PROP_MEDIA_LANGUAGE:
#  *
#  * The language this media is in, in some standard POSIX locale string, such as "de_DE".
#  */
CA_PROP_MEDIA_LANGUAGE = "media.language"

# /**
#  * CA_PROP_MEDIA_FILENAME:
#  *
#  * The file name this media was or can be loaded from.
#  */
CA_PROP_MEDIA_FILENAME = "media.filename"

# /**
#  * CA_PROP_MEDIA_ICON:
#  *
#  * An icon for this media in binary PNG format.
#  */
CA_PROP_MEDIA_ICON = "media.icon"

# /**
#  * CA_PROP_MEDIA_ICON_NAME:
#  *
#  * An icon name as defined in the XDG icon naming specifcation.
#  */
CA_PROP_MEDIA_ICON_NAME = "media.icon_name"

# /**
#  * CA_PROP_MEDIA_ROLE:
#  *
#  * The "role" this media is played in. For event sounds the string
#  * "event". For other cases strings like "music", "video", "game", ...
#  */
CA_PROP_MEDIA_ROLE = "media.role"

# /**
#  * CA_PROP_EVENT_ID:
#  *
#  * A textual id for an event sound, as mandated by the XDG sound naming specification.
#  */
CA_PROP_EVENT_ID = "event.id"

# /**
#  * CA_PROP_EVENT_DESCRIPTION:
#  *
#  * A descriptive string for the sound event. Localized if possible and applicable.
#  */
CA_PROP_EVENT_DESCRIPTION = "event.description"
 
# /**
#  * CA_PROP_EVENT_MOUSE_X:
#  *
#  * If this sound event was triggered by a mouse input event, the X
#  * position of the mouse cursor on the screen, formatted as string.
#  */
CA_PROP_EVENT_MOUSE_X = "event.mouse.x"
 
# /**
#  * CA_PROP_EVENT_MOUSE_Y:
#  *
#  * If this sound event was triggered by a mouse input event, the Y
#  * position of the mouse cursor on the screen, formatted as string.
#  */
CA_PROP_EVENT_MOUSE_Y = "event.mouse.y"
 
# /**
#  * CA_PROP_EVENT_MOUSE_HPOS:
#  *
#  * If this sound event was triggered by a mouse input event, the X
#  * position of the mouse cursor as fractional value between 0 and 1,
#  * formatted as string, 0 reflecting the left side of the screen, 1
#  * the right side.
#  */
CA_PROP_EVENT_MOUSE_HPOS = "event.mouse.hpos"
 
# /**
#  * CA_PROP_EVENT_MOUSE_VPOS:
#  *
#  * If this sound event was triggered by a mouse input event, the Y
#  * position of the mouse cursor as fractional value between 0 and 1,
#  * formatted as string, 0 reflecting the top end of the screen, 1
#  * the bottom end.
#  */
CA_PROP_EVENT_MOUSE_VPOS = "event.mouse.vpos"
 
# /**
#  * CA_PROP_EVENT_MOUSE_BUTTON:
#  *
#  * If this sound event was triggered by a mouse input event, the
#  * number of the mouse button that triggered it, formatted as string. 1
#  * for left mouse button, 3 for right, 2 for middle.
#  */
CA_PROP_EVENT_MOUSE_BUTTON = "event.mouse.button"
 
# /**
#  * CA_PROP_WINDOW_NAME:
#  *
#  * If this sound event was triggered by a window on the screen, the
#  * name of this window as human readable string.
#  */
CA_PROP_WINDOW_NAME = "window.name"
 
# /**
#  * CA_PROP_WINDOW_ID:
#  *
#  * If this sound event was triggered by a window on the screen, some
#  * identification string for this window, so that the sound system can
#  * recognize specific windows.
#  */
CA_PROP_WINDOW_ID = "window.id"
 
# /**
#  * CA_PROP_WINDOW_ICON:
#  *
#  * If this sound event was triggered by a window on the screen, binary
#  * icon data in PNG format for this window.
#  */
CA_PROP_WINDOW_ICON = "window.icon"
 
# /**
#  * CA_PROP_WINDOW_ICON_NAME:
#  *
#  * If this sound event was triggered by a window on the screen, an
#  * icon name for this window, as defined in the XDG icon naming
#  * specification.
#  */
CA_PROP_WINDOW_ICON_NAME = "window.icon_name"
 
# /**
#  * CA_PROP_WINDOW_X:
#  *
#  * If this sound event was triggered by a window on the screen, the X
#  * position of the window measured from the top left corner of the
#  * screen to the top left corner of the window.
#  *
#  * Since: 0.17
#  */
CA_PROP_WINDOW_X = "window.x"
 
# /**
#  * CA_PROP_WINDOW_Y:
#  *
#  * If this sound event was triggered by a window on the screen, the y
#  * position of the window measured from the top left corner of the
#  * screen to the top left corner of the window.
#  *
#  * Since: 0.17
#  */
CA_PROP_WINDOW_Y = "window.y"
 
# /**
#  * CA_PROP_WINDOW_WIDTH:
#  *
#  * If this sound event was triggered by a window on the screen, the
#  * pixel width of the window.
#  *
#  * Since: 0.17
#  */
CA_PROP_WINDOW_WIDTH = "window.width"
 
# /**
#  * CA_PROP_WINDOW_HEIGHT:
#  *
#  * If this sound event was triggered by a window on the screen, the
#  * pixel height of the window.
#  *
#  * Since: 0.17
#  */
CA_PROP_WINDOW_HEIGHT = "window.height"
 
# /**
#  * CA_PROP_WINDOW_HPOS:
#  *
#  * If this sound event was triggered by a window on the screen, the X
#  * position of the center of the window as fractional value between 0
#  * and 1, formatted as string, 0 reflecting the left side of the
#  * screen, 1 the right side.
#  *
#  * Since: 0.17
#  */
CA_PROP_WINDOW_HPOS = "window.hpos"
 
# /**
#  * CA_PROP_WINDOW_VPOS:
#  *
#  * If this sound event was triggered by a window on the screen, the Y
#  * position of the center of the window as fractional value between 0
#  * and 1, formatted as string, 0 reflecting the top side of the
#  * screen, 1 the bottom side.
#  *
#  * Since: 0.17
#  */
CA_PROP_WINDOW_VPOS = "window.vpos"
 
# /**
#  * CA_PROP_WINDOW_DESKTOP:
#  *
#  * If this sound event was triggered by a window on the screen and the
#  * windowing system supports multiple desktops, a comma seperated list
#  * of indexes of the desktops this window is visible on. If this
#  * property is an empty string, it is visible on all desktops
#  * (i.e. 'sticky'). The first desktop is 0. (e.g. "0,2,3")
#  *
#  * Since: 0.18
#  */
CA_PROP_WINDOW_DESKTOP = "window.desktop"
 
# /**
#  * CA_PROP_WINDOW_X11_DISPLAY:
#  *
#  * If this sound event was triggered by a window on the screen and the
#  * windowing system is X11, the X display name of the window (e.g. ":0").
#  */
CA_PROP_WINDOW_X11_DISPLAY = "window.x11.display"
 
# /**
#  * CA_PROP_WINDOW_X11_SCREEN:
#  *
#  * If this sound event was triggered by a window on the screen and the
#  * windowing system is X11, the X screen id of the window formatted as
#  * string (e.g. "0").
#  */
CA_PROP_WINDOW_X11_SCREEN = "window.x11.screen"
 
# /**
#  * CA_PROP_WINDOW_X11_MONITOR:
#  *
#  * If this sound event was triggered by a window on the screen and the
#  * windowing system is X11, the X monitor id of the window formatted as
#  * string (e.g. "0").
#  */
CA_PROP_WINDOW_X11_MONITOR = "window.x11.monitor"
 
# /**
#  * CA_PROP_WINDOW_X11_XID:
#  *
#  * If this sound event was triggered by a window on the screen and the
#  * windowing system is X11, the XID of the window formatted as string.
#  */
CA_PROP_WINDOW_X11_XID = "window.x11.xid"
 
# /**
#  * CA_PROP_APPLICATION_NAME:
#  *
#  * The name of the application this sound event was triggered by as
#  * human readable string. (e.g. "GNU Emacs") Localized if possible and
#  * applicable.
#  */
CA_PROP_APPLICATION_NAME = "application.name"
 
# /**
#  * CA_PROP_APPLICATION_ID:
#  *
#  * An identifier for the program this sound event was triggered
#  * by. (e.g. "org.gnu.emacs").
#  */
CA_PROP_APPLICATION_ID = "application.id"
 
# /**
#  * CA_PROP_APPLICATION_VERSION:
#  *
#  * A version number for the program this sound event was triggered
#  * by. (e.g. "22.2")
#  */
CA_PROP_APPLICATION_VERSION = "application.version"
 
# /**
#  * CA_PROP_APPLICATION_ICON:
#  *
#  * Binary icon data in PNG format for the application this sound event
#  * is triggered by.
#  */
CA_PROP_APPLICATION_ICON = "application.icon"
 
# /**
#  * CA_PROP_APPLICATION_ICON_NAME:
#  *
#  * An icon name for the application this sound event is triggered by,
#  * as defined in the XDG icon naming specification.
#  */
CA_PROP_APPLICATION_ICON_NAME = "application.icon_name"
 
# /**
#  * CA_PROP_APPLICATION_LANGUAGE:
#  *
#  * The locale string the application that is triggering this sound
#  * event is running in. A POSIX locale string such as de_DE@euro.
#  */
CA_PROP_APPLICATION_LANGUAGE = "application.language"
 
# /**
#  * CA_PROP_APPLICATION_PROCESS_ID:
#  *
#  * The unix PID of the process that is triggering this sound event, formatted as string.
#  */
CA_PROP_APPLICATION_PROCESS_ID = "application.process.id"
 
# /**
#  * CA_PROP_APPLICATION_PROCESS_BINARY:
#  *
#  * The path to the process binary of the process that is triggering this sound event.
#  */
CA_PROP_APPLICATION_PROCESS_BINARY = "application.process.binary"
 
# /**
#  * CA_PROP_APPLICATION_PROCESS_USER:
#  *
#  * The user that owns the process that is triggering this sound event.
#  */
CA_PROP_APPLICATION_PROCESS_USER = "application.process.user"
 
# /**
#  * CA_PROP_APPLICATION_PROCESS_HOST:
#  *
#  * The host name of the host the process that is triggering this sound event runs on.
#  */
CA_PROP_APPLICATION_PROCESS_HOST = "application.process.host"
 
# /**
#  * CA_PROP_CANBERRA_CACHE_CONTROL:
#  *
#  * A special property that can be used to control the automatic sound
#  * caching of sounds in the sound server. One of "permanent",
#  * "volatile", "never". "permanent" will cause this sample to be
#  * cached in the server permanently. This is useful for very
#  * frequently used sound events such as those used for input
#  * feedback. "volatile" may be used for cacheing sounds in the sound
#  * server temporarily. They will expire after some time or on cache
#  * pressure. Finally, "never" may be used for sounds that should never
#  * be cached, because they are only generated very seldomly or even
#  * only once at most (such as desktop login sounds).
#  *
#  * If this property is not explicitly passed to ca_context_play() it
#  * will default to "never". If it is not explicitly passed to
#  * ca_context_cache() it will default to "permanent".
#  *
#  * If the list of properties is handed on to the sound server this
#  * property is stripped from it.
#  */
CA_PROP_CANBERRA_CACHE_CONTROL = "canberra.cache-control"
 
# /**
#  * CA_PROP_CANBERRA_VOLUME:
#  *
#  * A special property that can be used to control the volume this
#  * sound event is played in if the backend supports it. A floating
#  * point value for the decibel multiplier for the sound. 0 dB relates
#  * to zero gain, and is the default volume these sounds are played in.
#  *
#  * If the list of properties is handed on to the sound server this
#  * property is stripped from it.
#  */
CA_PROP_CANBERRA_VOLUME = "canberra.volume"
 
# /**
#  * CA_PROP_CANBERRA_XDG_THEME_NAME:
#  *
#  * A special property that can be used to control the XDG sound theme that
#  * is used for this sample.
#  *
#  * If the list of properties is handed on to the sound server this
#  * property is stripped from it.
#  */
CA_PROP_CANBERRA_XDG_THEME_NAME = "canberra.xdg-theme.name"
 
# /**
#  * CA_PROP_CANBERRA_XDG_THEME_OUTPUT_PROFILE:
#  *
#  * A special property that can be used to control the XDG sound theme
#  * output profile that is used for this sample.
#  *
#  * If the list of properties is handed on to the sound server this
#  * property is stripped from it.
#  */
CA_PROP_CANBERRA_XDG_THEME_OUTPUT_PROFILE = "canberra.xdg-theme.output-profile"
 
# /**
#  * CA_PROP_CANBERRA_ENABLE:
#  *
#  * A special property that can be used to control whether any sounds
#  * are played at all. If this property is "1" or unset sounds are
#  * played as normal. However, if it is "0" all calls to
#  * ca_context_play() will fail with CA_ERROR_DISABLED.
#  *
#  * If the list of properties is handed on to the sound server this
#  * property is stripped from it.
#  */
CA_PROP_CANBERRA_ENABLE = "canberra.enable"

# /**
#  * CA_PROP_CANBERRA_FORCE_CHANNEL:
#  *
#  * A special property that can be used to control on which channel a
#  * sound is played. The value should be one of mono, front-left,
#  * front-right, front-center, rear-left, rear-right, rear-center, lfe,
#  * front-left-of-center, front-right-of-center, side-left, side-right,
#  * top-center, top-front-left, top-front-right, top-front-center,
#  * top-rear-left, top-rear-right, top-rear-center. This property is
#  * only honoured by some backends, other backends may choose to ignore
#  * it completely.
#  *
#  * If the list of properties is handed on to the sound server this
#  * property is stripped from it.
#  */
CA_PROP_CANBERRA_FORCE_CHANNEL = "canberra.force_channel"

# /**
#  * ca_context:
#  *
#  * A libcanberra context object.
#  */
# typedef struct ca_context ca_context;

ca_context = c_void_p


# /**
#  * ca_finish_callback_t:
#  * @c: The libcanberra context this callback is called for
#  * @id: The numerical id passed to the ca_context_play_full() when starting the event sound playback.
#  * @error_code: A numerical error code describing the reason this callback is called. If CA_SUCCESS is passed in the playback of the event sound was successfully completed.
#  * @userdata: Some arbitrary user data the caller of ca_context_play_full() passed in.
#  *
#  * Playback completion event callback. The context this callback is
#  * called in is undefined, it might or might not be called from a
#  * background thread, and from any stack frame. The code implementing
#  * this function may not call any libcanberra API call from this
#  * callback -- this might result in a deadlock. Instead it may only be
#  * used to asynchronously signal some kind of notification object
#  * (semaphore, message queue, ...).
#  */
# typedef void (*ca_finish_callback_t)(ca_context *c, uint32_t id, int error_code, void *userdata);

CA_FINISH_TYPE = CFUNCTYPE(None, ca_context, c_uint32, c_int, c_void_p)

# /**
#  * Error codes:
#  * @CA_SUCCESS: Success
#  *
#  * Error codes
#  */

CA_SUCCESS = 0
CA_ERROR_NOTSUPPORTED = -1
CA_ERROR_INVALID = -2
CA_ERROR_STATE = -3
CA_ERROR_OOM = -4
CA_ERROR_NODRIVER = -5
CA_ERROR_SYSTEM = -6
CA_ERROR_CORRUPT = -7
CA_ERROR_TOOBIG = -8
CA_ERROR_NOTFOUND = -9
CA_ERROR_DESTROYED = -10
CA_ERROR_CANCELED = -11
CA_ERROR_NOTAVAILABLE = -12
CA_ERROR_ACCESS = -13
CA_ERROR_IO = -14
CA_ERROR_INTERNAL = -15
CA_ERROR_DISABLED = -16
CA_ERROR_FORKED = -17
CA_ERROR_DISCONNECTED = -18
_CA_ERROR_MAX = -19

# /**
#  * ca_proplist:
#  *
#  * A canberra property list object. Basically a hashtable.
#  */
# typedef struct ca_proplist ca_proplist;

ca_proplist = c_void_p


_libHandle = None

def GetApi():
   global _libHandle
   if not _libHandle:
      _libHandle = CDLL("libcanberra.so.0")
   return _libHandle


# XXX: TODO: wrap ca_proplist_*
# int ca_proplist_create(ca_proplist **p);
# int ca_proplist_destroy(ca_proplist *p);
# int ca_proplist_sets(ca_proplist *p, const char *key, const char *value);
# int ca_proplist_setf(ca_proplist *p, const char *key, const char *format, ...) __attribute__((format(printf, 3, 4)));
# int ca_proplist_set(ca_proplist *p, const char *key, const void *data, size_t nbytes);


class CanberraException(Exception):
   def __init__(self, err, *args, **kwargs):
      self._err = err
      super(Exception, self).__init__(*args, **kwargs)

   def get_error(self):
      return self._err

   def __str__(self):
      return super(Exception, self).__str__() + " (error %d)" % self._err
   

class Canberra(object):
   def __init__(self):
      self._handle = ca_context()
      GetApi().ca_context_create(byref(self._handle))

   def set_driver(self, driver):
      res = GetApi().ca_context_set_driver(self._handle, driver)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to set driver")

   def change_device(self, device):
      res = GetApi().ca_context_change_device(self._handle, device)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to change device")
   
   def open(self):
      res = GetApi().ca_context_open(self._handle)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to open context")

   def destroy(self):
      res = GetApi().ca_context_destroy(self._handle)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to destroy context")

   def change_props(self, *args):
      args = tuple(b(arg) if isinstance(arg, string_types) else arg
                   for arg in args)
      res = GetApi().ca_context_change_props(self._handle, *args)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to change props")

   #XXX implement this with ca_props_* is wrapped
   def change_props_full(self, props):
      pass

   #XXX implement this with ca_props_* is wrapped
   def play_full(self, playId, props, cb, userData):
      pass

   #XXX implement this with ca_props_* is wrapped
   def cache_full(self, props):
      pass

   def play(self, playId, *args):
      args = tuple(b(arg) if isinstance(arg, string_types) else arg
                   for arg in args)
      res = GetApi().ca_context_play(self._handle, playId, *args)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to play!")

   def cache(self, *args):
      args = tuple(b(arg) if isinstance(arg, string_types) else arg
                   for arg in args)
      res = GetApi().ca_context_cache(self._handle, *args)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to cache")

   def cancel(self, playId):
      res = GetApi().ca_context_cancel(self._handle, playId)
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to cancel id %d" % playId)

   def playing(self, playId):
      isPlaying = c_int()
      res = GetApi().ca_context_playing(self._handle, playId, byref(isPlaying))
      if res != CA_SUCCESS:
         raise CanberraException(res, "Failed to test play status of id %d" % playId)
      return isPlaying

   def easy_play_sync(self, eventName):
      """ play an event sound synchronously """
      if isinstance(eventName, string_types):
          eventName = b(eventName)
      self.play(1,
                CA_PROP_EVENT_ID, eventName,
                None)
      while self.playing(1):
         time.sleep(0.01)

if __name__ == "__main__":
   canberra = Canberra()
   canberra.easy_play_sync("system-ready")
   canberra.destroy()
