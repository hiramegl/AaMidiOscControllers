# pip3 install python-osc
# pip3 install python-rtmidi

import rtmidi
from rtmidi.midiutil      import open_midiinput
from pythonosc.dispatcher import Dispatcher
from pythonosc            import osc_server, udp_client, osc_bundle_builder, osc_message_builder

port_idx = 3

class MidiFwd:
  def __init__(self, client):
    print("Starting MidiFwd")
    self.m_client = client

  def __call__(self, event, data=None):
    print("Rx midi msg")
    message, deltatime = event
    print("sending client message")
    self.m_client.send_message("/abc", message)
    print("sent client message")

  def finish(self):
    print("Finishing MidiFwd")

def print_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))
  print("Sending message ...")
  args[1].send_message("/abc", ["quack", 3.3])

def print_handler2(unused_addr, args, p1, p2):
  print("[{0}] ~ {1}, {2}".format(args[0], p1, p2))
  print("Sending bundle ...")
  bundleBuilder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
  msg1 = osc_message_builder.OscMessageBuilder(address="/abc")
  msg1.add_arg(1.0)
  msg1.add_arg(8)
  bundleBuilder.add_content(msg1.build())
  msg2 = osc_message_builder.OscMessageBuilder(address="/def")
  msg2.add_arg('quacky')
  msg2.add_arg(1.0)
  bundleBuilder.add_content(msg2.build())
  bundle = bundleBuilder.build()
  args[1].send(bundle)

  print("Sending midi ...")
  args[2].send_message([0xB0, 17, 100])
  args[2].send_message([0xB0, 18, 100])
  args[2].send_message([0xB0, 19, 100])
  args[2].send_message([0xB0, 20, 100])
  args[2].send_message([0xB0, 21, 100])
  args[2].send_message([0xB0, 22, 100])
  args[2].send_message([0xB0, 23, 100])
  args[2].send_message([0xB0, 24, 100])

# midi out **************************************
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print('available: %s' % (' | '.join(available_ports)))
midiout.open_port(port_idx)

# osc client ************************************
tx_addr = "169.254.176.5" # Macbook
tx_port = 2720
client = udp_client.SimpleUDPClient(tx_addr, tx_port)

# midi in ***************************************
midiin, port_name = open_midiinput(port_idx)
midifwd = MidiFwd(client)
midiin.set_callback(midifwd)

# server ****************************************
rx_addr = "169.254.210.136" # Raspberry Pi
rx_port = 2721
dispatcher = Dispatcher()
dispatcher.map("/abc", print_handler,  "ABC", client, midiout)
dispatcher.map("/def", print_handler,  "DEF", client, midiout)
dispatcher.map("/ghi", print_handler2, "GHI", client, midiout)
server = osc_server.ThreadingOSCUDPServer((rx_addr, rx_port), dispatcher)
print("Serving on {}".format(server.server_address))
try:
  server.serve_forever()
except:
  print("Finishing")
  del midiout
  del midiin

