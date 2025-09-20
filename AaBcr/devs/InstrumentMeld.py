from .Dev import Dev

class InstrumentMeld(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | A Reset     | A Reset To Voice Offset | A Filter Drive     | B Reset    | B Reset To Voice Offset | B Filter Drive'                                        ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nGR0Off | Engine B Delay    | Voice Spread      | Drive              | Volume            | A Mod A Slope    | A Mod D Slope | A Mod R Slope   | -'                   ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On         | Preset Prev       | Link Envelopes     | Limiter On        | Scale Aware      | Mono Legato   | -               | -'                   ,
      'Bank0 | nMB1Off | Preset Save       | Preset Next       | A On               | A Keytracking     | A Osc Scale Aware'                                                        ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | A Osc Type        | A Octave          | A Transpose        | A Detune          | A Osc Shape      | A Osc Tone    | A Transp Scale'                        ,
      'Bank0 | nMR1Off | A Amp Loop Mode   | A Amp Attack      | A Amp Decay        | A Amp Sustain     | A Amp Release    | A Amp A Slope | A Amp D Slope   | A Amp R Slope'       ,
      'Bank0 | nMR2Off | A Mod Loop Mode   | A Mod Attack      | A Mod Decay        | A Mod Sustain     | A Mod Release    | A Mod Initial | A Mod Peak      | A Mod Final'         ,
      #==============================================================================================================================================================================
      'Bank1 | nMB0Off | A LFO 1 Retrigger | A LFO 2 Retrigger | A Filter On        | A Glide Mode'                                                                                 ,
      'Bank1 | nMB1Off | A LFO 1 Sync      | A LFO 2 Sync      | A Filter Filter Scale Aware'                                                                                       ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | A LFO 1 Type      | A LFO 1 Phase     | A LFO 1 Rate       | A LFO 1 S. Rate   | A LFO 1 Shape    | A LFO 1 Fold  | A Glide Time'                          ,
      'Bank1 | nMR1Off | A LFO 1 FX 1 Type | A LFO 1 FX 2 Type | A LFO 1 FX 1 Scale | A LFO 1 FX 2 Ramp | A LFO 2 Waveform | A LFO 2 Rate  | A LFO 2 S. Rate | A LFO 2 Phase Offset',
      'Bank1 | nMR2Off | A Filter Type     | A Filter Freq     | A Filter Q         | A Filter L-B-H-N  | A Pan            | A Tone Filter | A Volume'                              ,
      #==============================================================================================================================================================================
      'Bank2 | nGR0Off | B Mod A Slope     | B Mod D Slope     | B Mod R Slope'                                                                                                     ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMB0Off | B On              | B Keytracking     | B Osc Scale Aware'                                                                                                 ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | B Osc Type        | B Octave          | B Transpose        | B Detune          | B Osc Shape      | B Osc Tone    | B Transp Scale'                        ,
      'Bank2 | nMR1Off | B Amp Loop Mode   | B Amp Attack      | B Amp Decay        | B Amp Sustain     | B Amp Release    | B Amp A Slope | B Amp D Slope   | B Amp R Slope'       ,
      'Bank2 | nMR2Off | B Mod Loop Mode   | B Mod Attack      | B Mod Decay        | B Mod Sustain     | B Mod Release    | B Mod Initial | B Mod Peak      | B Mod Final'         ,
      #==============================================================================================================================================================================
      'Bank3 | nMB0Off | B LFO 1 Retrigger | B LFO 2 Retrigger | B Filter On        | B Glide Mode'                                                                                 ,
      'Bank3 | nMB1Off | B LFO 1 Sync      | B LFO 2 Sync      | B Filter Filter Scale Aware'                                                                                       ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMR0Off | B LFO 1 Type      | B LFO 1 Phase     | B LFO 1 Rate       | B LFO 1 S. Rate   | B LFO 1 Shape    | B LFO 1 Fold  | B Glide Time'                          ,
      'Bank3 | nMR1Off | B LFO 1 FX 1 Type | B LFO 1 FX 2 Type | B LFO 1 FX 1 Scale | B LFO 1 FX 2 Ramp | B LFO 2 Waveform | B LFO 2 Rate  | B LFO 2 S. Rate | B LFO 2 Phase Offset',
      'Bank3 | nMR2Off | B Filter Type     | B Filter Freq     | B Filter Q         | B Filter L-B-H-N  | B Pan            | B Tone Filter | B Volume'                              ,
    ]
    self.reg('InstrumentMeld')
    self.parse_cfg()

