import Live

class MultiEq3():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_lCtrls = [
      'HighOn:GB0',
      'MidOn:MB0',
      'LowOn:MB1',
      'GainHi:MR0',
      'GainMid:MR1',
      'GainLo:MR2',
      'FreqHi:GR1',
      'FreqLo:GR0',
    ]
    self.connect()

    phObj['oMultiEq3'] = self

  def connect(self):
    fSyncCb = lambda ptKey, pnValue: self.handle_sync_rx_msg(pnValue)
    self.obj('oComm').reg_cc(
      self.cfg('nMultiEq3SyncChn'), self.cfg('nMultiEq3Sync'), 'MultiEq3Sync', fSyncCb)

    for sCtrl in self.m_lCtrls:
      lCtrl = sCtrl.split(':')
      for nIdx in range(8):
        self.add_ctrl_rx_handler(lCtrl[0], lCtrl[1], nIdx)

  def add_ctrl_rx_handler(self, psParam, psId, pnIdx):
    fCtrlCb = lambda ptKey, pnValue: self.handle_ctrl_rx_msg(psParam, pnIdx, pnValue)
    nChn  = self.cfg('nMultiEq3Chn')
    sId   = 'n%sOff' % (psId)
    sName = '%s-%d'  % (psParam, pnIdx)
    self.obj('oComm').reg_cc(
      nChn, self.cfg(sId) + pnIdx, sName, fCtrlCb)

  # ********************************************************

  def handle_sync_rx_msg(self, pnValue):
    if pnValue == 127:
      self.sync()

  def handle_ctrl_rx_msg(self, psParam, pnIdx, pnValue):
    oReturn = self.returns()[pnIdx]
    for oDev in oReturn.devices:
      if oDev.class_name != 'FilterEQ3': continue
      for oParam in oDev.parameters:
        if oParam.name != psParam: continue
        if (psParam == 'LowOn' or
          psParam == 'MidOn'   or
          psParam == 'HighOn'):
          oParam.value = (pnValue == 127)
        else:
          oParam.value = float(pnValue) / 127.0

  # ********************************************************

  def sync(self):
    lReturns = self.returns()
    for nIdx in range(8):
      for oDev in lReturns[nIdx].devices:
        if oDev.class_name != 'FilterEQ3': continue
        for oParam in oDev.parameters:
          sParam = oParam.name
          nValue = int(oParam.value * 127)
          if sParam == 'Device On':
            oParam.value = True
          elif sParam == 'HighOn':
            self.send_msg('nMultiEq3Chn', 'nGB0Off', nValue, nIdx)
          elif sParam == 'MidOn':
            self.send_msg('nMultiEq3Chn', 'nMB0Off', nValue, nIdx)
          elif sParam == 'LowOn':
            self.send_msg('nMultiEq3Chn', 'nMB1Off', nValue, nIdx)
          elif sParam == 'GainHi':
            self.send_msg('nMultiEq3Chn', 'nMR0Off', nValue, nIdx)
          elif sParam == 'GainMid':
            self.send_msg('nMultiEq3Chn', 'nMR1Off', nValue, nIdx)
          elif sParam == 'GainLo':
            self.send_msg('nMultiEq3Chn', 'nMR2Off', nValue, nIdx)
          elif sParam == 'FreqHi':
            self.send_msg('nMultiEq3Chn', 'nGR1Off', nValue, nIdx)
          elif sParam == 'FreqLo':
            self.send_msg('nMultiEq3Chn', 'nGR0Off', nValue, nIdx)

  # ********************************************************

  def disconnect(self):
    for sCtrl in self.m_lCtrls:
      lCtrl = sCtrl.split(':')
      sId   = 'n%sOff' % (lCtrl[1])
      for nIdx in range(8):
        self.send_msg('nMultiEq3Chn', sId, 0, nIdx)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def returns(self):
    return self.song().return_tracks

  def send_msg(self, psBankChn, psId, pnValue, pnIdx = 0):
    nBankChn = 0xB0 | self.cfg(psBankChn)
    nId      = self.cfg(psId) + pnIdx
    self.obj('oComm').send_msg([nBankChn, nId, pnValue])

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

