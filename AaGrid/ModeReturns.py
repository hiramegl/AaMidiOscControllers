import Live

class ModeReturns():
  def __init__(self, poCtrlInst, phCfg, phObj, poMatrix, plBottom, plSide):
    self.m_oCtrlInst = poCtrlInst
    self.m_hCfg      = phCfg
    self.m_hObj      = phObj
    self.m_oMatrix   = poMatrix
    self.m_lBottom   = plBottom
    self.m_lSide     = plSide

    self.m_lGridSkin = [
      'Eq3On' ,
      'HighOn',
      'MidOn' ,
      'LowOn' ,
      'FxOff' ,
      'Mute'  ,
      'Solo'  ,
      'Select',
    ]
    self.m_lSideSkin = [
      'Side', # Eq3On
      'Side', # HighOn
      'Side', # MidOn
      'Side', # LowOn
      'Side', # FxOff
      'Side', # Mute
      'Side', # Solo
      'DefaultButton',
    ]
    self.m_lBottomSkin = [
      'DefaultButton',
      'DefaultButton',
      'Bottom', # Returns Mode
      'DefaultButton',
    ]

  def set_active(self, pbActive):
    for nRow in range(self.cfg('nRows')):
      oBut = self.m_lSide[nRow]
      sSkin = self.m_lSideSkin[nRow] if pbActive else 'DefaultButton'
      oBut.set_on_off_values(sSkin)
      oBut.turn_on()
      for nCol in range(self.cfg('nCols')):
        oBut = self.get_btn(nCol, nRow)
        sSkin = 'Returns.' + self.m_lGridSkin[nRow] if pbActive else 'DefaultButton'
        oBut.set_on_off_values(sSkin)
        self.update_grid_button(nRow, nCol, oBut)

    for nCol in range(4):
      oBut = self.m_lBottom[nCol]
      sSkin = self.m_lBottomSkin[nCol] if pbActive else 'DefaultButton'
      oBut.set_on_off_values(sSkin)
      oBut.turn_on()

    if pbActive:
      self.song().view.add_selected_track_listener(self.on_sel_track_changed)
    else:
      self.song().view.remove_selected_track_listener(self.on_sel_track_changed)

  def get_btn(self, pnCol, pnRow):
    return self.m_oMatrix.get_button(pnCol, pnRow)

  def update_grid_button(self, pnRow, pnCol, poBut):
    lReturns = self.returns()
    if pnCol >= len(lReturns):
      poBut.turn_off()
      return

    oReturn   = lReturns[pnCol]
    oSelTrack = self.sel_track()

    if pnRow == 0: # Eq3On
      self.update_eq3_button(oReturn, 'Device On', poBut)
    elif pnRow == 1: # HighOn
      self.update_eq3_button(oReturn, 'HighOn'   , poBut)
    elif pnRow == 2: # MidOn
      self.update_eq3_button(oReturn, 'MidOn'    , poBut)
    elif pnRow == 3: # LowOn
      self.update_eq3_button(oReturn, 'LowOn'    , poBut)
    elif pnRow == 4: # FxOff
      poBut.turn_on() # always on!
    elif pnRow == 5: # Return Mute
      if oReturn.mute > 0:
        poBut.turn_off()
      else:
        poBut.turn_on()
    elif pnRow == 6: # Return Solo
      if oReturn.solo > 0:
        poBut.turn_on()
      else:
        poBut.turn_off()
    elif pnRow == 7: # Select track
      if oReturn == oSelTrack:
        poBut.turn_on()
      else:
        poBut.turn_off()

  def update_eq3_button(self, poReturn, psParam, poBut):
    for oDev in poReturn.devices:
      if oDev.class_name != 'FilterEQ3':
        continue
      for oParam in oDev.parameters:
        if oParam.name != psParam:
          continue
        if oParam.value > 0:
          poBut.turn_on()
        else:
          poBut.turn_off()
        return

  def on_sel_track_changed(self):
    oSelTrack = self.sel_track()
    lReturns  = self.returns()
    for nCol in range(len(lReturns)):
      oReturn = lReturns[nCol]
      oBut    = self.get_btn(nCol, 7)
      if oReturn == oSelTrack:
        oBut.turn_on()
      else:
        oBut.turn_off()

  # ********************************************************

  def on_grid(self, pnCol, pnRow):
    lReturns = self.returns()
    if pnCol >= len(lReturns):
      return
    oBut    = self.get_btn(pnCol, pnRow)
    oReturn = lReturns[pnCol]
    sReturn = oReturn.name

    if pnRow == 0: # Eq3On
      nVal = self.toggle_eq3_button(oReturn, 'Device On', oBut)
      self.alert('"%s": Eq3 %s' %
        (sReturn, 'On' if nVal else 'Off'))
    elif pnRow == 1: # HighOn
      nVal = self.toggle_eq3_button(oReturn, 'HighOn'   , oBut)
      self.alert('"%s": Eq3 High %s' %
        (sReturn, 'On' if nVal else 'Off'))
    elif pnRow == 2: # MidOn
      nVal = self.toggle_eq3_button(oReturn, 'MidOn'    , oBut)
      self.alert('"%s": Eq3 Mid %s' %
        (sReturn, 'On' if nVal else 'Off'))
    elif pnRow == 3: # LowOn
      nVal = self.toggle_eq3_button(oReturn, 'LowOn'    , oBut)
      self.alert('"%s": Eq3 Low %s' %
        (sReturn, 'On' if nVal else 'Off'))
    elif pnRow == 4: # FxOff
      self.return_fx_off(oReturn)
      self.alert('"%s": all effects off' % (sReturn))
    elif pnRow == 5: # Return Mute
      oReturn.mute = not oReturn.mute
      if oReturn.mute > 0:
        poBut.turn_off()
      else:
        poBut.turn_on()
      self.alert('"%s": Mute %s' %
        (sReturn, 'On' if oReturn.mute > 0 else 'Off'))
    elif pnRow == 6: # Return Solo
      oReturn.solo = not oReturn.solo
      if oReturn.solo > 0:
        poBut.turn_on()
      else:
        poBut.turn_off()
      self.alert('"%s": Solo %s' %
        (sReturn, 'On' if oReturn.mute > 0 else 'Off'))
    elif pnRow == 7: # Select track
      self.sel_track(oReturn)
      self.alert('"%s": selected' % (sReturn))

  def toggle_eq3_button(self, poReturn, psParam, poBut):
    for oDev in poReturn.devices:
      if oDev.class_name != 'FilterEQ3':
        continue
      for oParam in oDev.parameters:
        if oParam.name != psParam:
          continue
        oParam.value = 0 if oParam.value > 0 else 1
        if oParam.value > 0:
          poBut.turn_on()
        else:
          poBut.turn_off()
        return oParam.value

  def return_fx_off(self, poReturn):
    for oDev in poReturn.devices:
      for oParam in oDev.parameters:
        if oParam.name != 'Device On':
          continue
        oParam.value = 0
        return

  def on_side(self, pnRow):
    lReturns = self.returns()
    for nCol in range(len(lReturns)):
      oBut    = self.get_btn(nCol, pnRow)
      oReturn = lReturns[nCol]

      if pnRow == 0: # Eq3On
        self.turn_on_eq3_button(oReturn, 'Device On', oBut)
        self.alert('All Eq3 On')
      elif pnRow == 1: # HighOn
        self.turn_on_eq3_button(oReturn, 'HighOn'   , oBut)
        self.alert('All Eq3 - High On')
      elif pnRow == 2: # MidOn
        self.turn_on_eq3_button(oReturn, 'MidOn'    , oBut)
        self.alert('All Eq3 - Mid On')
      elif pnRow == 3: # LowOn
        self.turn_on_eq3_button(oReturn, 'LowOn'    , oBut)
        self.alert('All Eq3 - Low On')
      elif pnRow == 4: # FxOff
        self.return_fx_off(oReturn)
        self.alert('All effects off')
      elif pnRow == 5: # Return Mute
        oReturn.mute = 0
        if oReturn.mute > 0:
          poBut.turn_off()
        else:
          poBut.turn_on()
        self.alert('All mute off')
      elif pnRow == 6: # Return Solo
        oReturn.solo = 0
        if oReturn.solo > 0:
          poBut.turn_on()
        else:
          poBut.turn_off()
        self.alert('All solo off')

  def turn_on_eq3_button(self, poReturn, psParam, poBut):
    for oDev in poReturn.devices:
      if oDev.class_name != 'FilterEQ3':
        continue
      for oParam in oDev.parameters:
        if oParam.name != psParam:
          continue
        oParam.value = 1
        if oParam.value > 0:
          poBut.turn_on()
        else:
          poBut.turn_off()
        return

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def returns(self):
    return self.song().return_tracks

  def sel_track(self, poTrack = None):
    if poTrack != None:
      self.song().view.selected_track = poTrack
    return self.song().view.selected_track

  # ********************************************************

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.obj('oCtrlInst').show_message(psMsg)

