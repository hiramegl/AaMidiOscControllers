from .Dev import Dev

class EchoOut(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_bAddPanel = False # Do not add panel commands (Preset Save, etc.)
    self.m_bUseOrig  = True  # use original parameter name: Macro 1, Macro 2, etc.
    self.m_lCfg = [
      'Bank0 | nGB0Off | Macro 14  | Macro 15',
      'Bank0 | nGB0Off | Macro 16'            ,
      #----------------------------------------
      'Bank0 | nGR0Off | Macro 7   | Macro 8' ,
      'Bank0 | nGR1Off | Macro 9   | Macro 10',
      'Bank0 | nGR2Off | Macro 11  | Macro 12',
      'Bank0 | nGR3Off | Macro 13  | Macro 14',
      #----------------------------------------
      'Bank0 | nMB0Off | Device On | +EchoOut',
      #----------------------------------------
      'Bank0 | nMR0Off | Macro 1   | Macro 2' ,
      'Bank0 | nMR1Off | Macro 3   | Macro 4' ,
      'Bank0 | nMR2Off | Macro 5   | Macro 6' ,
    ]
    self.reg('AudioEffectGroupDevice', 'EchoOut')
    self.parse_cfg()

  def get_extra_param_tx_value(self, phParamCfg):
    sName = phParamCfg['sName']
    if sName == 'EchoOut':
      return 127

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName = phParamCfg['sName']
    if sName == 'EchoOut':
      self.set_param_value('Macro 1', 127.0)
      self.tx_param_msg('Macro 1', 127)

# ========================================================================
# > Class: AudioEffectGroupDevice, Device: EchoOut, Display: Audio Effect Rack
# > Q param: "Device On", orig: "Device On" => [Off, On]
# >   param: "Chain Selector", orig: "Macro 1", value: 127.000000, min: 0.000000, max: 127.000000
# >   param: "L 16th", orig: "Macro 2", value: 104.000000, min: 0.000000, max: 127.000000
# >   param: "Dry/Wet", orig: "Macro 3", value: 127.000000, min: 0.000000, max: 127.000000
# >   param: "Feedback", orig: "Macro 4", value: 100.000000, min: 0.000000, max: 127.000000
# >   param: "Filter Freq", orig: "Macro 5", value: 68.000000, min: 0.000000, max: 127.000000
# >   param: "Filter Width", orig: "Macro 6", value: 127.000000, min: 0.000000, max: 127.000000
# >   param: "L Sync", orig: "Macro 7", value: 127.000000, min: 0.000000, max: 127.000000
# >   param: "L Time", orig: "Macro 8", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 9", orig: "Macro 9", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 10", orig: "Macro 10", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 11", orig: "Macro 11", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 12", orig: "Macro 12", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 13", orig: "Macro 13", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 14", orig: "Macro 14", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 15", orig: "Macro 15", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Macro 16", orig: "Macro 16", value: 0.000000, min: 0.000000, max: 127.000000
# >   param: "Chain Selector", orig: "Chain Selector", value: 127.000000, min: 0.000000, max: 127.000000
# ------------------------------------------------------------------------
# -> Chain "Dry"
# ------------------------------------------------------------------------
# -> Chain "Wet"
# -> Chain Device "Delay"
# ========================================================================
# > Class: Delay, Device: Delay, Display: Delay
# > Q param: "Device On", orig: "Device On" => [Off, On]
# > Q param: "Delay Mode", orig: "Delay Mode" => [Repitch, Fade, Jump]
# > Q param: "Link", orig: "Link" => [Off, On]
# > Q param: "Ping Pong", orig: "Ping Pong" => [Off, On]
# > Q param: "L Sync", orig: "L Sync" => [Off, On]
# > Q param: "R Sync", orig: "R Sync" => [Off, On]
# >   param: "L Time", orig: "L Time", value: 0.595385, min: 0.000000, max: 1.000000
# >   param: "R Time", orig: "R Time", value: 0.595385, min: 0.000000, max: 1.000000
# > Q param: "L 16th", orig: "L 16th" => [1, 2, 3, 4, 5, 6, 8, 16]
# > Q param: "R 16th", orig: "R 16th" => [1, 2, 3, 4, 5, 6, 8, 16]
# >   param: "L Offset", orig: "L Offset", value: 0.500000, min: 0.000000, max: 1.000000
# >   param: "R Offset", orig: "R Offset", value: 0.500000, min: 0.000000, max: 1.000000
# >   param: "Feedback", orig: "Feedback", value: 0.787402, min: 0.000000, max: 1.000000
# > Q param: "Freeze", orig: "Freeze" => [Off, On]
# > Q param: "Filter On", orig: "Filter On" => [Off, On]
# >   param: "Filter Freq", orig: "Filter Freq", value: 0.535433, min: 0.000000, max: 1.000000
# >   param: "Filter Width", orig: "Filter Width", value: 1.000000, min: 0.000000, max: 1.000000
# >   param: "Mod Freq", orig: "Mod Freq", value: 0.471666, min: 0.000000, max: 1.000000
# >   param: "Dly < Mod", orig: "Dly < Mod", value: 0.000000, min: 0.000000, max: 1.000000
# >   param: "Filter < Mod", orig: "Filter < Mod", value: 0.000000, min: 0.000000, max: 1.000000
# >   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
