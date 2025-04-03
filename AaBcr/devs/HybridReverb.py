from .Dev import Dev

class HybridReverb(Dev):
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
    self.reg('Hybrid Reverb')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Hybrid, Device: Hybrid Reverb, Display: Hybrid Reverb

#ENC-BK1
#   param: "P.Dly Fb Time", orig: "P.Dly Fb Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "P.Dly Fb 16th", orig: "P.Dly Fb 16th", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Routing", orig: "Routing" => [Serial, Parallel, Algorithm, Convolution]
# Q param: "Algo Type", orig: "Algo Type" => [Dark Hall, Quartz, Shimmer, Tides, Prism]

#BUT-BK2
# Q param: "EQ On", orig: "EQ On" => [Off, On]
# Q param: "EQ Pre Algo", orig: "EQ Pre Algo" => [Off, On]
# Q param: "EQ Low Type", orig: "EQ Low Type" => [Cut, Shelf]
# Q param: "EQ High Type", orig: "EQ High Type" => [Cut, Shelf]

#BUT-MAIN
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "P.Dly Sync", orig: "P.Dly Sync" => [Off, On]
# Q param: "Freeze In", orig: "Freeze In" => [Off, On]
# Q param: "Freeze", orig: "Freeze" => [Off, On]
# Q param: "Bass Mono", orig: "Bass Mono" => [Off, On]

#ENC-MAIN
#   param: "Send Gain", orig: "Send Gain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "P.Dly Time", orig: "P.Dly Time", value: 0.165425, min: 0.000000, max: 1.000000
#   param: "P.Dly 16th", orig: "P.Dly 16th", value: 2.000000, min: 0.000000, max: 16.000000

#   param: "Blend", orig: "Blend", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Decay", orig: "Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Size", orig: "Size", value: 0.500000, min: 0.000000, max: 1.000000

#   param: "Damping", orig: "Damping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "DH Shape", orig: "DH Shape", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "DH BassMult", orig: "DH BassMult", value: 0.500000, min: 0.000000, max: 1.000000

#   param: "Width", orig: "Width", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vintage", orig: "Vintage", value: 0.000000, min: 0.000000, max: 4.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 0.500000, min: 0.000000, max: 1.000000

#-----

#   param: "Algo Delay", orig: "Algo Delay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Modulation", orig: "Modulation", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "DH Bass X", orig: "DH Bass X", value: 0.674953, min: 0.000000, max: 1.000000

#   param: "Diffusion", orig: "Diffusion", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Qz Low Damp", orig: "Qz Low Damp", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Qz Distance", orig: "Qz Distance", value: 0.500000, min: 0.000000, max: 1.000000

#   param: "Sh Pitch Shift", orig: "Sh Pitch Shift", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Sh Shimmer", orig: "Sh Shimmer", value: 0.500000, min: 0.000000, max: 1.000000

#   param: "Ti Waveform", orig: "Ti Waveform", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Ti Phase", orig: "Ti Phase", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Ti Tide", orig: "Ti Tide", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Ti Rate", orig: "Ti Rate", value: 22.000000, min: 0.000000, max: 29.000000

#   param: "Pr Sixth", orig: "Pr Sixth", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pr Seventh", orig: "Pr Seventh", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pr Low Mult", orig: "Pr Low Mult", value: 0.588592, min: 0.000000, max: 1.000000
#   param: "Pr High Mult", orig: "Pr High Mult", value: 0.588592, min: 0.000000, max: 1.000000
#   param: "Pr X Over", orig: "Pr X Over", value: 0.264455, min: 0.000000, max: 1.000000

#-----

#   param: "EQ Low Freq", orig: "EQ Low Freq", value: 0.200687, min: 0.000000, max: 1.000000
#   param: "EQ Low Gain", orig: "EQ Low Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ Low Slope", orig: "EQ Low Slope", value: 1.000000, min: 0.000000, max: 9.000000

#   param: "EQ P1 Freq", orig: "EQ P1 Freq", value: 0.514689, min: 0.000000, max: 1.000000
#   param: "EQ P1 Gain", orig: "EQ P1 Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ P1 Q", orig: "EQ P1 Q", value: 0.155668, min: 0.000000, max: 1.000000

#   param: "EQ P2 Freq", orig: "EQ P2 Freq", value: 0.625020, min: 0.000000, max: 1.000000
#   param: "EQ P2 Gain", orig: "EQ P2 Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ P2 Q", orig: "EQ P2 Q", value: 0.155668, min: 0.000000, max: 1.000000

