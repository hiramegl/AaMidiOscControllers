import Live

NavDirection = Live.Application.Application.View.NavDirection

class Session():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_nTrackOff = 0
    self.m_nSceneOff = 0
    self.m_nTempoVal = 0 # tempo value to compute tempo increment
    self.m_lCtrls = [
      'nSessLeft'  , 'nSessRight', 'nDevLeft'  , 'nDevRight',
      'nCrossfader', 'nCueVol'   , 'nMasterVol', 'nViewToggle',
      # transport controls
      'nLoop', 'nRewind', 'nForward',
      'nStop', 'nPlay'  , 'nRecord',
    ]
    self.connect()

    phObj['oSess'] = self

  def connect(self):
    self.connect_special_ctrls()
    self.connect_track_ctrls()
    for sCtrl in self.m_lCtrls:
      self.add_session_handler('nBank0Chn', sCtrl)

  def connect_special_ctrls(self):
    fSysexCb = lambda pnByte, paMsg: self.handle_sysex_rx_msg(pnByte, paMsg)
    self.obj('oComm').reg_sysex(fSysexCb)

    fPrChCb = lambda pnProgId, pnValue: self.handle_prch_rx_msg(pnProgId, pnValue)
    self.obj('oComm').reg_prch(self.cfg('nBank0Chn'), fPrChCb)

  def connect_track_ctrls(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      self.add_vol_handler   (nTrackIdxRel)
      self.add_track_handlers(nTrackIdxRel)
    self.highlight_session()

  # sysex ------------------------------
  def handle_sysex_rx_msg(self, pnByte, paMsg):
    nModeId = paMsg[11]
    self.log('----> In mode: %d' % (nModeId))

  # program change ---------------------
  def handle_prch_rx_msg(self, pnProgId, pnValue):
    #self.log('----> PrCh, value: %d' % (pnValue))
    if self.m_nTempoVal == pnValue:
      if pnValue == 0:
        self.song().tempo -= 1
      else:
        self.song().tempo += 1
    else:
      if pnValue < self.m_nTempoVal:
        self.song().tempo -= 1
      else:
        self.song().tempo += 1
      self.m_nTempoVal = pnValue

  # vol --------------------------------
  def add_vol_handler(self, pnTrackIdxRel):
    nTrackIdxAbs = self.get_track_idx_abs(pnTrackIdxRel)
    if self.is_track_available(nTrackIdxAbs) == False:
      return
    oVolume = self.get_track(nTrackIdxAbs).mixer_device.volume

    nBank0Chn = self.cfg('nBank0Chn')
    nVolOff   = self.cfg('nVolOff')
    self.obj('oComm').reg_cc(
      nBank0Chn, nVolOff + pnTrackIdxRel, oVolume)

  # track ------------------------------
  def add_track_handlers(self, pnTrackIdxRel):
    nTrackIdxAbs = self.get_track_idx_abs(pnTrackIdxRel)
    if self.is_track_available(nTrackIdxAbs) == False: next
    oTrack = self.get_track(nTrackIdxAbs)

    fTrkRxCb = lambda ptKey, pnValue: self.handle_track_rx_msg(ptKey, oTrack, pnTrackIdxRel, pnValue)
    nBank0Chn = self.cfg('nBank0Chn')
    nPanOff   = self.cfg('nPanOff')
    nSelOff   = self.cfg('nSelOff')
    nRstOff   = self.cfg('nResetOff')
    nMuteOff  = self.cfg('nMuteOff')
    nSoloOff  = self.cfg('nSoloOff')
    self.obj('oComm').reg_cc(nBank0Chn, nPanOff  + pnTrackIdxRel, 'Pan',  fTrkRxCb)
    self.obj('oComm').reg_cc(nBank0Chn, nSelOff  + pnTrackIdxRel, 'Sel',  fTrkRxCb)
    self.obj('oComm').reg_cc(nBank0Chn, nRstOff  + pnTrackIdxRel, 'Rst',  fTrkRxCb)
    self.obj('oComm').reg_cc(nBank0Chn, nMuteOff + pnTrackIdxRel, 'Mute', fTrkRxCb)
    self.obj('oComm').reg_cc(nBank0Chn, nSoloOff + pnTrackIdxRel, 'Solo', fTrkRxCb)

  def handle_track_rx_msg(self, ptKey, poTrack, pnTrackIdxRel, pnValue):
    if self.cfg('bDebug'):
      self.log('-----> HANDLING RX: [0x%X %d %d] for track %d' % (ptKey[0], ptKey[1], pnValue, pnTrackIdxRel))

    nId = ptKey[1]
    if self.msg_is(nId, 'nPanOff'):
      poTrack.mixer_device.panning.value = float(pnValue - 64) / 64.0
    elif self.msg_is(nId, 'nSelOff'):
      if pnValue == 0: return
      self.sel_track(poTrack)
    elif self.msg_is(nId, 'nResetOff'):
      if pnValue == 0: return
      for oDev in poTrack.devices:
        for oParam in oDev.parameters:
          if oParam.name == 'Device On':
            oParam.value = 0 # turn off the device
            break
    elif self.msg_is(nId, 'nMuteOff'):
      if pnValue == 0: return
      poTrack.mute = not poTrack.mute
    elif self.msg_is(nId, 'nSoloOff'):
      if pnValue == 0: return
      poTrack.solo = not poTrack.solo

  def msg_is(self, pnId, psType):
    return (pnId >= self.cfg(psType) and
      pnId < (self.cfg(psType) + self.cfg('nTracks')))

  # session ----------------------------
  def add_session_handler(self, psBankChn, psId):
    fSessionCb = lambda ptKey, pnValue: self.handle_session_rx_msg(ptKey, pnValue)
    self.obj('oComm').reg_cc(
      self.cfg(psBankChn), self.cfg(psId), psId, fSessionCb)

  def handle_session_rx_msg(self, ptKey, pnValue):
    if self.cfg('bDebug'):
      self.log('-----> HANDLING RX: 0x%X %d %d' % (ptKey[0], ptKey[1], pnValue))

    nId = ptKey[1]
    if nId == self.cfg('nSessLeft'):
      if pnValue == 0: return
      if self.m_nTrackOff != 0:
        self.handle_new_track_offset(self.m_nTrackOff - self.cfg('nTracks'))
    elif nId == self.cfg('nSessRight'):
      if pnValue == 0: return
      if self.m_nTrackOff + self.cfg('nTracks') < len(self.tracks_and_returns()):
        self.handle_new_track_offset(self.m_nTrackOff + self.cfg('nTracks'))
    elif nId == self.cfg('nDevLeft'):
      if pnValue == 0: return
      oView = self.application().view
      oView.show_view (u'Detail/DeviceChain')
      oView.focus_view(u'Detail/DeviceChain')
      oView.scroll_view(NavDirection.left, u'Detail/DeviceChain', False)
    elif nId == self.cfg('nDevRight'):
      if pnValue == 0: return
      oView = self.application().view
      oView.show_view (u'Detail/DeviceChain')
      oView.focus_view(u'Detail/DeviceChain')
      oView.scroll_view(NavDirection.right, u'Detail/DeviceChain', False)

    elif nId == self.cfg('nCrossfader'):
      self.master().mixer_device.crossfader.value = float(pnValue - 64) / 64.0
    elif nId == self.cfg('nCueVol'):
      self.master().mixer_device.cue_volume.value = float(pnValue) / 127.0
    elif nId == self.cfg('nMasterVol'):
      self.master().mixer_device.volume.value = float(pnValue) / 127.0
    elif nId == self.cfg('nViewToggle'):
      if pnValue == 0: return
      oView = self.application().view
      oView.show_view ('Detail')
      oView.focus_view('Detail')
      if (oView.is_view_visible('Detail/Clip')):
        oView.show_view ('Detail/DeviceChain')
        oView.focus_view('Detail/DeviceChain')
      else:
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')

    elif nId == self.cfg('nLoop'):
      if pnValue == 0: return
      oClipSlot = self.sel_clip_slot()
      if (oClipSlot == None): return
      oClip = oClipSlot.clip
      if (oClip == None): return
      oClip.looping = not oClip.looping
    elif nId == self.cfg('nRewind'):
      if pnValue == 0: return
      self.song().current_song_time = max(0.0, self.song().current_song_time - 1)
    elif nId == self.cfg('nForward'):
      if pnValue == 0: return
      self.song().current_song_time += 1
    elif nId == self.cfg('nStop'):
      if pnValue == 0: return
      oClipSlot = self.sel_clip_slot()
      if oClipSlot != None:
        oClipSlot.stop()
    elif nId == self.cfg('nPlay'):
      if pnValue == 0: return
      oClipSlot = self.sel_clip_slot()
      if oClipSlot != None:
        oClipSlot.fire()
    elif nId == self.cfg('nRecord'):
      if pnValue == 0: return
      self.song().record_mode = not self.song().record_mode

  def handle_new_track_offset(self, pnTrackOff):
    self.m_nTrackOff = pnTrackOff
    self.connect_track_ctrls()
    self.highlight_session()
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot != None):
      oClipSlot.stop()

  def highlight_session(self):
    self.obj('oCtrlInst').set_session_highlight(
      self.m_nTrackOff,
      self.m_nSceneOff,
      self.cfg('nTracks'),
      self.cfg('nScenes'),
      True) # include return tracks

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def application(self):
    return Live.Application.get_application()

  def tracks(self):
    return self.song().visible_tracks

  def returns(self):
    return self.song().return_tracks

  def master(self):
    return self.song().master_track

  def tracks_and_returns(self):
    return tuple(self.tracks()) + tuple(self.returns())

  def is_track_available(self, pnTrackIdxAbs):
    return (pnTrackIdxAbs < len(self.tracks_and_returns()))

  def get_track(self, pnTrackIdxAbs):
    return self.tracks_and_returns()[pnTrackIdxAbs]

  def get_track_idx_abs(self, pnTrackIdxRel):
    return self.m_nTrackOff + pnTrackIdxRel

  def get_track_idx_rel(self, pnTrackIdxAbs):
    nTrackIdxRel = pnTrackIdxAbs - self.m_nTrackOff
    if nTrackIdxRel < 0: return None
    return nTrackIdxRel

  def sel_track(self, poTrack = None):
    if (poTrack != None):
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  def sel_clip_slot(self):
    return self.song().view.highlighted_clip_slot

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

