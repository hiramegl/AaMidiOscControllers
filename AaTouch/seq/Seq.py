from AaTouch.Base import Base

from .SeqCmd   import SeqCmd
from .Rhythm   import Rhythm
from .LenVel   import LenVel
from .Scale    import Scale
from .Chord    import Chord
from .TimeMode import TimeMode
from .HalfSel  import HalfSel
from .Section  import Section
from .NoteSel  import NoteSel
from .SeqMap   import SeqMap
from .BitOp    import BitOp
from .BitOpSel import BitOpSel
from .Grid     import Grid
from .Patterns import Patterns

class Seq(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_nCurrMode = None
    self.connect()

    SeqCmd  (phCfg, phObj)
    Rhythm  (phCfg, phObj)
    LenVel  (phCfg, phObj)
    Scale   (phCfg, phObj)
    Chord   (phCfg, phObj)
    TimeMode(phCfg, phObj)
    HalfSel (phCfg, phObj)
    Section (phCfg, phObj)
    NoteSel (phCfg, phObj)
    SeqMap  (phCfg, phObj)
    BitOp   (phCfg, phObj) # depends on HalfSel, Section, TimeMode & SeqMap
    BitOpSel(phCfg, phObj)
    Grid    (phCfg, phObj)
    Patterns(phCfg, phObj)

    phObj['oSeq'] = self

    self.update()

  # ********************************************************

  def connect(self):
    for nGridIdx in range(4):
      self.reg_idx_cb(
        'seq/grid/%d' % (nGridIdx), 12 * 8, self.on_grid_bit)

  def disconnect(self):
    self.obj('oLenVel'  ).disconnect()
    self.obj('oScale'   ).disconnect()
    self.obj('oChord'   ).disconnect()
    self.obj('oTimeMode').disconnect()
    self.obj('oHalfSel' ).disconnect()
    self.obj('oSection' ).disconnect()
    self.obj('oBitOp'   ).disconnect()
    self.obj('oBitOpSel').disconnect()
    self.obj('oNoteSel' ).disconnect()
    self.obj('oSeqMap'  ).disconnect()

    if self.mode() == 'MIDI':
      self.grid().deactivate()
    elif self.mode() == 'EMPTY':
      self.obj('oPatt').send_pattern('add', 0.0)
    elif self.mode() == 'AUDIO':
      self.obj('oPatt').send_pattern('unav', 0.0)

  # ********************************************************

  def update(self):
    self.deactivate()
    self.activate()

  def activate(self):
    self.m_nCurrMode = self.mode()

    if self.m_nCurrMode == 'MIDI':
      self.obj('oSeqMap'  ).activate()
      self.obj('oBitOp'   ).activate()
      self.obj('oBitOpSel').activate()
      self.grid().activate() # grid depends on SeqMap activation, update it last

    elif self.m_nCurrMode == 'EMPTY':
      self.obj('oPatt').send_pattern('add', 1.0)

    elif self.m_nCurrMode == 'AUDIO':
      self.obj('oPatt').send_pattern('unav', 1.0)

    if self.state().view_mode() == 'SEQ':
      self.highlight_session()

  def deactivate(self):
    if self.m_nCurrMode == 'MIDI':
      self.grid().deactivate()
      self.obj('oBitOpSel').deactivate()
      self.obj('oBitOp'   ).deactivate()
      self.obj('oSeqMap'  ).deactivate()

    elif self.m_nCurrMode == 'EMPTY':
      self.obj('oPatt').send_pattern('add', 0.0)

    elif self.m_nCurrMode == 'AUDIO':
      self.obj('oPatt').send_pattern('unav', 0.0)

  # ********************************************************

  def on_grid_bit(self, plSegs, plMsg):
    sAddr    = plMsg[0]
    nGridIdx = int(plSegs[3])
    nBitIdx  = int(plSegs[4])
    nValue   = int(plMsg[2])

    if self.mode() == 'MIDI':
      self.state().pause_notes_listener(True) # used to prevent updating GUI unnecessarly
      self.grid().on_bit(nGridIdx, nBitIdx, nValue)

    elif self.mode() == 'EMPTY':
      if nValue > 0.5:
        self.send_msg(sAddr, 0.0) # prevent from turning on
      self.obj('oPatt').send_pattern('add', 0.0)
      self.create_empty_midi_clip()
      self.state().update()
      self.obj('oSeqMap').activate()
      self.grid().activate()

    elif self.mode() == 'AUDIO':
      if nValue < 0.5:
        self.send_msg(sAddr, 1.0) # prevent from turning off
      else:
        self.send_msg(sAddr, 0.0) # prevent from turning on

  def create_empty_midi_clip(self):
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return
    if (oClipSlot.has_clip): return # it should be an empty clip
    nLength = self.get_section_length()
    oClipSlot.create_clip(nLength)
    self.state().update()
    self.obj('oSeqMap'  ).activate()
    self.obj('oBitOp'   ).activate()
    self.obj('oBitOpSel').activate()

  # ********************************************************

  def highlight_session(self):
    self.obj('oCtrlInst').set_session_highlight(
      self.col_offset(),
      self.row_offset(),
      1, # 1 track
      1, # 1 scene
      False) # do not include return tracks

  # ********************************************************

  def grid(self):
    return self.obj('oGrid')

  def midi_track(self):
    return self.state().midi_track_or_none()

  def get_section_length(self):
    if self.obj('oTimeMode').time_mode() == 'BAR':
      return 4 # one bar
    return 16 # one phrase