#=======================================================================
# Class: InstrumentMeld, Device: Meld, Display: Meld
#   param: "Engine B Delay", orig: "MeldVoice_EngineBDelay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Voice Spread", orig: "MeldVoice_VoiceSpreadAmount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Drive", orig: "MeldVoice_Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Volume", orig: "Volume", value: 0.575440, min: 0.000000, max: 1.000000
#   param: "A Mod A Slope", orig: "MeldVoice_EngineA_FilterEnvelope_Slopes_Attack", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "A Mod D Slope", orig: "MeldVoice_EngineA_FilterEnvelope_Slopes_Decay", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "A Mod R Slope", orig: "MeldVoice_EngineA_FilterEnvelope_Slopes_Release", value: 0.750000, min: 0.000000, max: 1.000000

# Q param: "Device On", orig: "On" => [Off, On]
# Q param: "Link Envelopes", orig: "MeldVoice_LinkAmpEnvelopes" => [Off, On]
# Q param: "Limiter On", orig: "MeldVoice_LimiterOn" => [Off, On]
# Q param: "Scale Aware", orig: "MeldVoice_UseScale" => [Off, On]
# Q param: "Mono Legato", orig: "MonoLegato" => [Off, On]
# Q param: "A On", orig: "MeldVoice_EngineA_On" => [Off, On]
# Q param: "A Keytracking", orig: "MeldVoice_EngineA_Oscillator_Pitch_Keytracking" => [Off, On]
# Q param: "A Osc Scale Aware", orig: "MeldVoice_EngineA_Oscillator_UseScale" => [Off, On]

# Q param: "A Osc Type", orig: "MeldVoice_EngineA_Oscillator_OscillatorType" => [Basic Shapes, Dual Basic Shapes  (♭♯), Noisy Shapes, Square Sync, Square 5th, Sub, Swarm Sine  (♭♯), Swarm Triangle  (♭♯), Swarm Saw  (♭♯), Swarm Square  (♭♯), Harmonic Fm, Fold Fm, Squelch, Simple Fm, Chip  (♭♯), Shepard's Pi, Tarp, Extratone, Noise Loop, Filtered Noise, Bitgrunge, Crackle, Rain, Bubble]
#   param: "A Octave", orig: "MeldVoice_EngineA_Oscillator_Pitch_TransposeOctaves", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "A Transpose", orig: "MeldVoice_EngineA_Oscillator_Pitch_Transpose", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "A Detune", orig: "MeldVoice_EngineA_Oscillator_Pitch_Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "A Osc Shape", orig: "MeldVoice_EngineA_Oscillator_Macro1", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A Osc Tone", orig: "MeldVoice_EngineA_Oscillator_Macro2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A Transp Scale", orig: "MeldVoice_EngineA_Oscillator_Pitch_TransposeScaleDegrees", value: 0.000000, min: -48.000000, max: 48.000000

