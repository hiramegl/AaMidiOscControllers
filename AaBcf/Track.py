import Live

class Track():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_oCurrPan = None
    self.connect()

    phObj['oTrack'] = self

  def connect(self):
    fTrackCb  = lambda ptKey, pnValue: self.handle_track_rx_msg(ptKey, pnValue)
    nBank0Chn = self.cfg('nBank0Chn')
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTrkSel'),    'TrkSel',    fTrackCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTrkPan'),    'TrkPan',    fTrackCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTrkSelRst'), 'TrkSelRst', fTrackCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nTrkPanRst'), 'TrkPanRst', fTrackCb)

    self.m_oCurrPan = self.song().view.selected_track.mixer_device.panning
    self.m_oCurrPan.add_value_listener(self.handle_trkpan_tx_msg)
    self.song().view.add_selected_track_listener(self.handle_trksel_tx_msg)

  def handle_track_rx_msg(self, ptKey, pnValue):
    nId = ptKey[1]

    if nId == self.cfg('nTrkSel'):
      if self.is_track_available(pnValue) == False: return
      self.sel_track(self.get_track(pnValue))
      self.alert('Selected track: %d' % (pnValue + 1))
    elif nId == self.cfg('nTrkPan'):
      nPan = float(pnValue - 64) / 64.0
      self.song().view.selected_track.mixer_device.panning.value = nPan
      self.alert('Selected track PAN: %.2f' % (nPan))
    if nId == self.cfg('nTrkSelRst'):
      if self.is_track_available(0) == False: return
      self.sel_track(self.get_track(0))
      self.send_msg('nBank0Chn', 'nTrkSel', 0)
      self.alert('Selected track: %d' % (1))
    elif nId == self.cfg('nTrkPanRst'):
      self.song().view.selected_track.mixer_device.panning.value = 0.0
      self.alert('Selected track PAN: %.2f' % (0.0))

  def handle_trksel_tx_msg(self):
    # update selected track control
    oSelTrack = self.sel_track()
    if oSelTrack == self.master():
      self.send_msg('nBank0Chn', 'nTrkSel', 0)
      self.m_oCurrPan = None
    else:
      nTrackIdxAbs = list(self.tracks_and_returns()).index(oSelTrack)
      if nTrackIdxAbs > 127: nTrackIdxAbs = 127
      self.send_msg('nBank0Chn', 'nTrkSel', nTrackIdxAbs)

    # update current panning parameter
    try:
      self.m_oCurrPan.remove_value_listener(self.handle_trkpan_tx_msg)
    except:
      Live.Base.log('-> Could not remove value listener from panning parameter')

    self.m_oCurrPan = oSelTrack.mixer_device.panning
    self.m_oCurrPan.add_value_listener(self.handle_trkpan_tx_msg)
    self.handle_trkpan_tx_msg()

    # update clip parameters
    self.obj('oClip').update()

  def handle_trkpan_tx_msg(self):
    nPan     = self.song().view.selected_track.mixer_device.panning.value
    nPanMidi = int(nPan * 64.0) + 64
    if nPanMidi > 127: nPanMidi = 127
    self.send_msg('nBank0Chn', 'nTrkPan', nPanMidi)

  def sync(self):
    self.handle_trksel_tx_msg()
    self.handle_trkpan_tx_msg()

  def disconnect(self):
    self.song().view.remove_selected_track_listener(self.handle_trksel_tx_msg)
    if self.m_oCurrPan != None:
      self.m_oCurrPan.remove_value_listener(self.handle_trkpan_tx_msg)
    self.send_msg('nBank0Chn', 'nTrkSel', 0)
    self.send_msg('nBank0Chn', 'nTrkPan', 0)

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

  def is_track_available(self, pnTrackIdxAbs):
    return (pnTrackIdxAbs < len(self.tracks_and_returns()))

  def get_track(self, pnTrackIdxAbs):
    return self.tracks_and_returns()[pnTrackIdxAbs]

  def sel_track(self, poTrack = None):
    if (poTrack != None):
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  def send_msg(self, psBankChn, psId, pnValue, pnIdx = 0):
    nBankChn = 0xB0 | self.cfg(psBankChn)
    nId      = self.cfg(psId) + pnIdx
    self.obj('oComm').send_msg([nBankChn, nId, pnValue])

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

