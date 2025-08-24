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

    nTracks = 3
    nScenes = 3

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

    self.m_sOldMode = 'NONE'
    self.m_sNewMode = 'LOOP'

    # Modes
    self.m_oModeLoop = ModeLoop(
      poCtrlInst,
      phCfg,
      phObj,
      poMatrix,
      plBottom,
      plSide)
    self.m_oModeTune = ModeTune(
      poCtrlInst,
      phCfg,
      phObj,
      poMatrix,
      plBottom,
      plSide)

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
      if phAttr['nIdx'] == 4:
        self.m_sNewMode = 'LOOP'
        self.update()
        self.alert('MODE LOOP')
      elif phAttr['nIdx'] == 5:
        self.m_sNewMode = 'TUNE'
        self.update()
        self.alert('MODE TUNE')
      else:
        self.alert('BOTTOM, idx: %d' % (phAttr['nIdx']))

    elif sType == 'side':
      if self.m_sOldMode == 'LOOP':
        self.m_oModeLoop.on_side(phAttr['nIdx'])
      else:
        self.m_oModeTune.on_side(phAttr['nIdx'])

    else: # sType = 'grid'
      if self.m_sOldMode == 'LOOP':
        self.m_oModeLoop.on_grid(phAttr['nCol'], phAttr['nRow'])
      else:
        self.m_oModeTune.on_grid(phAttr['nCol'], phAttr['nRow'])

  def on_shift_value(self, pnValue):
    if pnValue == 0: return
    self.alert('SHIFT')

  # ********************************************************

  def session_component(self):
    return self.m_oSession

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)

