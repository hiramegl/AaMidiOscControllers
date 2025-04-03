import math

from AaTouch.Base import Base

class Roll(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lBeatIdx = -1 # no selection
    self.m_lSemiIdx = -1 # no selection
    self.connect()

    phObj['oRoll'] = self

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'roll/beat', 4, self.on_beat)
    self.comm().reg_indexed_rx_cb(
      'roll/semi', 8, self.on_semi)

  def disconnect(self):
    self.toggle_off()

  # ********************************************************

  def on_beat(self, plSegs, plMsg):
    oClip = self.state().get_clip_or_none()
    if oClip == None:
      sAddr = plMsg[0]
      self.send_msg(sAddr, 0)
      return

    nIdx   = int(plSegs[3])
    nValue = plMsg[2]

    if nValue < 0.5:
      # turning roll off
      if self.m_lBeatIdx != -1:
        # there was actually a beat rolling, turn loop off!
        self.m_lBeatIdx = -1
        oClip.looping = False
        self.send_msg('/loop/ext/0', 0) # loop-toggle
      return

    # turning roll on
    if self.m_lSemiIdx != -1:
      self.send_msg('/roll/semi/%d' % (self.m_lSemiIdx), 0)
      self.m_lSemiIdx = -1

    if self.m_lBeatIdx != -1:
      self.send_msg('/roll/beat/%d' % (self.m_lBeatIdx), 0)

    self.m_lBeatIdx = nIdx
    self.roll(float(nIdx), 1.0)
    self.obj('oLoop').toggle_loop(1)
    self.alert('ROLL BEAT %d' % (nIdx + 1))

  def on_semi(self, plSegs, plMsg):
    oClip = self.state().get_clip_or_none()
    if oClip == None:
      sAddr = plMsg[0]
      self.send_msg(sAddr, 0)
      return

    nIdx   = int(plSegs[3])
    nValue = plMsg[2]

    if nValue < 0.5:
      # turning roll off
      if self.m_lSemiIdx != -1:
        # there was actually a semi-beat rolling, turn loop off!
        self.m_lSemiIdx = -1
        oClip.looping = False
        self.send_msg('/loop/ext/0', 0) # loop-toggle
      return

    if self.m_lBeatIdx != -1:
      self.send_msg('/roll/beat/%d' % (self.m_lBeatIdx), 0)
      self.m_lBeatIdx = -1

    if self.m_lSemiIdx != -1:
      self.send_msg('/roll/semi/%d' % (self.m_lSemiIdx), 0)

    self.m_lSemiIdx = nIdx
    self.roll(float(nIdx) * 0.5, 0.5)
    self.obj('oLoop').toggle_loop(1)

    nBeatIdx = int(nIdx / 2) + 1
    nBitIdx  = ((nIdx % 2) * 2) + 1
    self.alert('ROLL SEMI %d.%d' % (nBeatIdx, nBitIdx))

  # ********************************************************

  def roll(self, pnOff, pnLen):
    oClip     = self.state().get_clip_or_none()
    nPlayPos  = oClip.playing_position
    nCurrBar  = (math.floor(math.floor(nPlayPos)/ 4.0)) * 4.0
    nCurrBeat = math.floor(nPlayPos)
    nNewStart = nCurrBar  + pnOff
    nNewEnd   = nNewStart + pnLen
    #self.log('Play pos: %.5f, curr bar: %.1f, curr beat: %.1f, start: %.5f, end: %.5f' %
    #  (nPlayPos, nCurrBar, nCurrBeat, nNewStart, nNewEnd))

    oClip.looping = True
    self.send_msg('/loop/ext/0', 1) # loop-toggle

    nOldStart = oClip.loop_start
    nOldEnd   = oClip.loop_end

    if nNewStart >= nOldEnd:
      oClip.loop_end   = nNewEnd
      oClip.loop_start = nNewStart
    else:
      oClip.loop_start = nNewStart
      oClip.loop_end   = nNewEnd

    oClip.position = nNewStart

  # ********************************************************

  def toggle_off(self):
    if self.m_lBeatIdx != -1:
      self.send_msg('/roll/beat/%d' % (self.m_lBeatIdx), 0)
      self.m_lBeatIdx = -1

    elif self.m_lSemiIdx != -1:
      self.send_msg('/roll/semi/%d' % (self.m_lSemiIdx), 0)
      self.m_lSemiIdx = -1

