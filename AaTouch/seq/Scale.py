from AaTouch.Base import Base

class Scale(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hScales = {
      'ION NAT MAJ' : [0, 2, 4, 5,  7,  9, 11, 12, 14, 16, 17, 19],
      'ION NAT MIN' : [0, 2, 3, 5,  7,  8, 10, 12, 14, 15, 17, 19],
      'ION HAR MAJ' : [0, 2, 4, 5,  7,  8, 11, 12, 14, 16, 17, 19],
      'ION HAR MIN' : [0, 2, 3, 5,  7,  8, 11, 12, 14, 15, 17, 19], # (ONLY WHEN GOING UPWARDS)
      'ION MEL MAJ' : [0, 2, 4, 5,  7,  8, 10, 12, 14, 16, 17, 19],
      'ION MEL MIN' : [0, 2, 3, 5,  7,  9, 11, 12, 14, 15, 17, 19], # (ONLY WHEN GOING UPWARDS)

      'DORIAN'      : [0, 2, 3, 5,  7,  9, 10, 12, 14, 15, 17, 19],
      'PHRYGIAN'    : [0, 1, 3, 5,  7,  8, 10, 12, 13, 15, 17, 19],
      'LYDIAN'      : [0, 2, 4, 6,  7,  9, 11, 12, 14, 16, 18, 19],
      'MYXOLYDIAN'  : [0, 2, 4, 5,  7,  9, 10, 12, 14, 16, 17, 19],
      'AEOLIAN'     : [0, 2, 3, 5,  7,  8, 10, 12, 14, 15, 17, 19],
      'LOCRIAN'     : [0, 1, 3, 5,  6,  8, 10, 12, 13, 15, 17, 18],

      'SUPERLOCRIAN': [0, 1, 3, 4,  6,  8, 10, 12, 13, 15, 16, 18],
      'MINOR GIPSY' : [0, 2, 3, 6,  7, 10, 11, 12, 14, 15, 18, 19],
      'MINOR PENTA' : [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24, 27],
      'MAJOR PENTA' : [0, 2, 4, 7,  9, 12, 14, 16, 19, 21, 24, 26],
      'MINOR BLUES' : [0, 3, 5, 6,  7, 10, 12, 15, 17, 18, 19, 22],
      'SPANISH'     : [0, 1, 3, 4,  5,  6,  8, 10, 12, 13, 15, 16],
    }
    self.m_lScaleNames = list(self.m_hScales.keys())

    #                    0    1     2    3     4    5    6     7    8     9    10    11
    self.m_lRoots    = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    self.m_nScaleIdx = -1    # Chromatic scale = -1
    self.m_nRootIdx  = 0     # C by default
    self.m_bTransp   = False # No transpose active

    phObj['oScale']  = self
    self.connect()

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'seq/scale', 18, self.on_scale)
    self.comm().reg_indexed_rx_cb(
      'seq/root', 12, self.on_root)
    self.reg_cb('seq/transp', self.on_transp)

    self.send_msg('/seq/root/0', 1)

  def disconnect(self):
    if self.m_nScaleIdx >= 0:
      self.send_msg('/seq/scale/%d' % (self.m_nScaleIdx), 0)

    self.send_msg('/seq/root/%d' % (self.m_nRootIdx), 0)

    if self.m_bTransp == True:
      self.send_msg('/seq/transp', 0)

  # ********************************************************

  def on_scale(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    if self.mode() != 'MIDI':
      self.send_msg(sAddr, 0)
      self.alert('Scale commands not available for Audio clips')
      return

    if nValue < 0.5: # turning off
      if nIdx == self.m_nScaleIdx: # removing current scale!
        sType = 'CHROMATIC'
        self.m_nScaleIdx = -1

        if self.m_bTransp:
          # turn off transpose since we are changing to
          # Chromatic scale
          self.send_msg('/seq/transp', 0)
          self.m_bTransp = False

    else: # turning on
      sType = self.m_lScaleNames[nIdx]
      if nIdx != self.m_nScaleIdx: # changing current scale!
        # turn off old button ONLY if the current mode
        # is not CHROMATIC!
        if self.m_nScaleIdx >= 0:
          self.send_msg('/seq/scale/%d'% (self.m_nScaleIdx), 0)
        nOldScaleIdx     = self.m_nScaleIdx
        self.m_nScaleIdx = nIdx

        if self.m_bTransp:
          self.transpose(nOldScaleIdx, self.m_nRootIdx)

    self.obj('oNoteSel').update()
    self.obj('oGrid'   ).update()

    if self.m_bTransp:
      self.send_msg('/seq/transp', 0)
      self.m_bTransp = False
    else:
      self.alert('SCALE: %s' % (sType))

  def on_root(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    if self.mode() != 'MIDI':
      self.send_msg(sAddr, 0)
      self.alert('Root commands not available for Audio clips')
      return

    sType = self.m_lRoots[nIdx]
    if nValue < 0.5: # turning off
      if nIdx == self.m_nRootIdx:
        self.send_msg(sAddr, 1) # prevent from turning off root note!

    else: # turning on
      if nIdx == self.m_nRootIdx:
        self.send_msg(sAddr, 1) # prevent from turning off root note!

      else: # changing current root!
        self.send_msg('/seq/root/%d' % (self.m_nRootIdx), 0)
        nOldRootIdx     = self.m_nRootIdx
        self.m_nRootIdx = nIdx # reassign the new root index

        if self.m_bTransp:
          self.transpose(self.m_nScaleIdx, nOldRootIdx)

    self.obj('oNoteSel').update()
    self.obj('oGrid'   ).update()

    if self.m_bTransp:
      self.send_msg('/seq/transp', 0)
      self.m_bTransp = False
    else:
      self.alert('ROOT: %s' % (sType))

  def on_transp(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nValue = plMsg[2]

    if (self.mode() != 'MIDI' or
      self.m_nScaleIdx == -1):
      self.send_msg(sAddr, 0)
      self.alert('Transpose command not available for Audio clips')
      return

    if nValue < 0.5: # turning off
      self.m_bTransp = False
      self.alert('TRANSPOSE OFF')

    else: # turning on
      self.m_bTransp = True
      self.alert('TRANSPOSE ON')

  # ********************************************************

  def transpose(self, pnOldScaleIdx, pnOldRootIdx):
    hVisSpan  = self.obj('oSeqMap').get_visible_span()
    sTimeMode = self.obj('oTimeMode').time_mode()   # BAR, PHRASE
    sHalfSel  = self.obj('oHalfSel' ).half_sel()    # LEFT, RIGHT
    sSection  = self.obj('oSection' ).section()      # 1/2, 1, 2, 4
    nSectLen  = 4.0 if sTimeMode == 'BAR' else 16.0 # time length for one section

    # compute start time and time span to apply command
    nTimeStart = hVisSpan['nTimeStart']
    if sSection == '1' or sSection == '2' or sSection == '4':
      nSectSpan = (nSectLen * int(sSection))
    else: # sSection = '1/2'
      nSectSpan = nSectLen / 2.0
      if sHalfSel == 'RIGHT':
        nTimeStart = nTimeStart + nSectLen / 2.0

    oMidiClip = self.state().midi_clip_or_none()
    lNotes = oMidiClip.get_notes_extended(
      0,          # select from the lowest pitch
      127,        # with all notes span
      nTimeStart, # from time start
      nSectSpan)  # with time span
    lSelNotes = self.obj('oNoteSel').get_sel_notes()

    nTimeEnd = nTimeStart + nSectSpan
    if len(lNotes) == 0:
      self.alert('No notes in [%.2f, %.2f]' % (nTimeStart, nTimeEnd))
      return # nothing else to do here!

    (sOldScale, lOldScale) = self.get_scale(pnOldScaleIdx   , pnOldRootIdx   )
    (sNewScale, lNewScale) = self.get_scale(self.m_nScaleIdx, self.m_nRootIdx)

    nNotesChaged = 0
    for oNote in lNotes:
      nOldPitxAbs = oNote.pitch
      if nOldPitxAbs in lOldScale:
        nNotesChaged  += 1
        nOldPitxAbsIdx = lOldScale.index(nOldPitxAbs)
        nNewPitxAbs    = lNewScale[nOldPitxAbsIdx]
        oNote.pitch    = nNewPitxAbs
        #self.dlog('-> Transposing note id: %3d, pitx: %3d -> %3d' %
        #  (oNote.note_id, nOldPitxAbs, nNewPitxAbs))

    if nNotesChaged == 0:
      self.alert('No notes to transpose')
    else:
      self.state().pause_notes_listener(True)    # prevent updating GUI
      oMidiClip.apply_note_modifications(lNotes) # this will trigger a GUI update
      self.alert('Transposing %d notes, %s -> %s' %
        (nNotesChaged, sOldScale, sNewScale))

  def get_scale(self, pnScaleIdx, pnRootIdx):
    sScale   = self.m_lScaleNames[pnScaleIdx]
    lScale   = self.m_hScales[sScale]
    lOctBase = [] # scale in base octave
    for nPitx in lScale:
      if nPitx < 12:
        lOctBase.append(nPitx)

    # create list with 10 octaves
    lOctScale = []
    for nOct in range(10):
      lOctScale = lOctScale + [(x + (12 * nOct) + pnRootIdx) for x in lOctBase]

    if sScale == 'SPANISH':
      # spanish scale has 8 notes and we remove the
      # first 3 notes so that for octave "1" the notes
      # are aligned with 7-note scales
      del lOctScale[:3]

    return (sScale, lOctScale)

  # ********************************************************

  def get_state(self):
    if self.m_nScaleIdx < 0:
      return ('CHROM', [], -1)

    sScale = self.m_lScaleNames[self.m_nScaleIdx]
    lScale = self.m_hScales[sScale]
    return (sScale, lScale, self.m_nRootIdx)

  def get_note_name(self, pnPitxIdxAbs):
    nOctave  = int(pnPitxIdxAbs / 12) - 2
    nNoteIdx = int(pnPitxIdxAbs % 12)
    sNote    = self.m_lRoots[nNoteIdx]
    return '%d_%s' % (nOctave, sNote)

