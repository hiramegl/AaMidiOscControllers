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
    self.reg_idx_cb('clip/nav'      , 4, self.on_clip_nav)
    self.reg_idx_cb('clip/focus_nav', 4, self.on_clip_focus_nav)

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
        self.alert('Select track to the left')
      else:
        self.alert('Cannot select track to the left')

    elif sDir == 'RIGHT':
      if nTrackIdxAbs < len(self.tracks_and_returns()):
        oTrackOrReturn = self.get_track_or_return(nTrackIdxAbs + 1)
        self.sel_track(oTrackOrReturn)
        self.alert('Selecting track to the right')
      else:
        self.alert('Cannot select track to the right')

    elif sDir == 'DOWN':
      if nTrackIdxAbs < len(self.scenes()):
        oScene = self.get_scene(nSceneIdxAbs + 1)
        self.sel_scene(oScene)
        self.alert('Selecting next scene')
      else:
        self.alert('Cannot select next scene')

    elif sDir == 'UP':
      if nSceneIdxAbs > 0:
        oScene = self.get_scene(nSceneIdxAbs - 1)
        self.sel_scene(oScene)
        self.alert('Selecting previous scene')
      else:
        self.alert('Cannot select previous scene')

  def on_clip_focus_nav(self, plSegs, plMsg):
    nIdx = int(plSegs[3])
    sDir = self.m_lDirs[nIdx]
    nColOff = self.col_offset()
    nRowOff = self.row_offset()

    if sDir == 'LEFT':
      if nColOff > 0:
        nColOff -= 1
        self.state().set_clip_offsets(nColOff, nRowOff)
        self.alert('Focused track to the left')
      else:
        self.alert('Cannot focus track to the left')

    elif sDir == 'RIGHT':
      if nColOff < len(self.tracks_and_returns()):
        nColOff += 1
        self.state().set_clip_offsets(nColOff, nRowOff)
        self.alert('Focusing track to the right')
      else:
        self.alert('Cannot focus track to the right')

    elif sDir == 'DOWN':
      if nColOff < len(self.scenes()):
        nRowOff += 1
        self.state().set_clip_offsets(nColOff, nRowOff)
        self.alert('Focusing next scene')
      else:
        self.alert('Cannot focus next scene')

    elif sDir == 'UP':
      if nRowOff > 0:
        nRowOff -= 1
        self.state().set_clip_offsets(nColOff, nRowOff)
        self.alert('Focusing previous scene')
      else:
        self.alert('Cannot focus previous scene')

