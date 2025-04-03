from .Dev import Dev

class InstrumentVector(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nMB0Off | Device On       | Preset Prev          | Sub On        | Osc 1 On        | Osc 2 On'                                                             ,
      'Bank0 | nMB1Off | Preset Save     | Preset Next'                                                                                                                   ,
      #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Sub Gain        | Osc 1 Pan            | Osc 1 Gain    | Osc 1 Effect 1  | Osc 1 Effect 2 | Osc 1 Transp   | Osc 1 Detune      | Osc 1 Pos'      ,
      'Bank0 | nMR1Off | Sub Tone        | Osc 2 Pan            | Osc 2 Gain    | Osc 2 Effect 1  | Osc 2 Effect 2 | Osc 2 Transp   | Osc 2 Detune      | Osc 2 Pos'      ,
      'Bank0 | nMR2Off | Sub Transpose   | Transpose            | Volume        | Glide           | Unison Amount  | Time           | Global Mod Amount'                  ,
      ##===================================================================================================================================================================
      'Bank1 | nMB0Off | Filter 1 On     | Filter 1 BP/NO/Morph | Filter 2 On   | Filter 2 BP/NO/Morph'                                                                   ,
      'Bank1 | nMB1Off | -               | Filter 1 Slope       | -             | Filter 2 Slope'                                                                         ,
      #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | Filter 1 Type   | Filter 1 LP/HP       | Filter 1 Freq | Filter 1 Res    | Filter 1 Drive | Filter 1 Morph'                                      ,
      'Bank1 | nMR1Off | Filter 2 Type   | Filter 2 LP/HP       | Filter 2 Freq | Filter 2 Res    | Filter 2 Drive | Filter 2 Morph'                                      ,
      'Bank1 | nMR2Off | Amp Attack      | Amp Decay            | Amp Sustain   | Amp Release     | Amp A Slope    | Amp D Slope    | Amp R Slope       | Amp Loop Mode'  ,
      #====================================================================================================================================================================
      'Bank2 | nMR0Off | Env 2 Attack    | Env 2 Decay          | Env 2 Sustain | Env 2 Release   | Env 3 Attack   | Env 3 Decay    | Env 3 Sustain     | Env 3 Release'  ,
      'Bank2 | nMR1Off | Env 2 A Slope   | Env 2 D Slope        | Env 2 R Slope | Env 2 Loop Mode | Env 3 A Slope  | Env 3 D Slope  | Env 3 R Slope     | Env 3 Loop Mode',
      'Bank2 | nMR2Off | Env 2 Initial   | Env 2 Peak           | Env 2 Final   | -               | Env 3 Initial  | Env 3 Peak     | Env 3 Final'                        ,
      #====================================================================================================================================================================
      'Bank3 | nMB0Off | LFO 1 Sync      | LFO 2 Sync'                                                                                                                    ,
      'Bank3 | nMB1Off | LFO 1 Retrigger | LFO 2 Retrigger'                                                                                                               ,
      #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMR0Off | LFO 1 Shape     | LFO 1 Attack Time    | LFO 1 Rate    | LFO 1 S. Rate   | LFO 1 Amount   | LFO 1 Shaping  | LFO 1 Phase Offset'                 ,
      'Bank3 | nMR1Off | LFO 2 Shape     | LFO 2 Attack Time    | LFO 2 Rate    | LFO 2 S. Rate   | LFO 2 Amount   | LFO 2 Shaping  | LFO 2 Phase Offset'                 ,
    ]
    self.reg('InstrumentVector')
    self.parse_cfg()