# Q param: "A Amp Loop Mode", orig: "MeldVoice_EngineA_AmpEnvelope_LoopMode" => [None, Trigger, Loop, AD Loop]
#   param: "A Amp Attack", orig: "MeldVoice_EngineA_AmpEnvelope_Times_Attack", value: 0.070711, min: 0.000000, max: 1.000000
#   param: "A Amp Decay", orig: "MeldVoice_EngineA_AmpEnvelope_Times_Decay", value: 0.349748, min: 0.000000, max: 1.000000
#   param: "A Amp Sustain", orig: "MeldVoice_EngineA_AmpEnvelope_Sustain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "A Amp Release", orig: "MeldVoice_EngineA_AmpEnvelope_Times_Release", value: 0.186606, min: 0.000000, max: 1.000000
#   param: "A Amp A Slope", orig: "MeldVoice_EngineA_AmpEnvelope_Slopes_Attack", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "A Amp D Slope", orig: "MeldVoice_EngineA_AmpEnvelope_Slopes_Decay", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "A Amp R Slope", orig: "MeldVoice_EngineA_AmpEnvelope_Slopes_Release", value: 0.750000, min: 0.000000, max: 1.000000

# Q param: "A Mod Loop Mode", orig: "MeldVoice_EngineA_FilterEnvelope_LoopMode" => [None, Trigger, Loop, AD Loop]
#   param: "A Mod Attack", orig: "MeldVoice_EngineA_FilterEnvelope_Times_Attack", value: 0.070711, min: 0.000000, max: 1.000000
#   param: "A Mod Decay", orig: "MeldVoice_EngineA_FilterEnvelope_Times_Decay", value: 0.349748, min: 0.000000, max: 1.000000
#   param: "A Mod Sustain", orig: "MeldVoice_EngineA_FilterEnvelope_Values_Sustain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A Mod Release", orig: "MeldVoice_EngineA_FilterEnvelope_Times_Release", value: 0.186606, min: 0.000000, max: 1.000000
#   param: "A Mod Initial", orig: "MeldVoice_EngineA_FilterEnvelope_Values_Initial", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A Mod Peak", orig: "MeldVoice_EngineA_FilterEnvelope_Values_Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "A Mod Final", orig: "MeldVoice_EngineA_FilterEnvelope_Values_Final", value: 0.000000, min: 0.000000, max: 1.000000
#--------------------------
# Q param: "A LFO 1 Retrigger", orig: "MeldVoice_EngineA_Lfo1_Retrigger" => [Off, On]
# Q param: "A LFO 1 Sync", orig: "MeldVoice_EngineA_Lfo1_Sync" => [Free, Tempo]
# Q param: "A LFO 2 Retrigger", orig: "MeldVoice_EngineA_Lfo2_Retrigger" => [Off, On]
# Q param: "A LFO 2 Sync", orig: "MeldVoice_EngineA_Lfo2_Sync" => [Free, Tempo]
# Q param: "A Filter On", orig: "MeldVoice_EngineA_Filter_On" => [Off, On]
# Q param: "A Filter Filter Scale Aware", orig: "MeldVoice_EngineA_Filter_UseScale" => [Off, On]

# Q param: "A LFO 1 Type", orig: "MeldVoice_EngineA_Lfo1_GeneratorType" => [Basic Shapes, Ramp, Wander, Alternate, Euclid, Pulsate]
#   param: "A LFO 1 Phase", orig: "MeldVoice_EngineA_Lfo1_PhaseOffset", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A LFO 1 Rate", orig: "MeldVoice_EngineA_Lfo1_Rate", value: 0.231380, min: 0.000000, max: 1.000000
#   param: "A LFO 1 S. Rate", orig: "MeldVoice_EngineA_Lfo1_SyncedRate", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "A LFO 1 Shape", orig: "MeldVoice_EngineA_Lfo1_GeneratorMacro1", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A LFO 1 Fold", orig: "MeldVoice_EngineA_Lfo1_GeneratorMacro2", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "A Glide Mode", orig: "MeldVoice_EngineA_GlideMode" => [Portamento, Glissando]
#   param: "A Glide Time", orig: "MeldVoice_EngineA_GlideTime", value: 0.000000, min: 0.000000, max: 1.000000

