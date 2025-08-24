import Live

BUTTON_OFF = 0
BUTTON_ON  = 127

class ModeTune():
  def __init__(self, poCtrlInst, phCfg, phObj, poMatrix, plBottom, plSide):
    self.m_oCtrlInst = poCtrlInst
    self.m_hCfg      = phCfg
    self.m_hObj      = phObj
    self.m_oMatrix   = poMatrix
    self.m_lBottom   = plBottom
    self.m_lSide     = plSide

    self.m_lGridSkin = [
      ['TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos'], # + Tune Coarse Reset
      ['TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos'],
      ['TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos'],
      ['TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos'],
      ['TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos'],
      ['TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaNeg', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos', 'TunCoaPos'],
      ['TunFinNeg', 'TunFinNeg', 'TunFinNeg', 'TunFinNeg', 'TunFinPos', 'TunFinPos', 'TunFinPos', 'TunFinPos'], # + Tune Fine Reset
      ['Gain'     , 'Gain'     , 'Gain'     , 'Gain'     , 'Gain'     , 'Gain'     , 'Gain'     , 'Gain'     ], # + Gain Reset
    ]
    self.m_lSideSkin = [
      'Side', # Coarse Tuning Reset
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'Side', # Fine Tuning Reset
      'Side', # Gain Reset
    ]
    self.m_lBottomSkin = [
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'Bottom', # Tune Mode
      'DefaultButton',
      'DefaultButton',
    ]

    self.m_lClipPitchC  = [ # Pitch Coarse, steps
      [ -4,  -3,  -2,  -1,  1,  2,  3,  4],
      [ -8,  -7,  -6,  -5,  5,  6,  7,  8],
      [-12, -11, -10,  -9,  9, 10, 11, 12],
      [-16, -15, -14, -13, 13, 14, 15, 16],
      [-20, -19, -18, -13, 17, 18, 19, 20],
      [-24, -23, -22, -21, 21, 22, 23, 24],
    ]
    self.m_lClipPitchF  = [-48, -36, -24, -12, +12, +24, +36, +48]
    self.m_lClipGains   = [0.1, 0.2, 0.3, 0.52, 0.64, 0.76, 0.88, 1.0]
    self.m_nGainReset   = 0.4

  def set_active(self, pbActive):
    for nRow in range(self.cfg('nRows')):
      oBut = self.m_lSide[nRow]
      sSkin = self.m_lSideSkin[nRow] if pbActive else 'DefaultButton'
      oBut.set_on_off_values(sSkin)
      oBut.turn_on()
      for nCol in range(self.cfg('nCols')):
        oBut = self.get_btn(nCol, nRow)
        sSkin = 'Tune.' + self.m_lGridSkin[nRow][nCol] if pbActive else 'DefaultButton'
        oBut.set_on_off_values(sSkin)
        oBut.turn_on()

    for nCol in range(self.cfg('nCols')):
      oBut = self.m_lBottom[nCol]
      sSkin = self.m_lBottomSkin[nCol] if pbActive else 'DefaultButton'
      oBut.set_on_off_values(sSkin)
      oBut.turn_on()

  def get_btn(self, pnCol, pnRow):
    return self.m_oMatrix.get_button(pnCol, pnRow)

  # ********************************************************

  def on_side(self, pnIdx):
    oAudioClip = self.get_audio_clip_or_none()
    oMidiTrack = self.get_midi_track_or_none()

    if pnIdx == 0: # coarse detune reset
      if oAudioClip != None:
        oAudioClip.pitch_coarse = 0
        self.alert('Audio pitch: 0')
      elif oMidiTrack != None:
        oParam = self.get_midi_pitch_param(oMidiTrack)
        oParam.value = 0
        self.alert('MIDI pitch: 0')
      else:
        self.alert('No audio or midi clip selected')

    elif pnIdx == 6: # fine detune reset
      if oAudioClip == None:
        self.alert('No audio clip selected')
      else:
        oAudioClip.pitch_fine = 0
        self.alert('Audio detune: 0')

    elif pnIdx == 7: # fine gain reset
      if oAudioClip == None:
        self.alert('No audio clip selected')
      else:
        oAudioClip.gain = self.m_nGainReset
        self.alert('Audio gain: %.2f' % (self.m_nGainReset))

  def on_grid(self, pnCol, pnRow):
    oAudioClip = self.get_audio_clip_or_none()
    oMidiTrack = self.get_midi_track_or_none()

    if pnRow >= 0 and pnRow <= 5: # coarse detune audio
      if oAudioClip != None:
        oAudioClip.pitch_coarse = self.m_lClipPitchC[pnRow][pnCol]
        self.alert('Audio pitch: %d' % (self.m_lClipPitchC[pnRow][pnCol]))
      elif oMidiTrack != None:
        oParam = self.get_midi_pitch_param(oMidiTrack)
        oParam.value = self.m_lClipPitchC[pnRow][pnCol]
        self.alert('MIDI pitch: %d' % (self.m_lClipPitchC[pnRow][pnCol]))
      else:
        self.alert('No audio or midi clip selected')

    elif pnRow == 6: # fine detune audio
      if oAudioClip == None:
        self.alert('No audio clip selected')
      else:
        oAudioClip.pitch_fine = self.m_lClipPitchF[pnCol]
        self.alert('Audio detune: %d' % (self.m_lClipPitchF[pnCol]))

    elif pnRow == 7: # gain audio
      if oAudioClip == None:
        self.alert('No audio clip selected')
      else:
        oAudioClip.gain = self.m_lClipGains[pnCol]
        self.alert('Audio gain: %.2f' % (self.m_lClipGains[pnCol]))

  def get_midi_pitch_param(self, poMidiTrack):
    lDevices = poMidiTrack.devices
    for nDevIdx in range(len(lDevices)):
      oDevice = lDevices[nDevIdx]
      sClass  = oDevice.class_name
      if (sClass != 'MidiPitcher'):
        continue

      lParams = oDevice.parameters
      for nPrmIdx  in range(len(lParams)):
        oParam = lParams[nPrmIdx]
        if (oParam.name == 'Pitch'):
          return oParam

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  # ****************************************************************

  def sel_clip_slot(self):
    return self.song().view.highlighted_clip_slot

  def get_audio_clip_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if oClipSlot == None:
      return None

    oClip = oClipSlot.clip
    if oClip == None:
      return None
    if oClip.is_audio_clip:
      return oClip
    return None

  def master(self):
    return self.song().master_track

  def tracks(self):
    return self.song().visible_tracks

  def sel_track(self, poTrack = None):
    if poTrack != None:
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  def get_midi_track_or_none(self):
    oSelTrack = self.sel_track()
    if oSelTrack == None:
      return None
    if oSelTrack == self.master():
      return None
    if (oSelTrack in self.tracks()) == False:
      return None
    if oSelTrack.has_midi_input:
      return oSelTrack
    return None

  # ********************************************************

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)