#=======================================================================
# Class: InstrumentVector, Device: Wavetable, Display: Wavetable
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Sub On", orig: "Sub On" => [Off, On]
# Q param: "Osc 1 On", orig: "Osc 1 On" => [Off, On]
# Q param: "Osc 2 On", orig: "Osc 2 On" => [Off, On]
#   param: "Sub Gain", orig: "Sub Gain", value: 0.501188, min: 0.000000, max: 1.000000
#   param: "Osc 1 Pan", orig: "Osc 1 Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Gain", orig: "Osc 1 Gain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Effect 1", orig: "Osc 1 Effect 1", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Effect 2", orig: "Osc 1 Effect 2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Transp", orig: "Osc 1 Transp", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Osc 1 Detune", orig: "Osc 1 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Pos", orig: "Osc 1 Pos", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Sub Tone", orig: "Sub Tone", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Pan", orig: "Osc 2 Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Gain", orig: "Osc 2 Gain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Effect 1", orig: "Osc 2 Effect 1", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Effect 2", orig: "Osc 2 Effect 2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Transp", orig: "Osc 2 Transp", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Osc 2 Detune", orig: "Osc 2 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Pos", orig: "Osc 2 Pos", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Sub Transpose", orig: "Sub Transpose" => [0, -1, -2]
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Volume", orig: "Volume", value: 0.595662, min: 0.000000, max: 1.000000
#   param: "Glide", orig: "Glide", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Unison Amount", orig: "Unison Amount", value: 0.300000, min: 0.000000, max: 1.000000
#   param: "Time", orig: "Time", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Global Mod Amount", orig: "Global Mod Amount", value: 0.500000, min: 0.000000, max: 1.000000
#---------------------
# Q param: "Filter 1 On", orig: "Filter 1 On" => [Off, On]
# Q param: "Filter 1 BP/NO/Morph", orig: "Filter 1 BP/NO/Morph" => [Clean, OSR]
# Q param: "Filter 1 Slope", orig: "Filter 1 Slope" => [12, 24]
# Q param: "Filter 2 On", orig: "Filter 2 On" => [Off, On]
# Q param: "Filter 2 BP/NO/Morph", orig: "Filter 2 BP/NO/Morph" => [Clean, OSR]
# Q param: "Filter 2 Slope", orig: "Filter 2 Slope" => [12, 24]
# Q param: "Filter 1 Type", orig: "Filter 1 Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter 1 LP/HP", orig: "Filter 1 LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter 1 Freq", orig: "Filter 1 Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Filter 1 Res", orig: "Filter 1 Res", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 1 Drive", orig: "Filter 1 Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 1 Morph", orig: "Filter 1 Morph", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Filter 2 Type", orig: "Filter 2 Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter 2 LP/HP", orig: "Filter 2 LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter 2 Freq", orig: "Filter 2 Freq", value: 0.000002, min: 0.000000, max: 1.000000
#   param: "Filter 2 Res", orig: "Filter 2 Res", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 2 Drive", orig: "Filter 2 Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 2 Morph", orig: "Filter 2 Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Amp Attack", orig: "Amp Attack", value: 0.084090, min: 0.000000, max: 1.000000
#   param: "Amp Decay", orig: "Amp Decay", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Amp Sustain", orig: "Amp Sustain", value: 0.707946, min: 0.000000, max: 1.000000
#   param: "Amp Release", orig: "Amp Release", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Amp A Slope", orig: "Amp A Slope", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Amp D Slope", orig: "Amp D Slope", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Amp R Slope", orig: "Amp R Slope", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "Amp Loop Mode", orig: "Amp Loop Mode" => [None, Trigger, Loop]
#---------------------
#   param: "Env 2 Attack", orig: "Env 2 Attack", value: 0.084090, min: 0.000000, max: 1.000000
#   param: "Env 2 Decay", orig: "Env 2 Decay", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 2 Sustain", orig: "Env 2 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 2 Release", orig: "Env 2 Release", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 3 Attack", orig: "Env 3 Attack", value: 0.084090, min: 0.000000, max: 1.000000
#   param: "Env 3 Decay", orig: "Env 3 Decay", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 3 Sustain", orig: "Env 3 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 3 Release", orig: "Env 3 Release", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 2 A Slope", orig: "Env 2 A Slope", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 2 D Slope", orig: "Env 2 D Slope", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Env 2 R Slope", orig: "Env 2 R Slope", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "Env 2 Loop Mode", orig: "Env 2 Loop Mode" => [None, Trigger, Loop]
#   param: "Env 3 A Slope", orig: "Env 3 A Slope", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 3 D Slope", orig: "Env 3 D Slope", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Env 3 R Slope", orig: "Env 3 R Slope", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "Env 3 Loop Mode", orig: "Env 3 Loop Mode" => [None, Trigger, Loop]
#   param: "Env 2 Initial", orig: "Env 2 Initial", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env 2 Peak", orig: "Env 2 Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Env 2 Final", orig: "Env 2 Final", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env 3 Initial", orig: "Env 3 Initial", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env 3 Peak", orig: "Env 3 Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Env 3 Final", orig: "Env 3 Final", value: 0.000000, min: 0.000000, max: 1.000000
#---------------------
# Q param: "LFO 1 Retrigger", orig: "LFO 1 Retrigger" => [Off, On]
# Q param: "LFO 1 Sync", orig: "LFO 1 Sync" => [Free, Tempo]
# Q param: "LFO 2 Retrigger", orig: "LFO 2 Retrigger" => [Off, On]
# Q param: "LFO 2 Sync", orig: "LFO 2 Sync" => [Free, Tempo]
# Q param: "LFO 1 Shape", orig: "LFO 1 Shape" => [Sine, Triangle, Sawtooth, Rectangle, Noise]
#   param: "LFO 1 Attack Time", orig: "LFO 1 Attack Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Rate", orig: "LFO 1 Rate", value: 0.320789, min: 0.000000, max: 1.000000
#   param: "LFO 1 S. Rate", orig: "LFO 1 S. Rate", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "LFO 1 Amount", orig: "LFO 1 Amount", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Shaping", orig: "LFO 1 Shaping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Phase Offset", orig: "LFO 1 Phase Offset", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "LFO 2 Shape", orig: "LFO 2 Shape" => [Sine, Triangle, Sawtooth, Rectangle, Noise]
#   param: "LFO 2 Attack Time", orig: "LFO 2 Attack Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Rate", orig: "LFO 2 Rate", value: 0.320789, min: 0.000000, max: 1.000000
#   param: "LFO 2 S. Rate", orig: "LFO 2 S. Rate", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "LFO 2 Amount", orig: "LFO 2 Amount", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Shaping", orig: "LFO 2 Shaping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Phase Offset", orig: "LFO 2 Phase Offset", value: 0.000000, min: 0.000000, max: 1.000000

