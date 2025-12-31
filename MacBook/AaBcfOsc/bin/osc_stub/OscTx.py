from pythonosc import udp_client

tx_addr = "127.0.0.1"
tx_port = 2720

client = udp_client.SimpleUDPClient(tx_addr, tx_port)
client.send_message("/abc", "abcd12")
