from .Base import Base

class Tempo(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_nFactor = 20
    self.m_lDeltasNeg = [-20, -10, -5, -1]
    self.m_lDeltasPos = [  1,   5, 10, 20]

    # registering callbacks
    self.reg_idx_cb(
      'tempo/cmd', 8, self.on_cmd)
    self.reg_idx_cb(
      'tempo/dlt/neg', 4, self.on_dlt_neg)
    self.reg_idx_cb(
      'tempo/dlt/pos', 4, self.on_dlt_pos)

  # ********************************************************

  def on_cmd(self, plSegs, plMsg):
    nIdx = int(plSegs[3])
    if nIdx == 7:
      self.song().tempo = 128
    else:
      self.song().tempo = (nIdx + 1) * self.m_nFactor

  def on_dlt_neg(self, plSegs, plMsg):
    nIdx   = int(plSegs[4])
    nTempo = self.song().tempo
    nDelta = self.m_lDeltasNeg[nIdx]
    if nTempo + nDelta >= 20:
      self.song().tempo = nTempo + nDelta
    else:
      self.alert('-> TEMPO OUT OF RANGE')

  def on_dlt_pos(self, plSegs, plMsg):
    nIdx   = int(plSegs[4])
    nTempo = self.song().tempo
    nDelta = self.m_lDeltasPos[nIdx]
    self.song().tempo = nTempo + nDelta

