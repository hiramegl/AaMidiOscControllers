# pip3 install python-rtmidi

import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

print('> Available ports:')
i = 0
for port in available_ports:
  print('  %d -> %s' % (i, port))
  i += 1

del midiout

