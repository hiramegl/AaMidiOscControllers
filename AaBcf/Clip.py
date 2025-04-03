class Clip():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_oCurrClip = None
    self.m_oCurrPitx = None
    self.m_bLstAdded = False
    self.connect()

    phObj['oClip'] = self

  def connect(self):
    fClipCb  = lambda ptKey, pnValue: self.handle_clip_rx_msg(ptKey, pnValue)
    nBank0Chn = self.cfg('nBank0Chn')
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nClpGain'),    'ClpGain',    fClipCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nClpPit'),     'ClpPit',     fClipCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nClpDet'),     'ClpDet',     fClipCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nClpGainRst'), 'ClpGainRst', fClipCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nClpPitRst'),  'ClpPitRst',  fClipCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nClpDetRst'),  'ClpDetRst',  fClipCb)

    self.add_listeners()

  def add_listeners(self):
    oTrack = self.get_track_or_none()
    if oTrack == None: return

    if (oTrack.has_audio_input):
      oClipSlot = self.sel_clip_slot_or_none()
      if oClipSlot == None: return

      oClip = oClipSlot.clip
      if oClip == None: return

      self.m_oCurrClip = oClip
      oClip.add_gain_listener        (self.handle_clip_tx_msg)
      oClip.add_pitch_coarse_listener(self.handle_clip_tx_msg)
      oClip.add_pitch_fine_listener  (self.handle_clip_tx_msg)
    else:
      if self.m_bLstAdded: return
      aDevices = oTrack.devices
      for nDevIdx in range(len(aDevices)):
        oDevice = aDevices[nDevIdx]
        sClass  = oDevice.class_name
        if (sClass != 'MidiPitcher'):
          continue
        aParams = oDevice.parameters
        for nPrmIdx  in range(len(aParams)):
          oParam = aParams[nPrmIdx]
          if (oParam.name != 'Pitch'): continue
          self.m_bLstAdded = True

          if self.m_oCurrPitx != None and self.m_oCurrPitx != oParam:
            m_oCurrPitx.remove_value_listener(self.handle_clip_tx_msg)

          self.m_oCurrPitx = oParam
          if oParam.value_has_listener(self.handle_clip_tx_msg) == False:
            oParam.add_value_listener(self.handle_clip_tx_msg)

  def handle_clip_rx_msg(self, ptKey, pnValue):
    if self.m_oCurrClip == None and self.m_oCurrPitx == None:
      self.clear_values()
      return

    nCh = ptKey[0]
    nId = ptKey[1]

    if self.m_oCurrClip != None:
      if nId == self.cfg('nClpGain'): # audio clip
        nGain = float(pnValue) / 127.0
        self.m_oCurrClip.gain = nGain
        self.alert('Current clip GAIN: %.3f' % (nGain))
      elif nId == self.cfg('nClpPit'):
        fValue = float(pnValue) - 64.0
        fPitch = fValue / 1.3 # coarse pitch, 128 / 97 ~= 1.3
        nPitch = int(fPitch)
        nPitch = -48 if nPitch < -48 else nPitch
        self.m_oCurrClip.pitch_coarse = nPitch
        self.alert('Current clip PITCH: %d' % (nPitch))
      elif nId == self.cfg('nClpDet'):
        fValue  = float(pnValue) - 64.0
        fDetune = fValue / 1.28 # fine pitch, 128 / 100
        nDetune = int(fDetune)
        nDetune = -49 if nDetune < -49 else nDetune
        nDetune =  49 if nDetune >  49 else nDetune
        self.m_oCurrClip.pitch_fine = nDetune
        self.alert('Current clip DETUNE: %d' % (nDetune))
      elif nId == self.cfg('nClpGainRst'):
        self.m_oCurrClip.gain = 0.4 # 0 dB
        self.alert('Current clip GAIN: %.3f' % (0.4))
      elif nId == self.cfg('nClpPitRst'):
        self.m_oCurrClip.pitch_coarse = 0
        self.alert('Current clip PITCH: %d' % (0))
      if nId == self.cfg('nClpDetRst'):
        self.m_oCurrClip.pitch_fine = 0
        self.alert('Current clip DETUNE: %d' % (0))

    else: # midi track with MidiPitcher device
      if nId == self.cfg('nClpPit'):
        nPitch = pnValue - 64
        nPitch = -64 if nPitch < -64 else nPitch
        nPitch =  63 if nPitch >  63 else nPitch
        self.m_oCurrPitx.value = nPitch
        self.alert('Current clip PITCH: %d' % (nPitch))
      elif nId == self.cfg('nClpPitRst'):
        self.m_oCurrPitx.value = 0
        self.alert('Current clip PITCH: %d' % (0))
      else:
        self.obj('oComm').send_msg([nCh, nId, 0])

  def handle_clip_tx_msg(self):
    if self.m_oCurrClip == None and self.m_oCurrPitx == None:
      self.clear_values()
      return

    if self.m_oCurrClip != None:
      # update AUDIO clip gain
      nValue = int(self.m_oCurrClip.gain * 127.0)
      self.send_msg('nBank0Chn', 'nClpGain', nValue)

      # update AUDIO clip pitch
      nPitch = self.m_oCurrClip.pitch_coarse
      fValue = float(nPitch) * 1.3 + 64.0
      nValue = int(fValue)
      self.send_msg('nBank0Chn', 'nClpPit', nValue)

      # update AUDIO clip detune
      nDetune = self.m_oCurrClip.pitch_fine # -49 ... 49
      fValue  = float(nDetune) * 1.28 + 64.0
      nValue  = int(fValue)
      nValue = 1   if nValue < 1   else nValue
      nValue = 127 if nValue > 127 else nValue
      self.send_msg('nBank0Chn', 'nClpDet', nValue)
    else:
      # update MIDI pitch only
      nValue = 0
      if self.m_oCurrPitx != None:
        nValue = int(self.m_oCurrPitx.value + 64)
        nValue = 0   if nValue < 0   else nValue
        nValue = 127 if nValue > 127 else nValue

      self.send_msg('nBank0Chn', 'nClpGain', 0)
      self.send_msg('nBank0Chn', 'nClpPit',  nValue)
      self.send_msg('nBank0Chn', 'nClpDet',  0)

  def clear_values(self):
    self.send_msg('nBank0Chn', 'nClpGain', 0)
    self.send_msg('nBank0Chn', 'nClpPit',  0)
    self.send_msg('nBank0Chn', 'nClpDet',  0)

  def sync(self):
    self.handle_clip_tx_msg()

  def update(self):
    self.remove_listeners()
    self.add_listeners()
    self.handle_clip_tx_msg()

  def remove_listeners(self):
    if self.m_oCurrClip != None:
      self.m_oCurrClip.remove_gain_listener        (self.handle_clip_tx_msg)
      self.m_oCurrClip.remove_pitch_coarse_listener(self.handle_clip_tx_msg)
      self.m_oCurrClip.remove_pitch_fine_listener  (self.handle_clip_tx_msg)

    if self.m_oCurrPitx != None:
      if self.m_oCurrPitx != None:
        self.m_bLstAdded = False
        self.m_oCurrPitx.remove_value_listener(self.handle_clip_tx_msg)

    self.m_oCurrClip = None
    self.m_oCurrPitx = None

  def disconnect(self):
    self.remove_listeners()
    self.clear_values()

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def tracks(self):
    return self.song().visible_tracks

  def master(self):
    return self.song().master_track

  def sel_track(self, poTrack = None):
    if (poTrack != None):
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  def get_track_or_none(self):
    oSelTrack = self.sel_track()
    if (oSelTrack == None):          return None
    if (oSelTrack == self.master()): return None
    if (oSelTrack in self.tracks()):
      return oSelTrack
    return None

  def sel_clip_slot_or_none(self):
    return self.song().view.highlighted_clip_slot

  def send_msg(self, psBankChn, psId, pnValue, pnIdx = 0):
    nBankChn = 0xB0 | self.cfg(psBankChn)
    nId      = self.cfg(psId) + pnIdx
    self.obj('oComm').send_msg([nBankChn, nId, pnValue])

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

