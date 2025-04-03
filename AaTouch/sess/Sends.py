from AaTouch.Base import Base

class Sends(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hCache = {} # grid cache
    self.connect()

    phObj['oSends'] = self

  # ********************************************************

  def connect(self):
    self.reg_idx_cb(
      'session/sends',
      self.cfg('nTracks') * self.cfg('nReturns'),
      self.on_sends)
    # it will be activated on 'refresh_state' instead

  def disconnect(self):
    self.deactivate() # turn off buttons

  # ********************************************************

  def update(self):
    self.deactivate()
    self.activate()

  def activate(self):
    for nTrackIdxRel in range(self.cfg('nTracks')):
      nTrackIdxAbs = self.track_idx_abs(nTrackIdxRel)
      if self.is_track_available(nTrackIdxAbs) == False:
        break # no more tracks to scan
      oTrack = self.get_track(nTrackIdxAbs)
      lSends = oTrack.mixer_device.sends
      for nSendIdx in range(self.cfg('nReturns')):
        oSend = lSends[nSendIdx]
        if oSend.value > 0.5:
          nCellId = nSendIdx * self.cfg('nTracks') + nTrackIdxRel
          self.m_hCache[nCellId] = True

    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0: return

    sAddr   = '/session/sends/%d'
    lBundle = list(map(lambda x: [
      sAddr % (x),
      1.0],
      lAddrs))
    self.send_bundle(lBundle)

  def deactivate(self):
    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0: return

    sAddr   = '/session/sends/%d'
    lBundle = list(map(lambda x: [
      sAddr % (x),
      0.0],
      lAddrs))
    self.send_bundle(lBundle)

    self.m_hCache.clear()

  # ********************************************************

  def on_sends(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    (nSndIdx, nTrkIdx) = self.get_row_col(nIdx, self.cfg('nTracks'))
    nTrackIdxAbs = self.state().get_track_idx_abs(nTrkIdx)
    if self.is_track_available(nTrackIdxAbs) == False:
      self.send_msg(sAddr, 0) # prevent from turning on
      return

    oTrack = self.get_track(nTrackIdxAbs)
    oSend  = oTrack.mixer_device.sends[nSndIdx]
    oSend.value = nValue

    if nValue > 0.5:
      self.m_hCache[nIdx] = True
    else:
      del self.m_hCache[nIdx]

  def update_track_send(self, pnTrackIdxRel, poTrack, pnSendIdx):
    oSend = poTrack.mixer_device.sends[pnSendIdx]
    nSend = 1.0 if oSend.value > 0.5 else 0.0
    nIdx  = pnSendIdx * self.cfg('nTracks') + pnTrackIdxRel
    self.send_msg(
      '/session/sends/%d' % (nIdx),
      nSend)

    if nSend > 0.5:
      self.m_hCache[nIdx] = True
    else:
      if nIdx in self.m_hCache:
        del self.m_hCache[nIdx]

