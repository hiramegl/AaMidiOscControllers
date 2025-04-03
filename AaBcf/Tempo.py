class Tempo():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_nTempo1 = 2
    self.m_nTempo2 = int(self.song().tempo)
    if self.m_nTempo2 > 127:
      self.m_nTempo2 = 127
    self.connect()

    phObj['oTempo'] = self

  def connect(self):
    fTempoCb = lambda ptKey, pnValue: self.handle_tempo_rx_msg(ptKey, pnValue)
    nBank0Chn = self.cfg('nBank0Chn')
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTempo1'),    'Tempo1',    fTempoCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTempo2'),    'Tempo2',    fTempoCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTempo1Rst'), 'Tempo1Rst', fTempoCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTempo2Rst'), 'Tempo2Rst', fTempoCb)

    self.song().add_tempo_listener(self.handle_tempo_tx_msg)

  def handle_tempo_rx_msg(self, ptKey, pnValue):
    nId = ptKey[1]

    if nId == self.cfg('nTempo1'):
      self.m_nTempo1 = pnValue
      self.alert('Tempo Incr: %d' % (self.m_nTempo1))
    elif nId == self.cfg('nTempo2'):
      nTempo = self.song().tempo
      if self.m_nTempo2 == pnValue and pnValue == 0:
        nTempo = nTempo - self.m_nTempo1
      elif self.m_nTempo2 == pnValue and pnValue == 127:
        nTempo = nTempo + self.m_nTempo1
      elif self.m_nTempo2 > pnValue:
        nTempo = nTempo - self.m_nTempo1
      elif self.m_nTempo2 < pnValue:
        nTempo = nTempo + self.m_nTempo1
      if nTempo < 20: return
      self.m_nTempo2    = int(pnValue)
      self.song().tempo = nTempo
    elif nId == self.cfg('nTempo1Rst'):
      self.m_nTempo1 = 2
      self.alert('Tempo Incr Reset: %d' % (self.m_nTempo1))
    elif nId == self.cfg('nTempo2Rst'):
      nTempo = 128
      self.song().tempo = nTempo
      self.alert('Tempo Reset: %d' % (nTempo))

  def handle_tempo_tx_msg(self):
    self.sync()

  def sync(self):
    nTempo2 = int(self.song().tempo / self.m_nTempo1)
    self.send_msg('nBank0Chn', 'nTempo1', self.m_nTempo1)
    self.send_msg('nBank0Chn', 'nTempo2', nTempo2)

  def disconnect(self):
    if self.song().tempo_has_listener(self.handle_tempo_tx_msg):
      self.song().remove_tempo_listener(self.handle_tempo_tx_msg)
    self.send_msg('nBank0Chn', 'nTempo1', 0)
    self.send_msg('nBank0Chn', 'nTempo2', 0)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def send_msg(self, psBankChn, psId, pnValue, pnIdx = 0):
    nBankChn = 0xB0 | self.cfg(psBankChn)
    nId      = self.cfg(psId) + pnIdx
    self.obj('oComm').send_msg([nBankChn, nId, pnValue])

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

