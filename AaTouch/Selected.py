from .Base import Base

class Selected(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_oAudioClip = None

    self.connect()
    self.update()

    phObj['oSelected'] = self

  # ********************************************************

  def connect(self):
    self.reg_cb('clip/sel/crop' , self.on_sel_clip_crop)
    self.reg_cb('clip/sel/warp' , self.on_sel_clip_warp)
    self.reg_cb('clip/sel/play' , self.on_sel_clip_play)
    self.reg_cb('track/sel/stop', self.on_sel_track_stop)
    self.reg_cb('track/sel/mute', self.on_sel_track_mute)
    self.reg_cb('track/sel/solo', self.on_sel_track_solo)
    self.reg_idx_cb(
      'clip/sel/sends', self.cfg('nReturns'), self.on_send)
    self.reg_idx_cb(
      'clip/sel/audio_det_coa_pos', 12, self.on_audio_det_coa)
    self.reg_idx_cb(
      'clip/sel/audio_det_coa_neg', 12, self.on_audio_det_coa)
    self.reg_idx_cb(
      'clip/sel/audio_det_fin_pos', 4, self.on_audio_det_fin)
    self.reg_idx_cb(
      'clip/sel/audio_det_fin_neg', 4, self.on_audio_det_fin)
    self.reg_cb('clip/sel/audio_gain', self.on_audio_gain)
    self.reg_idx_cb(
      'clip/sel/audio_reset', 3, self.on_audio_reset)

  def disconnect(self):
    self.send_msg('/track/sel/mute', 0.0)
    self.send_msg('/track/sel/solo', 0.0)
    self.send_msg('/clip/sel/warp' , 0.0)

    lBundle = []
    for nIdx in range(self.cfg('nReturns')):
      lBundle.append([
        '/clip/sel/sends/%d' % (nIdx),
        0.0])
    self.send_bundle(lBundle)
    self.send_msg('/clip/sel/audio_gain', 0.0)

  # ********************************************************

  def update(self):
    # update gain listener
    if self.m_oAudioClip != None:
      if self.m_oAudioClip.gain_has_listener(self.on_gain_change):
        self.m_oAudioClip.remove_gain_listener(self.on_gain_change)

    oAudioClip = self.state().get_audio_clip_or_none()
    if oAudioClip != None:
      oAudioClip.add_gain_listener(self.on_gain_change)
    self.m_oAudioClip = oAudioClip

    oTrack = self.sel_track()
    if oTrack in self.returns():
      self.disconnect()

    if oTrack == self.master():
      self.disconnect()
    else:
      # audio or return track -> update GUI controls
      nMute = 0.0 if oTrack.mute else 1.0
      nSolo = 1.0 if oTrack.solo else 0.0
      self.send_msg('/track/sel/mute', nMute)
      self.send_msg('/track/sel/solo', nSolo)

    self.update_warp()
    self.update_sends()

    oAudioClip = self.state().audio_clip_or_none()
    if oAudioClip == None:
      nValue = 0.0
    else:
      nValue = oAudioClip.gain
    self.send_msg('/clip/sel/audio_gain', nValue)

  def update_warp(self):
    oAudioClip = self.state().get_audio_clip_or_none()
    if oAudioClip == None:
      self.send_msg('/clip/sel/warp', 0.0)
      return
    nWarp = 1.0 if oAudioClip.warping else 0.0
    self.send_msg('/clip/sel/warp', nWarp)

  def update_sends(self):
    oTrack  = self.sel_track()
    lBundle = []
    lSends  = oTrack.mixer_device.sends
    for nIdx in range(self.cfg('nReturns')):
      if nIdx == len(lSends):
        break
      oSend = lSends[nIdx]
      nSend = 1.0 if oSend.value > 0.5 else 0.0
      lBundle.append([
        '/clip/sel/sends/%d' % (nIdx),
        nSend])
    self.send_bundle(lBundle)

  # ********************************************************

  def on_gain_change(self):
    nValue = self.m_oAudioClip.gain
    self.send_msg('/clip/sel/audio_gain', nValue)

  # ********************************************************

  def on_sel_clip_crop(self, plSegs, plMsg):
    oClip = self.state().get_clip_or_none()
    if oClip == None:
      self.alert('No clip to crop')
      return

    oClip.crop()
    self.alert('Cropping clip')

  def on_sel_clip_warp(self, plSegs, plMsg):
    oAudioClip = self.state().get_audio_clip_or_none()
    if oAudioClip == None:
      self.send_msg('/clip/sel/warp' , 0.0)
      self.alert('Warp only available on Audio clips')
      return

    nValue = plMsg[2]
    nWarp  = True if nValue > 0.5 else False
    oAudioClip.warping = nWarp
    # loop is turned off when warp = False
    self.obj('oLoop').update()

  def on_sel_clip_play(self, plSegs, plMsg):
    oClipSlot = self.state().focused_clip_slot_or_none()
    if oClipSlot != None:
      oClipSlot.fire()
      self.alert('Focused clip-slot fire')

  def on_sel_track_stop(self, plSegs, plMsg):
    oTrack = self.state().focused_track_or_none()
    if oTrack == None:
      return
    bQuantizedStop = True
    oTrack.stop_all_clips(bQuantizedStop)
    self.alert('Focused track stop')

  def on_sel_track_mute(self, plSegs, plMsg):
    oTrack = self.state().focused_track_or_none()
    if oTrack == None:
      return
    oTrack.mute = not oTrack.mute
    self.alert('Focused track mute')

  def on_sel_track_solo(self, plSegs, plMsg):
    oTrack = self.state().focused_track_or_none()
    if oTrack == None:
      return
    oTrack.solo = not oTrack.solo
    self.alert('Focused track solo')

  def on_send(self, plSegs, plMsg):
    nIdx   = int  (plSegs[4])
    nValue = float(plMsg[2])
    oTrack = self.state().focused_track_or_none()
    if oTrack == None:
      return
    oSend  = oTrack.mixer_device.sends[nIdx]
    oSend.value = nValue
    self.alert('Focused track send updated')

  def on_audio_det_coa(self, plSegs, plMsg):
    sAddr = plMsg[0]
    oAudioClip = self.state().audio_clip_or_none()
    if oAudioClip == None:
      self.alert('Coarse detune unavailable for MIDI clips')
      return

    nIdx = int(plSegs[4])
    if plSegs[3] == 'audio_det_coa_neg':
      nIdx -= 12
    else:
      nIdx += 1

    oAudioClip.pitch_coarse = nIdx
    self.alert('Clip coarse detune: %d' % (nIdx))

  def on_audio_det_fin(self, plSegs, plMsg):
    sAddr = plMsg[0]
    oAudioClip = self.state().audio_clip_or_none()
    if oAudioClip == None:
      self.alert('Fine detune unavailable for MIDI clips')
      return

    nIdx = int(plSegs[4])
    if plSegs[3] == 'audio_det_fin_neg':
      lValues = [-40, -30, -20, -10]
    else:
      lValues = [ 10,  20,  30,  40]

    oAudioClip.pitch_fine = lValues[nIdx]
    self.alert('Clip fine detune: %d' % (lValues[nIdx]))

  def on_audio_gain(self, plSegs, plMsg):
    sAddr = plMsg[0]
    oAudioClip = self.state().audio_clip_or_none()
    if oAudioClip == None:
      self.send_msg('/clip/sel/audio_gain' , 0.0)
      self.alert('Gain unavailable for MIDI clips')
      return

    nValue = plMsg[2]
    oAudioClip.gain = nValue
    self.alert('Gain: %.3f' % (nValue))

  def on_audio_reset(self, plSegs, plMsg):
    sAddr = plMsg[0]
    oAudioClip = self.state().audio_clip_or_none()
    if oAudioClip == None:
      self.alert('Reset unavailable for MIDI clips')
      return

    nIdx = int(plSegs[4])
    if nIdx == 0:
      oAudioClip.pitch_coarse = 0
      self.alert('Clip coarse detune: 0')

    elif nIdx == 1:
      oAudioClip.pitch_fine = 0
      self.alert('Clip fine detune: 0')

    elif nIdx == 2:
      oAudioClip.gain = 0.4
      self.alert('Gain: 0 dB')

