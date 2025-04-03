from AaTouch.Base import Base

class Clips(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hCache = {} # grid cache
    self.connect()

    phObj['oClips'] = self

  # ********************************************************

  def connect(self):
    self.set_visible(True) # show 'Clips' & hide 'Sends'
    self.activate()
    self.reg_idx_cb(
      'session/grid',
      self.cfg('nTracks') * self.cfg('nReturns'),
      self.on_grid)

  def disconnect(self):
    self.set_visible(True) # show 'Clips' & hide 'Sends'
    self.deactivate()      # turn off buttons

  # ********************************************************

  def update(self):
    self.deactivate()
    self.activate()

  def activate(self):
    lCells = []
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break # no more tracks to scan
      oTrack = self.get_track(nTrackIdxAbs)
      lSlots = oTrack.clip_slots

      for nSceneIdxRel in range(self.cfg('nScenes')):
        nSceneIdxAbs = self.scene_idx_abs(nSceneIdxRel)
        if self.is_scene_available(nSceneIdxAbs) == False:
          continue # continue with the next track

        oSlot = lSlots[nSceneIdxAbs]
        if oSlot.has_clip == False:
          continue # empty clip slot

        nCellId = nSceneIdxRel * self.cfg('nTracks') + nTrackIdxRel
        self.m_hCache[nCellId] = [nTrackIdxAbs, nSceneIdxAbs]

        oClip      = oSlot.clip
        sColor     = self.to_color(oClip.color)
        bPlaying   = oClip.is_playing
        bTriggered = oClip.is_triggered

        # build json attributes
        if   bTriggered:
          sStroke = '#ffff00ff'
          nWidth  = 9
        elif bPlaying:
          sStroke = '#ff0000ff'
          nWidth  = 9
        else:
          sStroke = ''
          nWidth  = 1
        sJsonFill    = '"colorFill":"%s"'   % sColor
        sJsonStroke  = '"colorStroke":"%s"' % sStroke
        sJsonWidth   = '"lineWidth":%d'     % nWidth
        sAttrs       = '{%s,%s,%s}' % (sJsonFill, sJsonStroke, sJsonWidth)
        lCells.append([nCellId, sAttrs])

    if len(lCells) > 0:
      sAddr   = '/session/grid/%d'
      lBundle = list(map(lambda x: [
        sAddr % (x[0]),
        1.0],
        lCells))
      self.send_bundle(lBundle)

      sAddr   = 'session/grid/%d'
      sFill   = '{"colorFill":"%s"}'
      lBundle = list(map(lambda x: [
        '/EDIT',
        [sAddr % (x[0]), x[1]]],
        lCells))
      self.send_bundle(lBundle)

    self.highlight_session()

  def deactivate(self):
    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0: return

    sAddr   = 'session/grid/%d'
    sFill   = '{"colorFill":"#6db5fd","colorStroke":"","lineWidth":1}'
    lBundle = list(map(lambda x: [
      '/EDIT',
      [sAddr % (x), sFill]],
      lAddrs))
    self.send_bundle(lBundle)

    sAddr   = '/session/grid/%d'
    lBundle = list(map(lambda x: [
      sAddr % (x),
      0.0],
      lAddrs))
    self.send_bundle(lBundle)

    self.m_hCache.clear()

  # ********************************************************

  def on_grid(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    (nScnIdx, nTrkIdx) = self.get_row_col(nIdx, self.cfg('nTracks'))
    nTrackIdxAbs = self.state().get_track_idx_abs(nTrkIdx)
    if self.is_track_available(nTrackIdxAbs) == False:
      self.send_msg(sAddr, 0) # prevent from turning on
      return

    nSceneIdxAbs = self.state().get_scene_idx_abs(nScnIdx)
    if self.is_scene_available(nSceneIdxAbs) == False:
      self.send_msg(sAddr, 0) # prevent from turning on
      return

    oTrack = self.get_track(nTrackIdxAbs)
    lSlots = oTrack.clip_slots
    oSlot  = lSlots[nSceneIdxAbs]
    nValue = 1 if oSlot.has_clip else 0
    self.send_msg(sAddr, nValue)

    sCellMode = self.obj('oSess').get_cell_mode()
    if sCellMode == 'FIRE':
      oSlot.fire()
      sFireMode = self.obj('oSess').get_fire_mode()
      if sFireMode == 'FIRE N FOLLOW':
        self.sel_clip_slot(oSlot) # select the clip slot

    else: # SELECT mode: only select the clip slot
      self.sel_clip_slot(oSlot)

  # ********************************************************

  def highlight_session(self):
    self.obj('oCtrlInst').set_session_highlight(
      self.track_offset(),
      self.scene_offset(),
      self.cfg('nTracks'),
      self.cfg('nScenes'),
      False) # do not include return tracks

  # ********************************************************

  def set_visible(self, bVisible):
    sValue = 'true' if bVisible else 'false'
    self.send_msg(
      '/EDIT',
      ['session/grid', '{"visible":%s}' % (sValue)])

  def update_clip_button(self, poClip, pnTrackIdxAbs, pnSceneIdxAbs):
    sColor       = self.to_color(poClip.color)
    bPlaying     = poClip.is_playing
    bTriggered   = poClip.is_triggered
    nTrackIdxRel = self.track_idx_rel(pnTrackIdxAbs)
    nSceneIdxRel = self.scene_idx_rel(pnSceneIdxAbs)
    nIdx         = nSceneIdxRel * self.cfg('nTracks') + nTrackIdxRel

    # build json attributes
    if   bTriggered:
      sStroke = '#ffff00ff'
      nWidth  = 9
    elif bPlaying:
      sStroke = '#ff0000ff'
      nWidth  = 9
    else:
      sStroke = ''
      nWidth  = 1
    sJsonFill    = '"colorFill":"%s"'   % sColor
    sJsonStroke  = '"colorStroke":"%s"' % sStroke
    sJsonWidth   = '"lineWidth":%d'     % nWidth
    sAttrs       = '{%s,%s,%s}' % (sJsonFill, sJsonStroke, sJsonWidth)

    self.send_msg('/session/grid/%d' % (nIdx), 1)
    self.send_msg(
      '/EDIT',
      ['session/grid/%d' % (nIdx), sAttrs])

    # add to cache if necessary
    nCellId = nSceneIdxRel * self.cfg('nTracks') + nTrackIdxRel
    if (nCellId in self.m_hCache) == False:
      self.m_hCache[nCellId] = [pnTrackIdxAbs, pnSceneIdxAbs]

  def turn_off_clip_button(self, pnTrackIdxAbs, pnSceneIdxAbs):
    nTrackIdxRel = self.track_idx_rel(pnTrackIdxAbs)
    nSceneIdxRel = self.scene_idx_rel(pnSceneIdxAbs)
    nIdx         = nSceneIdxRel * self.cfg('nTracks') + nTrackIdxRel
    self.send_msg('/session/grid/%d' % (nIdx), 0)

