import os
import Live

from .Comm         import Comm
from .State        import State
from .Tempo        import Tempo
from .Shift        import Shift
from .Selected     import Selected
from .ClipNav      import ClipNav
from .ClipCmd      import ClipCmd
from .loop.Loop    import Loop
from .seq.Seq      import Seq
from .sess.Session import Session

class AaTouch:
  __doc__ = 'Script for AaTouch'

  def __init__(self, poCtrlInstance):
    # Config
    self.m_hCfg = {
      'sProdName': 'AaTouch',
      'bDebug'   : False,
      'bClean'   : True,

      # Session
      'nTracks' : 32,
      'nScenes' : 8,
      'nReturns': 8,

      # OSC
      'sRxAddr' : '127.0.0.1', # Macbook: Ableton Live
      'nRxPort' : 2726,
      'sTxAddr' : '127.0.0.1', # Macbook: Open Stage Control
      'nTxPort' : 2727,
    }

    # Objects
    self.m_hObj = {
      'oCtrlInst': poCtrlInstance,
      'oSong'    : poCtrlInstance.song(),
    }

    Comm    (self.m_hCfg, self.m_hObj)
    State   (self.m_hCfg, self.m_hObj)
    Tempo   (self.m_hCfg, self.m_hObj)
    Shift   (self.m_hCfg, self.m_hObj)
    Selected(self.m_hCfg, self.m_hObj)
    ClipNav (self.m_hCfg, self.m_hObj)
    ClipCmd (self.m_hCfg, self.m_hObj)
    Loop    (self.m_hCfg, self.m_hObj)
    Seq     (self.m_hCfg, self.m_hObj)
    Session (self.m_hCfg, self.m_hObj)

  # Ableton ************************************************

  def disconnect(self):
    self.log('> %s: disconnecting ...' % (self.cfg('sProdName')))
    self.obj('oShift'   ).disconnect()
    self.obj('oSelected').disconnect()
    self.obj('oClipCmd' ).disconnect()
    self.obj('oLoop'    ).disconnect()
    self.obj('oSeq'     ).disconnect()
    self.obj('oSess'    ).disconnect()
    self.log('> %s: disconnected' % (self.cfg('sProdName')))

  def refresh_state(self):
    self.obj('oSelected').update_sends()
    self.obj('oSends'   ).activate()
    self.obj('oTracks'  ).update_volumes()

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

