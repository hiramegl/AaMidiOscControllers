import os
import time
import Live

from .Comm    import Comm
from .Session import Session

class AaWfd:
  __doc__ = 'Script for W-FADER through OSC'

  def __init__(self, poCtrlInstance):
    self.m_bRefreshed = False

    sNetwork = 'wired' # local or wired
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
      'sProdName': 'AaWfd',
      'bDebug'   : False,

      # Session
      'nTracks' : 8, 'nScenes': 1,

      # OSC (use bWired to configure wire ip addresses)
      'sRxAddr' : sRxAddr, # Macbook
      'nRxPort' : 2724,
      'sTxAddr' : sTxAddr, # Raspberry Pi
      'nTxPort' : 2725,
      'sOscAddr': '/wfd',

      # MIDI
      'nBank0Chn'  : 4,  # MIDI-CHANNEL 5
      'nSessLeft'  : 67, 'nSessRight': 64,
      'nDevLeft'   : 60, 'nDevRight' : 61,

      'nCrossfader': 9,
      'nCueVol'    : 57,
      'nMasterVol' : 58,
      'nViewToggle': 59,

      'nLoop'      : 26,
      'nRewind'    : 27,
      'nForward'   : 28,
      'nStop'      : 29,
      'nPlay'      : 30,
      'nRecord'    : 31,

      'nPanOff'    : 1,
      'nVolOff'    : 10,
      'nSelOff'    : 18, # bank 1: select
      'nResetOff'  : 33, # bank 2: reset
      'nMuteOff'   : 41, # bank 3: mute
      'nSoloOff'   : 49, # bank 3: solo
    }

    # Objects
    self.m_hObj = {
      'oCtrlInst': poCtrlInstance,
      'oSong'    : poCtrlInstance.song(),
    }

    # Init
    Comm   (self.m_hCfg, self.m_hObj)
    Session(self.m_hCfg, self.m_hObj)

  # Ableton ************************************************

  def disconnect(self):
    self.log('> %s: disconnecting ...' % (self.cfg('sProdName')))
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

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def alert(self, sMessage):
    self.m_oCtrlInstance.show_message(sMessage)

