from .Base import Base

class ClipNav(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lDirs = ['LEFT', 'RIGHT', 'DOWN', 'UP']
    phObj['oClipNav'] = self

    self.connect()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb('clip/nav', 4, self.on_clip_nav)

  # ********************************************************

  def on_clip_nav(self, plSegs, plMsg):
    nIdx = int(plSegs[3])
    sDir = self.m_lDirs[nIdx]
    nTrackIdxAbs = self.sel_track_idx_abs()
    nSceneIdxAbs = self.sel_scene_idx_abs()

    if sDir == 'LEFT':
      if nTrackIdxAbs > 0:
        oTrackOrReturn = self.get_track_or_return(nTrackIdxAbs - 1)
        self.sel_track(oTrackOrReturn)

    elif sDir == 'RIGHT':
      if nTrackIdxAbs < len(self.tracks_and_returns()):
        oTrackOrReturn = self.get_track_or_return(nTrackIdxAbs + 1)
        self.sel_track(oTrackOrReturn)

    elif sDir == 'DOWN':
      if nTrackIdxAbs < len(self.scenes()):
        oScene = self.get_scene(nSceneIdxAbs + 1)
        self.sel_scene(oScene)

    elif sDir == 'UP':
      if nSceneIdxAbs > 0:
        oScene = self.get_scene(nSceneIdxAbs - 1)
        self.sel_scene(oScene)

