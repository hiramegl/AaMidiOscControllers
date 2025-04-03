import Live

from .RemixNet import OSCServer

class Comm():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj
    self.c_instance = self.obj('oCtrlInst')

    # state
    self.m_oOscServer = OSCServer(
      self,
      self.cfg('sTxAddr'),
      self.cfg('nTxPort'),
      self.cfg('sRxAddr'),
      self.cfg('nRxPort'))
    self.m_oCallbackMgr = self.m_oOscServer.callbackManager

    # register in objects hash (after OSCServer init)
    phObj['oComm'] = self

  # ********************************************************

  def reg_rx_cb(self, psAddr, pfHandler):
    self.m_oCallbackMgr.add(pfHandler, '/%s' % (psAddr))

  def reg_indexed_rx_cb(self, psAddr, pnRange, pfHandler):
    for nIdx in range(pnRange):
      self.reg_rx_cb('%s/%d' % (psAddr, nIdx), pfHandler)

  def reg_multi_rx_cb(self, plAddrs, pnRange, pfHandler):
    for sAddr in plAddrs:
      self.reg_indexed_rx_cb(sAddr, pnRange, pfHandler)

  def reg_ns_multi_rx_cb(self, psNs, plAddrs, pnRange, pfHandler):
    for sAddr in plAddrs:
      self.reg_indexed_rx_cb('%s/%s' % (psNs, sAddr), pnRange, pfHandler)

  # ********************************************************

  def proc_msg(self):
    self.m_oOscServer.processIncomingUDP()

  def send_msg(self, psAddr, poMsg):
    self.dlog('-> TX: OSC msg "%s"' % (psAddr))
    self.m_oOscServer.sendOSC(psAddr, poMsg)

  def send_bundle(self, plMsgs):
    self.dlog('-> TX: OSC bundle -> %d messages' % (len(plMsgs)))
    self.m_oOscServer.sendBundle(plMsgs)

  def send_addr_bundle(self, psAddr, plMsgs):
    self.dlog('-> TX: OSC bundle "%s" -> %d messages' % (psAddr, len(plMsgs)))
    hBundle = map(
      lambda x: [psAddr, x],
      plMsgs)
    self.m_oOscServer.sendBundle(list(hBundle))

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

