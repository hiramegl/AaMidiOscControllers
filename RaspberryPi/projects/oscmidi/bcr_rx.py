from pythonosc.dispatcher import Dispatcher
from pythonosc            import osc_server

rx_addr  = '127.0.0.1'  # Rasberry Pi: "raspberrypi.local", "169.254.210.136"
rx_port  = 2723
osc_addr = "/bcr"

# global osc handlers ***************************
def handle_osc(osc_addr, osc_p1, osc_p2, osc_p3):
  print("> rx: %s -> [%x, %d, %d]" % (osc_addr, osc_p1, osc_p2, osc_p3))

# osc server ************************************
dispatcher = Dispatcher()
dispatcher.map(osc_addr, handle_osc)
server = osc_server.ThreadingOSCUDPServer((rx_addr, rx_port), dispatcher)

print("Serving OSC on {}".format(server.server_address))
try:
  server.serve_forever()
except:
  print("Finishing")

