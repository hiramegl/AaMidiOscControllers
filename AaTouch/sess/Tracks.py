from AaTouch.Base import Base

class Tracks(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hCache = {} # grid cache
    self.m_lCmd1Clr = [
      '#cc3300', # STOP,
      '#ffff33', # MUTE
      '#3333ff', # SOLO
      '#cc3366', # ARM
      '#6600cc', # MONITOR
      '#ffffff', # SELECT
    ]
    self.m_lCmd2Clr = [
      '#6699cc', # CENTER PAN
      '#33ffff', # CROSS
      '#00ff99', # VOL 0 dB
      '#006633', # VOL -INF dB
      '#990000', # SENDS OFF
      '#ffffff', # SELECT
    ]
    self.m_nSelTrackIdxRel = None
    self.connect()

    phObj['oTracks'] = self

  # ********************************************************

  def connect(self):
    self.reg_idx_cb('track/cmd1', self.cfg('nTracks') * 6, self.on_cmd1)
    self.reg_idx_cb('track/cmd2', self.cfg('nTracks') * 6, self.on_cmd2)
    self.reg_idx_cb('track/vol',  self.cfg('nTracks')    , self.on_vol)
    self.set_cmd1_visible(True) # show 'Cmd1' & hide 'Cmd2'
    self.activate(True)

  def disconnect(self):
    self.deactivate(True)

  # ********************************************************

  def update(self):
    self.deactivate(False)
    self.activate(False)
    self.update_volumes()
    self.update_track_colors()

  def update_volumes(self):
    lBundle = []
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs):
        oTrack = self.get_track(nTrackIdxAbs)
        nVol   = oTrack.mixer_device.volume.value
      else:
        nVol = 0.0
      lBundle.append(['/track/vol/%d' % (nTrackIdxRel), nVol])
    self.send_bundle(lBundle)

  def update_track_colors(self):
    lBundle = []
    sFill  = '{"colorFill":"%s"}'
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs):
        oTrack = self.get_track(nTrackIdxAbs)
        sColor = self.to_color(oTrack.color)
      else:
        sColor = '#ffffff'
      lBundle.append([
        '/EDIT',
        ['track/cmd1/%d' % (nTrackIdxRel), sFill % (sColor)]])
      lBundle.append([
        '/EDIT',
        ['track/cmd2/%d' % (nTrackIdxRel), sFill % (sColor)]])
    self.send_bundle(lBundle)

  def activate(self, pbUpdateColor):
    sAddr1 = 'track/cmd1/%d'
    sAddr2 = 'track/cmd2/%d'
    sFill  = '{"colorFill":"%s"}'
    lColors1 = []
    lColors2 = []
    lValues1 = []
    lValues2 = []
    oSelTrack = self.sel_track()

    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      for nRowIdx in range(6):
        if self.is_track_available(nTrackIdxAbs):
          sColor1 = self.m_lCmd1Clr[nRowIdx]
          sColor2 = self.m_lCmd2Clr[nRowIdx]
          oTrack  = self.get_track(nTrackIdxAbs)
          if   nRowIdx == 1: # MUTE
            nValue1 = 0.0 if oTrack.mute else 1.0
          elif nRowIdx == 2: # SOLO
            nValue1 = 1.0 if oTrack.solo else 0.0
          elif nRowIdx == 3: # ARM
            nValue1 = 1.0 if oTrack.arm  else 0.0
          elif nRowIdx == 5: # SELECT
            nValue1 = 1.0 if oTrack == oSelTrack else 0.0
            if oTrack == oSelTrack:
              self.m_nSelTrackIdxRel = nTrackIdxRel
          else:
            nValue1 = 1.0

          if nRowIdx == 5: # SELECT
            nValue2 = 1.0 if oTrack == oSelTrack else 0.0
          else:
            nValue2 = 1.0

          if nRowIdx == 0: # STOP/PAN CENTER
            sColor1 = self.to_color(oTrack.color)
            sColor2 = sColor1
        else:
          sColor1 = '#ffffff'
          sColor2 = '#ffffff'
          nValue1 = 0.0
          nValue2 = 0.0

        nIdx = nRowIdx * self.cfg('nTracks') + nTrackIdxRel
        lColors1.append([
          '/EDIT',
          [sAddr1 % nIdx, sFill % sColor1]])
        lColors2.append([
          '/EDIT',
          [sAddr2 % nIdx, sFill % sColor2]])

        lValues1.append([
          '/' + (sAddr1 % nIdx), nValue1])
        lValues2.append([
          '/' + (sAddr2 % nIdx), nValue2])

    if pbUpdateColor:
      self.send_bundle(lColors1)
      self.send_bundle(lColors2)
    self.send_bundle(lValues1)
    self.send_bundle(lValues2)

  def deactivate(self, pbUpdateColor):
    sAddr1 = 'track/cmd1/%d'
    sAddr2 = 'track/cmd2/%d'
    sFill = '{"colorFill":"%s"}'

    lColors1 = []
    lColors2 = []
    lValues1 = []
    lValues2 = []

    for nTrackIdxRel in range(self.cfg('nTracks')):
      for nRowIdx in range(6):
        nIdx = nRowIdx * self.cfg('nTracks') + nTrackIdxRel
        lColors1.append([
          '/EDIT',
          [sAddr1 % nIdx, sFill % '#ffffff']])
        lColors2.append([
          '/EDIT',
          [sAddr2 % nIdx, sFill % '#ffffff']])

        lValues1.append(['/' + (sAddr1 % nIdx), 0.0])
        lValues2.append(['/' + (sAddr2 % nIdx), 0.0])
      lValues1.append(['/track/vol/%d' % (nTrackIdxRel), 0.0])

    self.send_bundle(lValues1)
    self.send_bundle(lValues2)
    if pbUpdateColor:
      self.send_bundle(lColors1)
      self.send_bundle(lColors2)
    self.m_nSelTrackIdxRel = None

  # ********************************************************

  def on_cmd1(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    (nCmdIdx, nTrkIdx) = self.get_row_col(nIdx, self.cfg('nTracks'))
    nTrackIdxAbs = self.track_idx_abs(nTrkIdx)
    if self.is_track_available(nTrackIdxAbs):
      oTrack = self.get_track(nTrackIdxAbs)
      if   nCmdIdx == 0: # STOP
        oTrack.stop_all_clips()
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 1: # MUTE
        oTrack.mute = (nValue < 0.5)
      elif nCmdIdx == 2: # SOLO
        oTrack.solo = (nValue > 0.5)
      elif nCmdIdx == 3: # ARM
        oTrack.arm  = (nValue > 0.5)
      elif nCmdIdx == 4: # MONITOR
        nMonitor = (oTrack.current_monitoring_state - 1) % 3
        oTrack.current_monitoring_state = nMonitor
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 5: # SELECT
        if oTrack != self.sel_track():
          self.sel_track(oTrack)
    else:
      self.send_msg(sAddr, 0.0)

  def on_cmd2(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    (nCmdIdx, nTrkIdx) = self.get_row_col(nIdx, self.cfg('nTracks'))
    nTrackIdxAbs = self.track_idx_abs(nTrkIdx)
    if self.is_track_available(nTrackIdxAbs):
      oTrack = self.get_track(nTrackIdxAbs)
      if   nCmdIdx == 0: # PAN RESET
        oTrack.mixer_device.panning.value = 0
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 1: # CROSS
        nCross = (oTrack.mixer_device.crossfade_assign - 1) % 3
        oTrack.mixer_device.crossfade_assign = nCross
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 2: # VOL 0 dB
        oTrack.mixer_device.volume.value = 0.85
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 3: # VOL -INF dB
        oTrack.mixer_device.volume.value = 0.0
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 4: # SENDS OFF
        lSends = oTrack.mixer_device.sends
        for nSendIdx in range(self.cfg('nReturns')):
          lSends[nSendIdx].value = 0.0
        self.send_msg(sAddr, 1.0)
      elif nCmdIdx == 5: # SELECT
        if oTrack != self.sel_track():
          self.sel_track(oTrack)
    else:
      self.send_msg(sAddr, 0.0)

  def on_vol(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    nTrackIdxAbs = self.track_idx_abs(nIdx)
    if self.is_track_available(nTrackIdxAbs):
      oTrack = self.get_track(nTrackIdxAbs)
      oTrack.mixer_device.volume.value = nValue
    else:
      self.send_msg(sAddr, 0.0)

  # ********************************************************

  def set_cmd1_visible(self, bVisible):
    sValue = 'true' if bVisible else 'false'
    self.send_msg(
      '/EDIT',
      ['track/cmd1', '{"visible":%s}' % (sValue)])

  def update_sel_track(self):
    nSelTrackIdxAbs = self.sel_track_idx_abs()
    nSelTrackIdxRel = self.state().get_track_idx_rel_or_none(nSelTrackIdxAbs)

    if nSelTrackIdxRel == self.m_nSelTrackIdxRel:
      return # same track! nothing else to do here!

    if self.m_nSelTrackIdxRel != None:
      nIdx = self.m_nSelTrackIdxRel + self.cfg('nTracks') * 5
      self.send_msg('/track/cmd1/%d' % (nIdx), 0.0)
      self.send_msg('/track/cmd2/%d' % (nIdx), 0.0)

    self.m_nSelTrackIdxRel = nSelTrackIdxRel

    if nSelTrackIdxRel != None:
      nIdx = self.m_nSelTrackIdxRel + self.cfg('nTracks') * 5
      self.send_msg('/track/cmd1/%d' % (nIdx), 1.0)
      self.send_msg('/track/cmd2/%d' % (nIdx), 1.0)

  def update_volume(self, poTrack, pnTrackIdxRel):
    nVol = poTrack.mixer_device.volume.value
    self.send_msg('/track/vol/%d' % (pnTrackIdxRel), nVol)

