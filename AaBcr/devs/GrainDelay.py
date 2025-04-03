from .Dev import Dev

class GrainDelay(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB1Off | Delay Mode'               ,
      #---------------------------------------------
      'Bank0 | nGR0Off | Beat Delay  | Beat Swing' ,
      'Bank0 | nGR1Off | Time Delay'               ,
      #---------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev',
      'Bank0 | nMB1Off | Preset Save | Preset Next',
      #---------------------------------------------
      'Bank0 | nMR0Off | Spray       | Frequency'  ,
      'Bank0 | nMR1Off | Pitch       | Random'     ,
      'Bank0 | nMR2Off | Feedback    | DryWet'     ,
    ]
    self.reg('GrainDelay')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: GrainDelay, Device: Grain Delay, Display: Grain Delay
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Spray", orig: "Spray", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Frequency", orig: "Frequency", value: 0.817131, min: 0.000000, max: 1.000000
#   param: "Pitch", orig: "Pitch", value: 0.000000, min: -36.000000, max: 12.000000
#   param: "Random", orig: "Random", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Feedback", orig: "Feedback", value: 0.000000, min: 0.000000, max: 0.950000
#   param: "DryWet", orig: "DryWet", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Delay Mode", orig: "Delay Mode" => [Off, On]
# Q param: "Beat Delay", orig: "Beat Delay" => [1, 2, 3, 4, 5, 6, 8, 16]
#   param: "Beat Swing", orig: "Beat Swing", value: 0.000000, min: -0.333000, max: 0.333000
#   param: "Time Delay", orig: "Time Delay", value: 40.000000, min: 1.000000, max: 128.000000

