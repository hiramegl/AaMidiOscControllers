import os
import Live

from .Comm     import Comm
from .Track    import Track
from .Session  import Session
from .MultiEq3 import MultiEq3

class AaBcr:
  __doc__ = 'Script for BCR2000 through OSC'

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
      'sProdName': 'AaBcr',
      'bDebug'   : False,
      'bClean'   : True,
      'bUnknown' : False, # dump unknown devices

      # Session
      'nTracks' : 1, 'nScenes': 4,
      'nStrips' : 8,
      'bIncRet' : True, # control return tracks!

      # OSC (use bWired to configure wire ip addresses)
      'sRxAddr' : sRxAddr, # Macbook
      'nRxPort' : 2722,
      'sTxAddr' : sTxAddr, # Raspberry Pi
      'nTxPort' : 2723,
      'sOscAddr': '/bcr',

      # MIDI
      'nBank0Chn' : 15, # MIDI-CHANNEL 16
      'nSessLeft' : 1, 'nSessRight': 2,
      'nGoToSel'  : 3,

      'nBank1Sync': 4,  # midi channel 16
      'nBank2Sync': 5,  # midi channel 16
      'nBank3Sync': 6,  # midi channel 16
      'nBank4Sync': 7,  # midi channel 16
      'nBank5Sync': 8,  # midi channel 16
      'nBank6Sync': 9,  # midi channel 16

      'nBanks'    : 6,

      'nBank1Chn' : 0, 'nBank2Chn' : 1,
      'nBank3Chn' : 2, 'nBank4Chn' : 3,
      'nBank5Chn' : 4, 'nBank6Chn' : 5,

      # Rotary group
      'nGB0Off'   : 33, 'nGB1Off'   : 41,
      'nGB2Off'   : 1,  'nGB3Off'   : 57,

      'nGR0Off'   : 49, 'nGR1Off'   : 9,
      'nGR2Off'   : 17, 'nGR3Off'   : 25,

      # Main panel
      'nMB0Off'   : 65, 'nMB1Off'   : 73,
      'nMR0Off'   : 81, 'nMR1Off'   : 89,
      'nMR2Off'   : 97,

      # Multi Eq3 Mode
      'nMultiEq3SyncChn': 14, # MIDI-CHANNEL 15
      'nMultiEq3Sync'   :  1,
      'nMultiEq3Chn'    :  6,
    }

    # Objects
    self.m_hObj = {
      'oCtrlInst': poCtrlInstance,
      'oSong'    : poCtrlInstance.song(),
    }

    # Init
    Comm    (self.m_hCfg, self.m_hObj)
    Track   (self.m_hCfg, self.m_hObj)
    Session (self.m_hCfg, self.m_hObj)
    MultiEq3(self.m_hCfg, self.m_hObj)

  # Ableton ************************************************

  def disconnect(self):
    self.log('> %s: disconnecting ...' % (self.cfg('sProdName')))
    self.obj('oSess'    ).disconnect()
    self.obj('oMultiEq3').disconnect()
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
    self.obj('oRouter').update_sync_devs()
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
    self.obj('oCtrlInst').show_message(sMessage)

