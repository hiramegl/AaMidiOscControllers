import Live

from _Framework.ControlSurface      import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement       import ButtonElement

from .ConfigurableButtonElement     import ConfigurableButtonElement
from .Selector                      import Selector
from .Skin                          import make_skin

class AaGrid(ControlSurface):
  __doc__ = "AaGrid controller"

  def __init__(self, _oCtrlInstance):
    ControlSurface.__init__(self, _oCtrlInstance)
    self.m_oCtrlInst = _oCtrlInstance

    with self.component_guard():
      self._suppress_session_highlight = True
      self.load_config()
      self.init()
      self.log('initialized controller!')

  # ********************************************************

  def load_config(self):
    self.m_hCfg = {
      'nCols': 8,     # physical (APC buttons)
      'nRows': 8,     # physical (APC buttons)
      'nChan': 0,     # CHANNEL 1 (MIDI 0)
      'nGridOff': 0,  # GRID   buttons offset
      'nBottOff': 64, # BOTTOM buttons offset
      'nSideOff': 82, # SIDE   buttons offset
      'nShftAdr': 98, # SHIFT  button  address
    }
    self.m_hObj   = {
      'oCtrlInst': self.m_oCtrlInst,
      'oSong'    : self.m_oCtrlInst.song(),
    }

  def init(self):
    oSkin        = make_skin()
    bIsMomentary = True
    oMatrix      = ButtonMatrixElement()
    oMatrix.name = 'Button_Matrix'

    # create the 8x8 matrix of buttons
    for nRow in range(self.cfg('nRows')):
      lButtonRow = []
      nRowPhy = self.cfg('nRows') - 1 - nRow # reversed row order
      for nCol in range(self.cfg('nCols')):
        oButton = ConfigurableButtonElement(
          bIsMomentary,
          MIDI_NOTE_TYPE,
          self.cfg('nChan'),
          self.cfg('nGridOff') + nRowPhy * self.cfg('nCols') + nCol,
          skin = oSkin,
          control_surface = self,
          name = 'Clip_Button_%d_%d' % (nRowPhy, nCol))
        oButton.m_hAttr = {'sType': 'grid', 'nRow': nRow, 'nCol': nCol}
        lButtonRow.append(oButton)
      oMatrix.add_row(tuple(lButtonRow))

    # create side and bottom buttons
    lBottomButtons = []
    for nIdx in range(self.cfg('nCols')):
      oButton = ConfigurableButtonElement(
        bIsMomentary,
        MIDI_NOTE_TYPE,
        self.cfg('nChan'),
        self.cfg('nBottOff') + nIdx,
        skin = oSkin,
        name = u'track_but_%d' % (nIdx))
      oButton.m_hAttr = {'sType': 'bottom', 'nIdx': nIdx}
      lBottomButtons.append(oButton)

    lSideButtons = []
    for nIdx in range(self.cfg('nRows')):
      oButton = ConfigurableButtonElement(
        bIsMomentary,
        MIDI_NOTE_TYPE,
        self.cfg('nChan'),
        self.cfg('nSideOff') + nIdx,
        skin = oSkin,
        name = u'Side_%d' % (nIdx))
      oButton.m_hAttr = {'sType': 'side', 'nIdx': nIdx}
      lSideButtons.append(oButton)

    # create shift button
    oShiftButton = ButtonElement(
      bIsMomentary,
      MIDI_NOTE_TYPE,
      self.cfg('nChan'),
      self.cfg('nShftAdr'),
      name = u'shift_but')
    oShiftButton.add_value_listener(self._on_shift_value)

    # SELECTOR INIT ****************************************

    self.m_oSelector = Selector(
      self,
      self.m_hCfg,
      self.m_hObj,
      oMatrix,
      lBottomButtons,
      lSideButtons,
      oShiftButton)
    self.m_oSelector.name = 'Selector'
    for oControl in self.controls:
      if isinstance(oControl, ConfigurableButtonElement):
        oControl.add_value_listener(self._on_button_value, identify_sender = True)

    self._suppress_session_highlight = False
    self.set_highlighting_session_component(self.m_oSelector.session_component())
    self.m_oSelector.update()

  def _set_session_highlight(self, _nTrackOffset, _nSceneOffset, _nWidth, _nHeight, _nIncludeReturnTracks):
    if self._suppress_session_highlight == False:
      ControlSurface._set_session_highlight(self, _nTrackOffset, _nSceneOffset, _nWidth, _nHeight, _nIncludeReturnTracks)

  # ********************************************************

  def _on_button_value(self, pnValue, poSender):
    assert pnValue in range(128)
    self.m_oSelector.route(poSender.m_hAttr, pnValue)

  def _on_shift_value(self, pnValue):
    assert pnValue in range(128)
    self.m_oSelector.on_shift_value(pnValue)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.m_oCtrlInst.show_message(psMsg)