# Q param: "A LFO 1 FX 1 Type", orig: "MeldVoice_EngineA_Lfo1_Transformer1Type" => [None, Offset, Attenuverter, Gate, Skew Unipolar, Skew Bipolar, Unipolarizer, Quantizer, S&H, Independent S&H, Clipper, Fade In, Fade Out, Slew Down, Slew Up, Slew Up & Down, Trig Env, Comparator]
# Q param: "A LFO 1 FX 2 Type", orig: "MeldVoice_EngineA_Lfo1_Transformer2Type" => [None, Offset, Attenuverter, Gate, Skew Unipolar, Skew Bipolar, Unipolarizer, Quantizer, S&H, Independent S&H, Clipper, Fade In, Fade Out, Slew Down, Slew Up, Slew Up & Down, Trig Env, Comparator]
#   param: "A LFO 1 FX 1 Scale", orig: "MeldVoice_EngineA_Lfo1_Transformer1Macro", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A LFO 1 FX 2 Ramp", orig: "MeldVoice_EngineA_Lfo1_Transformer2Macro", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "A LFO 2 Waveform", orig: "MeldVoice_EngineA_Lfo2_Waveform" => [Sine, Tri, Saw Up, Saw Down, Rectangle, Random S&H]
#   param: "A LFO 2 Rate", orig: "MeldVoice_EngineA_Lfo2_Rate", value: 0.416011, min: 0.000000, max: 1.000000
#   param: "A LFO 2 S. Rate", orig: "MeldVoice_EngineA_Lfo2_SyncedRate", value: 12.000000, min: 0.000000, max: 21.000000
#   param: "A LFO 2 Phase Offset", orig: "MeldVoice_EngineA_Lfo2_PhaseOffset", value: 0.000000, min: 0.000000, max: 1.000000

# Q param: "A Filter Type", orig: "MeldVoice_EngineA_Filter_FilterType" => [SVF 12dB, SVF 24dB, LP 12dB MS2, HP 12dB MS2, BP 12dB OSR, LP Crunch 12dB, LP Switched Res, Filther, Eq Peak, Eq Notch, Phaser, Redux, Vowel, Comb +, Comb -, Plate Resonator  (♭♯), Membrane Resonator  (♭♯)]
#   param: "A Filter Freq", orig: "MeldVoice_EngineA_Filter_Frequency", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "A Filter Q", orig: "MeldVoice_EngineA_Filter_Macro1", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A Filter L-B-H-N", orig: "MeldVoice_EngineA_Filter_Macro2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "A Pan", orig: "MeldVoice_EngineA_Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "A Tone Filter", orig: "MeldVoice_EngineA_ToneFilter", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "A Volume", orig: "MeldVoice_EngineA_Volume", value: 0.635135, min: 0.000000, max: 1.000000
#-------------------------------
#   param: "B Mod A Slope", orig: "MeldVoice_EngineB_FilterEnvelope_Slopes_Attack", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "B Mod D Slope", orig: "MeldVoice_EngineB_FilterEnvelope_Slopes_Decay", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "B Mod R Slope", orig: "MeldVoice_EngineB_FilterEnvelope_Slopes_Release", value: 0.750000, min: 0.000000, max: 1.000000

# Q param: "B On", orig: "MeldVoice_EngineB_On" => [Off, On]
# Q param: "B Keytracking", orig: "MeldVoice_EngineB_Oscillator_Pitch_Keytracking" => [Off, On]
# Q param: "B Osc Scale Aware", orig: "MeldVoice_EngineB_Oscillator_UseScale" => [Off, On]

