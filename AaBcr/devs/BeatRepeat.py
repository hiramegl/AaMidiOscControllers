from .Dev import Dev

class BeatRepeat(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Repeat        | Block Triplets',
      'Bank0 | nGB1Off | Filter On'                     ,
      'Bank0 | nGB2Off | +Pitch Reset  | +PDecay Reset' ,
      'Bank0 | nGB3Off | +Volume Reset | +Decay Reset'  ,
      #--------------------------------------------------
      'Bank0 | nGR0Off | Mix Type      | Variation Type',
      'Bank0 | nGR1Off | Filter Freq   | Filter Width'  ,
      'Bank0 | nGR2Off | Pitch         | Pitch Decay'   ,
      'Bank0 | nGR3Off | Volume        | Decay'         ,
      #--------------------------------------------------
      'Bank0 | nMB0Off | Device On     | Preset Prev'   ,
      'Bank0 | nMB1Off | Preset Save   | Preset Next'   ,
      #--------------------------------------------------
      'Bank0 | nMR0Off | Interval      | Offset'        ,
      'Bank0 | nMR1Off | Grid          | Variation'     ,
      'Bank0 | nMR2Off | Chance        | Gate'          ,
    ]
    self.reg('BeatRepeat')
    self.parse_cfg()

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName = phParamCfg['sName']
    if sName == 'Pitch Reset':
      self.reset_param_value('Pitch')
    elif sName == 'PDecay Reset':
      self.reset_param_value('Pitch Decay')
    elif sName == 'Volume Reset':
      self.set_param_value('Volume', 0.85)
    elif sName == 'Decay Reset':
      self.reset_param_value('Decay')

#-----------------------------------------------------------------------
# Class: BeatRepeat, Device: Beat Repeat, Display: Beat Repeat
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Chance", orig: "Chance", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Interval", orig: "Interval", value: 5.000000, min: 0.000000, max: 7.000000
#   param: "Offset", orig: "Offset", value: 0.000000, min: 0.000000, max: 15.000000
#   param: "Grid", orig: "Grid", value: 7.000000, min: 0.000000, max: 15.000000
# Q param: "Block Triplets", orig: "Block Triplets" => [Off, On]
#   param: "Variation", orig: "Variation", value: 0.000000, min: 0.000000, max: 10.000000
# Q param: "Variation Type", orig: "Variation Type" => [Trigger, 1/4, 1/8, 1/16, Auto]
#   param: "Gate", orig: "Gate", value: 6.000000, min: 0.000000, max: 18.000000
#   param: "Decay", orig: "Decay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pitch Decay", orig: "Pitch Decay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pitch", orig: "Pitch", value: 0.000000, min: 0.000000, max: 12.000000
# Q param: "Mix Type", orig: "Mix Type" => [Mix, Ins, Gate]
#   param: "Volume", orig: "Volume", value: 0.850000, min: 0.000000, max: 1.000000
# Q param: "Filter On", orig: "Filter On" => [Off, On]
#   param: "Filter Freq", orig: "Filter Freq", value: 0.508950, min: 0.000000, max: 1.000000
#   param: "Filter Width", orig: "Filter Width", value: 4.000000, min: 0.500000, max: 9.000000
# Q param: "Repeat", orig: "Repeat" => [Off, On]
