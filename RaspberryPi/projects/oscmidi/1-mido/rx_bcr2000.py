import mido

names = mido.get_input_names()

for n in names:
  print("> %s" % (n))

with mido.open_input("BCR2000:BCR2000 MIDI 1 36:0") as inport:
  for message in inport:
    print(message)

