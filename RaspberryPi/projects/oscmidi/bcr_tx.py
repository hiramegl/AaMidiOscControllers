from pythonosc import udp_client

sTxAddr  = '127.0.0.1' # Macbook: "Hirams-MacBook-Pro-2.local", "169.254.193.70"
nTxPort  = 2722
sOscAddr = "/bcr"

print("> Starting OSC client")
oOscClient = udp_client.SimpleUDPClient(sTxAddr, nTxPort)

print('> New message to send:')
sMsg = input()
lOld = []

while sMsg[0] != 'x':
  if sMsg[0] == 'o': # send old message
    sMsg = '%02x, %d, %d' % (lOld[0], lOld[1], lOld[2])
    lMsg = lOld
  elif sMsg[0] == 'g': # go to sel
    lMsg = [0xBF, 3, 127]
    sMsg = '%02x, %d, %d' % (lMsg[0], lMsg[1], lMsg[2])
  elif sMsg[0] == 'r': # move to right
    lMsg = [0xBF, 2, 127]
    sMsg = '%02x, %d, %d' % (lMsg[0], lMsg[1], lMsg[2])
  else:
    lParts = sMsg.split(' ')
    lMsg   = [
      int(lParts[0], 16),
      int(lParts[1]),
      int(lParts[2])
    ]
  lOld = lMsg
  print('> Sending: [%s]' % sMsg)
  oOscClient.send_message(sOscAddr, lMsg)
  print('> New message to send:')
  sMsg = input()

print('> Done')

