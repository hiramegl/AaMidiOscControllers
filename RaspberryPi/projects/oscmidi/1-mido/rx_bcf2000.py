import mido

names = mido.get_input_names()

for n in names:
  print("> %s" % (n))

with mido.open_input("BCF2000:BCF2000 MIDI 1 32:0") as inport:
  for message in inport:
    print(message)

