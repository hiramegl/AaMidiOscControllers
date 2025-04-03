from .Dev import Dev

class UltraAnalog(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | OSC1 < LFO    | O1 Keytrack   | OSC1 PW       | O1 PW < LFO   | O1 Sub/Sync'                                                  ,
      'Bank0 | nGR1Off | OSC2 < LFO    | O2 Keytrack   | OSC2 PW       | O2 PW < LFO   | O2 Sub/Sync'                                                  ,
      'Bank0 | nGR2Off | Press Dest A  | Press Amt A   | Press Dest B  | Press Amt B   | Slide Dest A  | Slide Amt A   | Slide Dest B  | Slide Amt B'  ,
      'Bank0 | nGR3Off | Note PB Range'                                                                                                                ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On     | Preset Prev   | OSC1 On/Off   | OSC1 Mode     | Noise On/Off  | Unison On/Off | Glide On/Off  | Glide Legato' ,
      'Bank0 | nMB1Off | Preset Save   | Preset Next   | OSC2 On/Off   | OSC2 Mode     | -             | Unison Voices | Glide Mode'                   ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | OSC1 Level    | OSC1 Balance  | OSC1 Shape    | OSC1 Octave   | OSC1 Semi     | OSC1 Detune   | PEG1 Amount   | PEG1 Time'    ,
      'Bank0 | nMR1Off | Noise Level   | Noise Balance | Noise Color   | Volume        | Unison Delay  | Unison Detune | Glide Time'                   ,
      'Bank0 | nMR2Off | OSC2 Level    | OSC2 Balance  | OSC2 Shape    | OSC2 Octave   | OSC2 Semi     | OSC2 Detune   | PEG2 Amount   | PEG2 Time'    ,
      #=================================================================================================================================================
      'Bank1 | nGR0Off | FEG1 S Time   | FEG1 Rel      | FEG1 Loop     | FEG1 < Vel    | F1 Drive      | F1 Freq < LFO | F1 Freq < Key | F1 Freq < Env',
      'Bank1 | nGR1Off | F1 Res < LFO  | F1 Reso < Key | F1 Res < Env'                                                                                 ,
      'Bank1 | nGR2Off | FEG2 S Time   | FEG2 Rel      | FEG2 Loop     | FEG2 < Vel    | F2 Drive      | F2 Freq < LFO | F2 Freq < Key | F2 Freq < Env',
      'Bank1 | nGR3Off | F2 Res < LFO  | F2 Reso < Key | F2 Res < Env'                                                                                 ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMB0Off | F1 On/Off     | FEG1 Exp      | FEG1 Legato   | FEG1 Free'                                                                    ,
      'Bank1 | nMB1Off | F2 On/Off     | FEG2 Exp      | FEG2 Legato   | FEG2 Free     | F2 Slave'                                                     ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | F1 Type       | F1 To F2      | F1 Freq       | F1 Resonance  | FEG1 A < Vel  | FEG1 Attack   | FEG1 Decay    | FEG1 Sustain' ,
      'Bank1 | nMR1Off | Octave        | Semitone      | Detune        | Voices        | PB Range      | Key Stretch   | Key Error     | Key Priority' ,
      'Bank1 | nMR2Off | F2 Type       | -             | F2 Freq       | F2 Resonance  | FEG2 A < Vel  | FEG2 Attack   | FEG2 Decay    | FEG2 Sustain' ,
      #=================================================================================================================================================
      'Bank2 | nGR0Off | AEG1 Loop     | AEG1 < Vel    | A1 Pan < LFO  | A1 Pan < Key  | A1 Pan < Env  | AMP1 < LFO    | AMP1 < Key'                   ,
      'Bank2 | nGR1Off | LFO1 Shape    | LFO1 Speed    | LFO1 SncRate  | LFO1 PW       | LFO1 Phase    | LFO1 Delay    | LFO1 Fade In'                 ,
      'Bank2 | nGR2Off | AEG2 Loop     | AEG2 < Vel    | A2 Pan < LFO  | A2 Pan < Key  | A2 Pan < Env  | AMP2 < LFO    | AMP2 < Key'                   ,
      'Bank2 | nGR3Off | LFO2 Shape    | LFO2 Speed    | LFO2 SncRate  | LFO2 PW       | LFO2 Phase    | LFO2 Delay    | LFO2 Fade In'                 ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMB0Off | AMP1 On/Off   | AEG1 Exp      | AEG1 Legato   | AEG1 Free     | LFO1 On/Off   | LFO1 Sync     | LFO1 Retrig   | Vib On/Off'   ,
      'Bank2 | nMB1Off | AMP2 On/Off   | AEG2 Exp      | AEG2 Legato   | AEG2 Free     | LFO2 On/Off   | LFO2 Sync     | LFO2 Retrig'                  ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | AMP1 Pan      | AMP1 Level    | AEG1 A < Vel  | AEG1 Attack   | AEG1 Decay    | AEG1 Sustain  | AEG1 S Time   | AEG1 Rel'     ,
      'Bank2 | nMR1Off | Vib Delay     | Vib Fade-In   | Vib Error     | Vib < ModWh   | Vib Amount    | Vib Speed'                                    ,
      'Bank2 | nMR2Off | AMP2 Pan      | AMP2 Level    | AEG2 A < Vel  | AEG2 Attack   | AEG2 Decay    | AEG2 Sustain  | AEG2 S Time   | AEG2 Rel'     ,
    ]
    self.reg('UltraAnalog')
    self.parse_cfg()

