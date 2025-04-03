# pip3 install python-rtmidi
from __future__ import print_function

import logging
import sys
import time
import rtmidi

from rtmidi.midiutil import open_midiinput

port = 1

class MidiFwd:
  def __init__(self):
    log = logging.getLogger('fwd')
    logging.basicConfig(level=logging.DEBUG)

  def __call__(self, event, data=None):
    message, deltatime = event
    print('> %x %d %d' % (message[0], message[1], message[2]))

  def finish(self):
    pass

try:
    midiin, port_name = open_midiinput(port)
    #midiin, port_name = open_midiport(port, "input")
    midiin.ignore_types(sysex = False, timing = False, active_sense = True)
    midifwd = MidiFwd()
    midiin.set_callback(midifwd)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Entering main loop. Press Control-C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midifwd.finish()
    midiin.close_port()
    del midiin

