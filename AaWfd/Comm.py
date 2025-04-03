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
    self.m_hCcReg    = {}
    self.m_hSysexReg = {}
    self.m_hProgReg  = {}

    # register in objects hash (after OSCServer init)
    phObj['oComm'] = self

  # ********************************************************

  def reg_cc(self, pnChn, pnId, poParam, pfHandler = None):
    tKey = ((0xB0 | pnChn), pnId)
    self.dlog('----> Reg cc: 0x%X %d' % (tKey[0], tKey[1]))
    self.m_hCcReg[tKey] = {
      'oParam'  : poParam,
      'fHandler': pfHandler,
    }
    return tKey

  def reg_sysex(self, pfHandler = None):
    nByte = 0xF0
    self.dlog('----> Reg sysex: 0x%X' % (nByte))
    self.m_hSysexReg[nByte] = {
      'sType'   : 'sysex',
      'fHandler': pfHandler,
    }
    return nByte

  def reg_prch(self, pnProgId, pfHandler = None):
    nByte = (0xC0 | pnProgId)
    self.dlog('----> Reg prog_change: 0x%X' % (nByte))
    self.m_hProgReg[nByte] = {
      'sType'   : 'prog_change',
      'fHandler': pfHandler,
    }
    return nByte

  # ********************************************************

  def handle_osc(self, paMsg):
    sAddr = paMsg[0]
    sType = paMsg[1]
    if len(paMsg) == 5: # cc messages
      self.dlog("----> Rx CC: %s [%s]: 0x%X %d %d" % (sAddr, sType, paMsg[2], paMsg[3], paMsg[4]))
      self.handle_cc_msg(tuple(paMsg[2:4]), paMsg[4])
    elif paMsg[2] == 0xF0: # sysex messages
      self.dlog("----> Rx SYSEX: %s [%s]: 0x%X, len: %d" % (sAddr, sType, paMsg[2], len(paMsg) - 4))
      self.handle_sysex_msg(paMsg[2], paMsg)
    elif len(paMsg) == 4: # program change message
      self.dlog("----> Rx PRCH: %s [%s]: 0x%X %d" % (sAddr, sType, paMsg[2], paMsg[3]))
      self.handle_prch_msg(paMsg[2], paMsg[3])

  def handle_cc_msg(self, ptKey, pnValue):
    if ptKey in self.m_hCcReg:
      if self.m_hCcReg[ptKey]['fHandler'] != None:
        self.m_hCcReg[ptKey]['fHandler'](ptKey, pnValue)
      else:
        self.m_hCcReg[ptKey]['oParam'].value = float(pnValue) / 127.0
    else:
      self.dlog("----> Rx: No control or sysex mapped to 0x%X %d" % (ptKey[0], ptKey[1]))

  def handle_sysex_msg(self, pnByte, paMsg):
    if pnByte in self.m_hSysexReg:
      self.m_hSysexReg[pnByte]['fHandler'](pnByte, paMsg)
    else:
      self.dlog("----> Rx: No sysex mapped to 0x%X" % (pnByte))

  def handle_prch_msg(self, pnProgId, pnValue):
    if pnProgId in self.m_hProgReg:
      self.m_hProgReg[pnProgId]['fHandler'](pnProgId, pnValue)
    else:
      self.dlog("----> Rx: No prog change mapped to 0x%X, value: %d" % (pnProgId, pnValue))

  def update_midi_ctrl(self, ptKey):
    if ptKey in self.m_hCcReg:
      nValue = int(self.m_hCcReg[ptKey]['oParam'].value * 127.0)
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