#=======================================================================
# Class: UltraAnalog, Device: Analog, Display: Analog
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Voices", orig: "Voices" => [Mono, 2, 4, 8, 12, 16, 20, 24, 28, 32]
#   param: "PB Range", orig: "PB Range", value: 0.166667, min: 0.000000, max: 1.000000
#   param: "Volume", orig: "Volume", value: 0.704789, min: 0.000000, max: 1.000000
#   param: "Note PB Range", orig: "Note PB Range", value: 48.000000, min: 0.000000, max: 48.000000
# Q param: "Press Dest A", orig: "Press Dest A" => [No Destination, Vibrato Amount, Vibrato Speed, Unison Detune, Noise Level, Noise Balance, Noise Color, Osc 1 Pitch, Osc 1 LFO 1 -> Pitch, Osc 1 Pitch Env Depth, Osc 1 Pulse Width, Osc 1 LFO 1 -> Pulse Width, Osc 1 Sub Level, Osc 1 Sync Ratio, Osc 1 Level, Osc 1 Balance, Filter 1 Cutoff, Filter 1 LFO 1 -> Cutoff, Filter 1 Env -> Cutoff, Filter 1 Q, Filter 1 LFO 1 -> Q, Filter 1 Env -> Q, Amp 1 Volume, Amp 1 LFO 1 -> Volume, Amp 1 Pan, Amp 1 LFO 1 -> Pan, LFO 1 Rate, Osc 2 Pitch, Osc 2 LFO 2 -> Pitch, Osc 2 Pitch Env Depth, Osc 2 Pulse Width, Osc 2 LFO 2 -> Pulse Width, Osc 2 Sub Level, Osc 2 Sync Ratio, Osc 2 Level, Osc 2 Balance, Filter 2 Cutoff, Filter 2 LFO 2 -> Cutoff, Filter 2 Env -> Cutoff, Filter 2 Q, Filter 2 LFO 2 -> Q, Filter 2 Env -> Q, Amp 2 Volume, Amp 2 LFO 2 -> Volume, Amp 2 Pan, Amp 2 LFO 2 -> Pan, LFO 2 Rate]
#   param: "Press Amt A", orig: "Press Amt A", value: 0.500000, min: -1.000000, max: 1.000000
# Q param: "Press Dest B", orig: "Press Dest B" => [No Destination, Vibrato Amount, Vibrato Speed, Unison Detune, Noise Level, Noise Balance, Noise Color, Osc 1 Pitch, Osc 1 LFO 1 -> Pitch, Osc 1 Pitch Env Depth, Osc 1 Pulse Width, Osc 1 LFO 1 -> Pulse Width, Osc 1 Sub Level, Osc 1 Sync Ratio, Osc 1 Level, Osc 1 Balance, Filter 1 Cutoff, Filter 1 LFO 1 -> Cutoff, Filter 1 Env -> Cutoff, Filter 1 Q, Filter 1 LFO 1 -> Q, Filter 1 Env -> Q, Amp 1 Volume, Amp 1 LFO 1 -> Volume, Amp 1 Pan, Amp 1 LFO 1 -> Pan, LFO 1 Rate, Osc 2 Pitch, Osc 2 LFO 2 -> Pitch, Osc 2 Pitch Env Depth, Osc 2 Pulse Width, Osc 2 LFO 2 -> Pulse Width, Osc 2 Sub Level, Osc 2 Sync Ratio, Osc 2 Level, Osc 2 Balance, Filter 2 Cutoff, Filter 2 LFO 2 -> Cutoff, Filter 2 Env -> Cutoff, Filter 2 Q, Filter 2 LFO 2 -> Q, Filter 2 Env -> Q, Amp 2 Volume, Amp 2 LFO 2 -> Volume, Amp 2 Pan, Amp 2 LFO 2 -> Pan, LFO 2 Rate]
#   param: "Press Amt B", orig: "Press Amt B", value: 0.500000, min: -1.000000, max: 1.000000
# Q param: "Slide Dest A", orig: "Slide Dest A" => [No Destination, Vibrato Amount, Vibrato Speed, Unison Detune, Noise Level, Noise Balance, Noise Color, Osc 1 Pitch, Osc 1 LFO 1 -> Pitch, Osc 1 Pitch Env Depth, Osc 1 Pulse Width, Osc 1 LFO 1 -> Pulse Width, Osc 1 Sub Level, Osc 1 Sync Ratio, Osc 1 Level, Osc 1 Balance, Filter 1 Cutoff, Filter 1 LFO 1 -> Cutoff, Filter 1 Env -> Cutoff, Filter 1 Q, Filter 1 LFO 1 -> Q, Filter 1 Env -> Q, Amp 1 Volume, Amp 1 LFO 1 -> Volume, Amp 1 Pan, Amp 1 LFO 1 -> Pan, LFO 1 Rate, Osc 2 Pitch, Osc 2 LFO 2 -> Pitch, Osc 2 Pitch Env Depth, Osc 2 Pulse Width, Osc 2 LFO 2 -> Pulse Width, Osc 2 Sub Level, Osc 2 Sync Ratio, Osc 2 Level, Osc 2 Balance, Filter 2 Cutoff, Filter 2 LFO 2 -> Cutoff, Filter 2 Env -> Cutoff, Filter 2 Q, Filter 2 LFO 2 -> Q, Filter 2 Env -> Q, Amp 2 Volume, Amp 2 LFO 2 -> Volume, Amp 2 Pan, Amp 2 LFO 2 -> Pan, LFO 2 Rate]
#   param: "Slide Amt A", orig: "Slide Amt A", value: 0.500000, min: -1.000000, max: 1.000000
# Q param: "Slide Dest B", orig: "Slide Dest B" => [No Destination, Vibrato Amount, Vibrato Speed, Unison Detune, Noise Level, Noise Balance, Noise Color, Osc 1 Pitch, Osc 1 LFO 1 -> Pitch, Osc 1 Pitch Env Depth, Osc 1 Pulse Width, Osc 1 LFO 1 -> Pulse Width, Osc 1 Sub Level, Osc 1 Sync Ratio, Osc 1 Level, Osc 1 Balance, Filter 1 Cutoff, Filter 1 LFO 1 -> Cutoff, Filter 1 Env -> Cutoff, Filter 1 Q, Filter 1 LFO 1 -> Q, Filter 1 Env -> Q, Amp 1 Volume, Amp 1 LFO 1 -> Volume, Amp 1 Pan, Amp 1 LFO 1 -> Pan, LFO 1 Rate, Osc 2 Pitch, Osc 2 LFO 2 -> Pitch, Osc 2 Pitch Env Depth, Osc 2 Pulse Width, Osc 2 LFO 2 -> Pulse Width, Osc 2 Sub Level, Osc 2 Sync Ratio, Osc 2 Level, Osc 2 Balance, Filter 2 Cutoff, Filter 2 LFO 2 -> Cutoff, Filter 2 Env -> Cutoff, Filter 2 Q, Filter 2 LFO 2 -> Q, Filter 2 Env -> Q, Amp 2 Volume, Amp 2 LFO 2 -> Volume, Amp 2 Pan, Amp 2 LFO 2 -> Pan, LFO 2 Rate]
#   param: "Slide Amt B", orig: "Slide Amt B", value: 0.500000, min: -1.000000, max: 1.000000
#   param: "Octave", orig: "Octave", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "Semitone", orig: "Semitone", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "Detune", orig: "Detune", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Unison On/Off", orig: "Unison On/Off" => [Off, On]
# Q param: "Unison Voices", orig: "Unison Voices" => [2, 4]
#   param: "Unison Detune", orig: "Unison Detune", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Unison Delay", orig: "Unison Delay", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Key Priority", orig: "Key Priority" => [High, Low, Last]
#   param: "Key Stretch", orig: "Key Stretch", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Key Error", orig: "Key Error", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Vib On/Off", orig: "Vib On/Off" => [Off, On]
#   param: "Vib Speed", orig: "Vib Speed", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib Fade-In", orig: "Vib Fade-In", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Vib Amount", orig: "Vib Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Vib Error", orig: "Vib Error", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Vib Delay", orig: "Vib Delay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Vib < ModWh", orig: "Vib < ModWh", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Glide On/Off", orig: "Glide On/Off" => [Off, On]
#   param: "Glide Time", orig: "Glide Time", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Glide Mode", orig: "Glide Mode" => [Const, Prop]
# Q param: "Glide Legato", orig: "Glide Legato" => [Off, On]
# Q param: "Noise On/Off", orig: "Noise On/Off" => [Off, On]
#   param: "Noise Color", orig: "Noise Color", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Balance", orig: "Noise Balance", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Noise Level", orig: "Noise Level", value: 0.806200, min: 0.000000, max: 1.000000
# Q param: "OSC1 On/Off", orig: "OSC1 On/Off" => [Off, On]
# Q param: "OSC1 Shape", orig: "OSC1 Shape" => [Sine, Saw, Rect, Noise]
#   param: "OSC1 Octave", orig: "OSC1 Octave", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "OSC1 Semi", orig: "OSC1 Semi", value: 0.000000, min: -12.000000, max: 12.000000
# Q param: "OSC1 Mode", orig: "OSC1 Mode" => [Sub, Sync]
#   param: "PEG1 Time", orig: "PEG1 Time", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "OSC1 Detune", orig: "OSC1 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "O1 Keytrack", orig: "O1 Keytrack", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "OSC1 PW", orig: "OSC1 PW", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "O1 Sub/Sync", orig: "O1 Sub/Sync", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "OSC1 Balance", orig: "OSC1 Balance", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "PEG1 Amount", orig: "PEG1 Amount", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "OSC1 < LFO", orig: "OSC1 < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "O1 PW < LFO", orig: "O1 PW < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "OSC1 Level", orig: "OSC1 Level", value: 0.806200, min: 0.000000, max: 1.000000
# Q param: "F1 On/Off", orig: "F1 On/Off" => [Off, On]
# Q param: "F1 Type", orig: "F1 Type" => [Low-pass 12dB/oct, Low-pass 24dB/oct, Band-pass 6dB/oct, Band-pass 12dB/oct, Notch 2-pole, Notch 4-pole, High-pass 12dB/oct, High-pass 24dB/oct, Formant 6dB/oct, Formant 12dB/oct]
# Q param: "F1 Drive", orig: "F1 Drive" => [Off, Sym1, Sym2, Sym3, Asym1, Asym2, Asym3]
#   param: "F1 Freq < Key", orig: "F1 Freq < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F1 Freq", orig: "F1 Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "F1 Reso < Key", orig: "F1 Reso < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F1 Resonance", orig: "F1 Resonance", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "F1 To F2", orig: "F1 To F2", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "F1 Freq < LFO", orig: "F1 Freq < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F1 Freq < Env", orig: "F1 Freq < Env", value: 0.704761, min: -1.000000, max: 1.000000
#   param: "F1 Res < LFO", orig: "F1 Res < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F1 Res < Env", orig: "F1 Res < Env", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "FEG1 Exp", orig: "FEG1 Exp" => [Off, On]
# Q param: "FEG1 Loop", orig: "FEG1 Loop" => [Off, AD-R, ADR-R, ADS-AR]
# Q param: "FEG1 Free", orig: "FEG1 Free" => [Off, On]
# Q param: "FEG1 Legato", orig: "FEG1 Legato" => [Off, On]
#   param: "FEG1 A < Vel", orig: "FEG1 A < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG1 Attack", orig: "FEG1 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG1 Decay", orig: "FEG1 Decay", value: 0.600000, min: 0.000000, max: 1.000000
#   param: "FEG1 < Vel", orig: "FEG1 < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG1 Sustain", orig: "FEG1 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "FEG1 S Time", orig: "FEG1 S Time", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "FEG1 Rel", orig: "FEG1 Rel", value: 0.484784, min: 0.000000, max: 1.000000
# Q param: "AMP1 On/Off", orig: "AMP1 On/Off" => [Off, On]
#   param: "AMP1 < Key", orig: "AMP1 < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "AMP1 Level", orig: "AMP1 Level", value: 0.474312, min: 0.000000, max: 1.000000
#   param: "A1 Pan < Key", orig: "A1 Pan < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "AMP1 Pan", orig: "AMP1 Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "AMP1 < LFO", orig: "AMP1 < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "A1 Pan < LFO", orig: "A1 Pan < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "A1 Pan < Env", orig: "A1 Pan < Env", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "AEG1 Exp", orig: "AEG1 Exp" => [Off, On]
# Q param: "AEG1 Loop", orig: "AEG1 Loop" => [Off, AD-R, ADR-R, ADS-AR]
# Q param: "AEG1 Free", orig: "AEG1 Free" => [Off, On]
# Q param: "AEG1 Legato", orig: "AEG1 Legato" => [Off, On]
#   param: "AEG1 A < Vel", orig: "AEG1 A < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "AEG1 Attack", orig: "AEG1 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "AEG1 Decay", orig: "AEG1 Decay", value: 0.600000, min: 0.000000, max: 1.000000
#   param: "AEG1 < Vel", orig: "AEG1 < Vel", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "AEG1 Sustain", orig: "AEG1 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "AEG1 S Time", orig: "AEG1 S Time", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "AEG1 Rel", orig: "AEG1 Rel", value: 0.571805, min: 0.000000, max: 1.000000
# Q param: "LFO1 On/Off", orig: "LFO1 On/Off" => [Off, On]
# Q param: "LFO1 Shape", orig: "LFO1 Shape" => [Sine, Tri, Rect, Noise1, Noise2]
#   param: "LFO1 SncRate", orig: "LFO1 SncRate", value: 13.000000, min: 0.000000, max: 23.000000
# Q param: "LFO1 Sync", orig: "LFO1 Sync" => [Hertz, Beat]
# Q param: "LFO1 Retrig", orig: "LFO1 Retrig" => [Off, On]
#   param: "LFO1 PW", orig: "LFO1 PW", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO1 Speed", orig: "LFO1 Speed", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO1 Phase", orig: "LFO1 Phase", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO1 Delay", orig: "LFO1 Delay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO1 Fade In", orig: "LFO1 Fade In", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "OSC2 On/Off", orig: "OSC2 On/Off" => [Off, On]
# Q param: "OSC2 Shape", orig: "OSC2 Shape" => [Sine, Saw, Rect, Noise]
#   param: "OSC2 Octave", orig: "OSC2 Octave", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "OSC2 Semi", orig: "OSC2 Semi", value: 0.000000, min: -12.000000, max: 12.000000
# Q param: "OSC2 Mode", orig: "OSC2 Mode" => [Sub, Sync]
#   param: "PEG2 Time", orig: "PEG2 Time", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "OSC2 Detune", orig: "OSC2 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "O2 Keytrack", orig: "O2 Keytrack", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "OSC2 PW", orig: "OSC2 PW", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "O2 Sub/Sync", orig: "O2 Sub/Sync", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "OSC2 Balance", orig: "OSC2 Balance", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "PEG2 Amount", orig: "PEG2 Amount", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "OSC2 < LFO", orig: "OSC2 < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "O2 PW < LFO", orig: "O2 PW < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "OSC2 Level", orig: "OSC2 Level", value: 0.806200, min: 0.000000, max: 1.000000
# Q param: "F2 On/Off", orig: "F2 On/Off" => [Off, On]
# Q param: "F2 Type", orig: "F2 Type" => [Low-pass 12dB/oct, Low-pass 24dB/oct, Band-pass 6dB/oct, Band-pass 12dB/oct, Notch 2-pole, Notch 4-pole, High-pass 12dB/oct, High-pass 24dB/oct, Formant 6dB/oct, Formant 12dB/oct]
# Q param: "F2 Drive", orig: "F2 Drive" => [Off, Sym1, Sym2, Sym3, Asym1, Asym2, Asym3]
#   param: "F2 Freq < Key", orig: "F2 Freq < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F2 Freq", orig: "F2 Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "F2 Reso < Key", orig: "F2 Reso < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F2 Resonance", orig: "F2 Resonance", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "F2 Slave", orig: "F2 Slave" => [Off, On]
#   param: "F2 Freq < LFO", orig: "F2 Freq < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F2 Freq < Env", orig: "F2 Freq < Env", value: 0.704761, min: -1.000000, max: 1.000000
#   param: "F2 Res < LFO", orig: "F2 Res < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "F2 Res < Env", orig: "F2 Res < Env", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "FEG2 Exp", orig: "FEG2 Exp" => [Off, On]
# Q param: "FEG2 Loop", orig: "FEG2 Loop" => [Off, AD-R, ADR-R, ADS-AR]
# Q param: "FEG2 Free", orig: "FEG2 Free" => [Off, On]
# Q param: "FEG2 Legato", orig: "FEG2 Legato" => [Off, On]
#   param: "FEG2 A < Vel", orig: "FEG2 A < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG2 Attack", orig: "FEG2 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG2 Decay", orig: "FEG2 Decay", value: 0.600000, min: 0.000000, max: 1.000000
#   param: "FEG2 < Vel", orig: "FEG2 < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG2 Sustain", orig: "FEG2 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "FEG2 S Time", orig: "FEG2 S Time", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "FEG2 Rel", orig: "FEG2 Rel", value: 0.484784, min: 0.000000, max: 1.000000
# Q param: "AMP2 On/Off", orig: "AMP2 On/Off" => [Off, On]
#   param: "AMP2 < Key", orig: "AMP2 < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "AMP2 Level", orig: "AMP2 Level", value: 0.474312, min: 0.000000, max: 1.000000
#   param: "A2 Pan < Key", orig: "A2 Pan < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "AMP2 Pan", orig: "AMP2 Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "AMP2 < LFO", orig: "AMP2 < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "A2 Pan < LFO", orig: "A2 Pan < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "A2 Pan < Env", orig: "A2 Pan < Env", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "AEG2 Exp", orig: "AEG2 Exp" => [Off, On]
# Q param: "AEG2 Loop", orig: "AEG2 Loop" => [Off, AD-R, ADR-R, ADS-AR]
# Q param: "AEG2 Free", orig: "AEG2 Free" => [Off, On]
# Q param: "AEG2 Legato", orig: "AEG2 Legato" => [Off, On]
#   param: "AEG2 A < Vel", orig: "AEG2 A < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "AEG2 Attack", orig: "AEG2 Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "AEG2 Decay", orig: "AEG2 Decay", value: 0.600000, min: 0.000000, max: 1.000000
#   param: "AEG2 < Vel", orig: "AEG2 < Vel", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "AEG2 Sustain", orig: "AEG2 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "AEG2 S Time", orig: "AEG2 S Time", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "AEG2 Rel", orig: "AEG2 Rel", value: 0.571805, min: 0.000000, max: 1.000000
# Q param: "LFO2 On/Off", orig: "LFO2 On/Off" => [Off, On]
# Q param: "LFO2 Shape", orig: "LFO2 Shape" => [Sine, Tri, Rect, Noise1, Noise2]
#   param: "LFO2 SncRate", orig: "LFO2 SncRate", value: 13.000000, min: 0.000000, max: 23.000000
# Q param: "LFO2 Sync", orig: "LFO2 Sync" => [Hertz, Beat]
# Q param: "LFO2 Retrig", orig: "LFO2 Retrig" => [Off, On]
#   param: "LFO2 PW", orig: "LFO2 PW", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO2 Speed", orig: "LFO2 Speed", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO2 Phase", orig: "LFO2 Phase", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO2 Delay", orig: "LFO2 Delay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO2 Fade In", orig: "LFO2 Fade In", value: 0.000000, min: 0.000000, max: 1.000000

