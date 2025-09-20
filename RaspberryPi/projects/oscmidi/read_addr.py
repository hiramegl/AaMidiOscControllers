with open('/home/hiram/mac_addr.txt', 'rt') as oFile:
  sMacAddr = oFile.read()
print('> The macbook address is "%s"' % (sMacAddr))
