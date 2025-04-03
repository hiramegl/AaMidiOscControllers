import os
import time
import Live

from .Comm    import Comm
from .Tempo   import Tempo
from .Clip    import Clip
from .Track   import Track
from .Scene   import Scene
from .Session import Session

class AaBcf:
  __doc__ = 'Script for BCF2000 through OSC'

  def __init__(self, poCtrlInstance):
    self.m_bRefreshed = False

    sNetwork = 'wired'
    if sNetwork == 'local':
      sRxAddr = '1.1.0.1'      # Macbook
      sTxAddr = '1.1.0.2'      # Raspberry Pi
    elif sNetwork == 'fake':
      sRxAddr = '127.0.0.1'    # Macbook
      sTxAddr = '127.0.0.1'    # Raspberry Pi
    elif sNetwork == 'wired':
      sHome = os.getenv('HOME')
      with open('%s/AaConfig/mac_addr.txt' % sHome, 'rt') as oFile:
        sRxAddr = oFile.read() # Macbook
      with open('%s/AaConfig/pi_addr.txt'  % sHome, 'rt') as oFile:
        sTxAddr = oFile.read() # Raspberry Pi

    # Config
    self.m_hCfg = {
      'sProdName': 'AaBcf',
      'bDebug'   : False,
      'bClean'   : True,

      # Session
      'nTracks' : 8, 'nScenes': 2,
      'bIncRet' : False, # do not control return tracks!

      # OSC (use bWired to configure wire ip addresses)
      'sRxAddr' : sRxAddr, # Macbook
      'nRxPort' : 2720,
      'sTxAddr' : sTxAddr, # Raspberry Pi
      'nTxPort' : 2721,
      'sOscAddr': '/bcf',

      # MIDI
      'nBank0Chn'  : 0,  # MIDI-CHANNEL 1
      'nVolOff'    : 17,
      'nSessLeft'  : 25, 'nSessRight': 26,
      'nStopTot'   : 27,

      'nBank1Sync' : 28, # midi channel 1
      'nBank2Sync' : 29, # midi channel 1
      'nBank3Sync' : 30, # midi channel 1
      'nBank4Sync' : 31, # midi channel 1

      'nTempo1'    : 33, # Rotary Group 1
      'nTempo2'    : 34,
      'nTrkSel'    : 35,
      'nScnSel'    : 36,
      'nTrkPan'    : 37,
      'nClpGain'   : 38,
      'nClpPit'    : 39,
      'nClpDet'    : 40,

      'nTempo1Rst' : 41, # Rotary Buttons Group 1
      'nTempo2Rst' : 42,
      'nTrkSelRst' : 43,
      'nScnSelRst' : 44,
      'nTrkPanRst' : 45,
      'nClpGainRst': 46,
      'nClpPitRst' : 47,
      'nClpDetRst' : 48,

      # Bank 1
      'nBank1Chn': 0, # MIDI-CHANNEL 1
      'nMuteOff' : 1, 'nSoloOff': 9,  # Buttons

      # Bank 1
      'nBank2Chn': 1, # MIDI-CHANNEL 2
      'nStopOff' : 1, 'nSelOff' : 9,  # Buttons

      # Bank 1
      'nBank3Chn': 2, # MIDI-CHANNEL 3
      'nInputOff': 1, 'nArmOff': 9,   # Buttons

      # Bank 1
      'nBank4Chn': 3, # MIDI-CHANNEL 4
      'nAvVelOff': 33,                # Rotary Group 1
      'nCrossOff': 1, 'nAvDecOff': 9, # Buttons
    }

    # Objects
    self.m_hObj = {
      'oCtrlInst': poCtrlInstance,
      'oSong'    : poCtrlInstance.song(),
    }

    # Init
    Comm   (self.m_hCfg, self.m_hObj)
    Tempo  (self.m_hCfg, self.m_hObj)
    Clip   (self.m_hCfg, self.m_hObj)
    Track  (self.m_hCfg, self.m_hObj)
    Scene  (self.m_hCfg, self.m_hObj)
    Session(self.m_hCfg, self.m_hObj)

  # Ableton ************************************************

  def disconnect(self):
    self.log('> %s: disconnecting ...' % (self.cfg('sProdName')))
    self.obj('oSess').disconnect()
    self.log('> %s: disconnected' % (self.cfg('sProdName')))

  def refresh_state(self):
    if self.m_bRefreshed:
      return # already refreshed, nothing to do here
    self.m_bRefreshed = True

  def update_display(self):
    """
    This function is run every 100ms, so we use it to allow us to process incoming
    OSC commands as quickly as possible under the current listener scheme.
    """
    self.obj('oSess').update_sync_tasks()
    if self.obj('oComm'):
      try:
        self.obj('oComm').proc_msg()
      except:
        pass

  def connect_script_instances(self, instanciated_scripts):
    """
    Called by the Application as soon as all scripts are initialized.
    You can connect yourself to other running scripts here, as we do it
    connect the extension modules
    """
    return

  def can_lock_to_devices(self):
    return False

  def build_midi_map(self, midi_map_handle):
    return

  # ********************************************************

  def move_to_track_offset(self, pnTrackOffset):
    self.obj('oSess').handle_new_track_offset(pnTrackOffset)
    self.log('AaBcf: new track offset: %d' % (pnTrackOffset))

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

