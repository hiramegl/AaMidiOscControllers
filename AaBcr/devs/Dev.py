import re
import os
import time
import math
import datetime
import Live

class Dev():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state (static vars)
    self.m_sClass    = ''
    self.m_sName     = ''
    self.m_bAddPanel = True
    self.m_bUseOrig  = False
    self.m_nBanks    = 0
    self.m_nStrips   = 0
    self.m_lCfg      = []
    self.m_lExtra    = []
    self.m_hParamMap = {} # param addreses map, {sParamName: (nBankId, nId)}

    # bind vars (volatile)
    self.m_oDev       = None
    self.m_hBankIdMap = {} # {nId: hParamCfg}
    self.m_nBankOff   = 0
    self.m_nStripOff  = 0

  # ********************************************************

  def reg(self, psClass, psName = 'x'):
    self.m_sClass = psClass
    self.m_sName  = psName
    self.obj('oRouter').reg(psClass, psName, self)

  def add_to_sync_devs(self):
    self.obj('oRouter').add_sync_dev(self)

  def update_sync_params(self):
    pass # can be overriden by subclasses

  def get_qual_name(self):
    return '%s-%s' % (self.m_sClass, self.m_sName)

  def parse_cfg(self):
    for sCfg in self.m_lCfg:
      lParts  = re.split(r'\s+\|\s+', sCfg.strip())
      nBankId = int(lParts[0][4]) # 'Bank0' -> 0
      sRowId  = lParts[1]         # nGB0Off, nGR0Off, ..., nMR2Off
      lParams = lParts[2:]        # [Device On, Preset Save, ... ]
      nParams = len(lParams)
      nRootId = self.cfg(sRowId)

      if nBankId > self.m_nBanks:
          self.m_nBanks = nBankId # update number of banks

      if nParams > self.m_nStrips:
        self.m_nStrips = nParams # update number of strips

      for nIdx in range(nParams):
        sParam = lParams[nIdx].replace('_', ' ')
        if sParam == '-': continue
        if sParam[0] == '+':
          sParam = sParam[1:]
          self.m_lExtra.append(sParam)
        nId = nRootId + nIdx
        self.m_hParamMap[sParam] = (nBankId, nId) # tAddr (relative)

    self.m_nBanks += 1
    self.dlog('-> Found %d banks / %d strips and mapped %d params for "%s"' % (self.m_nBanks, self.m_nStrips, len(self.m_hParamMap.keys()), self.get_qual_name()))

  def get_banks(self):
    return self.m_nBanks

  def get_strips(self):
    return self.m_nStrips

  # ********************************************************

  def bind_dev(self, poDev):
    self.m_oDev = poDev
    for oParam in poDev.parameters:
      sParam = oParam.original_name if self.m_bUseOrig else oParam.name
      if sParam in self.m_hParamMap:
        tAddr = self.m_hParamMap[sParam]
        if tAddr in self.m_hBankIdMap:
          self.log('-> PARAM ALREADY MAPPED "%s" -> [Bank: %d, Id: %d]' % (sParam, tAddr[0], tAddr[1]))
        else:
          self.dlog('-> Dev: Logic route [0x%02X %3d] -> "%s"' % (tAddr[0], tAddr[1], sParam))
          self.m_hBankIdMap[tAddr] = {
            'tAddr' : tAddr,
            'sType' : 'param',
            'sName' : sParam,
            'oParam': oParam,
            'nMin'  : oParam.min,
            'nMax'  : oParam.max,
          }
          self.customize_param(self.m_hBankIdMap[tAddr])
          self.dlog('-> Dev: Adding value listener for "%s"' % (sParam))
          self.add_param_listener(oParam, tAddr)
      else:
        self.dlog('-> PARAM NOT MAPPED: "%s"' % (sParam))

    if self.m_bAddPanel:
      self.add_panel_params()
    self.add_extra_params()

  def customize_param(self, phParamCfg):
    pass # should be overriden by subclasses

  def add_param_listener(self, poParam, ptAddr):
    fTxCb = lambda :self.handle_param_tx_msg(ptAddr)
    poParam.add_value_listener(fTxCb)
    self.m_hBankIdMap[ptAddr]['fTxCb'] = fTxCb

  def handle_param_tx_msg(self, ptAddr):
    hParamCfg = self.m_hBankIdMap[ptAddr]
    self.dlog('-> Value updated for "%s" -> %s' % (hParamCfg['sName'], str(hParamCfg['oParam'].value)))
    self.send_msg(self.get_param_tx_msg(hParamCfg))

  def add_panel_params(self):
    lPanelParams = ['Preset Save', 'Preset Prev', 'Preset Next']
    for sParam in lPanelParams:
      if sParam in self.m_hParamMap:
        self.map_special_param(sParam, 'panel')
      else:
        self.log('-> PARAM "%s" NOT MAPPED FOR DEVICE "%s"' % (sParam, self.get_qual_name()))

  def add_extra_params(self):
    for sParam in self.m_lExtra:
      self.map_special_param(sParam, 'extra')
      self.customize_param(self.get_param_config(sParam))

  def map_special_param(self, psParam, psType):
    tAddr = self.m_hParamMap[psParam]
    self.dlog('-> Dev: Logic route [0x%02X %3d] -> "%s" [%s]' % (tAddr[0], tAddr[1], psParam, psType))
    self.m_hBankIdMap[tAddr] = {
      'tAddr': tAddr,
      'sType': psType,
      'sName': psParam,
    }

  def set_offsets(self, pnBankOff, pnStripOff):
    self.dlog('-> Device "%s" at BankOff: %d, StripOff: %d' % (self.get_qual_name(), pnBankOff, pnStripOff))
    self.m_nBankOff  = pnBankOff
    self.m_nStripOff = pnStripOff

  def unbind_dev(self):
    for hParamCfg in self.m_hBankIdMap.values():
      self.remove_param_bindings(hParamCfg)
    self.m_hBankIdMap.clear()
    self.m_oDev = None

  def remove_param_bindings(self, phParamCfg):
    sType = phParamCfg['sType']
    if sType == 'param':
      oParam = phParamCfg['oParam']
      fTxCb  = phParamCfg['fTxCb']
      self.dlog('-> Removing value listener for "%s"' % (phParamCfg['sName']))
      oParam.remove_value_listener(fTxCb)
    elif sType == 'extra':
      self.remove_extra_param_bindings(phParamCfg)
    elif sType == 'panel':
      pass # nothing to do for panel commands
    else:
      self.dlog('-> No bindings removed for %s' % (phParamCfg['sName']))

  def remove_extra_param_bindings(self, phParamCfg):
    pass # can be overriden by subclasses

  # ********************************************************

  def handle_rx_msg(self, pnBankAbs, pnIdAbs, pnValue):
    nBankRel = pnBankAbs - self.m_nBankOff
    nIdRel   = pnIdAbs   - self.m_nStripOff
    tAddr    = (nBankRel, nIdRel)
    self.dlog('-> Dev Rx: [0x%02X %3d] -> %d' % (nBankRel, nIdRel, pnValue))

    if tAddr in self.m_hBankIdMap:
      hParamCfg = self.m_hBankIdMap[tAddr]
      self.handle_rx_value(hParamCfg, pnValue)
    else:
      self.log('-> Dev "%s" has no parameter mapped to [0x%02X %3d], dropping message' % (nBankRel, nIdRel))

  def handle_rx_value(self, phParamCfg, pnValue):
    sType = phParamCfg['sType']

    if sType == 'panel': # is a panel function
      self.dlog('-> Handling panel function %s' % (phParamCfg['sName']))
      self.tx_msg(phParamCfg['tAddr'], 127) # panel functions always ON!
      self.handle_panel_cmd(phParamCfg['sName'])

    elif sType == 'extra':
      self.handle_rx_msg_extra_cmd(phParamCfg, pnValue)

    elif sType == 'param':
      oParam = phParamCfg['oParam']
      if oParam.is_quantized:
        nValues = len(oParam.value_items)
        if nValues == 2:
          nValue = int(pnValue / 127)
        elif nValues <= 11:
          nScale = 10                    # float(127.0 / nValues)
          nValue = int(pnValue / nScale) # int(pnValue / nScale)
          if nValue >= len(oParam.value_items):
            nValue = len(oParam.value_items) - 1
        else:
          nScale = float(127.0 / nValues)
          nValue = int(pnValue / nScale)
      else:
        nValue = self.get_scaled_rx_value(phParamCfg, pnValue)
      oParam.value = nValue

    self.dlog('-> Updating "%s": %d -> %f' % (phParamCfg['sName'], pnValue, nValue))

  def get_scaled_rx_value(self, phParamCfg, pnValue):
    nValue = float(pnValue) / 127.0
    nMin   = phParamCfg['nMin']
    nMax   = phParamCfg['nMax']
    return nValue * (nMax - nMin) + nMin

  # ********************************************************

  def handle_panel_cmd(self, psCmd):
    if psCmd == 'Preset Save':
      sTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
      sName = '%s_%s' % (sTime, self.get_qual_name()) # Preset Name
      self.alert('> STORING "%s"' % (sName))

      sHome       = os.getenv('HOME')
      sPresetsDir = 'Music/Ableton/User Library/Remote Scripts/AaBcr/presets'
      sFilePath   = '%s/%s/%s_presets.txt' % (sHome, sPresetsDir, self.get_qual_name())
      bFileExists = os.path.isfile(sFilePath)

      # Lineup is the first row in the presets file which
      # specifies the order in which the parameters are stored
      if bFileExists:
        with open(sFilePath) as oFile:
          sLineup = oFile.readline().strip('\n')
        aLineup = sLineup.split(':')[1].split('|')
        oFile = open(sFilePath, 'a')
      else:
        oFile   = open(sFilePath, 'w')
        aLineup = []
        for oParam in self.m_oDev.parameters:
          if oParam.original_name == 'Device On': continue
          aLineup.append(oParam.original_name)
        aLineup.sort()
        sLineup = '|'.join(aLineup)
        oFile.write('@params:%s\n' % (sLineup))

      # write the values in the presets file
      aStrValues = []
      for sParam in aLineup:
        hParamCfg = self.get_param_config(sParam)
        oValue    = hParamCfg['oParam'].value
        aStrValues.append(str(oValue))
      sStrValues = '|'.join(aStrValues)
      oFile.write('%s:%s\n' % (sName, sStrValues))
      oFile.close()

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    pass # should be overriden by subclasses

  def get_param_config(self, psParam):
    return self.m_hBankIdMap[self.m_hParamMap[psParam]]

  def get_param_value(self, psParam):
    return self.get_param_config(psParam)['oParam'].value

  def set_param_value(self, psParam, poValue):
    self.get_param_config(psParam)['oParam'].value = poValue

  def reset_param_value(self, psParam):
    self.set_param_value(psParam, 0)

  def add_to_param_value(self, psParam, pnDelta):
    self.set_param_value(
      psParam,
      self.get_param_value(psParam) + pnDelta)

  # ********************************************************

  def sync_dev(self, pnBankChn):
    if pnBankChn in range(self.m_nBankOff, self.m_nBankOff + self.m_nBanks):
      lBundle = []
      for hParamCfg in self.m_hBankIdMap.values():
        lMsg = self.get_param_tx_msg(hParamCfg)
        lBundle.append(lMsg)
      self.obj('oComm').send_bundle(lBundle)

  def get_param_tx_msg(self, phParamCfg):
    sType = phParamCfg['sType']

    if sType == 'panel': # is a panel function
      nValue = 127 # all panel functions always ON!
    elif sType == 'extra':
      nValue = self.get_extra_param_tx_value(phParamCfg)
    elif sType == 'param':
      oParam = phParamCfg['oParam']
      if oParam.is_quantized:
        nValues = len(oParam.value_items)
        if nValues == 2:
          nValue = int(oParam.value) * 127
        elif nValues <= 11:
          nScale = 10                         # int(127.0 / nValues)
          nValue = int(oParam.value * nScale) # int(oParam.value) * nScale
        else:
          nScale = int(127.0 / nValues)
          nValue = int(oParam.value) * nScale
      else:
        nValue = self.get_scaled_tx_value(phParamCfg, oParam.value)

    sName = phParamCfg['sName']
    lMsg  = self.to_physical_msg(phParamCfg['tAddr'], nValue)
    self.dlog('-> Tx [0x%02X %3d %3d] -> "%s"' % (lMsg[0], lMsg[1], lMsg[2], sName))
    return lMsg

  def to_physical_msg(self, ptAddr, pnValue):
    nBankChn = 0xB0 | (ptAddr[0] + self.m_nBankOff)
    nId      =         ptAddr[1] + self.m_nStripOff
    return [nBankChn, nId, int(pnValue)]

  def get_extra_param_tx_value(self, phParamCfg):
    return 0 # can be overriden by subclasses

  def get_scaled_tx_value(self, phParamCfg, pnValue):
    nMin   = phParamCfg['nMin']
    nMax   = phParamCfg['nMax']
    nValue = (pnValue - nMin) / (nMax - nMin)
    return int(nValue * 127)

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def song(self):
    return self.obj('oSong')

  def send_msg(self, plMsg):
    self.obj('oComm').send_msg(plMsg)

  def tx_msg(self, ptAddr, pnValue):
    self.send_msg(self.to_physical_msg(ptAddr, pnValue))

  def tx_param_msg(self, psName, pnValue):
    tAddr = self.get_param_config(psName)['tAddr']
    self.tx_msg(tAddr, pnValue)

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

  def alert(self, sMessage):
    self.obj('oCtrlInst').show_message(sMessage)

