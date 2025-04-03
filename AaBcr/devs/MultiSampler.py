from .Dev import Dev

class MultiSampler(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | Pe Init                      | Pe Peak      | Pe Sustain    | Pe End         | Pe Mode     | Spread          | Transpose      | Detune',
      'Bank0 | nGR1Off | Pe A Slope                   | Pe D Slope   | Pe R Slope    | Pe R < Vel     | Pe Loop     | Key Zone Shift  | Glide Mode     | Glide Time',
      'Bank0 | nGR2Off | Pe Retrig                    | Pe Attack    | Pe Decay      | Pe Release     | Pe < Env    | Sample Selector | Fade In        | Fade Out',
      #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On                    | Preset Prev  | Reverse       | Osc On         | O Fix On    | Pe On',
      'Bank0 | nMB1Off | Preset Save                  | Preset Next  | Snap          | O Mode',
      #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Oe Init                      | Oe Peak      | Oe Sustain    | Oe End         | Oe Mode     | O Type          | O Volume       | O Vol < Vel',
      'Bank0 | nMR1Off | Oe A Slope                   | Oe D Slope   | Oe R Slope    | Oe R < Vel     | Oe Loop     | O Coarse        | O Fine         | -',
      'Bank0 | nMR2Off | Oe Retrig                    | Oe Attack    | Oe Decay      | Oe Release     | -           | O Fix Freq      | O Fix Freq Mul | -',
      ##================================================================================================================================================================
      'Bank1 | nGR0Off | Volume                       | Vol < Vel    | Ve Init       | Ve Peak        | Ve Sustain  | Ve Mode',
      'Bank1 | nGR1Off | Ve A Slope                   | Ve D Slope   | Ve R Slope    | Ve R < Vel     | Ve Loop     | Ve Retrig',
      'Bank1 | nGR2Off | Ve Attack                    | Ve Decay     | Ve Release    | Pan            | Pan < Rnd   | Time            | Time < Key',
      ##----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMB0Off | F On                         | Filter Slope | Fe On         | Trigger Mode',
      'Bank1 | nMB1Off | Filter Circuit - BP/NO/Morph | Shaper On',
      #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | Filter Circuit - LP/HP       | Filter Freq  | Filter Res    | Fe Init        | Fe Peak     | Fe Sustain      | Fe End         | Fe Mode',
      'Bank1 | nMR1Off | Filter Drive                 | Filt < Vel   | Filt < Key    | Fe A Slope     | Fe D Slope  | Fe R Slope      | Fe R < Vel     | Fe Loop',
      'Bank1 | nMR2Off | Filter Type                  | Filter Morph | Fe < Env      | Fe Retrig      | Fe Attack   | Fe Decay        | Fe Release',
      ##================================================================================================================================================================
      'Bank2 | nGR0Off | -                            | -            | -             | -              | Vol < LFO   | Filt < LFO      | Pan < LFO      | Pitch < LFO ',
      #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMB0Off | Ae On                        | -            | -             | -              |  L 1 On     | L 1 Sync',
      'Bank2 | nMB1Off | -                            | -            | -             | -              |  L 1 Retrig | L 1 St Mode',
      #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | Ae Init                      | Ae Peak      | Ae Sustain    | Ae End         | Ae Mode     | L 1 Wave        | L 1 Rate       | L 1 Sync Rate',
      'Bank2 | nMR1Off | Ae A Slope                   | Ae D Slope   | Ae R Slope    | Ae R < Vel     | Ae Loop     | L 1 Attack      | L 1 Offset     | L 1 R < Key',
      'Bank2 | nMR2Off | Ae Retrig                    | Ae Attack    | Ae Decay      | Ae Release     | -           | L 1 Phase       | L 1 Spin       | L 1 Width',
      ##================================================================================================================================================================
      'Bank3 | nMB0Off | L 2 On                       | L 2 Retrig   | -             | -              | L 3 On      | L 3 Retrig',
      'Bank3 | nMB1Off | L 2 Sync                     | L 2 St Mode  | -             | -              | L 3 Sync    | L 3 St Mode',
      ##----------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMR0Off | L 2 Wave                     | L 2 Rate     | L 2 Sync Rate | -              | L 3 Wave    | L 3 Rate        | L 3 Sync Rate  | -',
      'Bank3 | nMR1Off | L 2 Attack                   | L 2 Offset   | L 2 R < Key   | -              | L 3 Attack  | L 3 Offset      | L 3 R < Key    | -',
      'Bank3 | nMR2Off | L 2 Phase                    | L 2 Spin     | L 2 Width     | -              | L 3 Phase   | L 3 Spin        | L 3 Width      | -',
    ]
    self.reg('MultiSampler')
    self.parse_cfg()

