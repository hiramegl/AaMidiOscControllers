from .Dev import Dev

class Redux2(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Pre-Filter On'  ,
      'Bank0 | nGB1Off | Post-Filter On' ,
      'Bank0 | nGB2Off | DC Shift'       ,
      #-----------------------------------
      'Bank0 | nGR0Off | Post-Filter'    ,
      'Bank0 | nGR1Off | Bit Depth'      ,
      'Bank0 | nGR2Off | Quantizer Shape',
      #-----------------------------------
      'Bank0 | nMB0Off | Device On'      ,
      'Bank0 | nMB1Off | Preset Next'    ,
      #-----------------------------------
      'Bank0 | nMR0Off | Sample Rate'    ,
      'Bank0 | nMR1Off | Jitter'         ,
      'Bank0 | nMR2Off | Dry/Wet'        ,
    ]
    self.reg('Redux2')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Redux2, Device: Redux, Display: Redux
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Sample Rate", orig: "Sample Rate", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Jitter", orig: "Jitter", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Bit Depth", orig: "Bit Depth", value: 16.000000, min: 1.000000, max: 16.000000
#   param: "Quantizer Shape", orig: "Quantizer Shape", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "DC Shift", orig: "DC Shift" => [Off, On]
# Q param: "Pre-Filter On", orig: "Pre-Filter On" => [Off, On]
# Q param: "Post-Filter On", orig: "Post-Filter On" => [Off, On]
#   param: "Post-Filter", orig: "Post-Filter", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
