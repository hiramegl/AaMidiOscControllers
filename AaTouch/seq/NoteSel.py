from AaTouch.Base import Base

class NoteSel(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hNotes = {}
    self.connect()

    phObj['oNoteSel'] = self

    # no need to activate since no notes are selected!

  # ********************************************************

  def connect(self):
    self.reg_idx_cb(
      'seq/note/sel', 12, self.on_note_sel)
    self.reg_cb('seq/note/sel_tog', self.on_toggle)

  def disconnect(self):
    self.deactivate()

  # ********************************************************

  def update(self):
    self.deactivate()
    self.activate()

  def activate(self):
    if len(self.m_hNotes) > 0:
      self.send_msg('/seq/note/sel_tog', 1.0)

    lPitxIdxRel = []
    for nPitxIdxAbs in self.m_hNotes.keys():
      nPitxIdxRel = self.obj('oSeqMap').get_pitx_idx_rel_or_none(nPitxIdxAbs)
      if nPitxIdxRel == None:
        continue # pitch out of scope!
      lPitxIdxRel.append(nPitxIdxRel)

    sAddr   = '/seq/note/sel/%d'
    lBundle = list(map(lambda x: [sAddr % (x), 1.0], lPitxIdxRel))
    self.send_bundle(lBundle)

  def deactivate(self):
    self.send_msg('/seq/note/sel_tog', 0.0)

    # turn off all note buttons
    sAddr   = '/seq/note/sel/%d'
    lBundle = list(map(lambda x: [sAddr % (x), 0.0], range(12)))
    self.send_bundle(lBundle)

  # ********************************************************

  def on_note_sel(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    nPitxIdxAbs = self.obj('oSeqMap').get_pitx_idx_abs(nIdx)
    sNoteName   = self.obj('oScale').get_note_name(nPitxIdxAbs)

    if nValue < 0.5:
      del self.m_hNotes[nPitxIdxAbs]
      if len(self.m_hNotes) == 0:
        self.send_msg('/seq/note/sel_tog', 0)
      self.alert('DEL NOTE: %s [%d]' % (sNoteName, nPitxIdxAbs))

    else:
      self.m_hNotes[nPitxIdxAbs] = True
      self.send_msg('/seq/note/sel_tog', 1)
      self.alert('ADD NOTE: %s [%d]' % (sNoteName, nPitxIdxAbs))

  def on_toggle(self, plSegs, plMsg):
    nValue = int(plMsg[2])

    if nValue < 0.5:
      nValue = 0.0
      self.m_hNotes.clear()
      self.alert('SEL NO NOTES')

    else:
      nValue = 1.0
      for nPitxIdxAbs in range(12 * 8):
        self.m_hNotes[nPitxIdxAbs] = True
      self.alert('SEL ALL NOTES')

    sAddr   = '/seq/note/sel/%d'
    lBundle = list(map(lambda x: [sAddr % (x), nValue], range(12)))
    self.send_bundle(lBundle)

  # ********************************************************

  def get_sel_notes(self):
    return list(self.m_hNotes.keys())

