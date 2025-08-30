from AaTouch.Base import Base

class SeqMap(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hClipsIdx   = {} # clip indexes hash
    self.m_hCache      = {} # midi areas
    self.m_nTimeOffIdx = 0  # 0, 1
    self.m_nPitxOffIdx = 3  # 0..7
    self.m_nDefaultIdx = 8  # time idx = 0, pitx idx = 3
    self.connect()

    phObj['oSeqMap'] = self

    self.activate()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb(
      'seq/map', 16, self.on_seq_map)

  def disconnect(self):
    self.deactivate()

  # ********************************************************

  def update(self, pbResetSel = False):
    self.deactivate()
    self.activate(pbResetSel)

  def activate(self, pbResetSel = False):
    if self.mode() != 'MIDI':
      return

    oMidiClip = self.state().midi_clip_or_none()
    nClipId   = hash(oMidiClip)

    if pbResetSel and nClipId in self.m_hClipsIdx:
      del self.m_hClipsIdx[nClipId]

    if nClipId in self.m_hClipsIdx:
      nIdx = self.m_hClipsIdx[nClipId]
    else:
      nIdx = self.m_nDefaultIdx
      self.m_hClipsIdx[nClipId] = nIdx

    self.send_msg(
      '/EDIT',
      ['seq/map/%d' % (nIdx), '{"colorFill":"#66cc66"}'])
    self.send_msg(
      '/seq/map/%d' % (nIdx),
      1)

    # update offsets
    (nRow, nCol) = self.get_row_col(nIdx, 2)
    self.m_nTimeOffIdx = nCol     # 0, 1
    self.m_nPitxOffIdx = 7 - nRow # 0..7

    # compute span variables
    nHalfSpan = self.time_span()
    nTimeSpan = nHalfSpan * 2 # 2 time intervals
    hLimits   = self.state().limits_or_none()
    if hLimits['nSpan'] < nTimeSpan:
      nTimeSpan = hLimits['nSpan']
    nTimeStart = hLimits['nStart']

    # read notes and create cache
    lNotes = oMidiClip.get_notes_extended(0, 8 * 12, nTimeStart, nTimeSpan)
    for oNote in lNotes:
      nButIdx = self.get_note_idx(oNote, nTimeStart, nHalfSpan)
      sColor  = '#66cc66' if nButIdx == nIdx else '#cccccc'
      self.m_hCache[nButIdx] = sColor

    # update seq map buttons
    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0:
      return

    sAddr   = 'seq/map/%d'
    sFill   = '{"colorFill":"%s"}'
    lBundle = list(map(lambda x: [
      '/EDIT',
      [sAddr % (x), sFill % (self.m_hCache[x])]],
      lAddrs))
    self.send_bundle(lBundle)

    sAddr   = '/seq/map/%d'
    lBundle = list(map(lambda x: [
      sAddr % (x),
      1.0],
      lAddrs))
    self.send_bundle(lBundle)

  def deactivate(self):
    self.m_hCache.clear()

    sAddr = 'seq/map/%d'
    sFill   = '{"colorFill":"#6db5fd"}'
    lBundle = list(map(lambda x: [
      '/EDIT',
      [sAddr % (x), sFill]],
      range(2 * 8)))
    self.send_bundle(lBundle)

    sAddr = '/seq/map/%d'
    lBundle = list(map(lambda x: [
      sAddr % (x),
      0.0],
      range(2 * 8)))
    self.send_bundle(lBundle)

  # ********************************************************

  def on_seq_map(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[3])
    nValue = int(plMsg[2])

    if self.state().midi_clip_or_none() == None:
      self.send_msg(sAddr, 0) # prevent from toggling on
      return

    if nValue < 0.5:
      self.send_msg(sAddr, 1) # prevent from toggling off

    nCurrIdx = self.get_idx()
    if nIdx == nCurrIdx:
      return # turning on same index, nothing to do here!

    # check if selected interval is valid
    (nRow, nCol) = self.get_row_col(nIdx, 2)
    nTimeOffIdx = nCol     # 0, 1
    nPitxOffIdx = 7 - nRow # 0..7
    if nCol == 1:
      nTimeOff = nCol * self.time_span()
      hLimits  = self.state().limits_or_none()
      if nTimeOff >= hLimits['nClipEnd']:
        self.send_msg(sAddr, 0) # turn unavailable interval off
        self.alert('UNAVAILABLE INTERVAL!')
        return # nothing else to do here

    sColor = '#cccccc' if nCurrIdx in self.m_hCache else '#6db5fd'
    self.send_msg(
      '/EDIT',
      ['seq/map/%d' % nCurrIdx, '{"colorFill":"%s"}' % (sColor)])
    self.send_msg(
      '/EDIT',
      ['seq/map/%d' % nIdx    , '{"colorFill":"#66cc66"}'])

    oMidiClip = self.state().midi_clip_or_none()
    nClipId   = hash(oMidiClip)
    self.m_hClipsIdx[nClipId] = nIdx

    nValue = 1 if nCurrIdx in self.m_hCache else 0
    self.send_msg('/seq/map/%d' % (nCurrIdx), nValue)
    self.m_nTimeOffIdx = nTimeOffIdx
    self.m_nPitxOffIdx = nPitxOffIdx
    self.obj('oGrid'   ).update()
    self.obj('oBitOp'  ).update()
    self.obj('oNoteSel').update()

    sMode = self.time_mode()
    self.alert('TIME: %d [%s], OCTAVE: %d' %
      (self.m_nTimeOffIdx * 2, sMode, self.m_nPitxOffIdx - 2))

  # ********************************************************

  def get_note_idx(self, poNote, pnTimeStart, pnHalfSpan):
    nTimeRel = poNote.start_time - pnTimeStart
    nTimeIdx = int(nTimeRel / pnHalfSpan)
    nPitxIdx = 7 - int(poNote.pitch / 12)
    return nPitxIdx * 2 + nTimeIdx

  def get_time_off_abs(self):
    return self.get_visible_span()['nTimeStart']

  def get_pitx_off_abs(self):
    (sScale, lScale, nRoot) = self.obj('oScale').get_state()
    if sScale == 'CHROM':
      return self.m_nPitxOffIdx * 12
    return self.m_nPitxOffIdx * 12 + nRoot

  def get_pitx_span_abs(self):
    (sScale, lScale, nRoot) = self.obj('oScale').get_state()
    if sScale == 'CHROM':
      return 12
    return lScale[11] + 1

  # pnPitxIdxRel: [0 .. 11]
  def get_pitx_idx_abs(self, pnPitxIdxRel):
    (sScale, lScale, nRoot) = self.obj('oScale').get_state()
    if sScale == 'CHROM':
      return self.m_nPitxOffIdx * 12 + (11 - pnPitxIdxRel)

    nPitxIdxAbs  = self.m_nPitxOffIdx * 12
    nPitxIdxAbs += nRoot
    nPitxIdxAbs += lScale[11 - pnPitxIdxRel]
    return nPitxIdxAbs

  # pnPitxIdxAbs: [0 .. 127]
  def get_pitx_idx_rel_or_none(self, pnPitxIdxAbs):
    (sScale, lScale, nRoot) = self.obj('oScale').get_state()
    if sScale == 'CHROM':
      nPitxIdxRel = 11 - (pnPitxIdxAbs - self.m_nPitxOffIdx * 12)
      if nPitxIdxRel < 0 or nPitxIdxRel > 11:
        return None
    else:
      nPitxIdxRel  = pnPitxIdxAbs
      nPitxIdxRel -= nRoot
      nPitxIdxRel -= self.m_nPitxOffIdx * 12
      if (nPitxIdxRel in lScale) == False:
        return None
      nPitxIdxRel = 11 - lScale.index(nPitxIdxRel)

    return nPitxIdxRel

  def get_visible_span(self):
    # 1 bar    = 4  beats, 2 bars    = 8 beats  (4 grids)
    # 1 phrase = 16 beats, 2 phrases = 32 beats (16 grids)
    nTimeSpan  = self.time_span() # number of visible beats
    nStart     = self.m_nTimeOffIdx * nTimeSpan
    hLimits    = self.state().limits_or_none()
    nTimeStart = hLimits['nStart'] + nStart # start from loop start if looping or clip start if no-looping
    nTimeEndMx = max(hLimits['nEnd'], hLimits['nClipEnd']) # maximum time end
    if nTimeStart + nTimeSpan > nTimeEndMx:
      nTimeSpan = nTimeEndMx - nTimeStart

    nPitxStart = self.get_pitx_off_abs()
    nPitxSpan  = self.get_pitx_span_abs()
    #self.log('-> Visible span: (%d, %d | %d, %d)' % (nPitxStart, nPitxSpan, nTimeStart, nTimeSpan))

    return {
      'nPitxStart': nPitxStart,
      'nPitxSpan' : nPitxSpan,
      'nTimeStart': nTimeStart, # start time considering loop/clip start offset and zoom offset
      'nTimeSpan' : nTimeSpan,
    }

  # ********************************************************

  def time_mode(self):
    return self.obj('oTimeMode').time_mode()

  def time_span(self):
    return self.obj('oTimeMode').time_span()

  def get_idx(self):
    return (7 - self.m_nPitxOffIdx) * 2 + self.m_nTimeOffIdx

