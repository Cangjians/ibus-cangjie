# ibus-shortn
# This is still a massive work in progress. Forked from Ibus-Cangjie. Nothing is finished but the IME currently functions

The Shortn algorithm and its IME is quite simple. Type the word you want, but without all the vowels, except the first one, if there are too many results, type the last vowel at the end to refine them, then select it.

For example, to type "humanity", you would type "humnt". You would see two results appearing '[1]  humanate', and '[2] humanity'. you can either add a 'y', thereby making it "humnty", refining the result to just one, and then clicking 1. or clicking 2. the IME then adds a space to prevent unnecessary strokes. in the end you will have typed "humnt2" instead of "humanity ", resulting in 3 less strokes typed. IE:

* "humanity "
vs
* "humnt2"


additional commands: 
escape=toggle off on engine
left shift=change caps (workaround)
type "'" = ,+right shift

But let me show you that on camera: 



# to do list
 * Finish readme.md and make it presentable
 * writing "test?" will only show "test" but still output "test? " if you press space
 * fix the enter not working on some text editors
 * make it such that pressing caps makes the text in all caps (while accounting for the shortn algorithm) instead of needing to click left shift twice.
 * add customizable settings.on settings
 * add support for other languages. in the works: french, russian. planned to include all applicable languages.
 * 
