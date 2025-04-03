from AaTouch.Base import Base

class Chord(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lChord    = ['TRIAD', '1ST INV', '2ND INV', 'AUGMENTED', 'POWER 5TH']
    self.m_nChordIdx = -1    # No chord mode selected

    phObj['oChord']  = self
    self.connect()

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'seq/chord', 5, self.on_chord)

  def disconnect(self):
    if self.m_nChordIdx >= 0:
      self.send_msg('/seq/chord/%d' % (self.m_nChordIdx), 0)

  # ********************************************************

  def on_chord(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    if self.mode() != 'MIDI':
      self.send_msg(sAddr, 0)
      self.alert('Chord commands not available for Audio clips')
      return

    if nValue < 0.5: # turning off
      self.m_nChordIdx = -1
      self.alert('CHORD OFF')

    else: # turning on
      sType = self.m_lChord[nIdx]
      if self.m_nChordIdx != -1:
        self.send_msg('/seq/chord/%d' % (self.m_nChordIdx), 0)
      self.m_nChordIdx = nIdx
      self.alert('CHORD: %s' % (sType))

  # ********************************************************

  def get_mode(self):
    if self.m_nChordIdx == -1:
      return 'NONE'
    return self.m_lChord[self.m_nChordIdx]

