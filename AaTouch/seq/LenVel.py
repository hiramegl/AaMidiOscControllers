from AaTouch.Base import Base

class LenVel(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lLens    = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    self.m_lVels    = [   10,   20,  40,  60,  80, 100, 120,  127]
    self.m_nLenIdx  = 1  # current bit length   index
    self.m_nVelIdx  = 7  # current bit velocity index
    self.connect()

    phObj['oLenVel'] = self

    self.update()

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'seq/bit/lenvel', 8 * 2, self.on_lenvel)

  def disconnect(self):
    self.send_bundle([
      ['/seq/bit/lenvel/%d' % (self.m_nLenIdx)    , 0],
      ['/seq/bit/lenvel/%d' % (self.m_nVelIdx + 8), 0],
    ])

  # ********************************************************

  def update(self):
    self.send_bundle([
      ['/seq/bit/lenvel/%d' % (self.m_nLenIdx)    , 1],
      ['/seq/bit/lenvel/%d' % (self.m_nVelIdx + 8), 1],
    ])

  # ********************************************************

  def on_lenvel(self, plSegs, plMsg):
    sAddr = plMsg[0]
    nIdx  = int(plSegs[4])
    (sCmd, nColIdx) = self.get_row_col(nIdx, 8, ['LEN' , 'VEL'])

    if plMsg[2] < 0.5: # turning off
      if self.mode() == 'MIDI':
        if sCmd == 'LEN' and self.m_nLenIdx == nColIdx:
          self.send_msg(sAddr, 1) # prevent from turning off
        elif sCmd == 'VEL' and self.m_nVelIdx == nColIdx:
          self.send_msg(sAddr, 1) # prevent from turning off
      return

    if sCmd == 'LEN':
      if nColIdx == self.m_nLenIdx:
        self.send_msg(sAddr, 1)
      else:
        self.send_msg('/seq/bit/lenvel/%d' % (self.m_nLenIdx), 0)
        self.m_nLenIdx = nColIdx
        self.alert('> BIT LEN: %0.3f' % (self.m_lLens[nColIdx]))

    elif sCmd == 'VEL':
      if nColIdx == self.m_nVelIdx:
        self.send_msg(sAddr, 1)
      else:
        self.send_msg('/seq/bit/lenvel/%d' % (self.m_nVelIdx + 8), 0)
        self.m_nVelIdx = nColIdx
        self.alert('> BIT VEL: %d' % (self.m_lVels[nColIdx]))

  # ********************************************************

  def get_attr(self, psAttr):
    if psAttr == 'LEN':
      return self.m_lLens[self.m_nLenIdx]
    elif psAttr == 'VEL':
      return self.m_lVels[self.m_nVelIdx]

