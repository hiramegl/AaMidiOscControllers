from .Dev import Dev

class DrumGroupDevice(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_bAddPanel = False # Do not add panel commands (Preset Save, etc.)
    self.m_bUseOrig  = True  # use original parameter name: Macro 1, Macro 2, etc.
    self.m_lCfg = [
      'Bank0 | nGR0Off | +Drum 16 | +Drum 17 | +Drum 18 | +Drum 19 | +Drum 12 | +Drum 13 | +Drum 14 | +Drum 15',
      'Bank0 | nGR1Off | +Drum 24 | +Drum 25 | +Drum 26 | +Drum 27 | +Drum 20 | +Drum 21 | +Drum 22 | +Drum 23',
      'Bank0 | nGR2Off | +Drum 32 | +Drum 33 | +Drum 34 | +Drum 35 | +Drum 28 | +Drum 28 | +Drum 30 | +Drum 31',
      'Bank0 | nGR3Off | +Drum 41 | +Drum 42 | +Drum 43 | +Drum 44 | +Drum 36 | +Drum 37 | +Drum 38 | +Drum 40',
      #---------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On'                                                                            ,
      #---------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Macro 1  | Macro 2  | Macro 3  | Macro 4  | +Drum 8  | +Drum 9  | +Drum 10 | +Drum 11',
      'Bank0 | nMR1Off | Macro 5  | Macro 6  | Macro 7  | Macro 8  | +Drum 4  | +Drum 5  | +Drum 6  | +Drum 7' ,
      'Bank0 | nMR2Off | Macro 9  | Macro 10 | Macro 11 | Macro 12 | +Drum 0  | +Drum 1  | +Drum 2  | +Drum 3' ,
    ]
    self.reg('DrumGroupDevice')
    self.parse_cfg()

  def bind_dev(self, poDev, psTrack, psDevName):
    # execute normal bind_dev for 'Device On',
    # macro params and extra params
    Dev.bind_dev(self, poDev, psTrack, psDevName)

    if len(poDev.drum_pads) < 1:
      self.log('-> Device "%s / %s" has no drum pads!' % (poDev.class_name, poDev.name))
      return

    # assign drum volume params for extra params,
    # look for OriginalSimpler devices
    nDrumId = 0
    for oDrumPad in poDev.drum_pads:
      if len(oDrumPad.chains) == 0: continue
      nNote  = oDrumPad.note
      oChain = oDrumPad.chains[0] # check the first chain only (Bassdrum)
      sDrum  = oChain.name

      for oChainDev in oChain.devices:
        if oChainDev.class_name == 'InstrumentGroupDevice':
          oChain2 = oChainDev.chains[0] # check the first chain only (Kick 606)
          for oDev in oChain2.devices:
            if oDev.class_name == 'OriginalSimpler':
              nDrumId = self.add_volume_bindings(oDev, nDrumId, sDrum, psTrack, psDevName)
        elif oChainDev.class_name == 'OriginalSimpler':
          nDrumId = self.add_volume_bindings(oChainDev, nDrumId, sDrum, psTrack, psDevName)

  def add_volume_bindings(self, poDev, pnDrumId, psDrum, psTrack, psDevName):
    for oParam in poDev.parameters:
      if oParam.name != 'Volume': continue
      sParam    = 'Drum %d' % (pnDrumId)
      hParamCfg = self.get_param_config(sParam)
      tAddr     = hParamCfg['tAddr']
      hParamCfg['oParam'] = oParam
      hParamCfg['sDrum']  = psDrum
      hParamCfg['nMin']   = oParam.min
      hParamCfg['nMax']   = oParam.max
      hParamCfg['sTrack'] = psTrack
      hParamCfg['sDev']   = psDevName
      self.dlog('-> Adding value listener for drum "%s"' % (psDrum))
      self.add_param_listener(oParam, tAddr, psDrum)
      self.dlog('-> Mapping [0x%02X %3d] -> "%s", drum "%7s"' % (tAddr[0], tAddr[1], sParam, psDrum))
      return pnDrumId + 1

  def get_extra_param_tx_value(self, phParamCfg):
    if 'oParam' in phParamCfg:
      oParam = phParamCfg['oParam']
      return self.get_scaled_tx_value(phParamCfg, oParam.value)
    else:
      return 0

  def remove_extra_param_bindings(self, phParamCfg):
    if 'oParam' in phParamCfg:
      oParam = phParamCfg['oParam']
      if 'fTxCb' in phParamCfg:
        fTxCb = phParamCfg['fTxCb']
        self.dlog('-> Removing value listener for drum "%s"' % (phParamCfg['sDrum']))
        if oParam.value_has_listener(fTxCb):
          oParam.remove_value_listener(fTxCb)
      phParamCfg['oParam'] = None

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    if 'oParam' in phParamCfg:
      sDrum  = phParamCfg['sDrum']
      oParam = phParamCfg['oParam']
      nValue = self.get_scaled_rx_value(phParamCfg, pnValue)
      oParam.value = nValue
      self.dlog('-> updating "%s/%s" with value %f' % (sDrum, oParam.name, nValue))
      self.alert('Track: %s, Dev: %s, Drum: %s -> %d (%f)' %
        (phParamCfg['sTrack'], phParamCfg['sDev'], sDrum, pnValue, nValue))
    else:
      tAddr = phParamCfg['tAddr']
      self.dlog('-> address [0x%02X %3d] has no drum assigned!' % (tAddr[0], tAddr[1]))
      self.alert('Track: %s, Dev: %s, Addr: [0x%02X %3d] has NO DRUM!' %
        (phParamCfg['sTrack'], phParamCfg['sDev'], tAddr[0], tAddr[1]))

# DrumGroupDevice
# - Params(8)
# - DrumPad[0]
#   - every note
#     - Chain[0] = InstrumentGroupDevice
#       - Chain[0] = Kick 606
#         - Device[0] = OriginalSimpler

#-----------------------------------------------------------------------
# Class: DrumGroupDevice, Device: 606 Core Kit, Display: Drum Rack
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Low Gain  ", orig: "Macro 1", value: 63.352802, min: 0.000000, max: 127.000000
#   param: "Mid Gain", orig: "Macro 2", value: 63.500000, min: 0.000000, max: 127.000000
#   param: "High Gain", orig: "Macro 3", value: 63.352802, min: 0.000000, max: 127.000000
#   param: "Gain", orig: "Macro 4", value: 47.679195, min: 0.000000, max: 127.000000
#   param: "Drive Amount", orig: "Macro 5", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Drive Tone", orig: "Macro 6", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Glue", orig: "Macro 7", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Vintage", orig: "Macro 8", value: 0.000000, min: 0.000000, max: 127.000000
#   ...
#   param: "Macro 16", orig: "Macro 16", value: 126.007812, min: 0.000000, max: 127.000000
#-----------------------------------------------------------------------
#> note: 36, chains: 1
#> Chain: Bassdrum
#> Chain Device "InstrumentGroupDevice"
#-----------------------------------------------------------------------
# Class: InstrumentGroupDevice, Device: Bassdrum, Display: Instrument Rack
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Tune", orig: "Macro 1", value: 63.500000, min: 0.000000, max: 127.000000
#   param: "Level", orig: "Macro 2", value: 107.950005, min: 0.000000, max: 127.000000
#   param: "Decay", orig: "Macro 3", value: 0.000000, min: 0.000000, max: 127.000000
#   ...
#   param: "Macro 16", orig: "Macro 16", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Chain Selector", orig: "Chain Selector", value: 0.000000, min: 0.000000, max: 127.000000
#-----------------------------------------------------------------------
#> Chain "Kick 606"
#> Chain Device "OriginalSimpler"
#-----------------------------------------------------------------------
# Class: OriginalSimpler, Device: Kick 606, Display: Simpler
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Snap", orig: "Snap" => [Off, On]
#   param: "Sample Selector", orig: "Sample Selector", value: 0.000000, min: 0.000000, max: 127.000000
#   ...
#   param: "Pe R < Vel", orig: "Pe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Volume", orig: "Volume", value: -12.000000, min: -36.000000, max: 36.000000
#   param: "Vol < Vel", orig: "Vol < Vel", value: 0.500000, min: 0.000000, max: 1.000000
#   ...
# Q param: "L Retrig", orig: "L Retrig" => [Off, On]
#   param: "L Offset", orig: "L Offset", value: 0.000000, min: 0.000000, max: 360.000000
#-----------------------------------------------------------------------
#> note: 37, chains: 1
#
# ...
#
#-----------------------------------------------------------------------
#> note: 51, chains: 1
#> Chain: Cymbal Mod
#> Chain Device "InstrumentGroupDevice"
#-----------------------------------------------------------------------
# Class: InstrumentGroupDevice, Device: Cymbal Mod, Display: Instrument Rack
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Tune", orig: "Macro 1", value: 63.500000, min: 0.000000, max: 127.000000
#   param: "Level", orig: "Macro 2", value: 107.950005, min: 0.000000, max: 127.000000
#   param: "Decay", orig: "Macro 3", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Macro 4", orig: "Macro 4", value: 0.000000, min: 0.000000, max: 127.000000
#   ...
#   param: "Macro 16", orig: "Macro 16", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Chain Selector", orig: "Chain Selector", value: 0.000000, min: 0.000000, max: 127.000000
#-----------------------------------------------------------------------
#> Chain "Cymbal 606"
#> Chain Device "OriginalSimpler"
#-----------------------------------------------------------------------
# Class: OriginalSimpler, Device: Cymbal 606, Display: Simpler
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Snap", orig: "Snap" => [Off, On]
#   param: "Sample Selector", orig: "Sample Selector", value: 0.000000, min: 0.000000, max: 127.000000
#   ...
#   param: "Pe R < Vel", orig: "Pe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Volume", orig: "Volume", value: -12.000000, min: -36.000000, max: 36.000000
#   param: "Vol < Vel", orig: "Vol < Vel", value: 0.220472, min: 0.000000, max: 1.000000
#   ...
# Q param: "L Retrig", orig: "L Retrig" => [Off, On]
#   param: "L Offset", orig: "L Offset", value: 0.000000, min: 0.000000, max: 360.000000
