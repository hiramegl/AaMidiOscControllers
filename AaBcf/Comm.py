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
    self.m_oCallbackMgr.add(self.handle_osc, self.cfg('sOscAddr'))
    self.m_hMidiReg = {}

    # register in objects hash (after OSCServer init)
    phObj['oComm'] = self

  # ********************************************************

  def reg_cc(self, pnChn, pnId, poParam, pfHandler = None):
    tKey = ((0xB0 | pnChn), pnId)
    self.dlog('----> Reg cc: 0x%X %d' % (tKey[0], tKey[1]))
    self.m_hMidiReg[tKey] = {
      'oParam'  : poParam,
      'fHandler': pfHandler,
    }
    return tKey

  # ********************************************************

  def handle_osc(self, paMsg):
    self.dlog("----> Rx: %s [%s]: 0x%X %d %d" % (paMsg[0], paMsg[1], paMsg[2], paMsg[3], paMsg[4]))
    self.update_param_value(tuple(paMsg[2:4]), paMsg[4])

  def update_param_value(self, ptKey, pnValue):
    if ptKey in self.m_hMidiReg:
      if self.m_hMidiReg[ptKey]['fHandler'] != None:
        self.m_hMidiReg[ptKey]['fHandler'](ptKey, pnValue)
      else:
        self.m_hMidiReg[ptKey]['oParam'].value = float(pnValue) / 127.0
    else:
      self.dlog("----> Rx: No control mapped to 0x%X %d" % (ptKey[0], ptKey[1]))

  def update_midi_ctrl(self, ptKey):
    if ptKey in self.m_hMidiReg:
      nValue = int(self.m_hMidiReg[ptKey]['oParam'].value * 127.0)
      self.dlog("----> Tx: 0x%X %d %d" % (ptKey[0], ptKey[1], nValue))
      self.m_oOscServer.sendOSC(self.cfg('sOscAddr'), [ptKey[0], ptKey[1], nValue])
    else:
      self.dlog("----> Tx: No control mapped to 0x%X %d" % (ptKey[0], ptKey[1]))

  # ********************************************************

  def proc_msg(self):
    self.m_oOscServer.processIncomingUDP()

  def send_msg(self, plMsg):
    sOscAddr = self.cfg('sOscAddr')
    self.dlog('-> TX: OSC msg "%s" -> [0x%X %d %d]' % (sOscAddr, plMsg[0], plMsg[1], plMsg[2]))
    self.m_oOscServer.sendOSC(
      self.cfg('sOscAddr'),
      plMsg)

  def send_bundle(self, plMsgs):
    sOscAddr = self.cfg('sOscAddr')
    self.dlog('-> TX: OSC bundle "%s" -> %d messages' % (sOscAddr, len(plMsgs)))
    hBundle = map(
      lambda x: [sOscAddr, x],
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

