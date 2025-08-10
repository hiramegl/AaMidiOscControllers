import Live

class Base():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def comm(self):
    return self.obj('oComm')

  def state(self):
    return self.obj('oState')

  def mode(self):
    return self.state().mode()

  # ********************************************************

  def reg_cb(self, psAddr, pfCallback):
    self.comm().reg_rx_cb(psAddr, pfCallback)

  def reg_idx_cb(self, psAddr, pnRange, pfCallback):
    self.comm().reg_indexed_rx_cb(psAddr, pnRange, pfCallback)

  def send_msg(self, psAddr, poMsg):
    self.comm().send_msg(psAddr, poMsg)

  def send_bundle(self, plBundle):
    self.comm().send_bundle(plBundle)

  # ********************************************************

  def get_row_col(self, pnIdx, pnCols, plRowStr = None, plColStr = None):
    nRowIdx = int(pnIdx / pnCols)
    nColIdx = pnIdx % pnCols
    oRow = nRowIdx if plRowStr == None else plRowStr[nRowIdx]
    oCol = nColIdx if plColStr == None else plColStr[nColIdx]
    return (oRow, oCol)

  # ********************************************************

  def track_offset(self):
    return self.state().track_offset()

  def scene_offset(self):
    return self.state().scene_offset()

  def track_idx_abs(self, pnTrackIdxRel):
    return pnTrackIdxRel + self.track_offset()

  def scene_idx_abs(self, pnSceneIdxRel):
    return pnSceneIdxRel + self.scene_offset()

  def track_idx_rel(self, pnTrackIdxAbs):
    return pnTrackIdxAbs - self.track_offset()

  def scene_idx_rel(self, pnSceneIdxAbs):
    return pnSceneIdxAbs - self.scene_offset()

  # ********************************************************

  def tracks(self):
    return self.song().visible_tracks

  def returns(self):
    return self.song().return_tracks

  def master(self):
    return self.song().master_track

  def tracks_and_returns(self):
    return tuple(self.tracks()) + tuple(self.returns())

  def get_track(self, pnTrackIdxAbs):
    return self.tracks()[pnTrackIdxAbs]

  def get_track_or_return(self, pnTrackIdxAbs):
    return self.tracks_and_returns()[pnTrackIdxAbs]

  def get_return(self, pnTrackIdxAbs):
    return self.returns()[pnTrackIdxAbs]

  def is_track_available(self, pnTrackIdxAbs):
    return (pnTrackIdxAbs < len(self.tracks()))

  def sel_track(self, poTrack = None):
    if poTrack != None:
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  def sel_track_idx_abs(self):
    oSelTrack = self.sel_track()
    if oSelTrack == self.master():
      return 'MASTER'
    lAllTracks = self.tracks_and_returns()
    return list(lAllTracks).index(oSelTrack)

  # ------------------------------------

  def scenes(self):
    return self.song().scenes

  def get_scene(self, pnSceneIdxAbs):
    return self.scenes()[pnSceneIdxAbs]

  def is_scene_available(self, pnSceneIdxAbs):
    return (pnSceneIdxAbs < len(self.scenes()))

  def sel_scene(self, poScene = None):
    if poScene != None:
      self.song().view.selected_scene = poScene
    return self.song().view.selected_scene

  def sel_scene_idx_abs(self):
    lAllScenes = self.scenes()
    oSelScene  = self.sel_scene()
    return list(lAllScenes).index(oSelScene)

  # ------------------------------------

  def sel_clip_slot(self, poSlot = None):
    if poSlot != None:
      self.song().view.highlighted_clip_slot = poSlot
    return self.song().view.highlighted_clip_slot

  def to_color(self, pnRgb):
    if pnRgb == 0:
      return 'var(--color-raised)'

    nB =  pnRgb        & 255
    nG = (pnRgb >> 8)  & 255
    nR = (pnRgb >> 16) & 255

    return '#%02x%02x%02x' % (nR, nG, nB)

  # ********************************************************

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

