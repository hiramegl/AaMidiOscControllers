import mido

names = mido.get_input_names()

for n in names:
  print("> %s" % (n))

with mido.open_input("W-FADER:W-FADER MIDI 1 20:0") as inport:
  for message in inport:
    print(message)