#=======================================================================
# Class: MultiSampler, Device: rock - The Doors - Summers Almost Gone, Display: Sampler
#   param: "Pe Init", orig: "Pe Init", value: -1.000000, min: -1.000000, max: 1.000000
#   param: "Pe Peak", orig: "Pe Peak", value: 0.796610, min: -1.000000, max: 1.000000
#   param: "Pe Sustain", orig: "Pe Sustain", value: 0.220339, min: -1.000000, max: 1.000000
#   param: "Pe End", orig: "Pe End", value: -0.898305, min: -1.000000, max: 1.000000
# Q param: "Pe Mode", orig: "Pe Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Spread", orig: "Spread", value: 53.000000, min: 0.000000, max: 100.000000
#   param: "Transpose", orig: "Transpose", value: -1.000000, min: -48.000000, max: 48.000000
#   param: "Detune", orig: "Detune", value: 18.000000, min: -50.000000, max: 50.000000
#   param: "Pe A Slope", orig: "Pe A Slope", value: -0.471698, min: -1.000000, max: 1.000000
#   param: "Pe D Slope", orig: "Pe D Slope", value: -1.000000, min: -1.000000, max: 1.000000
#   param: "Pe R Slope", orig: "Pe R Slope", value: 0.393939, min: -1.000000, max: 1.000000
#   param: "Pe R < Vel", orig: "Pe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Pe Loop", orig: "Pe Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Key Zone Shift", orig: "Key Zone Shift", value: 16.000000, min: -48.000000, max: 48.000000
# Q param: "Glide Mode", orig: "Glide Mode" => [Off, Portamento, Glide]
#   param: "Glide Time", orig: "Glide Time", value: 0.210938, min: 0.000000, max: 1.000000
#   param: "Pe Retrig", orig: "Pe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Pe Attack", orig: "Pe Attack", value: 0.438596, min: 0.000000, max: 1.000000
#   param: "Pe Decay", orig: "Pe Decay", value: 0.982456, min: 0.000000, max: 1.000000
#   param: "Pe Release", orig: "Pe Release", value: 0.947368, min: 0.000000, max: 1.000000
#   param: "Pe < Env", orig: "Pe < Env", value: 1.000000, min: -48.000000, max: 48.000000
#   param: "Sample Selector", orig: "Sample Selector", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Fade In", orig: "Fade In", value: 0.036840, min: 0.000000, max: 1.000000
#   param: "Fade Out", orig: "Fade Out", value: 0.036840, min: 0.000000, max: 1.000000
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Reverse", orig: "Reverse" => [Off, On]
# Q param: "Snap", orig: "Snap" => [Off, On]
# Q param: "Osc On", orig: "Osc On" => [Off, On]
# Q param: "O Mode", orig: "O Mode" => [FM, AM]
# Q param: "O Fix On", orig: "O Fix On" => [Off, On]
# Q param: "Pe On", orig: "Pe On" => [Off, On]
#   param: "Oe Init", orig: "Oe Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Oe Peak", orig: "Oe Peak", value: 0.847458, min: 0.000000, max: 1.000000
#   param: "Oe Sustain", orig: "Oe Sustain", value: 0.559322, min: 0.000000, max: 1.000000
#   param: "Oe End", orig: "Oe End", value: 0.084746, min: 0.000000, max: 1.000000
# Q param: "Oe Mode", orig: "Oe Mode" => [None, Loop, Beat, Sync, Trigger]
# Q param: "O Type", orig: "O Type" => [Sine, Sine 4 Bit, Sine 8 Bit, Sw 3, Sw 4, Sw 6, Sw 8, Sw 16, Sw 32, Sw 64, Sw D, Sq 3, Sq 4, Sq 6, Sq 8, Sq 16, Sq 32, Sq 64, Sq D, Tri, Noise]
#   param: "O Volume", orig: "O Volume", value: 0.265625, min: 0.000000, max: 1.000000
#   param: "O Vol < Vel", orig: "O Vol < Vel", value: 0.304688, min: 0.000000, max: 1.000000
#   param: "Oe A Slope", orig: "Oe A Slope", value: 0.640000, min: -1.000000, max: 1.000000
#   param: "Oe D Slope", orig: "Oe D Slope", value: 0.647059, min: -1.000000, max: 1.000000
#   param: "Oe R Slope", orig: "Oe R Slope", value: 0.071429, min: -1.000000, max: 1.000000
#   param: "Oe R < Vel", orig: "Oe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Oe Loop", orig: "Oe Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "O Coarse", orig: "O Coarse", value: 9.000000, min: -2.000000, max: 48.000000
#   param: "O Fine", orig: "O Fine", value: 0.000000, min: 0.000000, max: 1000.000000
#   param: "Oe Retrig", orig: "Oe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Oe Attack", orig: "Oe Attack", value: 0.649123, min: 0.000000, max: 1.000000
#   param: "Oe Decay", orig: "Oe Decay", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Oe Release", orig: "Oe Release", value: 0.929825, min: 0.000000, max: 1.000000
#   param: "O Fix Freq", orig: "O Fix Freq", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "O Fix Freq Mul", orig: "O Fix Freq Mul", value: 3.000000, min: 0.000000, max: 4.000000
#--------------
#   param: "Volume", orig: "Volume", value: -12.000000, min: -36.000000, max: 36.000000
#   param: "Vol < Vel", orig: "Vol < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ve Init", orig: "Ve Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ve Peak", orig: "Ve Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ve Sustain", orig: "Ve Sustain", value: 0.653846, min: 0.000000, max: 1.000000
# Q param: "Ve Mode", orig: "Ve Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Ve A Slope", orig: "Ve A Slope", value: 0.923077, min: -1.000000, max: 1.000000
#   param: "Ve D Slope", orig: "Ve D Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Ve R Slope", orig: "Ve R Slope", value: -0.176471, min: -1.000000, max: 1.000000
#   param: "Ve R < Vel", orig: "Ve R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Ve Loop", orig: "Ve Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Ve Retrig", orig: "Ve Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Ve Attack", orig: "Ve Attack", value: 0.403509, min: 0.000000, max: 1.000000
#   param: "Ve Decay", orig: "Ve Decay", value: 0.964912, min: 0.000000, max: 1.000000
#   param: "Ve Release", orig: "Ve Release", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Pan", orig: "Pan", value: 0.390625, min: -1.000000, max: 1.000000
#   param: "Pan < Rnd", orig: "Pan < Rnd", value: 0.398438, min: 0.000000, max: 1.000000
#   param: "Time", orig: "Time", value: 100.000000, min: -100.000000, max: 100.000000
#   param: "Time < Key", orig: "Time < Key", value: 87.000000, min: -100.000000, max: 100.000000
# Q param: "F On", orig: "F On" => [Off, On]
# Q param: "Filter Circuit - BP/NO/Morph", orig: "Filter Circuit - BP/NO/Morph" => [Clean, OSR]
# Q param: "Filter Slope", orig: "Filter Slope" => [12 dB, 24 dB]
# Q param: "Shaper On", orig: "Shaper On" => [Off, On]
# Q param: "Fe On", orig: "Fe On" => [Off, On]
# Q param: "Trigger Mode", orig: "Trigger Mode" => [Trigger, Gate]
# Q param: "Filter Circuit - LP/HP", orig: "Filter Circuit - LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter Freq", orig: "Filter Freq", value: 0.373016, min: 0.000000, max: 1.000000
#   param: "Filter Res", orig: "Filter Res", value: 0.954545, min: 0.000000, max: 1.250000
#   param: "Fe Init", orig: "Fe Init", value: 0.076923, min: 0.000000, max: 1.000000
#   param: "Fe Peak", orig: "Fe Peak", value: 0.980769, min: 0.000000, max: 1.000000
#   param: "Fe Sustain", orig: "Fe Sustain", value: 0.711538, min: 0.000000, max: 1.000000
#   param: "Fe End", orig: "Fe End", value: 0.019231, min: 0.000000, max: 1.000000
# Q param: "Fe Mode", orig: "Fe Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Filter Drive", orig: "Filter Drive", value: 0.000000, min: 0.000000, max: 24.000000
#   param: "Filt < Vel", orig: "Filt < Vel", value: 0.109375, min: 0.000000, max: 1.000000
#   param: "Filt < Key", orig: "Filt < Key", value: 0.398438, min: 0.000000, max: 1.000000
#   param: "Fe A Slope", orig: "Fe A Slope", value: 0.404255, min: -1.000000, max: 1.000000
#   param: "Fe D Slope", orig: "Fe D Slope", value: -0.714286, min: -1.000000, max: 1.000000
#   param: "Fe R Slope", orig: "Fe R Slope", value: -0.611111, min: -1.000000, max: 1.000000
#   param: "Fe R < Vel", orig: "Fe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Fe Loop", orig: "Fe Loop", value: 0.726562, min: 0.000000, max: 1.000000
# Q param: "Filter Type", orig: "Filter Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
#   param: "Filter Morph", orig: "Filter Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fe < Env", orig: "Fe < Env", value: 0.000000, min: -72.000000, max: 72.000000
#   param: "Fe Retrig", orig: "Fe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Fe Attack", orig: "Fe Attack", value: 0.105263, min: 0.000000, max: 1.000000
#   param: "Fe Decay", orig: "Fe Decay", value: 0.508772, min: 0.000000, max: 1.000000
#   param: "Fe Release", orig: "Fe Release", value: 0.754386, min: 0.000000, max: 1.000000
#--------------
#   param: "Vol < LFO", orig: "Vol < LFO", value: 0.015625, min: 0.000000, max: 1.000000
#   param: "Filt < LFO", orig: "Filt < LFO", value: 0.750000, min: 0.000000, max: 24.000000
#   param: "Pan < LFO", orig: "Pan < LFO", value: 0.234375, min: 0.000000, max: 1.000000
#   param: "Pitch < LFO", orig: "Pitch < LFO", value: 0.171875, min: 0.000000, max: 1.000000
# Q param: "Ae On", orig: "Ae On" => [Off, On]
# Q param: "L 1 On", orig: "L 1 On" => [Off, On]
# Q param: "L 1 Sync", orig: "L 1 Sync" => [Free, Sync]
# Q param: "L 1 Retrig", orig: "L 1 Retrig" => [Off, On]
# Q param: "L 1 St Mode", orig: "L 1 St Mode" => [Phase, Spin]
#   param: "Ae Init", orig: "Ae Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ae Peak", orig: "Ae Peak", value: 0.942308, min: 0.000000, max: 1.000000
#   param: "Ae Sustain", orig: "Ae Sustain", value: 0.557692, min: 0.000000, max: 1.000000
#   param: "Ae End", orig: "Ae End", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Ae Mode", orig: "Ae Mode" => [None, Loop, Beat, Sync, Trigger]
# Q param: "L 1 Wave", orig: "L 1 Wave" => [Sine, Square, Triangle, Saw Down, Saw Up, Random]
#   param: "L 1 Rate", orig: "L 1 Rate", value: 0.575188, min: 0.000000, max: 1.000000
#   param: "L 1 Sync Rate", orig: "L 1 Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "Ae A Slope", orig: "Ae A Slope", value: 0.591837, min: -1.000000, max: 1.000000
#   param: "Ae D Slope", orig: "Ae D Slope", value: 0.300000, min: -1.000000, max: 1.000000
#   param: "Ae R Slope", orig: "Ae R Slope", value: 0.034483, min: -1.000000, max: 1.000000
#   param: "Ae R < Vel", orig: "Ae R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Ae Loop", orig: "Ae Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "L 1 Attack", orig: "L 1 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L 1 Offset", orig: "L 1 Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "L 1 R < Key", orig: "L 1 R < Key", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ae Retrig", orig: "Ae Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Ae Attack", orig: "Ae Attack", value: 0.491228, min: 0.000000, max: 1.000000
#   param: "Ae Decay", orig: "Ae Decay", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ae Release", orig: "Ae Release", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "L 1 Phase", orig: "L 1 Phase", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "L 1 Spin", orig: "L 1 Spin", value: 0.000000, min: 0.000000, max: 0.500000
#   param: "L 1 Width", orig: "L 1 Width", value: 0.000000, min: 0.000000, max: 1.000000
#--------------
# Q param: "L 2 On", orig: "L 2 On" => [Off, On]
# Q param: "L 2 Sync", orig: "L 2 Sync" => [Free, Sync]
# Q param: "L 2 Retrig", orig: "L 2 Retrig" => [Off, On]
# Q param: "L 2 St Mode", orig: "L 2 St Mode" => [Phase, Spin]
# Q param: "L 3 On", orig: "L 3 On" => [Off, On]
# Q param: "L 3 Sync", orig: "L 3 Sync" => [Free, Sync]
# Q param: "L 3 Retrig", orig: "L 3 Retrig" => [Off, On]
# Q param: "L 3 St Mode", orig: "L 3 St Mode" => [Phase, Spin]
# Q param: "L 2 Wave", orig: "L 2 Wave" => [Sine, Square, Triangle, Saw Down, Saw Up, Random]
#   param: "L 2 Rate", orig: "L 2 Rate", value: 0.575188, min: 0.000000, max: 1.000000
#   param: "L 2 Sync Rate", orig: "L 2 Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
# Q param: "L 3 Wave", orig: "L 3 Wave" => [Sine, Square, Triangle, Saw Down, Saw Up, Random]
#   param: "L 3 Rate", orig: "L 3 Rate", value: 0.575188, min: 0.000000, max: 1.000000
#   param: "L 3 Sync Rate", orig: "L 3 Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "L 2 Attack", orig: "L 2 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L 2 Offset", orig: "L 2 Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "L 2 R < Key", orig: "L 2 R < Key", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L 3 Attack", orig: "L 3 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L 3 Offset", orig: "L 3 Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "L 3 R < Key", orig: "L 3 R < Key", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L 2 Phase", orig: "L 2 Phase", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "L 2 Spin", orig: "L 2 Spin", value: 0.000000, min: 0.000000, max: 0.500000
#   param: "L 2 Width", orig: "L 2 Width", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L 3 Phase", orig: "L 3 Phase", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "L 3 Spin", orig: "L 3 Spin", value: 0.000000, min: 0.000000, max: 0.500000
#   param: "L 3 Width", orig: "L 3 Width", value: 0.000000, min: 0.000000, max: 1.000000

