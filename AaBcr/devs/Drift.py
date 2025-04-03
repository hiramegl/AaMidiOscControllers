from .Dev import Dev

class Drift(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nMB0Off | Device On       | Preset Prev     | Osc 1 On          | Osc Retrig On       | Osc 2 On         | Noise On        | -                | -'           ,
      'Bank0 | nMB1Off | Preset Save     | Preset Next     | Osc 1 Flt On      | -                   | Osc 2 Flt On     | Noise Flt On'                                     ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Osc 1 Wave      | Osc 1 Oct       | Osc 1 Shape       | Osc 1 Shape Mod Amt | Osc 1 Gain'                                                          ,
      'Bank0 | nMR1Off | Osc 2 Wave      | Osc 2 Oct       | Osc 2 Detune      | Osc 2 Gain'                                                                                ,
      'Bank0 | nMR2Off | Pitch Mod Amt 1 | Pitch Mod Amt 2 | Noise Gain'                                                                                                    ,
      #======================================================================================================================================================================
      'Bank1 | nMB0Off | LP Type'                                                                                                                                           ,
      'Bank1 | nMB1Off | Env 2 Cyc On'                                                                                                                                      ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | LP Freq         | Key > LPF       | LP Reso           | HP Freq             | LP Mod Amt 1     | LP Mod Amt 2'                                     ,
      'Bank1 | nMR1Off | Env 1 Attack    | Env 1 Decay     | Env 1 Sustain     | Env 1 Release       | Env 2 Attack     | Env 2 Decay     | Env 2 Sustain   | Env 2 Release',
      'Bank1 | nMR2Off | Cyc Env Tilt    | Cyc Env Hold    | Cyc Env Time Mode | Cyc Env Rate        | Cyc Env Time     | Cyc Env Ratio   | Cyc Env Synced'                 ,
      ##=====================================================================================================================================================================
      'Bank2 | nMB0Off | LFO Retrig On   | Legato On       | Note Pitch Bend On'                                                                                            ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | LFO Time Mode   | LFO Rate        | LFO Time          | LFO Ratio           | LFO Synced       | LFO Wave        | LFO Amt         | LFO Mod Amt'  ,
      'Bank2 | nMR1Off | Thickness       | Spread          | Strength          | Poly Voice Depth    | Drift            | Glide Time'                                       ,
      'Bank2 | nMR2Off | Volume          | Vel > Vol       | Transpose         | Mod Matrix Amt 1    | Mod Matrix Amt 2 | Mod Matrix Amt 3'                                 ,
    ]
    self.reg('Drift')
    self.parse_cfg()

