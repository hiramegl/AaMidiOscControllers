import Live

class Session():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_nTrackOff = 0
    self.m_nSceneOff = 0
    self.m_lCtrls = [
      'nSessLeft',  'nSessRight', 'nGoToSel',
      'nBank1Sync', 'nBank2Sync',
      'nBank3Sync', 'nBank4Sync',
      'nBank5Sync', 'nBank6Sync',
    ]
    self.connect()

    phObj['oSess'] = self
    self.handle_new_track_offset(self.m_nTrackOff)

  def connect(self):
    for sCtrl in self.m_lCtrls:
      self.add_session_handler('nBank0Chn', sCtrl)
    self.update_nav_ctrls()
    self.highlight_session()

  # session ----------------------------
  def add_session_handler(self, psBankChn, psId):
    fSessionCb = lambda ptKey, pnValue: self.handle_session_rx_msg(ptKey, pnValue)
    self.obj('oComm').reg_cc(
      self.cfg(psBankChn), self.cfg(psId), psId, fSessionCb)

  def handle_session_rx_msg(self, ptKey, pnValue):
    self.dlog('-----> HANDLING RX: 0x%X %d %d' % (ptKey[0], ptKey[1], pnValue))

    nId = ptKey[1]
    if nId == self.cfg('nSessLeft'):
      if self.m_nTrackOff != 0:
        self.handle_new_track_offset(self.m_nTrackOff - self.cfg('nTracks'))
      self.update_nav_ctrls()

    elif nId == self.cfg('nSessRight'):
      if self.m_nTrackOff + self.cfg('nTracks') < len(self.tracks_and_returns()):
        self.handle_new_track_offset(self.m_nTrackOff + self.cfg('nTracks'))
      self.update_nav_ctrls()

    elif nId == self.cfg('nGoToSel'):
      if pnValue == 0: return
      nTrackIdxAbs = self.sel_track_idx_abs()
      self.handle_new_track_offset(nTrackIdxAbs)
      self.update_nav_ctrls()

    else:
      # bank sync
      if pnValue == 0: return
      self.update_nav_ctrls()
      nBankChn = nId - self.cfg('nBank1Sync')
      self.obj('oTrack').sync_track(nBankChn)

  def handle_new_track_offset(self, pnTrackOff):
    self.m_nTrackOff = pnTrackOff
    oTrack = list(self.tracks_and_returns())[pnTrackOff]
    self.obj('oTrack').update_track(oTrack)
    self.highlight_session()

  def update_nav_ctrls(self):
    if self.m_nTrackOff != 0:
      self.send_msg('nBank0Chn', 'nSessLeft', 127)
    else:
      self.send_msg('nBank0Chn', 'nSessLeft', 0)

    if self.m_nTrackOff + self.cfg('nTracks') < len(self.tracks_and_returns()):
      self.send_msg('nBank0Chn', 'nSessRight', 127)
    else:
      self.send_msg('nBank0Chn', 'nSessRight', 0)

  def highlight_session(self):
    self.obj('oCtrlInst').set_session_highlight(
      self.m_nTrackOff,
      self.m_nSceneOff,
      self.cfg('nTracks'),
      self.cfg('nScenes'),
      self.cfg('bIncRet'))

  def disconnect(self):
    if self.cfg('bClean') == False:
      return

    # reset midi controls
    nBk0Chn   = 0xB0 | self.cfg('nBank0Chn')
    lSessBnd  = list(map(lambda x: [nBk0Chn, self.cfg(x),   0], self.m_lCtrls))

    lBundle = lSessBnd
    self.obj('oComm').send_bundle(lBundle)
    self.obj('oTrack').disconnect()

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

  def sel_track_idx_abs(self):
    aAllTracks = self.tracks_and_returns()
    oSelTrack  = self.sel_track()
    return list(aAllTracks).index(oSelTrack)

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

