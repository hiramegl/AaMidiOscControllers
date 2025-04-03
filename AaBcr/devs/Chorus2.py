from .Dev import Dev

class Chorus2(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | FB Inv'                   ,
      'Bank0 | nGB1Off | HPF Enabled'              ,
      #---------------------------------------------
      'Bank0 | nGR0Off | Mode        | Width'      ,
      'Bank0 | nGR1Off | HPF Freq'                 ,
      'Bank0 | nGR2Off | Offset      | Shape'      ,
      #---------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev',
      'Bank0 | nMB1Off | Preset Save | Preset Next',
      #---------------------------------------------
      'Bank0 | nMR0Off | Rate        | Gain'       ,
      'Bank0 | nMR1Off | Amount      | Warmth'     ,
      'Bank0 | nMR2Off | Feedback    | Dry/Wet'    ,
    ]
    self.reg('Chorus2')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Chorus2, Device: Chorus-Ensemble, Display: Chorus-Ensemble
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Mode", orig: "Mode" => [Classic, Ensemble, Vibrato]
#   param: "Shape", orig: "Shape", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Rate", orig: "Rate", value: 0.415518, min: 0.000000, max: 1.000000
#   param: "Amount", orig: "Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Feedback", orig: "Feedback", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "FB Inv", orig: "FB Inv" => [Off, On]
#   param: "Offset", orig: "Offset", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "HPF Enabled", orig: "HPF Enabled" => [Off, On]
#   param: "HPF Freq", orig: "HPF Freq", value: 0.284178, min: 0.000000, max: 1.000000
#   param: "Width", orig: "Width", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Warmth", orig: "Warmth", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Gain", orig: "Gain", value: 0.707107, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 0.500000, min: 0.000000, max: 1.000000

