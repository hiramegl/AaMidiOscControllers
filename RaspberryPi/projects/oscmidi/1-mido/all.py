# pip install python-osc
# pip install mido

import threading
import mido

from pythonosc.dispatcher import Dispatcher
from pythonosc            import osc_server, udp_client

# shared osc client ******************************
print("> Starting shared OSC client")
tx_addr    = "192.168.0.11" # Macbook
tx_port    = 2720
osc_client = udp_client.SimpleUDPClient(tx_addr, tx_port)

# midi input thread function *********************
def midi_in_thread(device_name, osc_addr,  osc_client):
  print("> Starting MIDI server for: %s" % (device_name))
  with mido.open_input(device_name) as inport:
    for msg in inport:
      print(msg)
      osc_client.send_message(osc_addr, msg.bytes())

# midi in threads *******************************
mi1 = threading.Thread(
  target=midi_in_thread,
  args=("W-FADER:W-FADER MIDI 1 20:0", "/wfd", osc_client,))
mi2 = threading.Thread(
  target=midi_in_thread,
  args=("BCF2000:BCF2000 MIDI 1 32:0", "/bcf", osc_client,))
mi3 = threading.Thread(
  target=midi_in_thread,
  args=("BCR2000:BCR2000 MIDI 1 36:0", "/bcr", osc_client,))

mi1.start()
mi2.start()
mi3.start()

# global midi outports **************************
bcf = mido.open_output("BCF2000:BCF2000 MIDI 1 32:0")
bcr = mido.open_output("BCR2000:BCR2000 MIDI 1 36:0")

# global osc handlers ***************************
def handle_osc_bcf(osc_addr, args, osc_p1, osc_p2, osc_p3):
  print("> BCF rx: %s -> [%x, %d, %d]" % (osc_addr, osc_p1, osc_p2, osc_p3))
  midi_msg = mido.Message.from_bytes([osc_p1, osc_p2, osc_p3])
  args[0].send(midi_msg)

def handle_osc_bcr(osc_addr, args, osc_p1, osc_p2, osc_p3):
  print("> BCR rx: %s -> [%x, %d, %d]" % (osc_addr, osc_p1, osc_p2, osc_p3))
  midi_msg = mido.Message.from_bytes([osc_p1, osc_p2, osc_p3])
  args[0].send(midi_msg)

# shared osc server *****************************
rx_addr = "192.168.0.16" # Raspberry Pi
rx_port = 2721
dispatcher = Dispatcher()
dispatcher.map("/bcf", handle_osc_bcf, bcf)
dispatcher.map("/bcr", handle_osc_bcr, bcr)

server = osc_server.ThreadingOSCUDPServer((rx_addr, rx_port), dispatcher)
print("Serving OSC on {}".format(server.server_address))
try:
  server.serve_forever()
except:
  print("Finishing")

