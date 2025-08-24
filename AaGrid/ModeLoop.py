import Live
import math

BUTTON_OFF = 0
BUTTON_ON  = 127

class ModeLoop():
  def __init__(self, poCtrlInst, phCfg, phObj, poMatrix, plBottom, plSide):
    self.m_oCtrlInst = poCtrlInst
    self.m_hCfg      = phCfg
    self.m_hObj      = phObj
    self.m_oMatrix   = poMatrix
    self.m_lBottom   = plBottom
    self.m_lSide     = plSide

    self.m_lGridSkin = [
      ['ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize'],
      ['SongStart', 'SongStart', 'SongEnd'  , 'SongEnd'  , 'LoopStart', 'LoopStart', 'LoopEnd'  , 'LoopEnd'  ],
      ['Shift'    , 'Shift'    , 'LoopShSta', 'LoopShSta', 'LoopShMid', 'LoopShMid', 'LoopShEnd', 'LoopShEnd'], # + Loop toggle
      ['Roll'     , 'Roll'     , 'Roll'     , 'Roll'     , 'Roll14'   , 'Roll14'   , 'Roll14'   , 'Roll14'   ],
      ['Roll18'   , 'Roll18'   , 'Roll18'   , 'Roll18'   , 'Roll18'   , 'Roll18'   , 'Roll18'   , 'Roll18'   ],
      ['LoopCmd'  , 'LoopCmd'  , 'ClipCmd'  , 'ClipCmd'  , 'Legato'   , 'Warp'     , 'Warp'     , 'Crop'     ], # + Follow
      ['Tempo'    , 'Tempo'    , 'Tempo'    , 'Tempo'    , 'Tempo'    , 'Tempo'    , 'Tempo'    , 'Tempo'    ], # + Tempo reset
      ['TempoDec' , 'TempoDec' , 'TempoDec' , 'TempoDec' , 'TempoInc' , 'TempoInc' , 'TempoInc' , 'TempoInc' ],
    ]
    self.m_lSideSkin = [
      'DefaultButton',
      'DefaultButton',
      'Side', # Loop Toggle
      'DefaultButton',
      'DefaultButton',
      'Side', # Follow
      'Side', # Tempo Reset
      'DefaultButton',
    ]
    self.m_lBottomSkin = [
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
      'Bottom', # Loop Mode
      'DefaultButton',
      'DefaultButton',
      'DefaultButton',
    ]

    self.m_lShiftSizes = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0] # in beats
    self.m_nShiftIdx   = 3

    self.m_bLpEnvToggle = True

    self.m_nTempoFactor = 20
    self.m_nTempoReset  = 128
    self.m_lTempoDeltas = [-20, -10, -5, -1, 1, 5, 10, 20]

  def set_active(self, pbActive):
    for nRow in range(self.cfg('nRows')):
      oBut = self.m_lSide[nRow]
      sSkin = self.m_lSideSkin[nRow] if pbActive else 'DefaultButton'
      oBut.set_on_off_values(sSkin)
      oBut.turn_on()
      for nCol in range(self.cfg('nCols')):
        oBut = self.get_btn(nCol, nRow)
        sSkin = 'Loop.' + self.m_lGridSkin[nRow][nCol] if pbActive else 'DefaultButton'
        oBut.set_on_off_values(sSkin)
        if nRow == 0: # shift size
          if nCol == self.m_nShiftIdx:
            oBut.turn_on()
          else:
            oBut.turn_off()
        else:
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
    if pnIdx == 2: # loop toggle
      oClip = self.get_clip_or_none()
      if oClip == None:
        self.alert('Clip not available')
        return

      if oClip.looping:
        oClip.looping = False
        self.alert('Loop Off')
      else:
        oClip.looping = True
        self.alert('Loop On')

    elif pnIdx == 5: # follow
      bFollow = self.song().view.follow_song
      if bFollow:
        self.song().view.follow_song = False
        self.alert('Follow Off')
      else:
        self.song().view.follow_song = True
        self.alert('Follow On')

    elif pnIdx == 6: # tempo reset
      self.song().tempo = self.m_nTempoReset
      self.alert('Tempo: %d' % (self.m_nTempoReset))

  def on_grid(self, pnCol, pnRow):
    if pnRow == 0: # shift size
      self.on_shift_size(pnCol)

    elif pnRow == 1: # song start/end, loop start/end
      self.on_shift_cmd(pnCol)

    elif pnRow == 2: # loop shift, loop div/mul
      if pnCol == 0 or pnCol == 1: # loop shift
        self.on_shift_cmd(pnCol + 8)
      else:
        self.on_loop_div_mul(pnCol - 2) # loop sta/mid/end & div/mul

    elif pnRow == 3: # roll & roll 1/4
      if pnCol >= 0 and pnCol <= 3:
        lSpans = [0.5, 1.0, 2.0, 4.0] # in beats
        self.alert('Roll: %s beats' % (lSpans[pnCol]))
        self.on_roll(0.0, lSpans[pnCol])

      else: # roll 1/4
        nOffset = (pnCol - 4)
        self.alert('Roll 1/4 bar: %d' % (pnCol + 1))
        self.on_roll(nOffset, 1.0)

    elif pnRow == 4: # roll 1/8
        nOffset = pnCol * 0.5
        self.alert('Roll 1/8 bar: %d' % (pnCol + 1))
        self.on_roll(nOffset, 0.5)

    elif pnRow == 5: # loop or clip command
      self.on_loop_clip_cmd(pnCol)

    elif pnRow == 6: # tempo absolute
      self.on_tempo(pnCol)

    elif pnRow == 7: # tempo delta
      self.on_tempo_delta(pnCol)

  # ----------------------------------------------

  def on_shift_size(self, pnCol):
    if pnCol != self.m_nShiftIdx:
      # update shift size and button colors
      self.m_nShiftIdx = pnCol
      for nCol in range(self.cfg('nCols')):
        oBut = self.get_btn(nCol, 0)
        if nCol == self.m_nShiftIdx:
          oBut.turn_on()
        else:
          oBut.turn_off()
    self.alert('Shift size: %d' % (self.m_lShiftSizes[self.m_nShiftIdx]))

  def on_shift_cmd(self, pnCmd):
    oClip = self.get_clip_or_none()
    if oClip == None:
      self.alert('Clip not available')
      return

    nSize = self.m_lShiftSizes[self.m_nShiftIdx]

    if pnCmd == 0:   # song start shift left
      oClip.start_marker = oClip.start_marker - nSize
      self.alert('Song Start Shift Left')

    elif pnCmd == 1: # song start shift right
      oClip.start_marker = oClip.start_marker + nSize
      self.alert('Song Start Shift Right')

    elif pnCmd == 2: # song end   shift left
      oClip.end_marker = oClip.end_marker - nSize
      self.alert('Song End Shift Left')

    elif pnCmd == 3: # song end   shift right
      oClip.end_marker = oClip.end_marker + nSize
      self.alert('Song End Shift Right')

    else:
      if oClip.looping == False:
        self.alert('Clip not looping!')
        return

      if pnCmd == 4:   # loop start shift left
        oClip.loop_start = oClip.loop_start - nSize
        self.alert('Loop Start Shift Left')

      elif pnCmd == 5: # loop start shift right
        if (oClip.loop_start + nSize < oClip.loop_end):
          oClip.loop_start = oClip.loop_start + nSize
          self.alert('Loop Start Shift Right')
        else:
          self.alert('Not possible to Loop Start Shift Right')

      elif pnCmd == 6: # loop end   shift left
        if (oClip.loop_end - nSize > oClip.loop_start):
          oClip.loop_end = oClip.loop_end - nSize
          self.alert('Loop End Shift Left')
        else:
          self.alert('Not possible to Loop End Shift Left')

      elif pnCmd == 7: # loop end   shift right
        oClip.loop_end = oClip.loop_end + nSize
        self.alert('Loop End Shift Right')

      else:
        if pnCmd == 8:   # loop shift left
          if oClip.loop_start - nSize < 0.0:
            self.alert('Loop Start should be more than 0')
            return

          # update start first
          oClip.loop_start -= nSize
          oClip.loop_end   -= nSize
          self.alert('Loop Shift Left')

        elif pnCmd == 9: # loop shift right
          if oClip.loop_end + nSize > oClip.end_marker:
            self.alert('Loop End should be less than Clip End')
            return

          # update end first
          oClip.loop_end   += nSize
          oClip.loop_start += nSize
          self.alert('Loop Shift Right')

  def on_loop_div_mul(self, pnCmd):
    oClip = self.get_clip_or_none()
    if oClip == None:
      self.alert('Clip not available')
      return

    nLoopStart = oClip.loop_start
    nLoopEnd   = oClip.loop_end
    nLoopSpan  = nLoopEnd - nLoopStart
    nSize      = self.m_lShiftSizes[self.m_nShiftIdx]

    if pnCmd == 0:   # loop start div
      oClip.loop_start = nLoopStart + (nLoopSpan / 2)
      self.alert('Loop Start Div')

    elif pnCmd == 1: # loop start mul
      oClip.loop_start = nLoopStart - nLoopSpan
      self.alert('Loop Start Mul')

    elif pnCmd == 2: # loop middle div
      oClip.loop_start = nLoopStart + (nLoopSpan / 4)
      oClip.loop_end   = nLoopEnd   - (nLoopSpan / 4)
      self.alert('Loop Middle Div')

    elif pnCmd == 3: # loop middle mul
      oClip.loop_start = nLoopStart - (nLoopSpan / 2)
      oClip.loop_end   = nLoopEnd   + (nLoopSpan / 2)
      self.alert('Loop Middle Mul')

    elif pnCmd == 4: # loop end div
      oClip.loop_end = nLoopStart + (nLoopSpan / 2)
      self.alert('Loop End Div')

    elif pnCmd == 5: # loop end mul
      oClip.loop_end = nLoopStart + (nLoopSpan * 2)
      self.alert('Loop End Mul')

  def on_roll(self, pnOffset, pnSpan):
    oClip = self.get_clip_or_none()
    if oClip == None:
      self.alert('Clip not available')
      return

    nPlayPos  = oClip.playing_position
    nCurrBar  = (math.floor(math.floor(nPlayPos)/ 4.0)) * 4.0
    nCurrBeat = math.floor(nPlayPos)
    nNewStart = nCurrBar  + pnOffset
    nNewEnd   = nNewStart + pnSpan

    oClip.looping = True

    nOldStart = oClip.loop_start
    nOldEnd   = oClip.loop_end

    if nNewStart >= nOldEnd:
      oClip.loop_end   = nNewEnd
      oClip.loop_start = nNewStart
    else:
      oClip.loop_start = nNewStart
      oClip.loop_end   = nNewEnd

    oClip.position = nNewStart

  def on_loop_clip_cmd(self, pnCol):
    oClip      = self.get_clip_or_none()
    oAudioClip = self.get_audio_clip_or_none()
    oMidiClip  = self.get_midi_clip_or_none()

    if pnCol == 0: # loop duplicate
      if oMidiClip == None:
        self.alert('MIDI Clip not available')
        return

      if oClip.looping == False:
        self.alert('MIDI Clip not looping')
        return

      oClip.duplicate_loop()
      self.alert('MIDI Clip loop duplicated')

    elif pnCol == 1: # loop / envelope toggle
      oView = Live.Application.get_application().view
      oView.show_view('Detail')
      oView.focus_view('Detail')
      oView.show_view('Detail/Clip')
      oView.focus_view('Detail/Clip')

      if self.m_bLpEnvToggle:
        oClip.view.hide_envelope()
        oClip.view.show_loop()
        self.alert('Showing Loop')
      else:
        oClip.view.show_envelope()
        self.alert('Showing Envelope')
      self.m_bLpEnvToggle = not self.m_bLpEnvToggle

    elif pnCol == 2: # clip duplicate
      nSelSceneIdxAbs = self.sel_scene_idx_abs()
      oScene          = self.get_scene(nSelSceneIdxAbs + 1)
      oSelTrack       = self.sel_track()
      oSelTrack.duplicate_clip_slot(nSelSceneIdxAbs)
      self.sel_scene(oScene)
      self.alert('Clip duplicated at track "%s", scene: %d' %
        (oSelTrack.name, nSelSceneIdxAbs))

    elif pnCol == 3: # device chain / clip toggle
      oView = Live.Application.get_application().view
      oView.show_view ('Detail')
      oView.focus_view('Detail')
      if oView.is_view_visible('Detail/Clip'):
        oView.show_view ('Detail/DeviceChain')
        oView.focus_view('Detail/DeviceChain')
        self.alert('Showing Device Chain')
      else:
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')
        self.alert('Showing Clip')

    elif pnCol == 4: # legato (play a new clip from the position of the old clip!)
      if oAudioClip != None:
        if oAudioClip.legato:
          oAudioClip.legato = False
          self.alert('Legato Off')
        else:
          oAudioClip.legato = True
          self.alert('Legato On')
      else:
        self.alert('Audio clip not available')

    elif pnCol == 5: # warp
      if oAudioClip != None:
        if oAudioClip.warping:
          oAudioClip.warping = False
          self.alert('Warp Off')
        else:
          oAudioClip.warping = True
          self.alert('Warp On')
      else:
        self.alert('Audio clip not available')

    elif pnCol == 6: # warp mode
      nWarpMode = oAudioClip.warp_mode
      lWarpModes = [
        'Beats',         # 0
        'Tones',         # 1
        'Texture',       # 2
        'Re-Pitch',      # 3
        'Complex',       # 4
        'NOT AVAILABLE', # 5 -> should never be used!
        'Complex-Pro',   # 6
      ]
      if nWarpMode == 4:   # from Complex
        nWarpMode = 6      # to   Complex-Pro
      elif nWarpMode == 6: # from Complex-Pro
        nWarpMode = 0      # to   Beats
      else:
        nWarpMode += 1

      oAudioClip.warp_mode = nWarpMode
      self.alert('Warp mode: %s' % (lWarpModes[nWarpMode]))

    elif pnCol == 7: # crop
      if oClip != None:
        oClip.crop()
        self.alert('Cropping clip')
      else:
        self.alert('Clip not available')

  def on_tempo(self, pnCol):
    nTempo = (pnCol + 1) * self.m_nTempoFactor
    self.song().tempo = nTempo
    self.alert('Tempo: %d' % (nTempo))

  def on_tempo_delta(self, pnCol):
    nOldTempo = self.song().tempo
    nNewTempo = nOldTempo + self.m_lTempoDeltas[pnCol]
    if nNewTempo >= 20 and nNewTempo <= 500:
      self.song().tempo = nNewTempo
      self.alert('Tempo: %d' % (nNewTempo))
    else:
      self.alert('Tempo: %d' % (nOldTempo))

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  # ********************************************************

  def sel_clip_slot(self):
    return self.song().view.highlighted_clip_slot

  def get_clip_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if oClipSlot == None:
      return None
    if oClipSlot.has_clip:
      return oClipSlot.clip
    return None

  def get_audio_clip_or_none(self):
    oClip = self.get_clip_or_none()
    if oClip == None:
      return None
    if oClip.is_audio_clip:
      return oClip
    return None

  def get_midi_clip_or_none(self):
    oClip = self.get_clip_or_none()
    if oClip == None:
      return None
    if oClip.is_midi_clip:
      return oClip
    return None

  def sel_scene(self, poScene = None):
    if poScene != None:
      self.song().view.selected_scene = poScene
    return self.song().view.selected_scene

  def scenes(self):
    return self.song().scenes

  def get_scene(self, pnSceneIdxAbs):
    return self.scenes()[pnSceneIdxAbs]

  def sel_scene_idx_abs(self):
    lAllScenes = self.scenes()
    oSelScene  = self.sel_scene()
    return list(lAllScenes).index(oSelScene)

  def sel_track(self, poTrack = None):
    if poTrack != None:
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  # ********************************************************

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)

