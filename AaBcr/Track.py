import Live

from .Router import Router

class Track():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_lRootIds = []
    self.m_nBankChn = 0
    self.connect()
    phObj['oTrack'] = self

    # init
    Router(phCfg, phObj)

  def connect(self):
    self.m_lRootIds = []
    for nBankIdx in range(self.cfg('nBanks')):
      nBankChn = self.cfg('nBank%dChn' % (nBankIdx + 1))
      for nCtrlIdx in range(4): # 4 group button controls
        nRootName = 'nGB%dOff' % (nCtrlIdx)
        self.reg_cc(nBankChn, nRootName)
      for nCtrlIdx in range(4): # 4 group rotary controls
        nRootName = 'nGR%dOff' % (nCtrlIdx)
        self.reg_cc(nBankChn, nRootName)
      for nCtrlIdx in range(2): # 2 main button controls
        nRootName = 'nMB%dOff' % (nCtrlIdx)
        self.reg_cc(nBankChn, nRootName)
      for nCtrlIdx in range(3): # 3 main rotary controls
        nRootName = 'nMR%dOff' % (nCtrlIdx)
        self.reg_cc(nBankChn, nRootName)

  def reg_cc(self, pnBankChn, pnRootName):
    pnRootId = self.cfg(pnRootName)
    if pnBankChn == 0:
      self.m_lRootIds.append(pnRootId)

    fMidiCb = lambda ptKey, pnValue: self.handle_midi_rx_msg(ptKey, pnValue)
    for nStripIdx in range(self.cfg('nStrips')):
      nId = pnRootId + nStripIdx
      self.obj('oComm').reg_cc(
        pnBankChn, nId, 'Ctrl_%d_%d' % (pnBankChn, nId), fMidiCb)

  def handle_midi_rx_msg(self, ptKey, pnValue):
    self.dlog('-> Rx: 0x%X %d %d' % (ptKey[0], ptKey[1], pnValue))
    self.obj('oRouter').route(ptKey, pnValue)

  def disconnect(self):
    self.obj('oRouter').unbind_track_devs()
    self.clear()
    self.m_lRootIds.clear()

  def clear(self):
    for nCtrlIdx in range(4): # 4 group button controls
      nRootName = 'nGB%dOff' % (nCtrlIdx)
      self.send_clear_msgs(self.m_nBankChn, nRootName)
    for nCtrlIdx in range(4): # 4 group rotary controls
      nRootName = 'nGR%dOff' % (nCtrlIdx)
      self.send_clear_msgs(self.m_nBankChn, nRootName)
    for nCtrlIdx in range(2): # 2 main button controls
      nRootName = 'nMB%dOff' % (nCtrlIdx)
      self.send_clear_msgs(self.m_nBankChn, nRootName)
    for nCtrlIdx in range(3): # 3 main rotary controls
      nRootName = 'nMR%dOff' % (nCtrlIdx)
      self.send_clear_msgs(self.m_nBankChn, nRootName)

  def send_clear_msgs(self, pnBankChn, pnRootName):
    pnRootId = self.cfg(pnRootName)
    nBankChn = 0xB0 | pnBankChn

    lBundle = []
    for nStripIdx in range(self.cfg('nStrips')):
      nId = pnRootId + nStripIdx
      lBundle.append([nBankChn, nId, 0])
    self.obj('oComm').send_bundle(lBundle)

  # ********************************************************

  def bind_track(self, poTrack):
    self.dlog('-> Binding track: %s' % (poTrack.name))
    self.obj('oRouter').bind_track_devs(poTrack, self.m_lRootIds)

  def unbind_track(self):
    self.dlog('-> Unbinding track!')
    self.obj('oRouter').unbind_track_devs()

  def update_track(self, poTrack):
    self.unbind_track()
    self.bind_track(poTrack)
    self.sync_track(self.m_nBankChn) # use current bank channel

  def sync_track(self, pnBankChn = 0):
    self.m_nBankChn = pnBankChn
    self.dlog('-> Track: Syncing bank %d' % (pnBankChn))
    bSyncOk = self.obj('oRouter').sync_track_devs(pnBankChn)
    if bSyncOk == False:
      self.clear()
    self.alert('Syncing bank %d' % (pnBankChn))

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def tracks(self):
    return self.song().visible_tracks

  def returns(self):
    return self.song().return_tracks

  def master(self):
    return self.song().master_track

  def tracks_and_returns(self):
    return tuple(self.tracks()) + tuple(self.returns())

  def sel_track(self, poTrack = None):
    if (poTrack != None):
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  def get_track_or_none(self):
    oSelTrack = self.sel_track()
    if (oSelTrack == None):          return None
    if (oSelTrack == self.master()): return None
    if (oSelTrack in self.tracks_and_returns()):
      return oSelTrack
    return None

  def log(self, psMessage):
    Live.Base.log(psMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)

