from .Dev import Dev

class Reverb(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Freeze On       | Flat On        | Cut On'                       ,
      'Bank0 | nGB1Off | HiFilter On     | HiFilter Type  | LowShelf On'                  ,
      #------------------------------------------------------------------------------------
      'Bank0 | nGR0Off | Size Smoothing  | Chorus Amount  | Chorus Rate   | Density '     ,
      'Bank0 | nGR1Off | HiFilter Freq   | HiShelf Gain   | LowShelf Freq | LowShelf Gain',
      'Bank0 | nGR2Off | Diffusion       | Scale'                                         ,
      #------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On       | Preset Prev    | In LowCut On | In HighCut On' ,
      'Bank0 | nMB1Off | Preset Save     | Preset Next    | ER Spin On   | Chorus On'     ,
      #------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | In Filter Freq  | ER Spin Amount | Room Size    | Reflect Level' ,
      'Bank0 | nMR1Off | In Filter Width | ER Spin Rate   | Decay Time   | Diffuse Level' ,
      'Bank0 | nMR2Off | Predelay        | ER Shape       | Stereo Image | Dry/Wet'       ,
    ]
    self.reg('Reverb')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Reverb, Device: Reverb, Display: Reverb
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Size Smoothing", orig: "Size Smoothing" => [None, Slow, Fast]
# Q param: "In LowCut On", orig: "In LowCut On" => [Off, On]
# Q param: "In HighCut On", orig: "In HighCut On" => [Off, On]
# Q param: "ER Spin On", orig: "ER Spin On" => [Off, On]
# Q param: "Chorus On", orig: "Chorus On" => [Off, On]
#   param: "In Filter Freq", orig: "In Filter Freq", value: 0.477294, min: 0.000000, max: 1.000000
#   param: "In Filter Width", orig: "In Filter Width", value: 0.629412, min: 0.000000, max: 1.000000
#   param: "Predelay", orig: "Predelay", value: 0.258977, min: 0.000000, max: 1.000000
#   param: "ER Spin Rate", orig: "ER Spin Rate", value: 0.485693, min: 0.000000, max: 1.000000
#   param: "ER Spin Amount", orig: "ER Spin Amount", value: 0.654476, min: 0.000000, max: 1.000000
#   param: "ER Shape", orig: "ER Shape", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Room Size", orig: "Room Size", value: 0.791515, min: 0.000000, max: 1.000000
#   param: "Decay Time", orig: "Decay Time", value: 0.314135, min: 0.000000, max: 1.000000
#   param: "Stereo Image", orig: "Stereo Image", value: 0.833333, min: 0.000000, max: 1.000000
#   param: "Reflect Level", orig: "Reflect Level", value: 0.493563, min: 0.000000, max: 1.000000
#   param: "Diffuse Level", orig: "Diffuse Level", value: 0.493563, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 0.550000, min: 0.000000, max: 1.000000
# Q param: "HiFilter On", orig: "HiFilter On" => [Off, On]
# Q param: "HiFilter Type", orig: "HiFilter Type" => [Shelf, Lowpass]
#   param: "HiFilter Freq", orig: "HiFilter Freq", value: 0.810234, min: 0.000000, max: 1.000000
#   param: "HiShelf Gain", orig: "HiShelf Gain", value: 0.625000, min: 0.000000, max: 1.000000
# Q param: "LowShelf On", orig: "LowShelf On" => [Off, On]
#   param: "LowShelf Freq", orig: "LowShelf Freq", value: 0.227200, min: 0.000000, max: 1.000000
#   param: "LowShelf Gain", orig: "LowShelf Gain", value: 0.687500, min: 0.000000, max: 1.000000
#   param: "Diffusion", orig: "Diffusion", value: 0.624609, min: 0.000000, max: 1.000000
#   param: "Scale", orig: "Scale", value: 0.368421, min: 0.000000, max: 1.000000
# Q param: "Freeze On", orig: "Freeze On" => [Off, On]
# Q param: "Flat On", orig: "Flat On" => [Off, On]
# Q param: "Cut On", orig: "Cut On" => [Off, On]
#   param: "Chorus Rate", orig: "Chorus Rate", value: 0.103693, min: 0.000000, max: 1.000000
#   param: "Chorus Amount", orig: "Chorus Amount", value: 0.002506, min: 0.000000, max: 1.000000
# Q param: "Density", orig: "Density" => [Sparse, Low, Mid, High]

