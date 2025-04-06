import time
import Live

class Session():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_bBusy     = False
    self.m_hAutoVol  = {}
    self.m_lVolCbs   = []
    self.m_lTrackCbs = []
    self.m_nTrackOff = 0
    self.m_nSceneOff = 0
    self.m_lCtrls = [
      'nSessLeft',  'nSessRight', 'nStopTot',
      'nBank1Sync', 'nBank2Sync', 'nBank3Sync', 'nBank4Sync',
    ]
    self.connect()

    phObj['oSess'] = self

  def connect(self):
    self.connect_track_ctrls()
    for fTrkTxCb in self.m_lTrackCbs:
      fTrkTxCb()
    for nTrackIdxRel in range(self.cfg('nTracks')):
      self.send_msg('nBank2Chn', 'nStopOff', 127, nTrackIdxRel)
      self.send_msg('nBank2Chn', 'nSelOff',  127, nTrackIdxRel)
    for sCtrl in self.m_lCtrls:
      self.add_session_handler('nBank0Chn', sCtrl)
    self.update_nav_ctrls()
    self.highlight_session()
    self.obj('oTempo').sync()
    self.obj('oClip' ).sync()
    self.obj('oTrack').sync()
    self.obj('oScene').sync()

  def connect_track_ctrls(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      self.add_vol_handler   (nTrackIdxRel)
      self.add_track_handlers(nTrackIdxRel)

  # vol --------------------------------
  def add_vol_handler(self, pnTrackIdxRel):
    nTrackIdxAbs = self.get_track_idx_abs(pnTrackIdxRel)
    if self.is_track_available(nTrackIdxAbs) == False:
      return
    oVolume = self.get_track(nTrackIdxAbs).mixer_device.volume

    nBank0Chn = self.cfg('nBank0Chn')
    nVolOff   = self.cfg('nVolOff')
    tVolKey   = self.obj('oComm').reg_cc(
      nBank0Chn, nVolOff + pnTrackIdxRel, oVolume)

    fVolTxCb = lambda :self.handle_vol_tx_msg(tVolKey)
    oVolume.add_value_listener(fVolTxCb)
    self.m_lVolCbs.insert(pnTrackIdxRel, fVolTxCb)

  # No need for self.handle_vol_rx_msg() since volume
  # parameter change is handled in Comm (volume has '.value')

  def handle_vol_tx_msg(self, ptKey):
    if self.cfg('bDebug'):
      self.log('----> TX VOL CHANGE for: 0x%X %d' % (ptKey[0], ptKey[1]))
    self.obj('oComm').update_midi_ctrl(ptKey)

  # track ------------------------------
  def add_track_handlers(self, pnTrackIdxRel):
    nTrackIdxAbs = self.get_track_idx_abs(pnTrackIdxRel)
    if self.is_track_available(nTrackIdxAbs) == False:
      return
    oTrack = self.get_track(nTrackIdxAbs)

    fTrkRxCb = lambda ptKey, pnValue: self.handle_track_rx_msg(ptKey, oTrack, pnTrackIdxRel, pnValue)
    nBank1Chn = self.cfg('nBank1Chn')
    self.obj('oComm').reg_cc(
      nBank1Chn, self.cfg('nMuteOff') + pnTrackIdxRel, 'Mute', fTrkRxCb)
    self.obj('oComm').reg_cc(
      nBank1Chn, self.cfg('nSoloOff') + pnTrackIdxRel, 'Solo', fTrkRxCb)

    nBank2Chn = self.cfg('nBank2Chn')
    self.obj('oComm').reg_cc(
      nBank2Chn, self.cfg('nStopOff') + pnTrackIdxRel, 'Stop', fTrkRxCb)
    self.obj('oComm').reg_cc(
      nBank2Chn, self.cfg('nSelOff')  + pnTrackIdxRel, 'Sel',  fTrkRxCb)

    nBank3Chn = self.cfg('nBank3Chn')
    self.obj('oComm').reg_cc(
      nBank3Chn, self.cfg('nInputOff') + pnTrackIdxRel, 'Input', fTrkRxCb)
    self.obj('oComm').reg_cc(
      nBank3Chn, self.cfg('nArmOff')   + pnTrackIdxRel, 'Arm',   fTrkRxCb)

    nBank4Chn = self.cfg('nBank4Chn')
    self.obj('oComm').reg_cc(
      nBank4Chn, self.cfg('nCrossOff') + pnTrackIdxRel, 'Cross', fTrkRxCb)
    self.obj('oComm').reg_cc(
      nBank4Chn, self.cfg('nAvVelOff') + pnTrackIdxRel, 'AvVel', fTrkRxCb)
    self.obj('oComm').reg_cc(
      nBank4Chn, self.cfg('nAvDecOff') + pnTrackIdxRel, 'AvDec', fTrkRxCb)
    nTrackHash = hash(oTrack)
    if (nTrackHash in self.m_hAutoVol) == False:
      self.m_hAutoVol[nTrackHash] = {
        'nVel'    : 20,  # default is 20 bars
        'nVelMidi': 40,  # midi value
        'bOn'     : False,
        'nDelta'  : 0.0,
        'nStart'  : 0.0,
        'nTgtVol' : 0.0,
      }

    fTrkTxCb = lambda :self.handle_track_tx_msg(oTrack, pnTrackIdxRel)
    oTrack.add_mute_listener(fTrkTxCb)
    oTrack.add_solo_listener(fTrkTxCb)
    oTrack.add_current_monitoring_state_listener(fTrkTxCb)
    oTrack.add_arm_listener (fTrkTxCb)
    oTrack.mixer_device.add_crossfade_assign_listener(fTrkTxCb)
    self.m_lTrackCbs.insert(pnTrackIdxRel, fTrkTxCb)

  def handle_track_rx_msg(self, ptKey, poTrack, pnTrackIdxRel, pnValue):
    if self.cfg('bDebug'):
      self.log('-----> HANDLING RX: [0x%X %d %d] for track %d' % (ptKey[0], ptKey[1], pnValue, pnTrackIdxRel))

    nCh = ptKey[0] & 0x0F # lowest 4 bits is channel number
    nId = ptKey[1]
    if self.msg_is(nCh, 'nBank1Chn', nId, 'nMuteOff'):
      poTrack.mute = (pnValue == 0)
      self.alert('Track "%s", MUTE: %s' % (poTrack.name, 'ON' if pnValue == 0 else 'OFF'))
    elif self.msg_is(nCh, 'nBank1Chn', nId, 'nSoloOff'):
      poTrack.solo = (pnValue == 127)
      self.alert('Track "%s", SOLO: %s' % (poTrack.name, 'ON' if pnValue == 127 else 'OFF'))

    elif self.msg_is(nCh, 'nBank2Chn', nId, 'nStopOff'):
      poTrack.stop_all_clips()
      self.send_msg('nBank2Chn', 'nStopOff', 127, pnTrackIdxRel)
      self.alert('Track "%s", STOP ALL CLIPS' % (poTrack.name))
    elif self.msg_is(nCh, 'nBank2Chn', nId, 'nSelOff'):
      self.sel_track(poTrack)
      self.send_msg('nBank2Chn', 'nSelOff',  127, pnTrackIdxRel)
      self.alert('Track "%s", SELECTED' % (poTrack.name))

    elif self.msg_is(nCh, 'nBank3Chn', nId, 'nInputOff'):
      nMonitor = (poTrack.current_monitoring_state - 1) % 3
      poTrack.current_monitoring_state = nMonitor
      lTypes = ['IN', 'AUTO', 'OFF']
      self.alert('Track "%s", INPUT: %s' % (poTrack.name, lTypes[nMonitor]))
    elif self.msg_is(nCh, 'nBank3Chn', nId, 'nArmOff'):
      poTrack.arm = (pnValue == 127)
      self.alert('Track "%s", ARM: %s' % (poTrack.name, 'ON' if pnValue == 127 else 'OFF'))

    elif self.msg_is(nCh, 'nBank4Chn', nId, 'nCrossOff'):
      nCross = (poTrack.mixer_device.crossfade_assign - 1) % 3
      poTrack.mixer_device.crossfade_assign = nCross
      self.send_msg('nBank4Chn', 'nCrossOff', 127, pnTrackIdxRel)
      lTypes = ['A', 'OFF', 'B']
      self.alert('Track "%s", CROSS: %s' % (poTrack.name, lTypes[nCross]))
    elif self.msg_is(nCh, 'nBank4Chn', nId, 'nAvVelOff'):
      hAutoVol = self.m_hAutoVol[hash(poTrack)]
      hAutoVol['nVel']     = pnValue / 2 # 0 ... 63
      hAutoVol['nVelMidi'] = pnValue
      self.update_auto_vol(poTrack)
    elif self.msg_is(nCh, 'nBank4Chn', nId, 'nAvDecOff'):
      hAutoVol = self.m_hAutoVol[hash(poTrack)]
      hAutoVol['bOn']     = (pnValue == 127)
      hAutoVol['nStart']  = time.time()
      hAutoVol['nTgtVol'] = 0.0
      self.update_auto_vol(poTrack)

  def msg_is(self, pnCh, psBankChn, pnId, psType):
    return (pnCh == self.cfg(psBankChn) and
      pnId >=  self.cfg(psType) and
      pnId <  (self.cfg(psType) + self.cfg('nTracks')))

  def update_auto_vol(self, poTrack):
    hAutoVol = self.m_hAutoVol[hash(poTrack)]

    self.m_bBusy = True
    nVel      = hAutoVol['nVel']      # in bars
    nTgtVol   = hAutoVol['nTgtVol']   # target volume
    nCurrVol  = poTrack.mixer_device.volume.value
    nVel      = 0.5 if (nVel == 0) else nVel

    nTempo    = self.song().tempo     # in BPM
    nBarSpan  = (60.0 / nTempo) * 4.0 # in seconds
    nTimeSpan = nVel * nBarSpan       # in seconds
    nVolDelta = nTgtVol - nCurrVol
    nDelta    = (nVolDelta / nTimeSpan) / 10.0 # divide with 10.0 since update executes every 100 ms (~ish)

    hAutoVol['nDelta'] = nDelta
    sCmd = 'DECR' if (nDelta < 0.0) else 'INCR'
    self.alert('> VOL %s (%f -> %f) in %f [s] => %f [bars]' % (sCmd, nCurrVol, nTgtVol, nTimeSpan, nVel))
    self.m_bBusy = False

  def handle_track_tx_msg(self, poTrack, pnTrackIdxRel):
    if self.cfg('bDebug'):
      self.log('----> TX TRACK CHANGE for track %d' % (pnTrackIdxRel))
    hAutoVol = self.m_hAutoVol.get(hash(poTrack), None)

    nMute  = 0   if poTrack.mute else 127
    nSolo  = 127 if poTrack.solo else 0
    nInput = 127
    nArm   = 127 if poTrack.arm  else 0
    nAvVel = 0   if hAutoVol == None                             else hAutoVol['nVelMidi']
    nAvDec = 0   if hAutoVol == None or hAutoVol['bOn'] == False else 127

    nBank1Chn = 0xB0 | self.cfg('nBank1Chn')
    nMuteOff  = self.cfg('nMuteOff')
    nSoloOff  = self.cfg('nSoloOff')
    nBank3Chn = 0xB0 | self.cfg('nBank3Chn')
    nInputOff = self.cfg('nInputOff')
    nArmOff   = self.cfg('nArmOff')
    nBank4Chn = 0xB0 | self.cfg('nBank4Chn')
    nCrossOff = self.cfg('nCrossOff')
    nAvVelOff = self.cfg('nAvVelOff')
    nAvDecOff = self.cfg('nAvDecOff')

    self.obj('oComm').send_bundle([
      [nBank1Chn, nMuteOff  + pnTrackIdxRel, nMute],
      [nBank1Chn, nSoloOff  + pnTrackIdxRel, nSolo],
      [nBank3Chn, nInputOff + pnTrackIdxRel, nInput],
      [nBank3Chn, nArmOff   + pnTrackIdxRel, nArm],
      [nBank4Chn, nCrossOff + pnTrackIdxRel, 127],
      [nBank4Chn, nAvVelOff + pnTrackIdxRel, nAvVel],
      [nBank4Chn, nAvDecOff + pnTrackIdxRel, nAvDec],
    ])

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
      if self.m_nTrackOff != 0:
        self.handle_new_track_offset(self.m_nTrackOff - self.cfg('nTracks'))
      self.update_nav_ctrls()

    elif nId == self.cfg('nSessRight'):
      if self.m_nTrackOff + self.cfg('nTracks') < len(self.tracks()):
        self.handle_new_track_offset(self.m_nTrackOff + self.cfg('nTracks'))
      self.update_nav_ctrls()

    elif nId == self.cfg('nStopTot'):
      self.song().stop_all_clips()
      self.song().stop_playing()

    else:
      # bank sync
      self.sync_all_ctrls()
      self.update_nav_ctrls()
      self.obj('oTempo').sync()
      self.obj('oClip' ).sync()
      self.obj('oTrack').sync()
      self.obj('oScene').sync()

  def handle_new_track_offset(self, pnTrackOff):
    self.disconnect_track_ctrls()
    self.m_nTrackOff = pnTrackOff
    self.connect_track_ctrls()
    self.sync_all_ctrls()
    self.highlight_session()

  def sync_all_ctrls(self):
    for fVolTxCb in self.m_lVolCbs:
      fVolTxCb()
    for fTrkTxCb in self.m_lTrackCbs:
      fTrkTxCb()
    for nTrackIdxRel in range(self.cfg('nTracks')):
      self.send_msg('nBank2Chn', 'nStopOff', 127, nTrackIdxRel)
      self.send_msg('nBank2Chn', 'nSelOff',  127, nTrackIdxRel)

  def update_nav_ctrls(self):
    if self.m_nTrackOff != 0:
      self.send_msg('nBank0Chn', 'nSessLeft', 127)
    else:
      self.send_msg('nBank0Chn', 'nSessLeft', 0)

    if self.m_nTrackOff + self.cfg('nTracks') < len(self.tracks()):
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

  # disconnect -------------------------
  def disconnect(self):
    self.obj('oTempo').disconnect()
    self.obj('oClip' ).disconnect()
    self.obj('oTrack').disconnect()
    self.obj('oScene').disconnect()
    self.disconnect_track_ctrls();

    if self.cfg('bClean') == False:
      return

    # reset midi controls
    nTracks   = self.cfg('nTracks')
    nBk0Chn   = 0xB0 | self.cfg('nBank0Chn')
    nVolOff   = self.cfg('nVolOff')
    nBk1Chn   = 0xB0 | self.cfg('nBank1Chn')
    nMuteOff  = self.cfg('nMuteOff')
    nSoloOff  = self.cfg('nSoloOff')
    nBk2Chn   = 0xB0 | self.cfg('nBank2Chn')
    nStopOff  = self.cfg('nStopOff')
    nSelOff   = self.cfg('nSelOff')
    nBk3Chn   = 0xB0 | self.cfg('nBank3Chn')
    nInputOff = self.cfg('nInputOff')
    nArmOff   = self.cfg('nArmOff')
    nBk4Chn   = 0xB0 | self.cfg('nBank4Chn')
    nCrossOff = self.cfg('nCrossOff')
    nAvVelOff = self.cfg('nAvVelOff')
    nAvDecOff = self.cfg('nAvDecOff')

    lSessBnd  = list(map(lambda x: [nBk0Chn, self.cfg(x),   0], self.m_lCtrls))
    lVolBnd   = list(map(lambda x: [nBk0Chn, x + nVolOff,  10], range(nTracks)))
    lMuteBnd  = list(map(lambda x: [nBk1Chn, x + nMuteOff,  0], range(nTracks)))
    lSoloBnd  = list(map(lambda x: [nBk1Chn, x + nSoloOff,  0], range(nTracks)))
    lStopBnd  = list(map(lambda x: [nBk2Chn, x + nStopOff,  0], range(nTracks)))
    lSelBnd   = list(map(lambda x: [nBk2Chn, x + nSelOff,   0], range(nTracks)))
    lInputBnd = list(map(lambda x: [nBk3Chn, x + nInputOff, 0], range(nTracks)))
    lArmBnd   = list(map(lambda x: [nBk3Chn, x + nArmOff,   0], range(nTracks)))
    lCrossBnd = list(map(lambda x: [nBk4Chn, x + nCrossOff, 0], range(nTracks)))
    lAvVelBnd = list(map(lambda x: [nBk4Chn, x + nAvVelOff, 0], range(nTracks)))
    lAvDecBnd = list(map(lambda x: [nBk4Chn, x + nAvDecOff, 0], range(nTracks)))

    lBundle = lSessBnd + lVolBnd + lMuteBnd + lSoloBnd
    self.obj('oComm').send_bundle(lBundle)
    lBundle = lStopBnd + lSelBnd + lInputBnd + lArmBnd
    self.obj('oComm').send_bundle(lBundle)
    lBundle = lCrossBnd + lAvVelBnd + lAvDecBnd
    self.obj('oComm').send_bundle(lBundle)

  def disconnect_track_ctrls(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.get_track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break
      oTrack   = self.get_track(nTrackIdxAbs)
      oVolume  = oTrack.mixer_device.volume

      fVolTxCb = self.m_lVolCbs[nTrackIdxRel]
      if oVolume.value_has_listener(fVolTxCb):
        oVolume.remove_value_listener(fVolTxCb)

      fTrkTxCb = self.m_lTrackCbs[nTrackIdxRel]
      if oTrack.mute_has_listener(fTrkTxCb):
        oTrack.remove_mute_listener(fTrkTxCb)
      if oTrack.solo_has_listener(fTrkTxCb):
        oTrack.remove_solo_listener(fTrkTxCb)
      if oTrack.current_monitoring_state_has_listener(fTrkTxCb):
        oTrack.remove_current_monitoring_state_listener(fTrkTxCb)
      if oTrack.arm_has_listener(fTrkTxCb):
        oTrack.remove_arm_listener(fTrkTxCb)
      if oTrack.mixer_device.crossfade_assign_has_listener(fTrkTxCb):
        oTrack.mixer_device.remove_crossfade_assign_listener(fTrkTxCb)

    self.m_lVolCbs.clear()
    self.m_lTrackCbs.clear()

  # update sync tasks ------------------
  def update_sync_tasks(self):
    if (self.m_bBusy == True): return # busy updating delta

    lTracks = self.tracks()
    for nTrackIdxAbs in range(len(lTracks)):
      oTrack = lTracks[nTrackIdxAbs]
      if (hash(oTrack) in self.m_hAutoVol) == False: return
      hAutoVol = self.m_hAutoVol[hash(oTrack)]
      if hAutoVol['bOn'] == False: return
      nCurVol = oTrack.mixer_device.volume.value
      nDelta  = hAutoVol['nDelta']
      nNewVol = nCurVol + nDelta
      if (nDelta < 0.0):
        if (nNewVol < 0.0):
          hAutoVol['bOn'] = False
          nNewVol         = 0.0
          nTimeSpan       = time.time() - hAutoVol['nStart']
          self.alert('%s: reached MIN VOL in %f [sec]!' % (oTrack.name, nTimeSpan))
          nTrackIdxRel = self.get_track_idx_rel(nTrackIdxAbs)
          if nTrackIdxRel != None:
            self.send_msg('nBank4Chn', 'nAvDecOff', 0, nTrackIdxRel)
        oTrack.mixer_device.volume.value = nNewVol

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def tracks(self):
    return self.song().visible_tracks

  def is_track_available(self, pnTrackIdxAbs):
    return (pnTrackIdxAbs < len(self.tracks()))

  def get_track(self, pnTrackIdxAbs):
    return self.tracks()[pnTrackIdxAbs]

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

  def send_msg(self, psBankChn, psId, pnValue, pnIdx = 0):
    nBankChn = 0xB0 | self.cfg(psBankChn)
    nId      = self.cfg(psId) + pnIdx
    self.obj('oComm').send_msg([nBankChn, nId, pnValue])

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

