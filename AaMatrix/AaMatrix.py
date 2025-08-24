from __future__ import with_statement

import time
import Live

from _Framework.ControlSurface      import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement       import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement

from .ConfigurableButtonElement     import ConfigurableButtonElement
from .Selector                      import Selector

try:
  xrange
except NameError:
  xrange = range

LP_MINI_MK3_ID                 = 13
LP_X_ID                        = 12
SYSEX_START                    = 240
SYSEX_NON_REALTIME             = 126
SYSEX_GENERAL_INFO             = 6
SYSEX_IDENTITY_REQUEST_ID      = 1
SYSEX_END                      = 247
SYSEX_IDENTITY_REQUEST_MESSAGE = (SYSEX_START, SYSEX_NON_REALTIME, 127, SYSEX_GENERAL_INFO, SYSEX_IDENTITY_REQUEST_ID, SYSEX_END)
NOVATION_MANUFACTURER_ID       = (0, 32, 41)
FIRMWARE_MODE_COMMAND          = 16
STANDALONE_MODE                = 0
STD_MSG_HEADER                 = (SYSEX_START,) + NOVATION_MANUFACTURER_ID + (2,)

class AaMatrix(ControlSurface):
  __doc__ = "AaMatrix controller"
  _active_instances = []

  def __init__(self, poCtrlInst):
    ControlSurface.__init__(self, poCtrlInst)
    self.m_oCtrlInst = poCtrlInst
    self.m_oSelector = None # needed because update hardware is called.
    self.m_bLpx      = False
    self.m_bMk2Rgb   = False
    self.m_bMk3Rgb   = False

    with self.component_guard():
      self.load_config()
      self.m_bSuppressSendMidi         = True
      self.m_bSuppressSessionHighlight = True
      self._suggested_input_port       = ("Launchpad", "Launchpad Mini", "Launchpad S", "Launchpad MK2", "Launchpad X", "Launchpad Mini MK3")
      self._suggested_output_port      = ("Launchpad", "Launchpad Mini", "Launchpad S", "Launchpad MK2", "Launchpad X", "Launchpad Mini MK3")
      self.m_bControlIsWithAutomap     = False
      self.m_oUserByteWriteButton      = None
      self.m_oConfigButton             = None
      self.m_bWroteUserByte            = False
      self.m_nChallenge                = Live.Application.get_random_int(0, 400000000) & 2139062143
      self.m_bInitDone                 = False
      self.log('init started')

  def load_config(self):
    self.m_hCfg = {
      'nTracks': 32, # logical  (session clips)
      'nScenes': 32, # logical  (session clips)
      'nCols'  : 8,  # physical (launchpad buttons)
      'nRows'  : 8,  # physical (launchpad buttons)
    }
    self.m_hObj   = {
      'oCtrlInst': self.m_oCtrlInst,
      'oSong'    : self.m_oCtrlInst.song(),
    }

  # HANDSHAKE PROTOCOL *************************************

  def refresh_state(self):
    ControlSurface.refresh_state(self)
    self.schedule_message(5, self._update_hardware)

  def _update_hardware(self):
    self.m_bSuppressSendMidi = False
    if self.m_oUserByteWriteButton != None:
      self.m_oUserByteWriteButton.send_value(1)
      self.m_bWroteUserByte = True
    self.m_bSuppressSendMidi = True
    self.set_enabled(False)
    self.m_bSuppressSendMidi = False
    self._send_challenge()

  def _send_challenge(self):
    # send challenge for all models to allow to detect which one is actually plugged
    self._send_midi(SYSEX_IDENTITY_REQUEST_MESSAGE)                                          # for mk3 and LPX
    challenge_bytes = tuple([ self.m_nChallenge >> 8 * index & 127 for index in xrange(4) ]) # for mk2
    self._send_midi((240, 0, 32, 41, 2, 24, 64) + challenge_bytes + (247,))
    for index in range(4):                                                                   # for mk1's
      challenge_byte = self.m_nChallenge >> 8 * index & 127
      self._send_midi((176, 17 + index, challenge_byte))

  def handle_sysex(self, plMidiBytes):
    if len(plMidiBytes) >= 10 and plMidiBytes[:8] == (240, 126, 0, 6, 2, 0, 32, 41): #0,32,41=novation
      # MK3
      if len(plMidiBytes) >= 12 and plMidiBytes[8:10] == (19,1):
        self.m_bMk3Rgb = True
        #programmer mode
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 14, 1, SYSEX_END))
        #led feedback: internal off, external on
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 10, 0, 1, SYSEX_END))
        #disable sleep mode
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 9, 1, SYSEX_END))
        self.m_bSuppressSendMidi = False
        self.set_enabled(True)
        self.init()
      elif len(plMidiBytes) >= 12 and plMidiBytes[8:10] == (3,1):
        self.m_bLpx = True
        #programmer mode
        self._send_midi(STD_MSG_HEADER + (LP_X_ID, 14, 1, SYSEX_END))
        #led feedback: internal off, external on
        self._send_midi(STD_MSG_HEADER + (LP_X_ID, 10, 0, 1, SYSEX_END))
        #disable sleep mode
        self._send_midi(STD_MSG_HEADER + (LP_X_ID, 9, 1, SYSEX_END))
        self.m_bSuppressSendMidi = False
        self.set_enabled(True)
        self.init()
      else:
        ControlSurface.handle_sysex(self, plMidiBytes)
    elif len(plMidiBytes) == 9 and plMidiBytes[:9] == (240, 0, 32, 41, 2, 13, 14, 1, 247):
      self.log("Challenge Response ok (mk3)")
    elif len(plMidiBytes) == 10 and plMidiBytes[:7] == (240, 0, 32, 41, 2, 24, 64):
      # MK2
      response = long(plMidiBytes[7])
      response += long(plMidiBytes[8]) << 8
      if response == Live.Application.encrypt_challenge2(self.m_nChallenge):
        self.log("Challenge Response ok (mk2)")
        self.m_bMk2Rgb = True
        self.m_bSuppressSendMidi = False
        self.set_enabled(True)
        self.init()
    elif len(plMidiBytes) == 8 and plMidiBytes[1:5] == (0, 32, 41, 6):
      # MK1
      response = long(plMidiBytes[5])
      response += long(plMidiBytes[6]) << 8
      if response == Live.Application.encrypt_challenge2(self.m_nChallenge):
        self.log("Challenge Response ok (mk1)")
        self.m_bMk2Rgb = False
        self.init()
        self.m_bSuppressSendMidi = False
        self.set_enabled(True)
    else:
      ControlSurface.handle_sysex(self, plMidiBytes)

  def init(self):
    if self.m_bInitDone:
      self.log('Updating selector ...')
      self.m_oSelector.update()
      return

    self.m_bInitDone = True
    self.log('Init executing ...')

    # second part of the __init__ after model has been identified using its challenge response
    if self.m_bMk3Rgb or self.m_bLpx:
      from .SkinMK2 import make_skin
      self.m_oSkin = make_skin()
      self.m_lSideNotes = (89, 79, 69, 59, 49, 39, 29, 19)
    elif self.m_bMk2Rgb:
      from .SkinMK2 import make_skin
      self.m_oSkin = make_skin()
      self.m_lSideNotes = (89, 79, 69, 59, 49, 39, 29, 19)
    else:
      from .SkinMK1 import make_skin # @Reimport
      self.m_oSkin = make_skin()
      self.m_lSideNotes = (8, 24, 40, 56, 72, 88, 104, 120)

    with self.component_guard():
      bIsMomentary = True
      self.m_oConfigButton = ButtonElement(bIsMomentary, MIDI_CC_TYPE, 0, 0, optimized_send_midi=False)
      self.m_oConfigButton.add_value_listener(self._config_value)
      self.m_oUserByteWriteButton = ButtonElement(bIsMomentary, MIDI_CC_TYPE, 0, 16)
      self.m_oUserByteWriteButton.name = 'User_Byte_Button'
      self.m_oUserByteWriteButton.send_value(1)
      self.m_oUserByteWriteButton.add_value_listener(self._user_byte_value)

      oMatrix = ButtonMatrixElement()
      oMatrix.name = 'Button_Matrix'
      for nRow in range(self.cfg('nRows')):
        lButtonRow = []
        for nCol in range(self.cfg('nCols')):
          if self.m_bMk2Rgb or self.m_bMk3Rgb or self.m_bLpx:
            # for mk2 buttons are assigned "top to bottom"
            nMidiNote = (81 - (10 * nRow)) + nCol
          else:
            nMidiNote = nRow * 16 + nCol
          oButton = ConfigurableButtonElement(bIsMomentary, MIDI_NOTE_TYPE, 0, nMidiNote, skin = self.m_oSkin, control_surface = self)
          oButton.name = 'Grid_' + str(nCol) + '_' + str(nRow)
          oButton.m_hAttr = {'sType': 'grid', 'nRow': nRow, 'nCol': nCol}
          lButtonRow.append(oButton)
        oMatrix.add_row(tuple(lButtonRow))

      if self.m_bMk3Rgb or self.m_bLpx :
        lTopButtons  = [ConfigurableButtonElement(bIsMomentary, MIDI_CC_TYPE, 0, 91 + nCol, skin = self.m_oSkin) for nCol in range(self.cfg('nCols'))]
        lSideButtons = [ConfigurableButtonElement(bIsMomentary, MIDI_CC_TYPE, 0, self.m_lSideNotes[nRow], skin = self.m_oSkin) for nRow in range(self.cfg('nRows'))]
      else:
        lTopButtons  = [ConfigurableButtonElement(bIsMomentary, MIDI_CC_TYPE, 0, 104 + nCol, skin = self.m_oSkin) for nCol in range(self.cfg('nCols'))]
        lSideButtons = [ConfigurableButtonElement(bIsMomentary, MIDI_NOTE_TYPE, 0, self.m_lSideNotes[nRow], skin = self.m_oSkin) for nRow in range(self.cfg('nRows'))]

      for nCol in range(self.cfg('nCols')):
        lTopButtons[nCol].name    = 'Top_' + str(nCol)
        lTopButtons[nCol].m_hAttr = {'sType': 'top', 'nIdx': nCol}
      for nRow in range(self.cfg('nRows')):
        lSideButtons[nRow].name    = 'Side_' + str(nRow)
        lSideButtons[nRow].m_hAttr = {'sType': 'side', 'nIdx': nRow}

      # SELECTOR INIT **************************************

      self.m_oSelector = Selector(
        self,
        self.m_hCfg,
        self.m_hObj,
        oMatrix,
        lTopButtons,
        lSideButtons)
      self.m_oSelector.name = 'Selector'
      for oControl in self.controls:
        if isinstance(oControl, ConfigurableButtonElement):
          oControl.add_value_listener(self._on_button_value, identify_sender = True)

      self.m_bSuppressSessionHighlight = False
      self.set_highlighting_session_component(self.m_oSelector.session_component())
      self.request_rebuild_midi_map() # due to our 2 stage init, we need to rebuild midi map
      self.m_oSelector.update()       # and request update

      if self.m_bLpx:
        self.log("AaMatrix (LPX) Loaded !")
      elif self.m_bMk3Rgb:
        self.log("AaMatrix (mk3) Loaded !")
      elif self.m_bMk2Rgb:
        self.log("AaMatrix (mk2) Loaded !")
      else:
        self.log("AaMatrix (classic) Loaded !")

  def _user_byte_value(self, pnValue):
    assert (pnValue in range(128))
    if not self.m_bWroteUserByte:
      bEnabled = (pnValue == 1)
      self.m_bControlIsWithAutomap = not bEnabled
      self.m_bSuppressSendMidi = self.m_bControlIsWithAutomap
      if not self.m_bControlIsWithAutomap:
        for oControl in self.controls:
          if isinstance(oControl, ConfigurableButtonElement):
            oControl.force_next_send()
      self.set_enabled(bEnabled)
      self.m_bSuppressSendMidi = False
    else:
      self.m_bWroteUserByte = False

  def disconnect(self):
    self.m_bSuppressSendMidi = True
    for oControl in self.controls:
      if isinstance(oControl, ConfigurableButtonElement):
        oControl.remove_value_listener(self._on_button_value)
    if self.m_oSelector != None:
      self.m_oUserByteWriteButton.remove_value_listener(self._user_byte_value)
      self.m_oConfigButton.remove_value_listener(self._config_value)

    ControlSurface.disconnect(self)
    self.m_bSuppressSendMidi = False
    if self.m_bLpx:
      # lpx needs disconnect string sent
      self._send_midi(STD_MSG_HEADER + (LP_X_ID, 14, 0, SYSEX_END))
      self._send_midi(STD_MSG_HEADER + (LP_X_ID, FIRMWARE_MODE_COMMAND, STANDALONE_MODE, SYSEX_END))
    elif self.m_bMk3Rgb:
      # launchpad mk2 needs disconnect string sent
      self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 14, 0, SYSEX_END))
      self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, FIRMWARE_MODE_COMMAND, STANDALONE_MODE, SYSEX_END))
    elif self.m_bMk2Rgb:
      # launchpad mk2 needs disconnect string sent
      self._send_midi((240, 0, 32, 41, 2, 24, 64, 247))

    if self.m_oConfigButton != None:
      self.m_oConfigButton.send_value(32) #Send enable flashing led config message to LP
      self.m_oConfigButton.send_value(0)
      self.m_oConfigButton = None

    if self.m_oUserByteWriteButton != None:
      self.m_oUserByteWriteButton.send_value(0)
      self.m_oUserByteWriteButton = None
    self.log('disconnected!')

  # ********************************************************

  def _send_midi(self, midi_bytes, optimized=None):
    bSentSuccessfully = False
    if not self.m_bSuppressSendMidi:
      bSentSuccessfully = ControlSurface._send_midi(self, midi_bytes, optimized=optimized)
    return bSentSuccessfully

  def _config_value(self, value):
    assert value in range(128)

  def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
    if not self.m_bSuppressSessionHighlight:
      ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)

  def _on_button_value(self, pnValue, poSender):
    assert pnValue in range(128)
    self.m_oSelector.route(poSender.m_hAttr, pnValue)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def log(self, psMsg):
    Live.Base.log(psMsg)

  def alert(self, psMsg):
    self.m_oCtrlInst.show_message(psMsg)
