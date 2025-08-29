from AaTouch.Base import Base

class HalfSel(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lSides = ['LEFT', 'RIGHT']
    self.m_nHalf  = 0 # 0: Left half, 1: right half
    self.connect()

    phObj['oHalfSel'] = self

    self.update()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb(
      'seq/sec/half_sel', 2, self.on_half_sel)

  def disconnect(self):
      self.send_msg('/seq/sec/half_sel/%d' % self.m_nHalf, 0)

  # ********************************************************

  def update(self):
      self.send_msg('/seq/sec/half_sel/%d' % self.m_nHalf, 1)

  # ********************************************************

  def on_half_sel(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    if nValue < 0.5:
      if nIdx == self.m_nHalf:
        self.send_msg(sAddr, 1) # prevent from turning off
      return

    if nIdx != self.m_nHalf:
      self.send_msg('/seq/sec/half_sel/%d' % self.m_nHalf, 0)
      self.m_nHalf = nIdx
      self.obj('oBitOp').update()
      self.alert('HALF: %s' % (self.m_lSides[nIdx]))

  # ********************************************************

  def half_sel(self):
    return self.m_lSides[self.m_nHalf]

