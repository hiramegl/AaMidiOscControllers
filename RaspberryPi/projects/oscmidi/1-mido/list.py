import mido

names = mido.get_input_names()

for n in names:
  print("> %s" % (n))

# 0 > Midi Through:Midi Through Port-0 14:0
# 1 > W-FADER:W-FADER MIDI 1 20:0
# 2 > BCF2000:BCF2000 MIDI 1 32:0
# 3 > BCR2000:BCR2000 MIDI 1 36:0
