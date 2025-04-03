class Scene():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.connect()

    phObj['oScene'] = self

  def connect(self):
    fSceneCb  = lambda ptKey, pnValue: self.handle_scene_rx_msg(ptKey, pnValue)
    nBank0Chn = self.cfg('nBank0Chn')
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nScnSel'),    'ScnSel',    fSceneCb)
    self.obj('oComm').reg_cc(
      nBank0Chn, self.cfg('nScnSelRst'), 'ScnSelRst', fSceneCb)

    self.song().view.add_selected_scene_listener(self.handle_scnsel_tx_msg)

  def handle_scene_rx_msg(self, ptKey, pnValue):
    nId = ptKey[1]

    if nId == self.cfg('nScnSel'):
      if self.is_scene_available(pnValue) == False: return
      self.sel_scene(self.get_scene(pnValue))
      self.alert('Selected scene: %d' % (pnValue + 1))
    if nId == self.cfg('nScnSelRst'):
      if self.is_scene_available(0) == False: return
      self.sel_scene(self.get_scene(0))
      self.send_msg('nBank0Chn', 'nScnSel', 0)
      self.alert('Selected scene: %d' % (1))

  def handle_scnsel_tx_msg(self):
    oSelScene = self.sel_scene()
    nSceneIdxAbs = list(self.scenes()).index(oSelScene)
    if nSceneIdxAbs > 127: nSceneIdxAbs = 127
    self.send_msg('nBank0Chn', 'nScnSel', nSceneIdxAbs)

    # update clip parameters
    self.obj('oClip').update()

  def sync(self):
    self.handle_scnsel_tx_msg()

  def disconnect(self):
    self.song().view.remove_selected_scene_listener(self.handle_scnsel_tx_msg)
    self.send_msg('nBank0Chn', 'nScnSel', 0)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def scenes(self):
    return self.song().scenes

  def get_scene(self, pnSceneIdxAbs):
    aAllScenes = self.scenes()
    return aAllScenes[pnSceneIdxAbs]

  def sel_scene(self, poScene = None):
    if (poScene != None):
      self.song().view.selected_scene = poScene
    return self.song().view.selected_scene

  def is_scene_available(self, pnSceneIdxAbs):
    return (pnSceneIdxAbs < len(self.scenes()))

  def send_msg(self, psBankChn, psId, pnValue, pnIdx = 0):
    nBankChn = 0xB0 | self.cfg(psBankChn)
    nId      = self.cfg(psId) + pnIdx
    self.obj('oComm').send_msg([nBankChn, nId, pnValue])

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

