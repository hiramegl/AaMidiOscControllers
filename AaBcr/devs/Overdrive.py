from .Dev import Dev

class Overdrive(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | Filter Freq'      ,
      'Bank0 | nGR1Off | Filter Width'     ,
      'Bank0 | nGR2Off | Preserve Dynamics',
      #-------------------------------------
      'Bank0 | nMB0Off | Device On'        ,
      'Bank0 | nMB1Off | Preset Next'      ,
      #-------------------------------------
      'Bank0 | nMR0Off | Drive'            ,
      'Bank0 | nMR1Off | Tone'             ,
      'Bank0 | nMR2Off | Dry/Wet'          ,
    ]
    self.reg('Overdrive')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Overdrive, Device: Overdrive, Display: Overdrive
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Filter Freq", orig: "Filter Freq", value: 0.537244, min: 0.000000, max: 1.000000
#   param: "Filter Width", orig: "Filter Width", value: 6.500000, min: 0.500000, max: 9.000000
#   param: "Drive", orig: "Drive", value: 50.000000, min: 0.000000, max: 100.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 50.000000, min: 0.000000, max: 100.000000
#   param: "Tone", orig: "Tone", value: 50.000000, min: 0.000000, max: 100.000000
#   param: "Preserve Dynamics", orig: "Preserve Dynamics", value: 0.500000, min: 0.000000, max: 1.000000
