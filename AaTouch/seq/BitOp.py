import Live

from AaTouch.Base import Base

class BitOp(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_nBits = 0
    self.connect()

    phObj['oBitOp'] = self

    self.activate()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb('seq/bit/op' , 32   , self.on_bit_op)
    self.reg_idx_cb('seq/bit/enc', 32   , self.on_bit_enc)
    self.reg_cb    ('seq/bit/enc_master', self.on_bit_enc_master)

  def disconnect(self):
    self.deactivate()

  # ********************************************************

  def update(self):
    self.deactivate()
    self.activate()

  # PARAM \ MODE    |    BAR     |   PHRASE   |
  # TimeMode: bit   | 0.25 beats |  1.0 beat  |
  # SeqMap  : off   |  0|8 beats | 0|32 beats |
  # BitsLen : len   |    8 beats |   32 beats |
  #
  # track:       |<----------------------------------->|
  # visible:           |<---------------------->|
  # loop:              |<--------------->|
  # sel section:       |<-------->|
  #
  # COLORS:
  # sel half:          |<-->|                             # selected half
  # unsel half:              |<-->|                       # unselected half
  # inside:                        |<--->|                # inside  (loop scope)
  # outside:                             |<----------->|  # outside (loop scope)
  # offset 1:    |---->|                                  # when seq map has time index 0
  # offset 2:    |----------------------------->|         # when seq map has time index 1

  def activate(self):
    oMidiClip = self.state().get_midi_clip_or_none()
    if oMidiClip == None:
      return

    hLimits  = self.state().limits_or_none()
    nBitTime = self.obj('oTimeMode').bit_time()         # in beats (0.25 or 1.0)
    nTimeOff = self.obj('oSeqMap'  ).get_time_off_abs() # in beats
    sHalfSel = self.obj('oHalfSel' ).half_sel()         # 'LEFT', 'RIGHT'
    sSection = self.obj('oSection' ).section()          # '1/2', '1', '2', '4'

    nSectLen = nBitTime * 16.0                          # one section length (in beats)
    nSectFac = 1.0 if sSection == '1/2' else 2.0        # section factor
    nSectEnd = nTimeOff + (nSectFac * nSectLen)         # section end

    nHalfLen = nBitTime * 8.0 * nSectFac                # half section length
    nHalfSta = nTimeOff + (0.0      if sHalfSel == 'LEFT' else nHalfLen)
    nHalfEnd = nTimeOff + (nHalfLen if sHalfSel == 'LEFT' else nSectEnd)

    sSelClr = '#99ff99' # selected half color
    sUnsClr = '#669966' # unselected half color
    sInClr  = '#6666cc' # inside  (loop scope)
    sOutClr = '#999999' # outside (loop scope)
    sRstClr = '#6db5fd' # reset color
    lBitVal = []        # bit values
    lBitClr = []        # bit colors

    for nBit in range(32):
      nTime = nTimeOff + nBit * nBitTime

      if nTime >= hLimits['nClipEnd']:
        # bits outside clip length
        lBitVal.append([nBit, 0])
        lBitClr.append([nBit, sRstClr])

      elif nTime >= hLimits['nEnd']:
        # bits outside loop length
        lBitVal.append([nBit, 1])
        lBitClr.append([nBit, sOutClr])

      else:
        if sSection == '4' or sSection == '2':
          # bits in a 2 or 4 section (bar/phrase) are
          # always selected
          lBitVal.append([nBit, 1])
          lBitClr.append([nBit, sSelClr])

        elif sSection == '1' or sSection == '1/2':
          # it is possible that there are bits inside the
          # loop but outside the section
          if nTime >= nSectEnd:
            # outside section but inside selected
            # visible span
            if nTime >= hLimits['nEnd']:
              # outside loop length
              lBitVal.append([nBit, 1])
              lBitClr.append([nBit, sOutClr])
            else:
              # inside loop length
              lBitVal.append([nBit, 1])
              lBitClr.append([nBit, sInClr])

          else:
            # select only bits inside the selected half section
            if nTime >= nHalfSta and nTime < nHalfEnd:
              lBitVal.append([nBit, 1])
              lBitClr.append([nBit, sSelClr])
            else:
              lBitVal.append([nBit, 1])
              lBitClr.append([nBit, sUnsClr])

    sAddr   = '/seq/bit/op/%d'
    lBundle = list(map(lambda x: [sAddr % (x[0]), x[1]], lBitVal))
    self.send_bundle(lBundle)

    sAddr   = 'seq/bit/op/%d'
    sFill   = '{"colorFill":"%s"}'
    lBundle = list(map(lambda x: ['/EDIT', [sAddr % (x[0]), sFill % (x[1])]], lBitClr))
    self.send_bundle(lBundle)

    sAddr   = '/seq/bit/enc/%d'
    lBundle = list(map(lambda x: [sAddr % (x), 0.5], range(32)))
    self.send_bundle(lBundle)

    self.send_msg('/seq/bit/enc_master', 0.5)

  def deactivate(self):
    sAddr   = 'seq/bit/op/%d'
    sFill   = '{"colorFill":"#6db5fd"}'
    lBundle = list(map(lambda x: ['/EDIT', [sAddr % (x), sFill]], range(32)))
    self.send_bundle(lBundle)

    sAddr   = '/seq/bit/op/%d'
    lBundle = list(map(lambda x: [sAddr % (x), 0], range(32)))
    self.send_bundle(lBundle)

    sAddr   = '/seq/bit/enc/%d'
    lBundle = list(map(lambda x: [sAddr % (x), 0.0], range(32)))
    self.send_bundle(lBundle)

    self.send_msg('/seq/bit/enc_master', 0.0)

  # ********************************************************

  def on_bit_op(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    if nValue < 0.5:
      self.send_msg(sAddr, 1) # prevent from turning on
    else:
      self.send_msg(sAddr, 0) # prevent from turning off

    (bContinue, lNotes, lSelNotes, nBitStart) = self.filter_notes(nIdx)
    if bContinue == False: return

    sSelOp    = self.obj('oBitOpSel').get_but_sel_op()
    lAddNotes = []
    for oNote in lNotes:
      if oNote.pitch in lSelNotes:
        if   sSelOp == 'MUL':
          oNote.duration = (oNote.duration * 2.0)
        elif sSelOp == 'DIV':
          oNote.duration = (oNote.duration / 2.0)
        elif sSelOp == 'CHOP2':
          nDuration      = oNote.duration / 2.0
          oNote.duration = nDuration
          lAddNotes.append(Live.Clip.MidiNoteSpecification(
            pitch      = oNote.pitch,
            start_time = oNote.start_time + nDuration,
            duration   = nDuration,
            velocity   = oNote.velocity))
        elif sSelOp == 'CHOP3':
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

    # apply note modifications!
    oMidiClip = self.state().midi_clip_or_none()
    if sSelOp == 'MUL':
      oMidiClip.apply_note_modifications(lNotes) # this will trigger a GUI update

    elif (sSelOp == 'CHOP2' or
      sSelOp     == 'CHOP3'):
      oMidiClip.apply_note_modifications(lNotes) # update new note durations
      oMidiClip.add_new_notes(tuple(lAddNotes))  # this will trigger a GUI update

    else:
      # for DIV we do not need to update the grid!
      self.state().pause_notes_listener(True) # prevent updating GUI
      oMidiClip.apply_note_modifications(lNotes)

    self.alert('> (%d) SEL NOTES: %s' % (nCount, sSelOp))

  def on_bit_enc(self, plSegs, plMsg):
    nIdx   = int(plSegs[4])
    nValue = plMsg[2]

    (bContinue, lNotes, lSelNotes, nBitStart) = self.filter_notes(nIdx)
    if bContinue == False: return

    nBitTime = self.obj('oTimeMode').bit_time()
    sSelOp   = self.obj('oBitOpSel').get_enc_sel_op()
    for oNote in lNotes:
      if oNote.pitch in lSelNotes:
        if   sSelOp == 'LEN':
          oNote.duration = (nBitTime * 16.0 * nValue)
        elif sSelOp == 'VEL':
          oNote.velocity = int(127.0 * nValue)
        elif sSelOp == 'SHIFT':
          if nValue == 1.0: nValue = 0.98
          oNote.start_time = nBitStart + (nValue * nBitTime)

    oMidiClip = self.state().midi_clip_or_none()
    self.state().pause_notes_listener(True) # prevent updating GUI
    oMidiClip.apply_note_modifications(lNotes)

  def on_bit_enc_master(self, plSegs, plMsg):
    nValue = plMsg[2]

    hVisSpan  = self.obj('oSeqMap').get_visible_span()
    sTimeMode = self.obj('oTimeMode').time_mode()   # BAR, PHRASE
    sHalfSel  = self.obj('oHalfSel' ).half_sel()    # LEFT, RIGHT
    sSection  = self.obj('oSection' ).section()     # 1/2, 1, 2, 4
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
    for oNote in lNotes:
      if oNote.pitch in lSelNotes:
        nCount += 1

    if nCount == 0:
      self.alert('No selected notes in [%.2f, %.2f]' % (nTimeStart, nTimeEnd))
      return # nothing else to do here

    nBitTime = self.obj('oTimeMode').bit_time()
    sSelOp   = self.obj('oBitOpSel').get_enc_sel_op()
    for oNote in lNotes:
      if oNote.pitch in lSelNotes:
        if   sSelOp == 'LEN':
          oNote.duration = (nBitTime * 16.0 * nValue)
        elif sSelOp == 'VEL':
          oNote.velocity = int(127.0 * nValue)
        elif sSelOp == 'SHIFT':
          if nValue == 1.0: nValue = 0.98
          nNoteStart = float(int(oNote.start_time / nBitTime)) * nBitTime
          nTimeRel   = nNoteStart - nTimeStart
          nTimeIdx   = int(nTimeRel / nBitTime)
          oNote.start_time = nTimeStart + (nTimeIdx + nValue) * nBitTime

    self.state().pause_notes_listener(True) # prevent updating GUI
    oMidiClip.apply_note_modifications(lNotes)

  # ********************************************************

  def filter_notes(self, pnIdx):
    nBitSpan   = self.obj('oTimeMode').bit_time()
    hVisSpan   = self.obj('oSeqMap').get_visible_span()
    nTimeStart = hVisSpan['nTimeStart']
    nBitStart  = nTimeStart + float(pnIdx) * nBitSpan

    # find out if there is a note in the operated bit
    oMidiClip = self.state().midi_clip_or_none()
    lNotes    = oMidiClip.get_notes_extended(
      0,         # select from the lowest pitch
      127,       # with all notes span
      nBitStart, # from time start
      nBitSpan)  # with time span
    lSelNotes = self.obj('oNoteSel').get_sel_notes()

    nCount = 0
    for oNote in lNotes:
      if oNote.pitch in lSelNotes:
        nCount += 1

    bContinue = True
    if nCount == 0:
      bContinue = False
      self.alert('No selected notes in [%.2f, %.2f]' %
        (nBitStart, nBitStart + nBitSpan))

    return (bContinue, lNotes, lSelNotes, nBitStart)

  # ********************************************************

  def enc_reset(self, psSelOp):
    if psSelOp == 'LEN':
      nValue = 1.0 / 16.0 # 1 bit time
    elif psSelOp == 'VEL':
      nValue = 1.0        # velocity = 127
    elif psSelOp == 'SHIFT':
      nValue = 0.0        # no time shift

    self.on_bit_enc_master([], [None, None, nValue])