# Q param: "B Osc Type", orig: "MeldVoice_EngineB_Oscillator_OscillatorType" => [Basic Shapes, Dual Basic Shapes  (♭♯), Noisy Shapes, Square Sync, Square 5th, Sub, Swarm Sine  (♭♯), Swarm Triangle  (♭♯), Swarm Saw  (♭♯), Swarm Square  (♭♯), Harmonic Fm, Fold Fm, Squelch, Simple Fm, Chip  (♭♯), Shepard's Pi, Tarp, Extratone, Noise Loop, Filtered Noise, Bitgrunge, Crackle, Rain, Bubble]
#   param: "B Octave", orig: "MeldVoice_EngineB_Oscillator_Pitch_TransposeOctaves", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "B Transpose", orig: "MeldVoice_EngineB_Oscillator_Pitch_Transpose", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "B Detune", orig: "MeldVoice_EngineB_Oscillator_Pitch_Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "B Osc Shape", orig: "MeldVoice_EngineB_Oscillator_Macro1", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B Osc Tone", orig: "MeldVoice_EngineB_Oscillator_Macro2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B Transp Scale", orig: "MeldVoice_EngineB_Oscillator_Pitch_TransposeScaleDegrees", value: 0.000000, min: -48.000000, max: 48.000000

# Q param: "B Amp Loop Mode", orig: "MeldVoice_EngineB_AmpEnvelope_LoopMode" => [None, Trigger, Loop, AD Loop]
#   param: "B Amp Attack", orig: "MeldVoice_EngineB_AmpEnvelope_Times_Attack", value: 0.070711, min: 0.000000, max: 1.000000
#   param: "B Amp Decay", orig: "MeldVoice_EngineB_AmpEnvelope_Times_Decay", value: 0.349748, min: 0.000000, max: 1.000000
#   param: "B Amp Sustain", orig: "MeldVoice_EngineB_AmpEnvelope_Sustain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "B Amp Release", orig: "MeldVoice_EngineB_AmpEnvelope_Times_Release", value: 0.186606, min: 0.000000, max: 1.000000
#   param: "B Amp A Slope", orig: "MeldVoice_EngineB_AmpEnvelope_Slopes_Attack", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "B Amp D Slope", orig: "MeldVoice_EngineB_AmpEnvelope_Slopes_Decay", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "B Amp R Slope", orig: "MeldVoice_EngineB_AmpEnvelope_Slopes_Release", value: 0.750000, min: 0.000000, max: 1.000000

# Q param: "B Mod Loop Mode", orig: "MeldVoice_EngineB_FilterEnvelope_LoopMode" => [None, Trigger, Loop, AD Loop]
#   param: "B Mod Attack", orig: "MeldVoice_EngineB_FilterEnvelope_Times_Attack", value: 0.070711, min: 0.000000, max: 1.000000
#   param: "B Mod Decay", orig: "MeldVoice_EngineB_FilterEnvelope_Times_Decay", value: 0.349748, min: 0.000000, max: 1.000000
#   param: "B Mod Sustain", orig: "MeldVoice_EngineB_FilterEnvelope_Values_Sustain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B Mod Release", orig: "MeldVoice_EngineB_FilterEnvelope_Times_Release", value: 0.186606, min: 0.000000, max: 1.000000
#   param: "B Mod Initial", orig: "MeldVoice_EngineB_FilterEnvelope_Values_Initial", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B Mod Peak", orig: "MeldVoice_EngineB_FilterEnvelope_Values_Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "B Mod Final", orig: "MeldVoice_EngineB_FilterEnvelope_Values_Final", value: 0.000000, min: 0.000000, max: 1.000000
#-------------------------------
# Q param: "B LFO 1 Retrigger", orig: "MeldVoice_EngineB_Lfo1_Retrigger" => [Off, On]
# Q param: "B LFO 1 Sync", orig: "MeldVoice_EngineB_Lfo1_Sync" => [Free, Tempo]
# Q param: "B LFO 2 Retrigger", orig: "MeldVoice_EngineB_Lfo2_Retrigger" => [Off, On]
# Q param: "B LFO 2 Sync", orig: "MeldVoice_EngineB_Lfo2_Sync" => [Free, Tempo]
# Q param: "B Filter On", orig: "MeldVoice_EngineB_Filter_On" => [Off, On]
# Q param: "B Filter Filter Scale Aware", orig: "MeldVoice_EngineB_Filter_UseScale" => [Off, On]

