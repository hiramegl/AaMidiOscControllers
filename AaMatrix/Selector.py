from _Framework.CompoundComponent import CompoundComponent

from .SpecialSessionComponent     import SpecialSessionComponent
from .SpecialMixerComponent       import SpecialMixerComponent
from .ModeSession                 import ModeSession
from .ColorsMK2                   import CLIP_COLOR_TABLE, RGB_COLOR_TABLE

class Selector(CompoundComponent):
  def __init__(self, poCtrlInst, phCfg, phObj, poMatrix, plTop, plSide):
    self.m_oCtrlInst = poCtrlInst
    super(Selector, self).__init__()
    self.m_hCfg      = phCfg
    self.m_hObj      = phObj
    self.m_oMatrix   = poMatrix
    self.m_lTop      = plTop
    self.m_lSide     = plSide
    self.m_hObj['oSelector'] = self

    self.m_oSession = SpecialSessionComponent(
      self.m_hObj,
      self.cfg('nTracks'),
      self.cfg('nScenes'))
    self.m_hObj['oSession'] = self.m_oSession

    self.m_oMixer = SpecialMixerComponent(
      num_tracks  = self.cfg('nTracks'),
      name        = 'Mixer')
    self.m_hObj['oMixer'] = self.m_oMixer

    for nTrackIdx in range(self.cfg('nTracks')):
      oStrip = self.m_oMixer.channel_strip(nTrackIdx)
      oStrip.name = 'Channel_Strip_' + str(nTrackIdx)

    self.m_oSession.set_mixer(self.m_oMixer)
    self.m_oSession.set_rgb_mode(CLIP_COLOR_TABLE, RGB_COLOR_TABLE)

    self.m_oModeSession = ModeSession(
      poCtrlInst,
      phCfg,
      phObj,
      poMatrix,
      plTop,
      plSide)

  def disconnect(self):
    self.m_oModeSession.set_active(False)
    self.m_oSession     = None
    self.m_oMixer       = None
    self.m_oModeSession = None

  # ********************************************************

  def update(self):
    self.m_oSession.set_allow_update(False)
    self.m_oMixer.set_allow_update(False)

    # enable buttons
    for nRowIdx in range(self.cfg('nRows')):
      for nColIdx in range(self.cfg('nCols')):
        oButton = self.m_oMatrix.get_button(nColIdx, nRowIdx)
        oButton.set_enabled(True)
    for nColIdx in range(self.cfg('nCols')):
      self.m_lTop[nColIdx].set_enabled(True)
    for nRowIdx in range(self.cfg('nRows')):
      self.m_lSide[nRowIdx].set_enabled(True)

    self.m_oModeSession.set_active(True)

    self.m_oSession.set_allow_update(True)
    self.m_oMixer.set_allow_update(True)

  def route(self, phAttr, pnValue):
    sType = phAttr['sType']

    if sType == 'top':
      nIdx = phAttr['nIdx']
      if nIdx >= 0 and nIdx <= 3:
        return # navigation event handled by the session component
      else:
        self.m_oModeSession.on_col_nav(nIdx - 4, pnValue)

    elif sType == 'side':
      nIdx = phAttr['nIdx']
      if nIdx >= 0 and nIdx <= 3:
        self.m_oModeSession.on_row_nav(nIdx, pnValue)
      else:
        self.m_oModeSession.on_mode(nIdx - 4, pnValue)

    else: # sType = 'grid'
      self.m_oModeSession.on_grid(phAttr['nCol'], phAttr['nRow'], pnValue)

  # ********************************************************

  def session_component(self):
    return self.m_oSession

  def sync_grid(self):
    self.m_oModeSession.setup_grid_buttons(False)
    self.m_oModeSession.setup_grid_buttons(True)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]