#=======================================================================
# Class: Drift, Device: Drift, Display: Drift
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Osc 1 On", orig: "Osc 1 On" => [Off, On]
# Q param: "Osc 1 Flt On", orig: "Osc 1 Flt On" => [Off, On]
# Q param: "Osc Retrig On", orig: "Osc Retrig On" => [Off, On]
# Q param: "Osc 2 On", orig: "Osc 2 On" => [Off, On]
# Q param: "Osc 2 Flt On", orig: "Osc 2 Flt On" => [Off, On]
# Q param: "Noise On", orig: "Noise On" => [Off, On]
# Q param: "Noise Flt On", orig: "Noise Flt On" => [Off, On]
# Q param: "Osc 1 Wave", orig: "Osc 1 Wave" => [Sine, Triangle, Shark Tooth, Saturated, Saw, Pulse, Rectangle]
#   param: "Osc 1 Oct", orig: "Osc 1 Oct", value: 0.000000, min: -2.000000, max: 3.000000
#   param: "Osc 1 Shape", orig: "Osc 1 Shape", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Shape Mod Amt", orig: "Osc 1 Shape Mod Amt", value: 0.525000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Gain", orig: "Osc 1 Gain", value: 0.547833, min: 0.000000, max: 1.000000
# Q param: "Osc 2 Wave", orig: "Osc 2 Wave" => [Sine, Triangle, Saturated, Saw, Rectangle]
#   param: "Osc 2 Oct", orig: "Osc 2 Oct", value: -1.000000, min: -3.000000, max: 2.000000
#   param: "Osc 2 Detune", orig: "Osc 2 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Gain", orig: "Osc 2 Gain", value: 0.498777, min: 0.000000, max: 1.000000
#   param: "Pitch Mod Amt 1", orig: "Pitch Mod Amt 1", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Pitch Mod Amt 2", orig: "Pitch Mod Amt 2", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Gain", orig: "Noise Gain", value: 0.000000, min: 0.000000, max: 1.000000
#----------
# Q param: "LP Type", orig: "LP Type" => [I, II]
# Q param: "Env 2 Cyc On", orig: "Env 2 Cyc On" => [Env, Cyc]
#   param: "LP Freq", orig: "LP Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Key > LPF", orig: "Key > LPF", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LP Reso", orig: "LP Reso", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "HP Freq", orig: "HP Freq", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LP Mod Amt 1", orig: "LP Mod Amt 1", value: 0.967593, min: 0.000000, max: 1.000000
#   param: "LP Mod Amt 2", orig: "LP Mod Amt 2", value: 0.782846, min: 0.000000, max: 1.000000
#   param: "Env 1 Attack", orig: "Env 1 Attack", value: 0.110757, min: 0.000000, max: 1.000000
#   param: "Env 1 Decay", orig: "Env 1 Decay", value: 0.397448, min: 0.000000, max: 1.000000
#   param: "Env 1 Sustain", orig: "Env 1 Sustain", value: 0.700000, min: 0.000000, max: 1.000000
#   param: "Env 1 Release", orig: "Env 1 Release", value: 0.396784, min: 0.000000, max: 1.000000
#   param: "Env 2 Attack", orig: "Env 2 Attack", value: 0.110757, min: 0.000000, max: 1.000000
#   param: "Env 2 Decay", orig: "Env 2 Decay", value: 0.397448, min: 0.000000, max: 1.000000
#   param: "Env 2 Sustain", orig: "Env 2 Sustain", value: 0.200000, min: 0.000000, max: 1.000000
#   param: "Env 2 Release", orig: "Env 2 Release", value: 0.396784, min: 0.000000, max: 1.000000
#   param: "Cyc Env Tilt", orig: "Cyc Env Tilt", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Cyc Env Hold", orig: "Cyc Env Hold", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Cyc Env Time Mode", orig: "Cyc Env Time Mode" => [Freq, Time, Ratio, Sync]
#   param: "Cyc Env Rate", orig: "Cyc Env Rate", value: 0.312256, min: 0.000000, max: 1.000000
#   param: "Cyc Env Time", orig: "Cyc Env Time", value: 0.296170, min: 0.000000, max: 1.000000
#   param: "Cyc Env Ratio", orig: "Cyc Env Ratio", value: 0.047619, min: 0.000000, max: 1.000000
#   param: "Cyc Env Synced", orig: "Cyc Env Synced", value: 15.000000, min: 0.000000, max: 21.000000
#----------
# Q param: "LFO Retrig On", orig: "LFO Retrig On" => [Off, On]
# Q param: "Legato On", orig: "Legato On" => [Off, On]
# Q param: "Note Pitch Bend On", orig: "Note Pitch Bend On" => [Off, On]
# Q param: "LFO Time Mode", orig: "LFO Time Mode" => [Freq, Time, Ratio, Sync]
#   param: "LFO Rate", orig: "LFO Rate", value: 0.113181, min: 0.000000, max: 1.000000
#   param: "LFO Time", orig: "LFO Time", value: 0.296170, min: 0.000000, max: 1.000000
#   param: "LFO Ratio", orig: "LFO Ratio", value: 0.047619, min: 0.000000, max: 1.000000
#   param: "LFO Synced", orig: "LFO Synced", value: 15.000000, min: 0.000000, max: 21.000000
# Q param: "LFO Wave", orig: "LFO Wave" => [Sine, Triangle, Saw Up, Saw Down, Square, Sample & Hold, Wander, Linear Env, Exponential Env]
#   param: "LFO Amt", orig: "LFO Amt", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "LFO Mod Amt", orig: "LFO Mod Amt", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Thickness", orig: "Thickness", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Spread", orig: "Spread", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Strength", orig: "Strength", value: 0.050000, min: 0.000000, max: 1.000000
#   param: "Poly Voice Depth", orig: "Poly Voice Depth", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Drift", orig: "Drift", value: 0.072000, min: 0.000000, max: 1.000000
#   param: "Glide Time", orig: "Glide Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Volume", orig: "Volume", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vel > Vol", orig: "Vel > Vol", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Mod Matrix Amt 1", orig: "Mod Matrix Amt 1", value: 0.967593, min: 0.000000, max: 1.000000
#   param: "Mod Matrix Amt 2", orig: "Mod Matrix Amt 2", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Mod Matrix Amt 3", orig: "Mod Matrix Amt 3", value: 0.500000, min: 0.000000, max: 1.000000

