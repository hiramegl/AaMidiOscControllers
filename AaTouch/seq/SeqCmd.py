import Live

from AaTouch.Base import Base

class SeqCmd(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.connect()

    phObj['oSeqCmd'] = self

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'seq/bit/shift', 4 * 2, self.on_shift)
    self.comm().reg_indexed_rx_cb(
      'seq/bit/fact_chop', 4 * 2, self.on_fact_chop)
    self.comm().reg_indexed_rx_cb(
      'seq/bit/cmd', 4 * 2, self.on_cmd)

  # ********************************************************

  def on_shift(self, plSegs, plMsg):
    if self.mode() != 'MIDI':
      self.alert('Shift commands not available for Audio clips')
      return

    nButIdx = int(plSegs[4])
    (sType, sCmd) = self.get_row_col(
      nButIdx, 4, ['ALL' , 'SEL'], ['LEFT', 'RIGHT', 'DOWN', 'UP'])
    self.operate_notes(sType, sCmd)

  def on_fact_chop(self, plSegs, plMsg):
    if self.mode() != 'MIDI':
      self.alert('Factor/Chop commands not available for Audio clips')
      return
    nButIdx = int(plSegs[4])
    (sType, sCmd) = self.get_row_col(
      nButIdx, 4, ['ALL' , 'SEL'], ['MUL', 'DIV', 'CHOP2', 'CHOP3'])
    self.operate_notes(sType, sCmd)

  def on_cmd(self, plSegs, plMsg):
    if self.mode() != 'MIDI':
      self.alert('MIDI commands not available for Audio clips')
      return
    nButIdx = int(plSegs[4])
    (sType, sCmd) = self.get_row_col(
      nButIdx, 4, ['ALL' , 'SEL'], ['MUTE', 'SOLO', 'VEL_RST', 'DEL'])
    self.operate_notes(sType, sCmd)

  # ********************************************************

  def operate_notes(self, psType, psCmd):
    hVisSpan  = self.obj('oSeqMap').get_visible_span()
    sTimeMode = self.obj('oTimeMode').time_mode()   # 'BAR', 'PHRASE'
    sHalfSel  = self.obj('oHalfSel' ).half_sel()    # 'LEFT', 'RIGHT'
    sSection  = self.obj('oSection' ).section()     # '1/2', '1', '2', '4'
    nSectLen  = 4.0 if sTimeMode == 'BAR' else 16.0 # time length for one section

    # compute start time and time span to apply command
    nTimeStart = hVisSpan['nTimeStart']
    if sSection == '2' or sSection == '4':
      nSectSpan = (nSectLen * int(sSection))
    elif sSection == '1':
      nSectSpan = nSectLen
      if sHalfSel == 'RIGHT':
        nTimeStart = nTimeStart + nSectLen
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
    nCount   = 0
    if psType == 'ALL': # operate all notes
      sErrMsg = 'No notes in [%.2f, %.2f]' % (nTimeStart, nTimeEnd)
      nCount  = len(lNotes)

    else: # psType = 'SEL' operate only in selected notes
      sErrMsg   = 'No selected notes in [%.2f, %.2f]' % (nTimeStart, nTimeEnd)
      for oNote in lNotes:
        if oNote.pitch in lSelNotes:
          nCount += 1

    if nCount == 0:
      self.alert(sErrMsg)
      return # nothing else to do here

    nVel      = self.obj('oLenVel'  ).get_attr('VEL')
    nBitTime  = self.obj('oTimeMode').bit_time()
    lAddNotes = []
    lDelNotes = []
    for oNote in lNotes:
      # apply in SELECTED notes
      if psType == 'ALL' or (oNote.pitch in lSelNotes):
        if   psCmd == 'LEFT':
          nTime = oNote.start_time - nBitTime
          if nTime < nTimeStart: # wrap around to the end of section
            nTime = nTimeEnd - (nTimeStart - nTime)
          oNote.start_time = nTime
        elif psCmd == 'RIGHT':
          nTime = oNote.start_time + nBitTime
          if nTime == nTimeEnd: # wrap around to the start of section
            nTime = nTimeStart
          elif nTime > nTimeEnd: # wrap around to the start of section
            nTime = nTimeStart + (nTime - nTimeEnd)
          oNote.start_time = nTime
        elif psCmd == 'DOWN':
          if oNote.pitch > 0:
            oNote.pitch = oNote.pitch - 1
        elif psCmd == 'UP':
          if oNote.pitch < 127:
            oNote.pitch = oNote.pitch + 1

        elif psCmd == 'MUL':
          oNote.duration = (oNote.duration * 2.0)
        elif psCmd == 'DIV':
          oNote.duration = (oNote.duration / 2.0)
        elif psCmd == 'CHOP2':
          nDuration      = oNote.duration / 2.0
          oNote.duration = nDuration
          lAddNotes.append(Live.Clip.MidiNoteSpecification(
            pitch      = oNote.pitch,
            start_time = oNote.start_time + nDuration,
            duration   = nDuration,
            velocity   = oNote.velocity))
        elif psCmd == 'CHOP3':
          nDuration      = oNote.duration / 3.0
          oNote.duration = nDuration
          lAddNotes.append(Live.Clip.MidiNoteSpecification(
            pitch      = oNote.pitch,
            start_time = oNote.start_time + nDuration,
            duration   = nDuration,
            velocity   = oNote.velocity))
          lAddNotes.append(Live.Clip.MidiNoteSpecification(
            pitch      = oNote.pitch,
            start_time = oNote.start_time + nDuration * 2,
            duration   = nDuration,
            velocity   = oNote.velocity))

        elif psCmd == 'MUTE':
          oNote.mute = not oNote.mute
        elif psCmd == 'VEL_RST':
          oNote.velocity = nVel
        elif psCmd == 'DEL':
          lDelNotes.append(oNote.note_id)

      # apply in UNSELECTED notes
      if (psCmd == 'SOLO' and
        psType  == 'SEL' and
        ((oNote.pitch in lSelNotes) == False)):
        oNote.mute = not oNote.mute

    # apply note modifications!
    if (psCmd == 'LEFT'  or
      psCmd   == 'RIGHT' or
      psCmd   == 'DOWN'  or
      psCmd   == 'UP'    or
      psCmd   == 'MUL'):
      oMidiClip.apply_note_modifications(lNotes) # this will trigger a GUI update

    elif (psCmd == 'CHOP2' or
      psCmd     == 'CHOP3'):
      oMidiClip.apply_note_modifications(lNotes) # update new note durations
      oMidiClip.add_new_notes(tuple(lAddNotes))  # this will trigger a GUI update

    elif psCmd == 'DEL':
      oMidiClip.remove_notes_by_id(lDelNotes) # this will trigger a GUI update

    else:
      # for DIV, MUTE, UNMUTE, VEL_RST we do not need to
      # update the grid!
      self.state().pause_notes_listener(True) # prevent updating GUI
      oMidiClip.apply_note_modifications(lNotes)

    self.alert('> (%d) %s NOTES: %s' % (nCount, psType, psCmd))

