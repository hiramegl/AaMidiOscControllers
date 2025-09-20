import Live

from _Framework.CompoundComponent import CompoundComponent
from _Framework.SessionComponent  import SessionComponent
from _Framework.MixerComponent    import MixerComponent

from .ModeLoop                    import ModeLoop
from .ModeTune                    import ModeTune

class Selector(CompoundComponent):
  def __init__(self, poCtrlInst, phCfg, phObj, poMatrix, plBottom, plSide, poShift):
    self.m_oCtrlInst = poCtrlInst
    super(Selector, self).__init__()
    self.m_hCfg    = phCfg
    self.m_hObj    = phObj
    self.m_oMatrix = poMatrix
    self.m_lBottom = plBottom
    self.m_lSide   = plSide
    self.m_lNavig  = plBottom[:4]

    # 1 track, 1 scene => 1 clip
    nTracks = 1
    nScenes = 1

    # Session and mixer components
    self.m_hObj['oSelector'] = self
    self.m_oSession = SessionComponent(
      nTracks,
      nScenes)
    self.m_hObj['oSession'] = self.m_oSession
    self.m_oMixer = MixerComponent(
      num_tracks  = nTracks,
      name        = 'Mixer')
    self.m_hObj['oMixer'] = self.m_oMixer
    self.m_oSession.set_mixer(self.m_oMixer)

    self.setup_paging_controls()

    self.m_sOldMode = 'NONE'
    self.m_sNewMode = 'LOOP'

    # Modes
    self.m_oModeLoop = ModeLoop(
      poCtrlInst,
      phCfg,
      phObj,
      poMatrix,
      plBottom[4:], # discard navigation buttons
      plSide)
    self.m_oModeTune = ModeTune(
      poCtrlInst,
      phCfg,
      phObj,
      poMatrix,
      plBottom[4:], # discard navigation buttons
      plSide)

  def setup_paging_controls(self):
    for oButton in self.m_lNavig:
      oButton.set_on_off_values("Nav.On", "Nav.Off")
      oButton.turn_on()

    self.m_oSession.set_page_up_button   (self.m_lNavig[0])
    self.m_oSession.set_page_down_button (self.m_lNavig[1])
    self.m_oSession.set_page_left_button (self.m_lNavig[2])
    self.m_oSession.set_page_right_button(self.m_lNavig[3])

    self.m_oSession._vertical_paginator.update()
    self.m_oSession._horizontal_paginator.update()

  # ********************************************************

  def update(self):
    if self.m_sOldMode == self.m_sNewMode:
      return

    # Clear the old mode
    if self.m_sOldMode == 'LOOP':
      self.m_oModeLoop.set_active(False)
    else:
      self.m_oModeTune.set_active(False)

    self.m_sOldMode = self.m_sNewMode

    # Set the new mode
    if self.m_sNewMode == 'LOOP':
      self.m_oModeLoop.set_active(True)
    else:
      self.m_oModeTune.set_active(True)

  # ********************************************************

  def route(self, phAttr, pnValue):
    if pnValue == 0: return
    sType = phAttr['sType']

    if sType == 'bottom':
      nIdx  = phAttr['nIdx']
      if nIdx == 4:
        self.m_sNewMode = 'LOOP'
        self.update()
        self.alert('MODE LOOP')

      elif nIdx == 5:
        self.m_sNewMode = 'TUNE'
        self.update()
        self.alert('MODE TUNE')

    elif sType == 'side':
      nIdx  = phAttr['nIdx']
      if self.m_sOldMode == 'LOOP':
        self.m_oModeLoop.on_side(nIdx)
      else:
        self.m_oModeTune.on_side(nIdx)

    else: # sType = 'grid'
      if self.m_sOldMode == 'LOOP':
        self.m_oModeLoop.on_grid(phAttr['nCol'], phAttr['nRow'])
      else:
        self.m_oModeTune.on_grid(phAttr['nCol'], phAttr['nRow'])

  def on_shift_value(self, pnValue):
    if pnValue == 0:
      return

    nTrackOff = self.sel_track_idx_abs()
    nSceneOff = self.sel_scene_idx_abs()
    self.m_oSession.set_offsets(nTrackOff, nSceneOff)
    self.alert('Focusing clip (%d, %d)' % (nTrackOff, nSceneOff))

  # ********************************************************

  def session_component(self):
    return self.m_oSession

  def scene_offset(self):
    return self.m_oSession.scene_offset()

  def track(self):
    return self.get_track(self.m_oSession.track_offset())

  def scene(self):
    return self.get_scene(self.m_oSession.scene_offset())

  def clip_slot(self):
    oTrack       = self.track()
    nSceneIdxAbs = self.m_oSession.scene_offset()
    return oTrack.clip_slots[nSceneIdxAbs]

  # ********************************************************

  def tracks(self):
    return self.song().visible_tracks

  def get_track(self, pnTrackIdxAbs):
    return self.tracks()[pnTrackIdxAbs]

  def sel_track(self):
    return self.song().view.selected_track

  def sel_track_idx_abs(self):
    aAllTracks = self.tracks()
    oSelTrack  = self.sel_track()
    return list(aAllTracks).index(oSelTrack)

  def scenes(self):
    return self.song().scenes

  def get_scene(self, pnSceneIdxAbs):
    return self.scenes()[pnSceneIdxAbs]

  def sel_scene(self):
    return self.song().view.selected_scene

  def sel_scene_idx_abs(self):
    aAllScenes = self.scenes()
    oSelScene  = self.sel_scene()
    return list(aAllScenes).index(oSelScene)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)

