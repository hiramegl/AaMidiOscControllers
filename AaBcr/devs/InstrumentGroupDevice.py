from .Dev import Dev

class InstrumentGroupDevice(Dev):
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
    self.reg('InstrumentGroupDevice')
    self.parse_cfg()

  def bind_dev(self, poDev, psTrack, psDevName):
    # execute normal bind_dev for 'Device On',
    # macro params and extra params
    Dev.bind_dev(self, poDev, psTrack, psDevName)

    if len(poDev.chains) < 1:
      self.log('-> Device "%s / %s" has no drum pads!' % (poDev.class_name, poDev.name))
      return

    nDrumId   = 0
    oChain    = poDev.chains[0]   # scan only first chain
    oChainDev = oChain.devices[0] # scan only first device
    if oChainDev.class_name == 'DrumGroupDevice':
      if len(oChainDev.drum_pads) < 1:
        self.log('-> Device "%s / %s" has no drum pads!' % (oChainDev.class_name, oChainDev.name))
        return

      for oDrumPad in oChainDev.drum_pads:
        if len(oDrumPad.chains) == 0: continue
        nNote  = oDrumPad.note
        oChain = oDrumPad.chains[0] # check the first chain only (Kick Logical)
        sDrum  = oChain.name

        for oDev in oChain.devices:
          if oDev.class_name == 'OriginalSimpler':
            for oParam in oDev.parameters:
              if oParam.name != 'Volume': continue
              sParam    = 'Drum %d' % (nDrumId)
              hParamCfg = self.get_param_config(sParam)
              tAddr     = hParamCfg['tAddr']
              hParamCfg['oParam'] = oParam
              hParamCfg['sDrum']  = sDrum
              hParamCfg['nMin']   = oParam.min
              hParamCfg['nMax']   = oParam.max
              hParamCfg['sTrack'] = psTrack
              hParamCfg['sDev']   = psDevName
              self.dlog('-> Adding value listener for drum "%s"' % (sDrum))
              self.add_param_listener(oParam, tAddr, sDrum)
              self.dlog('-> Mapping [0x%02X %3d] -> "%s", drum "%7s"' % (tAddr[0], tAddr[1], sParam, sDrum))
              nDrumId += 1

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
      self.dlog('-> address [0x%02X %3d] has no drum assinged!' % (tAddr[0], tAddr[1]))
      self.alert('Track: %s, Dev: %s, Addr: [0x%02X %3d] has NO DRUM!' %
        (phParamCfg['sTrack'], phParamCfg['sDev'], tAddr[0], tAddr[1]))

# InstrumentGroupDevice
# - Params(8)
# - Chain[0] = DrumGroupDevice
#   - No Params
#   - DrumPad[0]
#     - every note:
#       - Chain[0]
#         - OriginalSimpler

#=======================================================================
# Class: InstrumentGroupDevice, Device: Bird Kit, Display: Instrument Rack
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Drive Amount", orig: "Macro 1", value: 104.000000, min: 0.000000, max: 127.000000
#   param: "Drive Color", orig: "Macro 2", value: 43.038891, min: 0.000000, max: 127.000000
#   param: "Drive Output", orig: "Macro 3", value: 72.316666, min: 0.000000, max: 127.000000
#   param: "Dry/Wet", orig: "Macro 4", value: 27.940001, min: 0.000000, max: 127.000000
#   param: "Macro 5", orig: "Macro 5", value: 0.000000, min: 0.000000, max: 127.000000
# ...
#   param: "Macro 16", orig: "Macro 16", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Chain Selector", orig: "Chain Selector", value: 0.000000, min: 0.000000, max: 127.000000
#-----------------------------------------------------------------------
#> Chain "Bird Kit"
#> Chain Device "DrumGroupDevice"
#=======================================================================
# Class: DrumGroupDevice, Device: Bird Kit, Display: Drum Rack
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Macro 1", orig: "Macro 1", value: 0.000000, min: 0.000000, max: 127.000000
# ...
#   param: "Macro 16", orig: "Macro 16", value: 0.000000, min: 0.000000, max: 127.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#> note: 36, chains: 1
#> Chain: Kick Logical
#> Chain Device "OriginalSimpler"
#=======================================================================
# Class: OriginalSimpler, Device: Kick Logical, Display: Simpler
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Snap", orig: "Snap" => [Off, On]
# ...
# Q param: "Pe On", orig: "Pe On" => [Off, On]
#   param: "Volume", orig: "Volume", value: -14.010001, min: -36.000000, max: 36.000000
#   param: "Vol < Vel", orig: "Vol < Vel", value: 0.359375, min: 0.000000, max: 1.000000
# ...
#   param: "Filt < LFO", orig: "Filt < LFO", value: 0.000000, min: 0.000000, max: 24.000000
# Q param: "L On", orig: "L On" => [Off, On]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#> note: 37, chains: 1
#> Chain: Snare Wood Combo Hoosier
#> Chain Device "OriginalSimpler"
# ...
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#> note: 51, chains: 1
#> Chain: Perc Combo Chop
#> Chain Device "OriginalSimpler"
#=======================================================================
# Class: OriginalSimpler, Device: Perc Combo Chop, Display: Simpler
# Q param: "Device On", orig: "Device On" => [Off, On]
# ...
# Q param: "Pe On", orig: "Pe On" => [Off, On]
#   param: "Volume", orig: "Volume", value: -15.000001, min: -36.000000, max: 36.000000
#   param: "Vol < Vel", orig: "Vol < Vel", value: 0.500000, min: 0.000000, max: 1.000000
# ...
#   param: "Filt < LFO", orig: "Filt < LFO", value: 0.000000, min: 0.000000, max: 24.000000
# Q param: "L On", orig: "L On" => [Off, On]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#> Chain Device "Saturator"
#=======================================================================
# Class: Saturator, Device: Saturator, Display: Saturator
# Q param: "Device On", orig: "Device On" => [Off, On]
# ...
#   param: "WS Depth", orig: "WS Depth", value: 0.023438, min: 0.000000, max: 1.000000
