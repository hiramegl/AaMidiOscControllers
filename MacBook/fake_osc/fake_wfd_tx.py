from pythonosc import udp_client

# config *****************************************
tx_addr  = "127.0.0.1" # Macbook
tx_port  = 2724
osc_addr = "/wfd"

# osc client *************************************
print("> Starting OSC client")
osc_tx = udp_client.SimpleUDPClient(tx_addr, tx_port)
print("> Sending message ...")
osc_tx.send_message(osc_addr, [0xBF, 3, 127])

