from .Dev import Dev

class StringStudio(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | Exc Prot < Vel  | Exc Prot < Key  | Exc Stiff < Vel | Exc Stiff < Key | Exc Vel < Vel   | Exc Vel < Key   | E Pos < Vel     | E Pos < Key',
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On       | Preset Prev     | Exc On/Off      | E Pos Abs'                                                                          ,
      'Bank0 | nMB1Off | Preset Save     | Preset Next     | Term On/Off     | Pickup On/Off'                                                                      ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Exciter Type    | Exc Protrusion  | Exc Stiffness   | Exc Velocity    | E Pos           | Exc Damping'                                    ,
      'Bank0 | nMR1Off | String Decay    | S Decay < Key   | S Decay Ratio   | Str Inharmon    | Str Damping     | S Damp < Key'                                   ,
      'Bank0 | nMR2Off | T Mass < Vel    | T Mass < Key    | Term Mass       | Term Fng Stiff  | Term Fret Stiff | Pickup Pos'                                     ,
      #=============================================================================================================================================================
      'Bank1 | nGR0Off | D Mass < Key    | D Stiff < Key   | D Velo < Key    | D Pos < Key     | D Pos < Vel'                                                      ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMB0Off | Damper On       | D Pos Abs       | Vibrato On/Off'                                                                                       ,
      'Bank1 | nMB1Off | Damper Gated    | -               | Body On/Off'                                                                                          ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | Damper Mass     | D Stiffness     | D Velocity      | Damp Pos        | D Damping'                                                        ,
      'Bank1 | nMR1Off | Vib Delay       | Vib Fade-In     | Vib Speed       | Vib Amount      | Vib < ModWh     | Vib Error'                                      ,
      'Bank1 | nMR2Off | Body Type       | Body Size       | Body Decay      | Body Mix        | Body Low-Cut    | Body High-Cut   | Volume          | -'          ,
      #=============================================================================================================================================================
      'Bank2 | nGR0Off | Filter Type'                                                                                                                              ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMB0Off | Filter On/Off   | FEG On/Off      | LFO On/Off'                                                                                           ,
      'Bank2 | nMB1Off | -               | -               | LFO Sync On'                                                                                          ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | Filter Freq     | Filter Reso     | Freq < Env      | Reso < Env      | Freq < LFO      | Reso < LFO      | Freq < Key      | Reso < Key' ,
      'Bank2 | nMR1Off | FEG Attack      | FEG Att < Vel   | FEG Decay       | FEG Sustain     | FEG < Vel       | FEG Release'                                    ,
      'Bank2 | nMR2Off | LFO Shape       | LFO Speed       | LFO SyncRate    | LFO Delay       | LFO Fade In'                                                      ,
      #=============================================================================================================================================================
      'Bank3 | nMB0Off | Porta On/Off    | Porta Legato    | Unison On/Off'                                                                                        ,
      'Bank3 | nMB1Off | -               | Porta Prop      | Unison Voices'                                                                                        ,
      #-------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMR0Off | Press Dest A    | Press Amt A     | Press Dest B    | Press Amt B     | Slide Dest A    | Slide Amt A     | Slide Dest B    | Slide Amt B',
      'Bank3 | nMR1Off | PB Range        | Note PB Range   | Uni Detune      | Uni Delay'                                                                          ,
      'Bank3 | nMR2Off | Octave          | Semitone        | Fine Tune       | Voices          | Stretch         | Error           | Key Priority    | Porta Time' ,
    ]
    self.reg('StringStudio')
    self.parse_cfg()

