from .Dev import Dev

class FilterEQ3(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | LowOn'      ,
      'Bank0 | nGB1Off | HighOn'     ,
      'Bank0 | nGB2Off | MidOn'      ,
      'Bank0 | nGB3Off | Slope'      ,
      #-------------------------------
      'Bank0 | nGR0Off | FreqLo'     ,
      'Bank0 | nGR1Off | FreqHi'     ,
      #-------------------------------
      'Bank0 | nMB0Off | Device On'  ,
      'Bank0 | nMB1Off | Preset Next',
      #-------------------------------
      'Bank0 | nMR0Off | GainHi'     ,
      'Bank0 | nMR1Off | GainMid'    ,
      'Bank0 | nMR2Off | GainLo'     ,
    ]
    self.reg('FilterEQ3')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: FilterEQ3, Device: EQ Three, Display: EQ Three
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "GainLo", orig: "GainLo", value: 0.850000, min: 0.000000, max: 1.000000
#   param: "GainMid", orig: "GainMid", value: 0.850000, min: 0.000000, max: 1.000000
#   param: "GainHi", orig: "GainHi", value: 0.850000, min: 0.000000, max: 1.000000
#   param: "FreqLo", orig: "FreqLo", value: 0.349485, min: 0.000000, max: 1.000000
#   param: "FreqHi", orig: "FreqHi", value: 0.561297, min: 0.000000, max: 1.000000
# Q param: "LowOn", orig: "LowOn" => [Off, On]
# Q param: "MidOn", orig: "MidOn" => [Off, On]
# Q param: "HighOn", orig: "HighOn" => [Off, On]
# Q param: "Slope", orig: "Slope" => [24, 48]

