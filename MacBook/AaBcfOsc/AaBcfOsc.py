import os
import time
import Live

from .RemixNet import OSCServer

class AaBcfOsc:
  __doc__ = 'Script for BCF2000 through OSC'

  def __init__(self, poCtrlInstance):
    self.c_instance      = poCtrlInstance
    self.m_oCtrlInstance = poCtrlInstance
    self.m_sProductName  = 'AaBcfOsc'

    self.m_oCtrlInstance.set_session_highlight(0, 0, 8, 2, True)

    self.m_sTxAddr = '192.168.0.16' # Raspberry Pi
    #self.m_sTxAddr = '169.254.210.136' # Raspberry Pi
    #self.m_sTxAddr = '127.0.0.1' # Open Stage Control
    self.m_nTxPort = 2721

    self.m_sRxAddr = '192.168.0.11' # Macbook
    #self.m_sRxAddr = '169.254.176.5' # Macbook
    #self.m_sRxAddr = '127.0.0.1' # Macbook
    self.m_nRxPort = 2720

    self.m_oOscServer = OSCServer(
      self,
      self.m_sTxAddr,
      self.m_nTxPort,
      self.m_sRxAddr,
      self.m_nRxPort)
    self.m_oCallbackMgr = self.m_oOscServer.callbackManager
    self.m_oCallbackMgr.add(self.handle_message, '/abc')
    self.m_oCallbackMgr.add(self.handle_message, '/def')
    self.m_oCallbackMgr.add(self.handle_message, '/ghi')
    self.m_oCallbackMgr.add(self.handle_bitlen0, '/bit_len_vel/0')

    self.m_oSong = self.m_oCtrlInstance.song()
    nTempo = self.m_oSong.tempo
    self.m_oOscServer.sendOSC('/abc', '---')
    self.m_oOscServer.sendBundle([
      ['/def', 123],
      ['/ghi', [7, 8]],
      ['/abc', 123.456],
    ])

    # BCF: 0xb0, 17, 100
    # BCR: 0xb0, 104, 120

  def handle_message(self, paMsg):
    sAddr = paMsg[0]
    sType = paMsg[1]
    sVal1 = paMsg[2]
    sVal2 = paMsg[3]
    self.log("----> Rx: %s: [%s] %s, %s" % (sAddr, str(sType), str(sVal1), str(sVal2)))

  def handle_bitlen0(self, paMsg):
    sAddr = paMsg[0]
    sType = paMsg[1]
    sVal1 = paMsg[2]
    self.log("----> Rx: %s: [%s] %s" % (sAddr, str(sType), str(sVal1)))
    self.m_oOscServer.sendOSC('/bit_len_vel/1', 1.0)
    self.m_oOscServer.sendOSC(
      '/EDIT/GET',
      [
        '127.0.0.1:2721',
        '/bit_len_vel/1',
      ])
    self.m_oOscServer.sendOSC(
      '/EDIT',
      [
        'bit_len_vel/2',
        '{"label":"zxcv","colorFill":"#00ff00"}'
      ])
    self.m_oOscServer.sendOSC('/bit_len_vel/2', 1.0)

  # Ableton ************************************************

  def disconnect(self):
    self.log('> %s: disconnecting ...' % (self.m_sProductName))
    self.log('> %s: disconnected' % (self.m_sProductName))

  def update_display(self):
    """
    This function is run every 100ms, so we use it to allow us to process incoming
    OSC commands as quickly as possible under the current listener scheme.
    """
    if self.m_oOscServer:
      try:
        self.m_oOscServer.processIncomingUDP()
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

  def refresh_state(self):
    self.log('> %s: Refreshing state' % (self.m_sProductName));

  def build_midi_map(self, midi_map_handle):
    return

  # ********************************************************

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def alert(self, sMessage):
    self.m_oCtrlInstance.show_message(sMessage)

