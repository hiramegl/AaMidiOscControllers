import Live

from AaTouch.Base import Base

class Grid(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_hCache = {} # bit addresses cache

    phObj['oGrid'] = self

  # ********************************************************

  def update(self):
    self.deactivate()
    self.activate()

  def activate(self):
    oMidiClip = self.midi_clip()
    if oMidiClip == None:
      return # nothing else to do here

    hNotesState = self.get_notes_state(oMidiClip)

    for oNote in hNotesState['lVisNotes']: # all notes in the list are visible!
      self.cache_note(oNote, hNotesState)

    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0:
      return # no notes to show for this span!

    lBundle = list(map(lambda x: [
      '/seq/grid/%s' % (x),
      1.0],
      lAddrs))
    self.send_bundle(lBundle)

  def deactivate(self):
    lAddrs = self.m_hCache.keys()
    if len(lAddrs) == 0:
      return # nothing else to do here

    lBundle = list(map(lambda x: [
      '/seq/grid/%s' % (x),
      0.0],
      lAddrs))
    self.send_bundle(lBundle)
    self.m_hCache.clear()

  # ********************************************************

  def on_clip_notes_changed(self):
    oMidiClip   = self.midi_clip()
    hNotesState = self.get_notes_state(oMidiClip)
    hNotesById  = self.get_notes_by_id()

    lBitsToAdd = []
    # compare cached visible notes with notes in Ableton Live roll
    for oNote in hNotesState['lVisNotes']: # all notes in the list are visible!
      if oNote.note_id in hNotesById:
        sOldAddr = hNotesById[oNote.note_id]
        sNewAddr = self.get_addr_from_note(oNote, hNotesState)

        if sNewAddr == None:
          # not visible with current scale and root
          # we keep the note in hNotesById in order to be removed
          # in the next step!
          pass

        elif sOldAddr == sNewAddr:
          # remove it from hNotesById since the note exists in roll
          # and has the same time start and pitch; this note will
          # not be removed in the next step!
          del hNotesById[oNote.note_id]

        else:
          # the note has not the same address, it has been moved in Ableton Live!
          # add the note to the cache again and to the list of bits to add
          sAddr = self.cache_note(oNote, hNotesState)
          if sAddr != None:
            lBitsToAdd.append(sAddr) # visible with current scale and root

          # we keep the note in hNotesById in order to be removed
          # in the next step!

      else:
        # the note does not exist in the cache!
        # cache it and add it to list of bit addresses to turn on
        sAddr = self.cache_note(oNote, hNotesState)
        if sAddr != None:
          lBitsToAdd.append(sAddr) # visible with current scale and root

    # find out which notes remain in hNotesById, those notes
    # do not exist any longer in Ableton Live roll and need
    # to be removed from the GUI
    lBitsToDel = []
    for nNoteId in hNotesById:
      sAddr = hNotesById[nNoteId]
      self.m_hCache[sAddr].remove(nNoteId) # remove the note from the cache
      if len(self.m_hCache[sAddr]) == 0:   # if there are no more notes for that bit address
        del self.m_hCache[sAddr]           # then remove entry from cache
        lBitsToDel.append(sAddr)           # and add it to list of bit addresses to del

    lBitsToDel = list(set(lBitsToDel)) # unique bit addresses to del
    if len(lBitsToDel) > 0:
      lBundle = list(map(lambda x: ['/seq/grid/%s' % (x), 0.0], lBitsToDel))
      self.send_bundle(lBundle)
      #self.dlog('> del notes: %s' % (str(lBitsToDel)))

    lBitsToAdd = list(set(lBitsToAdd)) # unique bit addresses to add
    if len(lBitsToAdd) > 0:
      lBundle = list(map(lambda x: ['/seq/grid/%s' % (x), 1.0], lBitsToAdd))
      self.send_bundle(lBundle)
      #self.dlog('> add notes: %s' % (str(lBitsToAdd)))

    # notes have changed, update the sequencer map!
    self.seq_map().update()

  # ********************************************************

  def on_bit(self, pnGridIdx, pnBitIdx, pnValue):
    nTimeIdxRel =     pnBitIdx % 8
    nPitxIdxRel = int(pnBitIdx / 8) # int [0 .. 11]
    #self.dlog('-> grid %d, time %d, note rel %d, val %d' %
    #  (pnGridIdx, nTimeIdxRel, nPitxIdxRel, pnValue))

    sAddr     = '%s/%s' % (pnGridIdx, pnBitIdx)
    oMidiClip = self.midi_clip()

    if pnValue < 0.5: # remove note
      for nNoteId in self.m_hCache[sAddr]:
        oMidiClip.remove_notes_by_id([nNoteId])
      del self.m_hCache[sAddr]

    else: # add note
      sTimeMode = self.obj('oTimeMode').time_mode()
      nTimeFact = 0.25 if sTimeMode == 'BAR' else 1   # beats
      nGridSpan = 2.0  if sTimeMode == 'BAR' else 8.0 # beats
      nTimeOff  = self.seq_map().get_time_off_abs()   # offset due to the zoom section and loop start
      nTimeAbs  = nTimeIdxRel * nTimeFact + (pnGridIdx * nGridSpan) + nTimeOff
      nPitxAbs  = self.seq_map().get_pitx_idx_abs(nPitxIdxRel)
      nDuration = self.obj('oLenVel').get_attr('LEN')
      nVelocity = self.obj('oLenVel').get_attr('VEL')

      (sScale, lScale, nRoot) = self.obj('oScale').get_state()
      sChordMode = self.obj('oChord').get_mode()
      if (sScale == 'CHROM' or sChordMode == 'NONE'):
        self.add_note(nPitxAbs, nTimeAbs, nDuration, nVelocity)

      else:
        lPitxOff = [] # pitch offset (absolute)
        lOctBase = [] # scale in base octave
        for nPitx in lScale:
          if nPitx < 12:
            lOctBase.append(nPitx)
        nNumNotes = len(lOctBase)                 # number of notes in one base octave
        nRootBase = lScale[11 - nPitxIdxRel] % 12 # root note inside base octave
        lOctDown  = [x - 12 for x in lOctBase]
        lOctUp    = [x + 12 for x in lOctBase]
        lOctaves  = lOctDown + lOctBase + lOctUp
        nRootIdx  = lOctaves.index(nRootBase)     # index of the root node inside octaves list

        #   0   1   2   3   4   5   6
        #[-12,-10, -8, -7, -5, -3, -1]
        #[  0,  2,  4,  5,  7,  9, 11] -> len = 7 (base octave)
        #[ 12, 14, 16, 17, 19, 21, 23]
        # Pressing 17 (index 3 & pitch 5 base octave)
        #            Pitch Abs    ->  Pitch Offsets
        # Triad    : 5, 9, 12     ->  0,  4,  7
        # 1st Inv  : 0, 5, 9      -> -5,  0,  4
        # 2nd Inv  : 0, 4, 5      -> -5, -1,  0
        # Augmented: 5, 9, 12, 16 ->  0,  4,  7, 11
        # Power 5th: 5, 12, 17    ->  0,  7, 12
        if   sChordMode == 'TRIAD':
          lPitxOff.append(lOctaves[nRootIdx + 0] - nRootBase) # should be zero
          lPitxOff.append(lOctaves[nRootIdx + 2] - nRootBase)
          lPitxOff.append(lOctaves[nRootIdx + 4] - nRootBase)

        elif sChordMode == '1ST INV':
          lPitxOff.append(lOctaves[nRootIdx + 0            ] - nRootBase) # should be zero
          lPitxOff.append(lOctaves[nRootIdx + 2            ] - nRootBase)
          lPitxOff.append(lOctaves[nRootIdx + 4 - nNumNotes] - nRootBase)

        elif sChordMode == '2ND INV':
          lPitxOff.append(lOctaves[nRootIdx + 0            ] - nRootBase) # should be zero
          lPitxOff.append(lOctaves[nRootIdx + 2 - nNumNotes] - nRootBase)
          lPitxOff.append(lOctaves[nRootIdx + 4 - nNumNotes] - nRootBase)

        elif sChordMode == 'AUGMENTED':
          lPitxOff.append(lOctaves[nRootIdx + 0] - nRootBase) # should be zero
          lPitxOff.append(lOctaves[nRootIdx + 2] - nRootBase)
          lPitxOff.append(lOctaves[nRootIdx + 4] - nRootBase)
          lPitxOff.append(lOctaves[nRootIdx + 6] - nRootBase)

        elif sChordMode == 'POWER 5TH':
          lPitxOff.append(lOctaves[nRootIdx + 0] - nRootBase) # should be zero
          lPitxOff.append(lOctaves[nRootIdx + 4] - nRootBase)
          lPitxOff.append(lOctaves[nRootIdx + 7] - nRootBase)

        for nPitxOff in lPitxOff:
          nPitx = nPitxAbs + nPitxOff
          if nPitx < 0: continue # invalid note pitch

          # the pitch is valid, add the note!
          sAddr = self.add_note(nPitx, nTimeAbs, nDuration, nVelocity)

          if sAddr == None: continue # non-visible pitch
          if nPitxOff == 0: continue # the root note is already displayed in GUI

          # the note is visible, turn the grid-bit on since is not the root note!
          self.send_msg('/seq/grid/%s' % (sAddr), 1)

    self.seq_map().update()
    #self.log('-> Notes in cache: %d' % (len(self.m_hCache)))

  def add_note(self, pnPitxAbs, pnTimeAbs, pnDuration, pnVelocity):
    oNote = Live.Clip.MidiNoteSpecification(
      pitch      = pnPitxAbs,
      start_time = pnTimeAbs,
      duration   = pnDuration,
      velocity   = pnVelocity)
    oMidiClip = self.midi_clip()
    oMidiClip.add_new_notes(tuple([oNote]))

    # add note to the cache
    lNotes = oMidiClip.get_notes_extended(pnPitxAbs, 1, pnTimeAbs, pnDuration)
    #self.dlog('-> note id: %d, time abs: %f, pitx abs: %d' %
    #  (lNotes[0].note_id, pnTimeAbs, pnPitxAbs))

    hNotesState = self.get_notes_state(oMidiClip)
    sAddr       = self.get_addr_from_note(lNotes[0], hNotesState)

    if sAddr != None:
      if sAddr in self.m_hCache:
        self.m_hCache[sAddr].append(lNotes[0].note_id)
      else:
        self.m_hCache[sAddr] = [lNotes[0].note_id]

    return sAddr

  # ********************************************************

  def get_notes_state(self, poMidiClip):
    hVisSpan = self.seq_map().get_visible_span()
    lVisNotes = poMidiClip.get_notes_extended(
      hVisSpan['nPitxStart'],
      hVisSpan['nPitxSpan'],
      hVisSpan['nTimeStart'],
      hVisSpan['nTimeSpan'])
    nTimeFact = self.obj('oTimeMode').time_factor()
    return {
      'lVisNotes': lVisNotes,
      'hVisSpan' : hVisSpan,
      'nTimeFact': nTimeFact,
    }

  def get_notes_by_id(self):
    # convert hash {sAddr: [id1, id2]} to hash {id1: sAddr, id2: sAddr}
    hNotesById = dict([
      tIdNotePair
      for lPairs in
      list(map(
        lambda sAddr: [(nId, sAddr) for nId in self.m_hCache[sAddr]],
        self.m_hCache))
      for tIdNotePair in lPairs])

    return hNotesById

  def cache_note(self, poNote, phNotesState):
    sAddr = self.get_addr_from_note(poNote, phNotesState)

    if sAddr == None:
      # Do not cache the note! Even though it exists in Ableton's roll
      # it is not visible with the current scale and root
      return None

    elif sAddr in self.m_hCache:
      self.m_hCache[sAddr].append(poNote.note_id)

    else:
      self.m_hCache[sAddr] = [poNote.note_id]

    return sAddr

  def get_addr_from_note(self, poNote, phNotesState):
    #self.log('-> Note, id: %d, time: %2.3f, pitx: %d, duration: %2.3f, vel: %d, mute: %d' %
    #  (poNote.note_id, poNote.start_time, poNote.pitch, poNote.duration, poNote.velocity, poNote.mute))

    # compute time index
    nNoteTimeRel  = poNote.start_time
    nNoteTimeRel -= phNotesState['hVisSpan']['nTimeStart'] # remove loop/clip start
    nNoteTimeRel *= phNotesState['nTimeFact']              # from time to scaled time (due to time mode) [float]
    nTimeIdxRel   = int(nNoteTimeRel)                      # scaled time that needs to be converted to bit index

    nPitxIdxRel   = self.seq_map().get_pitx_idx_rel_or_none(poNote.pitch)

    if nPitxIdxRel == None:
      self.dlog('-> Note NOT VISIBLE with current scale and root')
      return None # not visible with current scale and root

    return self.get_addr_from_time_pitx(nTimeIdxRel, nPitxIdxRel)

  # ********************************************************

  def get_addr_from_time_pitx(self, pnTimeIdxRel, pnPitxIdxRel):
    (nGridIdx, nBitIdx) = self.get_grid_bit(pnTimeIdxRel, pnPitxIdxRel)
    return '%d/%d' % (nGridIdx, nBitIdx)

  def get_grid_bit(self, pnTimeIdxRel, pnPitxIdxRel):
    nGridIdx = int(pnTimeIdxRel / 8)
    nBitIdx  = (pnPitxIdxRel * 8) + (pnTimeIdxRel % 8)
    return (nGridIdx, nBitIdx)

  # ********************************************************

  def seq_map(self):
    return self.obj('oSeqMap')

  def midi_clip(self):
    return self.state().midi_clip_or_none()

