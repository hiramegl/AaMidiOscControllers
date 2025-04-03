import re
import threading
import mido

from pythonosc.dispatcher import Dispatcher
from pythonosc            import osc_server, udp_client

# read ip addresses ******************************
with open('/home/hiram/pi_addr.txt', 'rt') as oFile:
  sPiAddr = oFile.read()

with open('/home/hiram/mac_addr.txt', 'rt') as oFile:
  sMacAddr = oFile.read()

# config *****************************************
rx_addr  = sPiAddr  # Rasberry Pi: "raspberrypi.local", "169.254.210.136"
rx_port  = 2721
tx_addr  = sMacAddr # Macbook: "Hirams-MacBook-Pro-2.local", "169.254.193.70"
tx_port  = 2720
dev_name = "BCF2000"
osc_addr = "/bcf"

print("> Rx: %s:%d, Tx: %s:%d" % (rx_addr, rx_port, tx_addr, tx_port))

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

# global midi outports **************************
midi_out = mido.open_output(device)

# global osc handlers ***************************
def handle_osc(osc_addr, args, osc_p1, osc_p2, osc_p3):
  print("> rx: %s -> [%x, %d, %d]" % (osc_addr, osc_p1, osc_p2, osc_p3))
  midi_msg = mido.Message.from_bytes([osc_p1, osc_p2, osc_p3])
  args[0].send(midi_msg)

# osc server ************************************
dispatcher = Dispatcher()
dispatcher.map(osc_addr, handle_osc, midi_out)
server = osc_server.ThreadingOSCUDPServer((rx_addr, rx_port), dispatcher)

print("Serving OSC on {}".format(server.server_address))
try:
  server.serve_forever()
except:
  print("Finishing")

