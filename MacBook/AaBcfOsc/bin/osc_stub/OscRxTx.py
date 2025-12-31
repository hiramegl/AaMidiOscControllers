# pip3 install python-osc

import argparse
import math

from pythonosc.dispatcher import Dispatcher
from pythonosc            import osc_server, udp_client, osc_bundle_builder, osc_message_builder

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

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

# client

tx_addr = "127.0.0.1"
tx_port = 2720

client = udp_client.SimpleUDPClient(tx_addr, tx_port)

# server

rx_addr = "127.0.0.1"
rx_port = 2721

dispatcher = Dispatcher()
dispatcher.map("/abc", print_handler,  "ABC", client)
dispatcher.map("/def", print_handler,  "DEF", client)
dispatcher.map("/ghi", print_handler2, "GHI", client)

server = osc_server.ThreadingOSCUDPServer((rx_addr, rx_port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

