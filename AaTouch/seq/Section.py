from AaTouch.Base import Base

class Section(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lSections = ['1/2', '1', '2', '4']
    self.m_nSection  = 1 # BAR
    self.connect()

    phObj['oSection'] = self

    self.update()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb(
      'seq/sec/sel', 4, self.on_section)

  def disconnect(self):
      self.send_msg('/seq/sec/sel/%d' % self.m_nSection, 0)

  # ********************************************************

  def update(self):
      self.send_msg('/seq/sec/sel/%d' % self.m_nSection, 1)

  # ********************************************************

  def on_section(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    if nValue < 0.5:
      if nIdx == self.m_nSection:
        self.send_msg(sAddr, 1) # prevent from turning off
      return

    if nIdx != self.m_nSection:
      self.send_msg('/seq/sec/sel/%d' % self.m_nSection, 0)
      self.m_nSection = nIdx
      self.obj('oBitOp').update()

    self.alert('SECTION: %s' % (self.m_lSections[nIdx]))

  # ********************************************************

  def section(self):
    return self.m_lSections[self.m_nSection]

  def section_len(self):
    sTimeMode = self.obj('oTimeMode').time_mode()
    nSectLen  = 4.0 if sTimeMode == 'BAR' else 16.0

    if self.m_nSection == 0 or self.m_nSection == 1:
      return nSectLen

    if self.m_nSection == 2:
      return nSectLen * 2.0

    return nSectLen * 4.0

