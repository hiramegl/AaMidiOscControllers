import Live

class Stub:
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj
    self.m_lOffsets = []

    self.obj('oRouter').reg('Stub', 'x', self)

  # ********************************************************

  def add_offsets(self, pnCurrBank, pnCurrStrip, pnStrips, plRootIds):
    self.m_lOffsets.append([pnCurrBank, pnCurrStrip, pnStrips, plRootIds])

  def sync_dev(self, pnBankChn):
    self.dlog('-> STUB: sync dev, bank chn: %d' % (pnBankChn))
    lBundle = []
    for lOffset in self.m_lOffsets:
      nBank    = lOffset[0]
      nStrip   = lOffset[1] # start strip
      nStrips  = lOffset[2] # number of strips
      lRootIds = lOffset[3] # root ids
      for nStripIdx in range(nStrips):
        for nRootId in lRootIds:
          nBankChn = 0xB0 | nBank
          nId      = nRootId + nStripIdx + nStrip
          lMsg     = [nBankChn, nId, 0]
          self.dlog(' -> key: %02X % 3d -> 0' %
            (nBankChn, nId))
          lBundle.append(lMsg)
    self.obj('oComm').send_bundle(lBundle)

  def handle_rx_msg(self, pnBankAbs, pnIdAbs, pnValue):
    self.dlog('-> STUB: Turning off bank: %d, id: %d' % (pnBankAbs, pnIdAbs))
    nBankChn = 0xB0 | pnBankAbs
    lMsg     = [nBankChn, pnIdAbs, 0]
    self.obj('oComm').send_msg(lMsg)
    self.dlog('-> STUB Tx: %02X % 3d -> 0' %
      (nBankChn, pnIdAbs))

  def unbind_dev(self):
    # nothing to unbind
    pass

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