#=======================================================================
# Class: StringStudio, Device: Tension, Display: Tension
#   param: "Exc Prot < Vel", orig: "Exc ForceMassProt < Vel", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Exc Prot < Key", orig: "Exc ForceMassProt < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Exc Stiff < Vel", orig: "Exc FricStiff < Vel", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Exc Stiff < Key", orig: "Exc FricStiff < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Exc Vel < Vel", orig: "Exc Vel < Vel", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Exc Vel < Key", orig: "Exc Vel < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "E Pos < Vel", orig: "E Pos < Vel", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "E Pos < Key", orig: "E Pos < Key", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Exc On/Off", orig: "Exc On/Off" => [Off, On]
# Q param: "Term On/Off", orig: "Term On/Off" => [Off, On]
# Q param: "E Pos Abs", orig: "E Pos Abs" => [Off, On]
# Q param: "Pickup On/Off", orig: "Pickup On/Off" => [Off, On]
# Q param: "Exciter Type", orig: "Exciter Type" => [Bow, Hammer, Hammer (bouncing), Plectrum]
#   param: "Exc Protrusion", orig: "Exc ForceMassProt", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Exc Stiffness", orig: "Exc FricStiff", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Exc Velocity", orig: "Exc Velocity", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "E Pos", orig: "E Pos", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Exc Damping", orig: "Exc Damping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "String Decay", orig: "String Decay", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "S Decay < Key", orig: "S Decay < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "S Decay Ratio", orig: "S Decay Ratio", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Str Inharmon", orig: "Str Inharmon", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Str Damping", orig: "Str Damping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "S Damp < Key", orig: "S Damp < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "T Mass < Vel", orig: "T Mass < Vel", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "T Mass < Key", orig: "T Mass < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Term Mass", orig: "Term Mass", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Term Fng Stiff", orig: "Term Fng Stiff", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Term Fret Stiff", orig: "Term Fret Stiff", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Pickup Pos", orig: "Pickup Pos", value: 0.500000, min: 0.000000, max: 1.000000
#-------------------------
#   param: "D Mass < Key", orig: "D Mass < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "D Stiff < Key", orig: "D Stiff < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "D Velo < Key", orig: "D Velo < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "D Pos < Key", orig: "D Pos < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "D Pos < Vel", orig: "D Pos < Vel", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "Damper On", orig: "Damper On" => [Off, On]
# Q param: "Damper Gated", orig: "Damper Gated" => [Off, On]
# Q param: "D Pos Abs", orig: "D Pos Abs" => [Off, On]
# Q param: "Vibrato On/Off", orig: "Vibrato On/Off" => [Off, On]
# Q param: "Body On/Off", orig: "Body On/Off" => [Off, On]
#   param: "Damper Mass", orig: "Damper Mass", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "D Stiffness", orig: "D Stiffness", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "D Velocity", orig: "D Velocity", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Damp Pos", orig: "Damp Pos", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "D Damping", orig: "D Damping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib Delay", orig: "Vib Delay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib Fade-In", orig: "Vib Fade-In", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib Speed", orig: "Vib Speed", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib Amount", orig: "Vib Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib < ModWh", orig: "Vib < ModWh", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Vib Error", orig: "Vib Error", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Body Type", orig: "Body Type" => [Piano, Guitar, Violin, Generic]
# Q param: "Body Size", orig: "Body Size" => [XS, S, M, L, XL]
#   param: "Body Decay", orig: "Body Decay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Body Mix", orig: "Body Mix", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Body Low-Cut", orig: "Body Low-Cut", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Body High-Cut", orig: "Body High-Cut", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Volume", orig: "Volume", value: 0.705000, min: 0.000000, max: 1.000000
#-------------------------
# Q param: "Filter Type", orig: "Filter Type" => [Low-pass 12dB/oct, Low-pass 24dB/oct, Band-pass 6dB/oct, Band-pass 12dB/oct, Notch 2-pole, Notch 4-pole, High-pass 12dB/oct, High-pass 24dB/oct, Formant 6dB/oct, Formant 12dB/oct]
# Q param: "Filter On/Off", orig: "Filter On/Off" => [Off, On]
# Q param: "FEG On/Off", orig: "FEG On/Off" => [Off, On]
# Q param: "LFO On/Off", orig: "LFO On/Off" => [Off, On]
# Q param: "LFO Sync On", orig: "LFO Sync On" => [Hertz, Beat]
#   param: "Filter Freq", orig: "Filter Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Filter Reso", orig: "Filter Reso", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Freq < Env", orig: "Freq < Env", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Reso < Env", orig: "Reso < Env", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Freq < LFO", orig: "Freq < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Reso < LFO", orig: "Reso < LFO", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Freq < Key", orig: "Freq < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Reso < Key", orig: "Reso < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "FEG Attack", orig: "FEG Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG Att < Vel", orig: "FEG Att < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG Decay", orig: "FEG Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "FEG Sustain", orig: "FEG Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "FEG < Vel", orig: "FEG < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "FEG Release", orig: "FEG Release", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "LFO Shape", orig: "LFO Shape" => [Sine, Tri, Rect, Random 1, Random 2]
#   param: "LFO Speed", orig: "LFO Speed", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO SyncRate", orig: "LFO SyncRate", value: 13.000000, min: 0.000000, max: 23.000000
#   param: "LFO Fade In", orig: "LFO Fade In", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO Delay", orig: "LFO Delay", value: 0.500000, min: 0.000000, max: 1.000000
#-------------------------
# Q param: "Porta On/Off", orig: "Porta On/Off" => [Off, On]
# Q param: "Porta Legato", orig: "Porta Legato" => [Off, On]
# Q param: "Porta Prop", orig: "Porta Prop" => [Off, On]
# Q param: "Unison On/Off", orig: "Unison On/Off" => [Off, On]
# Q param: "Unison Voices", orig: "Unison Voices" => [2, 4]
# Q param: "Press Dest A", orig: "Press Dest A" => [None, Voice Volume, Vibrato Amount, Vibrato Speed, Unison Detune, String Inharmon., LFO Rate, F. Cutoff, F. Cut. LFO Depth, F. Cut. Env Depth, F. Q, F. Q LFO Depth, F. Q Env Depth]
#   param: "Press Amt A", orig: "Press Amt A", value: 0.250000, min: -1.000000, max: 1.000000
# Q param: "Press Dest B", orig: "Press Dest B" => [None, Voice Volume, Vibrato Amount, Vibrato Speed, Unison Detune, String Inharmon., LFO Rate, F. Cutoff, F. Cut. LFO Depth, F. Cut. Env Depth, F. Q, F. Q LFO Depth, F. Q Env Depth]
#   param: "Press Amt B", orig: "Press Amt B", value: 0.500000, min: -1.000000, max: 1.000000
# Q param: "Slide Dest A", orig: "Slide Dest A" => [None, Voice Volume, Vibrato Amount, Vibrato Speed, Unison Detune, String Inharmon., LFO Rate, F. Cutoff, F. Cut. LFO Depth, F. Cut. Env Depth, F. Q, F. Q LFO Depth, F. Q Env Depth]
#   param: "Slide Amt A", orig: "Slide Amt A", value: 0.500000, min: -1.000000, max: 1.000000
# Q param: "Slide Dest B", orig: "Slide Dest B" => [None, Voice Volume, Vibrato Amount, Vibrato Speed, Unison Detune, String Inharmon., LFO Rate, F. Cutoff, F. Cut. LFO Depth, F. Cut. Env Depth, F. Q, F. Q LFO Depth, F. Q Env Depth]
#   param: "Slide Amt B", orig: "Slide Amt B", value: 0.500000, min: -1.000000, max: 1.000000
#   param: "PB Range", orig: "PB Range", value: 2.000000, min: 0.000000, max: 12.000000
#   param: "Note PB Range", orig: "Note PB Range", value: 48.000000, min: 0.000000, max: 48.000000
#   param: "Uni Detune", orig: "Uni Detune", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Uni Delay", orig: "Uni Delay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Octave", orig: "Octave", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "Semitone", orig: "Semitone", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "Fine Tune", orig: "Fine Tune", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Voices", orig: "Voices" => [Mono, 2, 4, 8, 12, 16, 20, 24, 28, 32]
#   param: "Stretch", orig: "Stretch", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Error", orig: "Error", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Key Priority", orig: "Key Priority" => [High, Low, Last]
#   param: "Porta Time", orig: "Porta Time", value: 0.500000, min: 0.000000, max: 1.000000

