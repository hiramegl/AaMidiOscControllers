from AaTouch.Base import Base

class State(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_nColOff    = 0         # for SEQ  view mode
    self.m_nRowOff    = 0         # for SEQ  view mode
    self.m_nTrackOff  = 0         # for SESS view mode
    self.m_nSceneOff  = 0         # for SESS view mode
    self.m_sViewMode  = 'SEQ'     # view mode: SEQ, SESS
    self.m_sMode      = 'UNKNOWN' # clip mode: MIDI, AUDIO, EMPTY(MIDI)
    self.m_oMidiTrack = None
    self.m_oClip      = None
    self.m_oMidiClip  = None
    self.m_oAudioClip = None
    self.m_hLimits    = None
    self.m_bPauseList = False # pause notes listener flag
    self.m_hSendsCbs  = []
    self.m_hSlotsCbs  = {}
    self.m_hClipsCbs  = {}
    self.m_hTracksCbs = {}
    self.m_bFollowSel = False # follow selected clip

    self.connect()
    self.update()

    phObj['oState'] = self

  # ********************************************************

  def connect(self):
    self.song().add_scenes_listener(self.on_scenes_changed)
    self.song().add_tracks_listener(self.on_tracks_changed)
    if self.m_bFollowSel:
      self.song().view.add_selected_scene_listener(self.on_sel_clip_changed)
      self.song().view.add_selected_track_listener(self.on_sel_clip_changed)
    self.add_tracks_listeners()
    self.add_sends_listeners()
    self.add_clips_listeners()

  def disconnect(self):
    oSong = self.song()
    oSong.remove_scenes_listener(self.on_scenes_changed)
    oSong.remove_tracks_listener(self.on_tracks_changed)
    if self.m_bFollowSel:
      oSong.view.remove_selected_scene_listener(self.on_sel_clip_changed)
      oSong.view.remove_selected_track_listener(self.on_sel_clip_changed)
    self.remove_tracks_listeners()
    self.remove_sends_listeners()
    self.remove_clips_listeners()

  # ********************************************************

  def add_tracks_listeners(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break # no more tracks to scan
      oTrack = self.get_track(nTrackIdxAbs)
      self.reg_vol_listener(oTrack, nTrackIdxRel)

  def reg_vol_listener(self, poTrack, pnTrackIdxRel):
    fTrackCb = lambda :self.on_vol(poTrack, pnTrackIdxRel)
    poTrack.mixer_device.volume.add_value_listener(fTrackCb)
    self.m_hTracksCbs[poTrack] = fTrackCb

  def remove_tracks_listeners(self):
    if len(self.m_hTracksCbs) == 0: return
    for oTrack in self.m_hTracksCbs:
      try:
        fTrackCb = self.m_hTracksCbs[oTrack]
        oTrack.mixer_device.volume.remove_value_listener(fTrackCb)
      except:
        self.dlog('-> Could not remove volume listener for track')
    self.m_hTracksCbs.clear()

  # ----------------------------------------------

  def add_sends_listeners(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break # no more tracks to scan
      oTrack = self.get_track(nTrackIdxAbs)
      lSends = oTrack.mixer_device.sends
      for nSendIdx in range(self.cfg('nReturns')):
        if nSendIdx < len(lSends):
          self.reg_send_listener(lSends[nSendIdx], nTrackIdxRel, oTrack, nSendIdx)

  def reg_send_listener(self, poSend, pnTrackIdxRel, poTrack, pnSendIdx):
    fSendCb = lambda :self.on_send(pnTrackIdxRel, poTrack, pnSendIdx)
    poSend.add_value_listener(fSendCb)
    oSendId = hash(poSend)
    self.m_hSendsCbs.insert(oSendId, fSendCb)

  def remove_sends_listeners(self):
    if len(self.m_hSendsCbs) == 0: return
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break # no more tracks to scan
      oTrack = self.get_track(nTrackIdxAbs)
      lSends = oTrack.mixer_device.sends
      if len(lSends) == 0: return
      for nSendIdx in range(self.cfg('nReturns')):
        oSend   = lSends[nSendIdx]
        oSendId = hash(oSend)
        if oSendId in self.m_hSendsCbs:
          fSendCb = self.m_hSendsCbs[oSendId]
          oSend.remove_value_listener(fSendCb)
    self.m_hSendsCbs.clear()

  # ----------------------------------------------

  def add_clips_listeners(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break # no more tracks to scan
      lSlots = self.get_track(nTrackIdxAbs).clip_slots
      for nSceneIdxRel in range(self.cfg('nScenes')):
        nSceneIdxAbs = self.scene_idx_abs(nSceneIdxRel)
        if nSceneIdxAbs >= len(lSlots): next
        oSlot = lSlots[nSceneIdxAbs]
        self.add_slot_listener(oSlot, nTrackIdxAbs, nSceneIdxAbs)
        if oSlot.has_clip:
          self.add_clip_listener(oSlot.clip, nTrackIdxAbs, nSceneIdxAbs)

  def add_slot_listener(self, poSlot, pnTrackIdxAbs, pnSceneIdxAbs):
    fViewCb = lambda :self.on_slot_changed(poSlot, pnTrackIdxAbs, pnSceneIdxAbs)
    if (poSlot in self.m_hSlotsCbs) == False:
      poSlot.add_has_clip_listener(fViewCb)
      self.m_hSlotsCbs[poSlot] = fViewCb

  def on_slot_changed(self, poSlot, pnTrackIdxAbs, pnSceneIdxAbs):
    if (poSlot.has_clip):
      oClip = poSlot.clip
      self.add_clip_listener(oClip, pnTrackIdxAbs, pnSceneIdxAbs) # clip added to the clip-slot
      self.obj('oClips').update_clip_button(oClip, pnTrackIdxAbs, pnSceneIdxAbs)
    else: # the clip is gone!
      self.obj('oClips').turn_off_clip_button(pnTrackIdxAbs, pnSceneIdxAbs)

  def add_clip_listener(self, poClip, pnTrackIdxAbs, pnSceneIdxAbs):
    fClipCb = lambda :self.on_clip_changed(poClip, pnTrackIdxAbs, pnSceneIdxAbs)
    if (poClip in self.m_hClipsCbs) == False:
      poClip.add_playing_status_listener(fClipCb)
      poClip.add_color_listener(fClipCb)
      self.m_hClipsCbs[poClip] = fClipCb

  def on_clip_changed(self, poClip, pnTrackIdxAbs, pnSceneIdxAbs):
    self.obj('oClips').update_clip_button(poClip, pnTrackIdxAbs, pnSceneIdxAbs)

  def remove_clips_listeners(self):
    for oSlot in self.m_hSlotsCbs:
      try:
        fViewCb = self.m_hSlotsCbs[oSlot]
        oSlot.remove_has_clip_listener(fViewCb)
      except:
        self.dlog('-> Could not remove clip listener for slot')
    self.m_hSlotsCbs = {}

    for oClip in self.m_hClipsCbs:
      try:
        fClipCb = self.m_hClipsCbs[oClip]
        oClip.remove_playing_status_listener(fClipCb)
        oClip.remove_color_listener(fClipCb)
      except:
        self.dlog('-> Could not remove listeners for clip')

    self.m_hClipsCbs = {}

  # ********************************************************

  def update(self):
    if self.m_oMidiClip != None:
      self.m_oMidiClip.remove_start_marker_listener(self.on_clip_length_changed)
      self.m_oMidiClip.remove_end_marker_listener  (self.on_clip_length_changed)
      self.m_oMidiClip.remove_loop_start_listener  (self.on_clip_length_changed)
      self.m_oMidiClip.remove_loop_end_listener    (self.on_clip_length_changed)
      self.m_oMidiClip.remove_notes_listener       (self.on_clip_notes_changed )

    self.m_oMidiTrack = self.get_midi_track_or_none()
    self.m_oClip      = self.get_clip_or_none      ()
    self.m_oMidiClip  = self.get_midi_clip_or_none ()
    self.m_oAudioClip = self.get_audio_clip_or_none()

    if self.m_oMidiClip != None:
      self.m_sMode = 'MIDI'
      self.m_oMidiClip.add_start_marker_listener(self.on_clip_length_changed)
      self.m_oMidiClip.add_end_marker_listener  (self.on_clip_length_changed)
      self.m_oMidiClip.add_loop_start_listener  (self.on_clip_length_changed)
      self.m_oMidiClip.add_loop_end_listener    (self.on_clip_length_changed)
      self.m_oMidiClip.add_notes_listener       (self.on_clip_notes_changed )

    else: # Audio clip
      if self.m_oMidiTrack != None:
        self.m_sMode = 'EMPTY'
      else:
        self.m_sMode = 'AUDIO'

    self.update_limits()

  # ********************************************************

  def on_scenes_changed(self):
    self.update()
    self.obj('oClips'   ).update()
    self.obj('oZoom'    ).update()
    self.obj('oSeq'     ).update()
    self.obj('oSelected').update()

    # re-bind clips again since there are changes
    # in the scenes
    self.remove_clips_listeners()
    self.add_clips_listeners()

  def on_tracks_changed(self):
    self.update()
    self.obj('oSends'   ).update()
    self.obj('oClips'   ).update()
    self.obj('oZoom'    ).update()
    self.obj('oSeq'     ).update()
    self.obj('oSelected').update()

    # re-bind sends and clips again since there
    # are changes in the tracks
    self.remove_tracks_listeners()
    self.remove_sends_listeners()
    self.remove_clips_listeners()
    self.add_tracks_listeners()
    self.add_sends_listeners()
    self.add_clips_listeners()

  def on_sel_clip_changed(self):
    self.update()
    self.obj('oSeq'     ).update()
    self.obj('oLoop'    ).update()
    self.obj('oSelected').update()
    self.obj('oTracks'  ).update_sel_track()

  def on_clip_length_changed(self):
    self.update_limits()
    self.obj('oSeq').update()

  def on_clip_notes_changed(self):
    if self.m_bPauseList:
      self.m_bPauseList = False
      return
    self.obj('oSeq').update()

  def on_send(self, pnTrackIdxRel, poTrack, pnSendIdx):
    # update selected track sends (if necessary)
    oSelTrack = self.sel_track()
    if poTrack == oSelTrack:
      self.obj('oSelected').update_sends()

    # update track sends
    self.obj('oSends').update_track_send(pnTrackIdxRel, poTrack, pnSendIdx)

  def on_vol(self, poTrack, pnTrackIdxRel):
    self.obj('oTracks').update_volume(poTrack, pnTrackIdxRel)

  # ********************************************************

  def update_limits(self):
    oClip = self.m_oClip
    if oClip == None:
      self.m_hLimits = None
      return

    if oClip.looping:
      nStart = oClip.loop_start
      nEnd   = oClip.loop_end
    else:
      nStart = oClip.start_marker
      nEnd   = oClip.end_marker

    self.m_hLimits = {
      'bLoop' : oClip.looping,
      'nStart': nStart,
      'nEnd'  : nEnd,
      'nSpan' : nEnd - nStart,

      # absolute limits
      'nClipStart': oClip.start_marker,
      'nClipEnd'  : oClip.end_marker,
      'nLoopStart': oClip.loop_start,
      'nLoopEnd'  : oClip.loop_end,
    }

  # ********************************************************

  def mode(self):
    return self.m_sMode

  def view_mode(self):
    return self.m_sViewMode

  def set_view_mode(self, psViewMode):
    self.m_sViewMode = psViewMode

  def limits_or_none(self):
    return self.m_hLimits

  def midi_track_or_none(self):
    return self.m_oMidiTrack

  def midi_clip_or_none(self):
    return self.m_oMidiClip

  def audio_clip_or_none(self):
    return self.m_oAudioClip

  def pause_notes_listener(self, pbValue):
    self.m_bPauseList = pbValue

  # ********************************************************

  def col_offset(self):
    return self.m_nColOff

  def row_offset(self):
    return self.m_nRowOff

  def set_clip_offsets(self, pnColOff, pnRowOff):
    self.m_nColOff = pnColOff
    self.m_nRowOff = pnRowOff
    self.on_sel_clip_changed()

  def track_offset(self):
    return self.m_nTrackOff

  def scene_offset(self):
    return self.m_nSceneOff

  def set_session_offsets(self, pnTrackOff, pnSceneOff):
    self.remove_tracks_listeners()
    self.remove_sends_listeners()
    self.remove_clips_listeners()
    self.m_nTrackOff = pnTrackOff
    self.m_nSceneOff = pnSceneOff
    self.add_tracks_listeners()
    self.add_sends_listeners()
    self.add_clips_listeners()

  def get_track_idx_abs(self, pnTrackIdxRel):
    return self.m_nTrackOff + pnTrackIdxRel

  def get_scene_idx_abs(self, pnSceneIdxRel):
    return self.m_nSceneOff + pnSceneIdxRel

  def get_track_idx_rel_or_none(self, pnTrackIdxAbs):
    nIdx = pnTrackIdxAbs - self.m_nTrackOff
    if nIdx < 0 or nIdx >= self.cfg('nTracks'):
      return None
    return nIdx

  # ********************************************************

  def get_midi_track_or_none(self):
    if self.is_track_available(self.m_nColOff) == False:
      return None

    oTrack = self.get_track(self.m_nColOff)
    if oTrack.has_midi_input:
      return oTrack
    return None

  def get_clip_or_none(self):
    if self.is_track_available(self.m_nColOff) == False:
      return None
    if self.is_scene_available(self.m_nRowOff) == False:
      return None

    oTrack     = self.get_track(self.m_nColOff)
    lClipSlots = oTrack.clip_slots
    oClipSlot  = lClipSlots[self.m_nRowOff]
    if oClipSlot == None:
      return None
    if oClipSlot.has_clip:
      return oClipSlot.clip
    return None

  def get_midi_clip_or_none(self):
    oClip = self.get_clip_or_none()
    if oClip == None:
      return None
    if oClip.is_midi_clip:
      return oClip
    return None

  def get_audio_clip_or_none(self):
    oClip = self.get_clip_or_none()
    if oClip == None:
      return None
    if oClip.is_audio_clip:
      return oClip
    return None

  def focused_clip_slot_or_none(self):
    if self.is_track_available(self.m_nColOff) == False:
      return None
    if self.is_scene_available(self.m_nRowOff) == False:
      return None

    oTrack     = self.get_track(self.m_nColOff)
    lClipSlots = oTrack.clip_slots
    oClipSlot  = lClipSlots[self.m_nRowOff]
    return oClipSlot

  def focused_track_or_none(self):
    if self.is_track_available(self.m_nColOff) == False:
      return None

    return self.get_track(self.m_nColOff)