#   param: "EQ High Freq", orig: "EQ High Freq", value: 0.767010, min: 0.000000, max: 1.000000
#   param: "EQ High Gain", orig: "EQ High Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ High Slope", orig: "EQ High Slope", value: 1.000000, min: 0.000000, max: 9.000000

# Class: Hybrid, Device: Hybrid Reverb, Display: Hybrid Reverb
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "P.Dly Sync", orig: "P.Dly Sync" => [Off, On]
#   param: "P.Dly Time", orig: "P.Dly Time", value: 0.165425, min: 0.000000, max: 1.000000
#   param: "P.Dly 16th", orig: "P.Dly 16th", value: 2.000000, min: 0.000000, max: 16.000000
#   param: "P.Dly Fb Time", orig: "P.Dly Fb Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "P.Dly Fb 16th", orig: "P.Dly Fb 16th", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Algo Type", orig: "Algo Type" => [Dark Hall, Quartz, Shimmer, Tides, Prism]
#   param: "Algo Delay", orig: "Algo Delay", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Freeze", orig: "Freeze" => [Off, On]
# Q param: "Freeze In", orig: "Freeze In" => [Off, On]
#   param: "Decay", orig: "Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Size", orig: "Size", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Damping", orig: "Damping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Diffusion", orig: "Diffusion", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Modulation", orig: "Modulation", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "DH Shape", orig: "DH Shape", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "DH BassMult", orig: "DH BassMult", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "DH Bass X", orig: "DH Bass X", value: 0.674953, min: 0.000000, max: 1.000000
#   param: "Sh Shimmer", orig: "Sh Shimmer", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Sh Pitch Shift", orig: "Sh Pitch Shift", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ti Tide", orig: "Ti Tide", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Ti Rate", orig: "Ti Rate", value: 22.000000, min: 0.000000, max: 29.000000
#   param: "Ti Waveform", orig: "Ti Waveform", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Ti Phase", orig: "Ti Phase", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Qz Low Damp", orig: "Qz Low Damp", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Qz Distance", orig: "Qz Distance", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Pr High Mult", orig: "Pr High Mult", value: 0.588592, min: 0.000000, max: 1.000000
#   param: "Pr Low Mult", orig: "Pr Low Mult", value: 0.588592, min: 0.000000, max: 1.000000
#   param: "Pr X Over", orig: "Pr X Over", value: 0.264455, min: 0.000000, max: 1.000000
#   param: "Pr Sixth", orig: "Pr Sixth", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pr Seventh", orig: "Pr Seventh", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "EQ On", orig: "EQ On" => [Off, On]
# Q param: "EQ Pre Algo", orig: "EQ Pre Algo" => [Off, On]
# Q param: "EQ Low Type", orig: "EQ Low Type" => [Cut, Shelf]
#   param: "EQ Low Freq", orig: "EQ Low Freq", value: 0.200687, min: 0.000000, max: 1.000000
#   param: "EQ Low Gain", orig: "EQ Low Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ Low Slope", orig: "EQ Low Slope", value: 1.000000, min: 0.000000, max: 9.000000
#   param: "EQ P1 Freq", orig: "EQ P1 Freq", value: 0.514689, min: 0.000000, max: 1.000000
#   param: "EQ P1 Gain", orig: "EQ P1 Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ P1 Q", orig: "EQ P1 Q", value: 0.155668, min: 0.000000, max: 1.000000
#   param: "EQ P2 Freq", orig: "EQ P2 Freq", value: 0.625020, min: 0.000000, max: 1.000000
#   param: "EQ P2 Gain", orig: "EQ P2 Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ P2 Q", orig: "EQ P2 Q", value: 0.155668, min: 0.000000, max: 1.000000
# Q param: "EQ High Type", orig: "EQ High Type" => [Cut, Shelf]
#   param: "EQ High Freq", orig: "EQ High Freq", value: 0.767010, min: 0.000000, max: 1.000000
#   param: "EQ High Gain", orig: "EQ High Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "EQ High Slope", orig: "EQ High Slope", value: 1.000000, min: 0.000000, max: 9.000000
#   param: "Send Gain", orig: "Send Gain", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Routing", orig: "Routing" => [Serial, Parallel, Algorithm, Convolution]
#   param: "Blend", orig: "Blend", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vintage", orig: "Vintage", value: 0.000000, min: 0.000000, max: 4.000000
#   param: "Width", orig: "Width", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Bass Mono", orig: "Bass Mono" => [Off, On]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 0.500000, min: 0.000000, max: 1.000000