# Q param: "B LFO 1 Type", orig: "MeldVoice_EngineB_Lfo1_GeneratorType" => [Basic Shapes, Ramp, Wander, Alternate, Euclid, Pulsate]
#   param: "B LFO 1 Phase", orig: "MeldVoice_EngineB_Lfo1_PhaseOffset", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B LFO 1 Rate", orig: "MeldVoice_EngineB_Lfo1_Rate", value: 0.231380, min: 0.000000, max: 1.000000
#   param: "B LFO 1 S. Rate", orig: "MeldVoice_EngineB_Lfo1_SyncedRate", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "B LFO 1 Shape", orig: "MeldVoice_EngineB_Lfo1_GeneratorMacro1", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B LFO 1 Fold", orig: "MeldVoice_EngineB_Lfo1_GeneratorMacro2", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "B Glide Mode", orig: "MeldVoice_EngineB_GlideMode" => [Portamento, Glissando]
#   param: "B Glide Time", orig: "MeldVoice_EngineB_GlideTime", value: 0.000000, min: 0.000000, max: 1.000000

# Q param: "B LFO 1 FX 1 Type", orig: "MeldVoice_EngineB_Lfo1_Transformer1Type" => [None, Offset, Attenuverter, Gate, Skew Unipolar, Skew Bipolar, Unipolarizer, Quantizer, S&H, Independent S&H, Clipper, Fade In, Fade Out, Slew Down, Slew Up, Slew Up & Down, Trig Env, Comparator]
#   param: "B LFO 1 FX 1 Scale", orig: "MeldVoice_EngineB_Lfo1_Transformer1Macro", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "B LFO 1 FX 2 Type", orig: "MeldVoice_EngineB_Lfo1_Transformer2Type" => [None, Offset, Attenuverter, Gate, Skew Unipolar, Skew Bipolar, Unipolarizer, Quantizer, S&H, Independent S&H, Clipper, Fade In, Fade Out, Slew Down, Slew Up, Slew Up & Down, Trig Env, Comparator]
#   param: "B LFO 1 FX 2 Ramp", orig: "MeldVoice_EngineB_Lfo1_Transformer2Macro", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "B LFO 2 Waveform", orig: "MeldVoice_EngineB_Lfo2_Waveform" => [Sine, Tri, Saw Up, Saw Down, Rectangle, Random S&H]
#   param: "B LFO 2 Rate", orig: "MeldVoice_EngineB_Lfo2_Rate", value: 0.416011, min: 0.000000, max: 1.000000
#   param: "B LFO 2 S. Rate", orig: "MeldVoice_EngineB_Lfo2_SyncedRate", value: 12.000000, min: 0.000000, max: 21.000000
#   param: "B LFO 2 Phase Offset", orig: "MeldVoice_EngineB_Lfo2_PhaseOffset", value: 0.000000, min: 0.000000, max: 1.000000

# Q param: "B Filter Type", orig: "MeldVoice_EngineB_Filter_FilterType" => [SVF 12dB, SVF 24dB, LP 12dB MS2, HP 12dB MS2, BP 12dB OSR, LP Crunch 12dB, LP Switched Res, Filther, Eq Peak, Eq Notch, Phaser, Redux, Vowel, Comb +, Comb -, Plate Resonator  (♭♯), Membrane Resonator  (♭♯)]
#   param: "B Filter Freq", orig: "MeldVoice_EngineB_Filter_Frequency", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "B Filter Q", orig: "MeldVoice_EngineB_Filter_Macro1", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B Filter L-B-H-N", orig: "MeldVoice_EngineB_Filter_Macro2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "B Pan", orig: "MeldVoice_EngineB_Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "B Tone Filter", orig: "MeldVoice_EngineB_ToneFilter", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "B Volume", orig: "MeldVoice_EngineB_Volume", value: 0.635135, min: 0.000000, max: 1.000000

