from .Dev import Dev

class Echo(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | L Sync      | R Sync'                                                                  ,
      'Bank0 | nGB1Off | Mod Sync    | Mod 4x'                                                                  ,
      'Bank0 | nGB2Off | Gate On     | -            | Duck On      | -            | Noise On'                   ,
      'Bank0 | nGB3Off | Wobble On   | Repitch'                                                                 ,
      #----------------------------------------------------------------------------------------------------------
      'Bank0 | nGR0Off | L Time      | R Time       | L 16th       | R 16th       | LP Res'                     ,
      'Bank0 | nGR1Off | Mod Wave    | Mod Rate     | Mod Freq     | Mod Phase    | Dly < Mod    | Flt < Mod'   ,
      'Bank0 | nGR2Off | Gate Thr    | Gate Release | Duck Thr     | Duck Release | Noise Amt    | Noise Mrph'  ,
      'Bank0 | nGR3Off | Wobble Amt  | Wobble Mrph  | Env Mix',
      #----------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev  | Link         | Clip Dry     | Feedback Inv | Filter On'   ,
      'Bank0 | nMB1Off | Preset Save | Preset Next'                                                             ,
      #----------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | L Division  | R Division   | Input Gain   | HP Freq      | Reverb Level | Stereo Width',
      'Bank0 | nMR1Off | L Sync Mode | R Sync Mode  | Feedback     | HP Res       | Reverb Loc   | Output Gain' ,
      'Bank0 | nMR2Off | L Offset    | R Offset     | Channel Mode | LP Freq      | Reverb Decay | Dry Wet'     ,
    ]
    self.reg('Echo')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Echo, Device: Echo, Display: Echo
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "L Sync", orig: "L Sync" => [Off, On]
#   param: "L Time", orig: "L Time", value: 0.565306, min: 0.000000, max: 1.000000
#   param: "L Division", orig: "L Division", value: -3.000000, min: -6.000000, max: 0.000000
#   param: "L 16th", orig: "L 16th", value: 3.000000, min: 1.000000, max: 16.000000
# Q param: "L Sync Mode", orig: "L Sync Mode" => [Notes, Triplet, Dotted, 16th]
#   param: "L Offset", orig: "L Offset", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "R Time", orig: "R Time", value: 0.565306, min: 0.000000, max: 1.000000
# Q param: "R Sync", orig: "R Sync" => [Off, On]
#   param: "R Division", orig: "R Division", value: -3.000000, min: -6.000000, max: 0.000000
#   param: "R 16th", orig: "R 16th", value: 3.000000, min: 1.000000, max: 16.000000
# Q param: "R Sync Mode", orig: "R Sync Mode" => [Notes, Triplet, Dotted, 16th]
#   param: "R Offset", orig: "R Offset", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Link", orig: "Link" => [Off, On]
# Q param: "Repitch", orig: "Repitch" => [Off, On]
#   param: "Feedback", orig: "Feedback", value: 0.333333, min: 0.000000, max: 1.000000
# Q param: "Feedback Inv", orig: "Feedback Inv" => [Off, On]
# Q param: "Channel Mode", orig: "Channel Mode" => [Stereo, Ping Pong, Mid/Side]
#   param: "Input Gain", orig: "Input Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Output Gain", orig: "Output Gain", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Clip Dry", orig: "Clip Dry" => [Off, On]
# Q param: "Gate On", orig: "Gate On" => [Off, On]
#   param: "Gate Thr", orig: "Gate Thr", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Gate Release", orig: "Gate Release", value: 0.602836, min: 0.000000, max: 1.000000
# Q param: "Duck On", orig: "Duck On" => [Off, On]
#   param: "Duck Thr", orig: "Duck Thr", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Duck Release", orig: "Duck Release", value: 0.372772, min: 0.000000, max: 1.000000
# Q param: "Filter On", orig: "Filter On" => [Off, On]
#   param: "HP Freq", orig: "HP Freq", value: 0.132647, min: 0.000000, max: 1.000000
#   param: "HP Res", orig: "HP Res", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LP Freq", orig: "LP Freq", value: 0.799313, min: 0.000000, max: 1.000000
#   param: "LP Res", orig: "LP Res", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Mod Wave", orig: "Mod Wave" => [Sine, Triangle, Saw Up, Saw Down, Square, Random]
#   param: "Mod Freq", orig: "Mod Freq", value: 0.638809, min: 0.000000, max: 1.000000
# Q param: "Mod Sync", orig: "Mod Sync" => [Off, On]
#   param: "Mod Rate", orig: "Mod Rate", value: 12.000000, min: 0.000000, max: 21.000000
#   param: "Mod Phase", orig: "Mod Phase", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env Mix", orig: "Env Mix", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Dly < Mod", orig: "Dly < Mod", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Flt < Mod", orig: "Flt < Mod", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Mod 4x", orig: "Mod 4x" => [Off, On]
#   param: "Reverb Level", orig: "Reverb Level", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Reverb Decay", orig: "Reverb Decay", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Reverb Loc", orig: "Reverb Loc" => [Pre, Post, Feedback]
# Q param: "Noise On", orig: "Noise On" => [Off, On]
#   param: "Noise Amt", orig: "Noise Amt", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Noise Mrph", orig: "Noise Mrph", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Wobble On", orig: "Wobble On" => [Off, On]
#   param: "Wobble Amt", orig: "Wobble Amt", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Wobble Mrph", orig: "Wobble Mrph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Stereo Width", orig: "Stereo Width", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Dry Wet", orig: "Dry Wet", value: 0.449667, min: 0.000000, max: 1.000000
