import Live

from AaTouch.Base import Base

class Rhythm(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lRhythms = [
      # NAME, LENGTH, BIT DURATION, PATTERN
      ['REAGGE'   , 1.0, 0.25, [0.5]],
      ['REAGGETON', 2.0, 0.25, [0.0, 0.75, 1.0, 1.5]],
      ['CLAVE'    , 4.0, 0.25, [0.5, 1.0, 2.0, 2.75, 3.5]],
      ['HEART'    , 2.0, 0.25, [0.0, 0.5]],
      ['4/7'      , 4.0, 0.57, [0.0, 0.57, 1.14, 1.71, 2.28, 2.86, 4.74]],
      ['5/4'      , 4.0, 0.20, [0.0, 0.8 , 1.6, 2.4, 3.2]],
      ['AMEN_S'   , 4.0, 0.25, [1.0, 1.75, 2.25, 3.0, 3.75]],
      ['FILL ALL' , 1.0, 0.25, [0.0, 0.25, 0.5, 0.75]],

      ['HOUSE'    , 1.0, 0.25, [0.0]],
      ['ZOUK'     , 2.0, 0.25, [0.0, 0.75, 1.5]],
      ['SALSA'    , 4.0, 0.25, [0.0, 0.75, 1.5, 2.5, 3.0]],
      ['RUMBA'    , 4.0, 0.25, [0.0, 0.75, 1.75, 2.5, 3.0]],
      ['HIP HOP'  , 4.0, 0.25, [0.0, 0.75, 1.0, 1.25, 3.0, 3.25]],
      ['12/8'     , 4.0, 0.33, [0.0, 0.66, 1.33, 1.66, 2.33, 3.0, 3.66]],
      ['AMEN_D'   , 4.0, 0.25, [0.0, 0.5, 1.5, 2.0, 2.5, 2.75]],
      ['TRIPLET'  , 1.0, 0.33, [0.0, 0.33, 0.66]],

    ]
    phObj['oRhythm'] = self
    self.connect()

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'seq/rhythm', 8 * 2, self.on_rhythm)

  # ********************************************************

  def on_rhythm(self, plSegs, plMsg):
    if self.mode() != 'MIDI':
      self.alert('Rhythm commands not available for Audio clips')
      return

    lSelNotes = self.obj('oNoteSel').get_sel_notes()
    if len(lSelNotes) == 0:
      self.alert('NO SELECTED NOTES FOR RHYTHM')
      return

    nIdx    = int(plSegs[3])
    lRhythm = self.m_lRhythms[nIdx]
    hLimits = self.state().limits_or_none()
    nStart  = hLimits['nStart'] # Clip/Loop start
    nSpan   = self.obj('oSection').section_len()

    lNotes  = []
    sName   = lRhythm[0]
    nPatLen = lRhythm[1]
    nBitLen = lRhythm[2]
    lPatt   = lRhythm[3]
    nVel    = self.obj('oLenVel').get_attr('VEL')
    nTimes  = int(nSpan / nPatLen)

    for nIdx in range(nTimes):
      nPatOff = float(nIdx) * nPatLen
      for nBitOff in lPatt:
        for nPitch in lSelNotes:
          lNotes.append(Live.Clip.MidiNoteSpecification(
            pitch      = nPitch,
            start_time = nStart + nPatOff + nBitOff,
            duration   = nBitLen,
            velocity   = nVel))

    oMidiClip = self.state().midi_clip_or_none()
    oMidiClip.add_new_notes(tuple(lNotes))  # this will trigger a GUI update

    self.alert('APPLYING RHYTHM %s' % (sName))

