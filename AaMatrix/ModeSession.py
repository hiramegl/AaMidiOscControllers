import Live

BUTTON_OFF = 0
BUTTON_ON  = 127

MODE_SENDS  = 0
MODE_TRACK  = 1
MODE_SELECT = 2
MODE_FIRE   = 3

SUBMODE_FIRE_CLIPS  = 0
SUBMODE_FIRE_SCENES = 1
NUM_FIRE_SUBMODES   = 2

class ModeSession():
  def __init__(self, poCtrlInst, phCfg, phObj, poMatrix, plTop, plSide):
    self.m_oCtrlInst = poCtrlInst
    self.m_hCfg      = phCfg
    self.m_hObj      = phObj

    self.m_oMatrix   = poMatrix
    self.m_lNav      = plTop[:4]  # first 4 top  buttons for page navigation
    self.m_lColNav   = plTop[4:]  # last  4 top  buttons for col  navigation
    self.m_lRowNav   = plSide[:4] # first 4 side buttons for row  navigation
    self.m_lMode     = plSide[4:] # last  4 side buttons for mode change

    self.m_nMainMode = MODE_FIRE
    self.m_nSubMode  = SUBMODE_FIRE_CLIPS
    self.m_bSubUpdt  = False
    self.m_nColNav   = 0 # navigation col index
    self.m_nRowNav   = 0 # navigation row index
    self.m_nTrackOff = 0 # real track offset
    self.m_nSceneOff = 0 # real scene offset

  # ********************************************************

  def set_active(self, pbActive):
    self.setup_paging_buttons(pbActive)
    self.setup_nav_buttons(pbActive)
    self.setup_mode_buttons(pbActive)
    self.setup_grid_buttons(pbActive)

  def setup_paging_buttons(self, pbActive):
    if pbActive:
      for oBut in self.m_lNav:
        oBut.set_on_off_values('Session.Nav')
        oBut.turn_on()
      self.session().set_page_up_button(self.m_lNav[0])
      self.session().set_page_down_button(self.m_lNav[1])
      self.session().set_page_left_button(self.m_lNav[2])
      self.session().set_page_right_button(self.m_lNav[3])

    else:
      for oBut in self.m_lNav:
        oBut.set_on_off_values('DefaultButton.Disabled', 'DefaultButton.Disabled')
      self.session().set_page_up_button(None)
      self.session().set_page_down_button(None)
      self.session().set_page_left_button(None)
      self.session().set_page_right_button(None)

  def setup_nav_buttons(self, pbActive):
    if pbActive:
      for nIdx in range(4):
        oColBut = self.m_lColNav[nIdx]
        oColBut.set_on_off_values('Session.ColNav')
        if nIdx == self.m_nColNav:
          oColBut.turn_on()
        else:
          oColBut.turn_off()

        oRowBut = self.m_lRowNav[nIdx]
        oRowBut.set_on_off_values('Session.RowNav')
        if nIdx == self.m_nRowNav:
          oRowBut.turn_on()
        else:
          oRowBut.turn_off()

    else:
      for nIdx in range(4):
        oColBut = self.m_lColNav[nIdx]
        oColBut.set_on_off_values('DefaultButton.Disabled', 'DefaultButton.Disabled')
        oRowBut = self.m_lRowNav[nIdx]
        oRowBut.set_on_off_values('DefaultButton.Disabled', 'DefaultButton.Disabled')

  def setup_mode_buttons(self, pbActive):
    if pbActive:
      lModeColors = ['Sends', 'Track', 'Select', 'Fire']
      lSubColors  = ['Clips', 'Scenes']
      for nIdx in range(4):
        oModeBut   = self.m_lMode[nIdx]
        if nIdx == MODE_FIRE:
          sModeColor = 'Session.ModeFire.%s' % (lSubColors[self.m_nSubMode])
        else:
          sModeColor = 'Session.Mode%s' % (lModeColors[nIdx])
        oModeBut.set_on_off_values(sModeColor)
        if nIdx == self.m_nMainMode:
          oModeBut.turn_on()
        else:
          oModeBut.turn_off()

    else:
      for oModeBut in self.m_lMode:
        oModeBut.set_on_off_values('DefaultButton.Disabled', 'DefaultButton.Disabled')

  def setup_grid_buttons(self, pbActive):
    if pbActive:
      if self.m_nMainMode == MODE_SENDS:
        for nCol in range(self.cfg('nCols')):
          nTrackIdx = self.m_nTrackOff + nCol
          for nRow in range(self.cfg('nRows')):
            nSceneIdx = self.m_nSceneOff + nRow

            oBut = self.get_btn(nCol, nRow)
            oBut.set_on_off_values("Session.Send")

          oStrip = self.mixer().channel_strip(nTrackIdx)
          oStrip.set_send_controls(
              self.get_btn(nCol, 0),
              self.get_btn(nCol, 1),
              self.get_btn(nCol, 2),
              self.get_btn(nCol, 3),
              self.get_btn(nCol, 4),
              self.get_btn(nCol, 5),
              self.get_btn(nCol, 6),
              self.get_btn(nCol, 7))

      elif self.m_nMainMode == MODE_TRACK:
        lColors = ['Stop', 'Mute', 'Solo', 'Arm', 'Monitor', 'Deck', 'SendsOff', 'Select']
        for nCol in range(self.cfg('nCols')):
          nTrackIdx = self.m_nTrackOff + nCol
          for nRow in range(self.cfg('nRows')):
            oBut = self.get_btn(nCol, nRow)
            oBut.set_on_off_values('Session.%s' % (lColors[nRow]))

          oStrip = self.mixer().channel_strip(nTrackIdx)
          oStrip.set_stop_button  (self.get_btn(nCol, 0))
          oStrip.set_mute_button  (self.get_btn(nCol, 1))
          oStrip.set_solo_button  (self.get_btn(nCol, 2))
          oStrip.set_arm_button   (self.get_btn(nCol, 3))
          oStrip.set_input_control(self.get_btn(nCol, 4))
          oStrip.set_deck_control (self.get_btn(nCol, 5))
          oStrip.set_sends_control(self.get_btn(nCol, 6))
          oStrip.set_select_button(self.get_btn(nCol, 7))
          oStrip.set_invert_mute_feedback(True)

      elif self.m_nMainMode == MODE_SELECT:
        for nRow in range(self.cfg('nRows')):
          nSceneIdx = self.m_nSceneOff + nRow
          oScene = self.session().scene(nSceneIdx)
          for nCol in range(self.cfg('nCols')):
            nTrackIdx = self.m_nTrackOff + nCol

            oBut = self.get_btn(nCol, nRow)
            oBut.set_on_off_values("Unav")
            oBut.set_enabled(True)

            oClipSlot = oScene.clip_slot(nTrackIdx)
            oClipSlot.set_launch_button(oBut)
            oClipSlot.set_select_button(oBut)

      elif self.m_nMainMode == MODE_FIRE:
        if self.m_nSubMode == SUBMODE_FIRE_CLIPS:
          for nRow in range(self.cfg('nRows')):
            nSceneIdx = self.m_nSceneOff + nRow
            oScene = self.session().scene(nSceneIdx)
            for nCol in range(self.cfg('nCols')):
              nTrackIdx = self.m_nTrackOff + nCol

              oBut = self.get_btn(nCol, nRow)
              oBut.set_on_off_values("Unav")
              oBut.set_enabled(True)

              oClipSlot = oScene.clip_slot(nTrackIdx)
              oClipSlot.set_launch_button(oBut)

        else: # SUBMODE_FIRE_SCENES
          for nCol in range(self.cfg('nCols')):
            for nRow in range(self.cfg('nRows')):
              oBut = self.get_btn(nCol, nRow)
              if nCol == 0:
                nSceneIdx = self.m_nSceneOff + nRow
                oScene = self.session().scene(nSceneIdx)
                oScene.set_launch_button(oBut)
              else:
                oBut.set_on_off_values("Session.ModeFire.Scenes")
                oBut.turn_off()

    else:
      if self.m_nMainMode == MODE_SENDS:
        for nCol in range(self.cfg('nCols')):
          nTrackIdx = self.m_nTrackOff + nCol
          oStrip = self.mixer().channel_strip(nTrackIdx)
          oStrip.set_send_controls(None, None, None, None, None, None, None, None)

      elif self.m_nMainMode == MODE_TRACK:
        for nCol in range(self.cfg('nCols')):
          nTrackIdx = self.m_nTrackOff + nCol

          oStrip = self.mixer().channel_strip(nTrackIdx)
          oStrip.set_stop_button  (None)
          oStrip.set_mute_button  (None)
          oStrip.set_solo_button  (None)
          oStrip.set_arm_button   (None)
          oStrip.set_input_control(None)
          oStrip.set_deck_control (None)
          oStrip.set_sends_control(None)
          oStrip.set_select_button(None)

      elif self.m_nMainMode == MODE_SELECT:
        for nRow in range(self.cfg('nRows')):
          nSceneIdx = self.m_nSceneOff + nRow
          oScene = self.session().scene(nSceneIdx)
          for nCol in range(self.cfg('nCols')):
            nTrackIdx = self.m_nTrackOff + nCol

            oClipSlot = oScene.clip_slot(nTrackIdx)
            oClipSlot.set_launch_button(None)
            oClipSlot.set_select_button(None)

      elif self.m_nMainMode == MODE_FIRE:
        if self.m_nSubMode == SUBMODE_FIRE_CLIPS:
          for nRow in range(self.cfg('nRows')):
            nSceneIdx = self.m_nSceneOff + nRow
            oScene = self.session().scene(nSceneIdx)
            for nCol in range(self.cfg('nCols')):
              nTrackIdx = self.m_nTrackOff + nCol

              oClipSlot = oScene.clip_slot(nTrackIdx)
              oClipSlot.set_launch_button(None)

        else: # SUBMODE_FIRE_SCENES
          for nCol in range(self.cfg('nCols')):
            for nRow in range(self.cfg('nRows')):
              oBut = self.get_btn(nCol, nRow)
              oBut.turn_off()
              oBut.set_on_off_values("Session.ModeFire.Scenes")
              if nCol == 0:
                nSceneIdx = self.m_nSceneOff + nRow
                oScene = self.session().scene(nSceneIdx)
                oScene.set_launch_button(None)

  def get_btn(self, pnCol, pnRow):
    return self.m_oMatrix.get_button(pnCol, pnRow)

  # ********************************************************

  def on_col_nav(self, pnIdx, pnValue):
    if pnValue == BUTTON_OFF: return
    if pnIdx == self.m_nColNav:
      return # we are not changing navigation column, ignore event

    self.setup_grid_buttons(False)
    self.setup_nav_buttons(False)
    self.m_nColNav = pnIdx
    self.m_nTrackOff = pnIdx * 8
    self.setup_grid_buttons(True)
    self.setup_nav_buttons(True)

    self.alert('NAV: COL %d, ROW %d' % (self.m_nColNav + 1, self.m_nRowNav + 1))

    self.session().set_inner_track_offset(self.m_nTrackOff)
    oAaBcf = self.get_faders_or_none()
    if oAaBcf == None:
      self.alert('No BCF controller found!')
    else:
      oAaBcf.move_to_track_offset(self.m_nTrackOff + self.obj('oSession').track_offset())

  def on_row_nav(self, pnIdx, pnValue):
    if pnValue == BUTTON_OFF: return
    if pnIdx == self.m_nRowNav:
      return # we are not changing navigation row, ignore event

    self.setup_grid_buttons(False)
    self.setup_nav_buttons(False)
    self.m_nRowNav = pnIdx
    self.m_nSceneOff = pnIdx * 8
    self.setup_grid_buttons(True)
    self.setup_nav_buttons(True)

    self.alert('NAV: COL %d, ROW %d' % (self.m_nColNav + 1, self.m_nRowNav + 1))

  def on_mode(self, pnIdx, pnValue):
    if pnValue == BUTTON_OFF: return
    if pnIdx == self.m_nMainMode and pnIdx != MODE_FIRE:
      return # we are not changing mode, ignore event

    # we are changing mode! turn off colors!
    self.setup_grid_buttons(False)
    self.setup_mode_buttons(False)

    self.m_nMainMode = pnIdx # update the new mode

    if pnIdx == MODE_FIRE:
      self.m_bSubUpdt = False
      self.m_nSubMode = ((self.m_nSubMode + 1) % NUM_FIRE_SUBMODES) # change FIRE submode
      lSubModes = ['CLIPS', 'SCENES']
      self.alert('MODE: FIRE %s' % (lSubModes[self.m_nSubMode]))

    else:
      if self.m_bSubUpdt == False:
        self.m_nSubMode = ((self.m_nSubMode + 1) % NUM_FIRE_SUBMODES) # advance submode to remain in it next time
        self.m_bSubUpdt = True
      lModes = ['SENDS', 'TRACKS', 'SELECT']
      self.alert('MODE: %s' % (lModes[self.m_nMainMode]))

    # now turn on colors and setup buttons
    self.setup_grid_buttons(True)
    self.setup_mode_buttons(True)

  def on_grid(self, pnCol, pnRow, pnValue):
    if pnValue == BUTTON_OFF:
      return (pnCol, pnRow) # dummy result just to use the parameters
    # ignore event, it is handled by the mode mappings

  # ********************************************************

  def get_faders_or_none(self):
    lCtrlInsts = Live.Application.get_application().control_surfaces
    for oCtrlInst in lCtrlInsts:
      sCtrlName = oCtrlInst.__class__.__name__
      if sCtrlName == 'AaBcf':
        return oCtrlInst

    return None

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def session(self):
    return self.obj('oSession')

  def mixer(self):
    return self.obj('oMixer')

  # ********************************************************

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)
