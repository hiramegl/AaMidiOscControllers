from AaTouch.Base import Base

class Zoom(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hCache    = {} # grid cache
    self.m_nBank     = 0
    self.m_nTracks   = self.cfg('nTracks') # 32
    self.m_nScenes   = self.cfg('nScenes') # 8
    self.m_nZoomCols = 4
    self.m_nZoomRows = 8
    self.m_nSelCol   = 0
    self.m_nSelRow   = 0
    self.m_nSelCell  = None
    self.connect()

    phObj['oZoom'] = self
    self.activate()
    self.send_msg('/session/bank', self.m_nBank)

  # ********************************************************

  def connect(self):
    self.reg_cb('session/bank', self.on_bank)
    self.reg_idx_cb(
      'session/zoom',
      self.m_nZoomCols * self.m_nZoomRows,
      self.on_zoom)

  def disconnect(self):
    self.deactivate()

  # ********************************************************

  # called when clips are added, removed, fired or stopped
  def update(self):
    self.deactivate()
    self.activate()

  def activate(self):
    # start scanning from nSceneOff
    nSceneOff = self.m_nBank * self.m_nZoomRows * self.m_nScenes
    self.m_nSelCell = None

    lCells = []
    for nRowIdx in range(self.m_nZoomRows):
      for nColIdx in range(self.m_nZoomCols):
        (bHasClips, sColor) = self.scan_zoom_area(
          nColIdx             * self.m_nTracks, # absolute track offset
          nSceneOff + nRowIdx * self.m_nScenes) # absolute scene offset

        if (nColIdx == self.m_nSelCol and
          nRowIdx == self.m_nSelRow - (self.m_nBank * self.m_nZoomRows)):
          # we are in the active cell!
          nCellId = nRowIdx * self.m_nZoomCols + nColIdx
          self.m_hCache[nCellId] = sColor
          lCells.append([nCellId, '#66cc66'])
          self.m_nSelCell = nCellId
          continue

        if bHasClips:
          nCellId = nRowIdx * self.m_nZoomCols + nColIdx
          self.m_hCache[nCellId] = sColor
          lCells.append([nCellId, sColor])

    if len(lCells) == 0: return

    sAddr   = '/session/zoom/%d'
    lBundle = list(map(lambda x: [sAddr % (x[0]), 1.0], lCells))
    self.send_bundle(lBundle)

    sAddr   = 'session/zoom/%d'
    sFill   = '{"colorFill":"%s"}'
    lBundle = list(map(lambda x: ['/EDIT', [sAddr % (x[0]), sFill % (x[1])]], lCells))
    self.send_bundle(lBundle)

  def deactivate(self):
    if self.m_nSelCell != None:
      self.send_msg(
        '/session/zoom/%d' % (self.m_nSelCell),
        0) # turn selected cell off!

    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0: return

    sAddr   = 'session/zoom/%d'
    sFill   = '{"colorFill":"#66cc66ff"}'
    lBundle = list(map(lambda x: [
      '/EDIT',
      [sAddr % (x), sFill]],
      lAddrs))
    self.send_bundle(lBundle)

    sAddr   = '/session/zoom/%d'
    lBundle = list(map(lambda x: [
      sAddr % (x),
      0.0],
      lAddrs))
    self.send_bundle(lBundle)

    self.m_hCache.clear()

  # ********************************************************

  def on_bank(self, plSegs, plMsg):
    nValue = plMsg[2]
    if self.m_nBank == nValue:
      return # nothing else to do here!

    self.m_nBank = int(nValue)
    self.deactivate()
    self.activate()
    self.alert('SESSION BANK: %d' % nValue)

  def on_zoom(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    # sanity checks to make sure track and scene are available
    (nRowIdx, nColIdx) = self.get_row_col(nIdx, self.m_nZoomCols)
    nFirstTrackIdxAbs  = nColIdx * self.m_nTracks
    nFirstSceneIdxAbs  = (nRowIdx + (self.m_nBank * self.m_nZoomRows)) * self.m_nScenes

    if self.is_track_available(nFirstTrackIdxAbs) == False:
      self.send_msg(sAddr, 0) # prevent from turning on
      self.alert('No tracks available!')
      return

    if self.is_scene_available(nFirstSceneIdxAbs) == False:
      self.send_msg(sAddr, 0) # prevent from turning on
      self.alert('No scenes available!')
      return

    # change to original color or turn off the
    # selected cell
    if self.m_nSelCell != None:
      if self.m_nSelCell in self.m_hCache:
        sColor = self.m_hCache[self.m_nSelCell]
        self.send_msg(
          '/EDIT',
          [
            'session/zoom/%d' % (self.m_nSelCell),
            '{"colorFill":"%s"}' % (sColor)
          ])
      else:
        self.send_msg(
          '/session/zoom/%d' % (self.m_nSelCell),
          0) # turn it off! it did not have clips!

    # update new track and scene offsets
    nOldSelCell     = self.m_nSelCell
    self.m_nSelCell = nIdx
    self.m_nSelCol  = nColIdx
    self.m_nSelRow  = nRowIdx + (self.m_nBank * self.m_nZoomRows)
    self.obj('oState').set_session_offsets(
      self.m_nSelCol * self.m_nTracks,
      self.m_nSelRow * self.m_nScenes)

    # select first track and scene in the new region
    self.sel_track(self.get_track(nFirstTrackIdxAbs))
    self.sel_scene(self.get_scene(nFirstSceneIdxAbs))

    # update clips
    self.obj('oClips').update()

    # update tracks and sends ONLY if the tracks-span has changed
    nOldZoomCol = nOldSelCell     % self.m_nZoomCols
    nNewZoomCol = self.m_nSelCell % self.m_nZoomCols
    if nOldZoomCol != nNewZoomCol:
      self.obj('oSends').update()
      self.obj('oTracks').update()

    # update gui
    self.send_msg(
      '/EDIT',
      [
        'session/zoom/%d' % (self.m_nSelCell),
        '{"colorFill":"#66cc66"}'
      ])

    if nValue < 0.5:
      self.send_msg(sAddr, 1) # prevent from turning off

  # ********************************************************

  def scan_zoom_area(self, pnTrackIdxStartAbs, pnSceneIdxStartAbs):
    tResult = (False, None) # default result: no clips in this area!

    for nColIdx in range(self.m_nTracks):
      nTrackIdxAbs = pnTrackIdxStartAbs + nColIdx
      if self.is_track_available(nTrackIdxAbs) == False:
        return tResult # nothing else to check! there's no more tracks!
      oTrack = self.get_track(nTrackIdxAbs)
      lSlots = oTrack.clip_slots

      for nRowIdx in range(self.m_nScenes):
        nSceneIdxAbs = pnSceneIdxStartAbs + nRowIdx
        if self.is_scene_available(nSceneIdxAbs) == False:
          break # continue with the next track

        oSlot = lSlots[nSceneIdxAbs]
        if oSlot.has_clip == False:
          continue # empty clip slot, continue with next scene

        oClip = oSlot.clip
        if oClip.is_playing:
          return (True, '#33cc33') # at least one clip playing! return now!
        else:
          tResult = (True, '#ffffff') # at least one clip ready

    return tResult

