import re
import threading
import mido

from pythonosc import udp_client

# read ip addresses ******************************
with open('/home/hiram/mac_addr.txt', 'rt') as oFile:
  sMacAddr = oFile.read()

# config *****************************************
tx_addr  = sMacAddr # Macbook: "Hirams-MacBook-Pro-2.local", "169.254.193.70"
tx_port  = 2724
dev_name = "W-FADER"
osc_addr = "/wfd"

print("> Tx: %s:%d" % (tx_addr, tx_port))

# search complete device name ********************
def find_dev(dev):
  for x in mido.get_input_names():
    if re.match(dev, x):
      return x;
device = find_dev(dev_name)

# osc client *************************************
print("> Starting OSC client")
osc_client = udp_client.SimpleUDPClient(tx_addr, tx_port)

# midi input thread function *********************
def midi_in_thread(device_name, osc_addr, osc_client):
  print("> Starting MIDI server for: %s" % (device_name))
  with mido.open_input(device_name) as inport:
    for msg in inport:
      print(msg)
      osc_client.send_message(osc_addr, msg.bytes())

# midi in thread ********************************
midi_in = threading.Thread(
  target=midi_in_thread,
  args=(device, osc_addr, osc_client,))
midi_in.start()

