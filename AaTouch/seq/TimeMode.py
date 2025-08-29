from AaTouch.Base import Base

class TimeMode(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_nMode  = 0 # 0 = BAR, 1 = PHRASE
    self.m_lModes = ['BAR', 'PHRASE']
    self.connect()

    phObj['oTimeMode'] = self

    self.activate()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb(
      'seq/time/mode', 2, self.on_mode)

  def disconnect(self):
    self.deactivate()

  # ********************************************************

  def activate(self):
    self.send_msg('/seq/time/mode/%d' % self.m_nMode, 1)

  def deactivate(self):
    self.send_msg('/seq/time/mode/%d' % self.m_nMode, 0)

  # ********************************************************

  def on_mode(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    if nValue < 0.5:
      if nIdx == self.m_nMode:
        self.send_msg(sAddr, 1) # prevent from turning off
      return

    if nIdx != self.m_nMode:
      self.send_msg('/seq/time/mode/%d' % self.m_nMode, 0)
      self.m_nMode = nIdx
      self.obj('oSeqMap').update(True)
      self.obj('oGrid'  ).update()
      self.obj('oBitOp' ).update()

    self.alert('TIME MODE: %s' % (self.m_lModes[nIdx]))

  # ********************************************************

  def time_mode(self):
    return self.m_lModes[self.m_nMode]

  def time_span(self):
    return 8 if self.m_nMode == 0 else 32

  def time_factor(self):
    return 4.0 if self.m_nMode == 0 else 1.0

  def bit_time(self):
    return 0.25 if self.m_nMode == 0 else 1.0

