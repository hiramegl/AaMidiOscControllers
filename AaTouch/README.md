# FEATURES

* Script in Macos to detect IP address and setup raspberry pi address
* Script in Raspberry pi to detct ip addres and setup macos address

CLIPS:
* Clips mode
* zoom map
* Sends mode
* grid   mode: SELECT / FIRE
* launch mode: FIRE / FIRE & SELECT
* clips listeners
* when adding/removing tracks
* when adding/removing scenes
  * stop
  * mute
  * solo
  * monitoring
  * arm
  * select
  * pan reset
  * A/B cross
  * vol 0 dB
  * vol -inf dB
  * sends off
  * select
* Volumes
* Loop Extra
* Coarse detune + reset
* Fine detune + reset
* Audio gain
* reset detunes & gain
* Audio gain selected clip listener
* Faders picker
* Sync volumes (fix track listeners for volumes)

SEQ:
* grid
* Update GUI when notes change
* update correctly bits when loop start changes (it should be shifted left-right)
* move notes in Live and update GUI
* Region selection indicators / BIT CMD Operator
* zoom map
* len & vel selection
* scale selection (chromatic & extended)
* Loop
  - Roll 1/8, 1/4 -> Loop Button
* Clip tools:
  - Follow toggle
* Bug when using a region in SEQ MAP in the second column (wrong time offset)
'/shift/amount'. Msg: [['/shift/amount', ',f', 2.0]]
'/shift/type'. Msg: [['/shift/type', ',s', 'SH']] CS, CE, LS, LE, SH
'/shift/dir/0'. Msg: [['/shift/dir/0', ',']]
'/shift/dir/1'. Msg: [['/shift/dir/1', ',']]
* SHIFT, edge cases and correct values for amount
* Note selection (chromatic)
  - Master note selection (chromatic)
* BitOp
* BUG, BitOp not working with Section=1
* Note selection (with scale)
  - Master note selection (with scale)
* Grid handle scales and roots
* Bit Commands:
  - All: Mute Solo VelRst Del
  - Sel: Mute Solo VelRst Del
* Shift Commands:
  - All: Left Right Down Up
  - Sel: Left Right Down Up
* Fact & Chop Commands:
  - All: Div Mul 2 3
  - Sel: Div Mul 2 3
* Rhythms
* Sel Clip play
* Sel Track Stop
* Sel Track Mute
* Sel Track Solo
* BitOp Cmd:
  Mul, Div, Chop2, Chop3
* Clip Navigation
* Chords
* Transpose
* Warp
* Crop
* Roll: beat and half beat
* Clip tools:
  * Loop toggle, loop dupl, clip dupl
  * CLIP/DEV toggle, LOOP/ENV toggle
* Bit Encoders Modes:
  * Time shift
  * Len
  * Vel
  * Reset
* Bit Encoders
* Master Encoder
* Encoder Modes
* sel track sends

============================================================

TODO:

Effects:
  - Shifter
  - Hybrid-Reverb
  - Auto Shift
  - Spectral-resonator
  - Spectral-time
  - Corpus
  - Roar
  - Multiband Dynamics

  - Looper
  - Erosion
  - Gate

  - Amp
  - Cabinet
  - Pedal

  - Drum-Buss
  - Dynamic Tube
  - Glue Compressor
  - Limiter
  - Saturator
  - Utility
  - Vinyl Distortion

  - Channel EQ
  - Auto-Filter

<pre>
#=======================================================================
# Class: Amp, Device: Amp, Display: Amp - 10
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Amp Type", orig: "Amp Type" => [Clean, Boost, Blues, Rock, Lead, Heavy, Bass]
#   param: "Bass", orig: "Bass", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Middle", orig: "Middle", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Treble", orig: "Treble", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Presence", orig: "Presence", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Gain", orig: "Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Volume", orig: "Volume", value: 0.900000, min: 0.000000, max: 1.000000
# Q param: "Dual Mono", orig: "Dual Mono" => [Off, On]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: AutoFilter, Device: Auto Filter, Display: Auto Filter - 26
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Filter Type", orig: "Filter Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter Circuit - LP/HP", orig: "Filter Circuit - LP/HP" => [Clean, OSR, MS2, SMP, PRD]
# Q param: "Filter Circuit - BP/NO/Morph", orig: "Filter Circuit - BP/NO/Morph" => [Clean, OSR]
# Q param: "Slope", orig: "Slope" => [12 dB, 24 dB]
#   param: "Frequency", orig: "Frequency", value: 127.000000, min: 20.000000, max: 135.000000
#   param: "Resonance", orig: "Resonance", value: 0.000000, min: 0.000000, max: 1.250000
#   param: "Morph", orig: "Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Drive", orig: "Drive", value: 0.000000, min: 0.000000, max: 24.000000
#   param: "Env. Modulation", orig: "Env. Modulation", value: 0.000000, min: -127.000000, max: 127.000000
#   param: "Env. Attack", orig: "Env. Attack", value: 6.000000, min: 0.100000, max: 30.000000
#   param: "Env. Release", orig: "Env. Release", value: 200.000000, min: 0.100000, max: 400.000000
#   param: "LFO Amount", orig: "LFO Amount", value: 0.000000, min: 0.000000, max: 30.000000
# Q param: "LFO Waveform", orig: "LFO Waveform" => [Sine, Square, Triangle, SawUp, SawDown, S&H Stereo, S&H Mono]
#   param: "LFO Frequency", orig: "LFO Frequency", value: 0.347131, min: 0.000000, max: 1.000000
# Q param: "LFO Sync", orig: "LFO Sync" => [Free, Sync]
#   param: "LFO Sync Rate", orig: "LFO Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
# Q param: "LFO Stereo Mode", orig: "LFO Stereo Mode" => [Phase, Spin]
#   param: "LFO Spin", orig: "LFO Spin", value: 0.000000, min: 0.000000, max: 0.500000
#   param: "LFO Phase", orig: "LFO Phase", value: 180.000000, min: 0.000000, max: 360.000000
#   param: "LFO Offset", orig: "LFO Offset", value: 0.000000, min: 0.000000, max: 360.000000
# Q param: "LFO Quantize On", orig: "LFO Quantize On" => [Off, On]
# Q param: "LFO Quantize Rate", orig: "LFO Quantize Rate" => [0.5, 1, 2, 3, 4, 5, 6, 8, 12, 16]
# Q param: "S/C On", orig: "S/C On" => [Off, On]
#   param: "S/C Gain", orig: "S/C Gain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "S/C Mix", orig: "S/C Mix", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: AutoShift, Device: Auto Shift, Display: Auto Shift - 44
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Input Gain", orig: "Input Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Dry Wet", orig: "Dry Wet", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Scale Aware", orig: "Scale Aware" => [Off, On]
#   param: "MIDI Glide", orig: "MIDI Glide", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "MIDI Pitch Bend Range", orig: "MIDI Pitch Bend Range", value: 6.000000, min: 0.000000, max: 48.000000
#   param: "MIDI Attack Time", orig: "MIDI Attack Time", value: 0.141421, min: 0.000000, max: 1.000000
#   param: "MIDI Release Time", orig: "MIDI Release Time", value: 0.158740, min: 0.000000, max: 1.000000
# Q param: "MIDI Latch", orig: "MIDI Latch" => [Gate, Latch]
#   param: "Shift Semitones", orig: "Shift Semitones", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "Shift Scale Degrees", orig: "Shift Scale Degrees", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "Detune", orig: "Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Formant Shift", orig: "Formant Shift", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Formant Follow", orig: "Formant Follow", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Quantizer Active", orig: "Quantizer Active" => [Off, On]
# Q param: "Quantizer Smooth", orig: "Quantizer Smooth" => [Off, On]
#   param: "Quantizer Smoothing Time", orig: "Quantizer Smoothing Time", value: 0.707107, min: 0.000000, max: 1.000000
#   param: "Quantizer Amount", orig: "Quantizer Amount", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Quantizer Root", orig: "Quantizer Root" => [C, C♯, D, D♯, E, F, F♯, G, G♯, A, A♯, B]
# Q param: "Quantizer Internal Scale", orig: "Quantizer Internal Scale" => [Custom, Chromatic, Major, Minor, Dorian, Mixolydian, Lydian, Phrygian, Locrian, Whole Tone, Half-whole Dim., Whole-half Dim., Minor Blues, Minor Pentatonic, Major Pentatonic, Harmonic Minor, Harmonic Major, Dorian #4, Phrygian Dominant, Melodic Minor, Lydian Augmented, Lydian Dominant, Super Locrian, 8-Tone Spanish, Bhairav, Hungarian Minor, Hirajoshi, In-Sen, Iwato, Kumoi, Pelog Selisir, Pelog Tembung, Messiaen 3, Messiaen 4, Messiaen 5, Messiaen 6, Messiaen 7]
# Q param: "Lfo Lfo Enabled", orig: "Lfo Lfo Enabled" => [Off, On]
# Q param: "Lfo Retrigger", orig: "Lfo Retrigger" => [Off, On]
#   param: "Lfo Delay", orig: "Lfo Delay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Lfo Attack", orig: "Lfo Attack", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Lfo Waveform", orig: "Lfo Waveform" => [Sine, Triangle, Triangle 8, Triangle 16, Saw Up, Saw Down, Rectangle, Random, Random S&H]
# Q param: "Lfo Sync", orig: "Lfo Sync" => [Off, On]
#   param: "Lfo Rate Hz", orig: "Lfo Rate Hz", value: 0.514679, min: 0.000000, max: 1.000000
#   param: "Lfo S. Rate", orig: "Lfo S. Rate", value: 12.000000, min: 0.000000, max: 21.000000
#   param: "Vibrato Attack", orig: "Vibrato Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Vibrato Rate Hz", orig: "Vibrato Rate Hz", value: 0.455769, min: 0.000000, max: 1.000000
#   param: "Vibrato Amount", orig: "Vibrato Amount", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Vibrato Humanization", orig: "Vibrato Humanization" => [Off, On]
#   param: "Lfo To Pitch Mod Amount", orig: "Lfo To Pitch Mod Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Lfo To Formant Mod Amount", orig: "Lfo To Formant Mod Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Lfo To Volume Mod Amount", orig: "Lfo To Volume Mod Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Lfo To Pan Mod Amount", orig: "Lfo To Pan Mod Amount", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Midi To Pitch Mod Source", orig: "Midi To Pitch Mod Source" => [None, Velocity, Pressure, Mod Wheel, Pitch Bend, Note PB, Slide]
# Q param: "Midi To Formant Mod Source", orig: "Midi To Formant Mod Source" => [None, Velocity, Pressure, Mod Wheel, Pitch Bend, Note PB, Slide]
# Q param: "Midi To Volume Mod Source", orig: "Midi To Volume Mod Source" => [None, Velocity, Pressure, Mod Wheel, Pitch Bend, Note PB, Slide]
# Q param: "Midi To Pan Mod Source", orig: "Midi To Pan Mod Source" => [None, Velocity, Pressure, Mod Wheel, Pitch Bend, Note PB, Slide]
#   param: "Midi To Pitch Mod Amount", orig: "Midi To Pitch Mod Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Midi To Formant Mod Amount", orig: "Midi To Formant Mod Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Midi To Volume Mod Amount", orig: "Midi To Volume Mod Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Midi To Pan Mod Amount", orig: "Midi To Pan Mod Amount", value: 0.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Cabinet, Device: Cabinet, Display: Cabinet - 6
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Cabinet Type", orig: "Cabinet Type" => [1x12, 2x12, 4x12, 4x10, 4x10 Bass]
# Q param: "Microphone Type", orig: "Microphone Type" => [Condenser, Dynamic]
# Q param: "Microphone Position", orig: "Microphone Position" => [Near On-Axis, Near Off-Axis, Far]
# Q param: "Dual Mono", orig: "Dual Mono" => [Off, On]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: ChannelEq, Device: Channel EQ, Display: Channel EQ - 7
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Highpass On", orig: "Highpass On" => [Off, On]
#   param: "Low Gain", orig: "Low Gain", value: 0.498841, min: 0.000000, max: 1.000000
#   param: "Mid Gain", orig: "Mid Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Mid Freq", orig: "Mid Freq", value: 0.610793, min: 0.000000, max: 1.000000
#   param: "High Gain", orig: "High Gain", value: 0.498841, min: 0.000000, max: 1.000000
#   param: "Gain", orig: "Gain", value: 0.500000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Corpus, Device: Corpus, Display: Corpus - 39
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Resonance Type", orig: "Resonance Type" => [Beam, Marimba, String, Membrane, Plate, Pipe, Tube]
# Q param: "Resonator Quality", orig: "Resonator Quality" => [Eco, Low, Med, High]
#   param: "Tune", orig: "Tune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Fine", orig: "Fine", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "Spread", orig: "Spread", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Decay", orig: "Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Material", orig: "Material", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Radius", orig: "Radius", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Brightness", orig: "Brightness", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Inharmonics", orig: "Inharmonics", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Opening", orig: "Opening", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ratio", orig: "Ratio", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Hit", orig: "Hit", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Listening L", orig: "Listening L", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Listening R", orig: "Listening R", value: 0.900000, min: 0.000000, max: 1.000000
# Q param: "LFO On/Off", orig: "LFO On/Off" => [Off, On]
# Q param: "LFO Shape", orig: "LFO Shape" => [Sine, Square, Triangle, SawUp, SawDown, Sample & Hold, Random Ramp]
# Q param: "LFO Sync", orig: "LFO Sync" => [Free, Sync]
#   param: "LFO Rate", orig: "LFO Rate", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO Sync Rate", orig: "LFO Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
# Q param: "LFO Stereo Mode", orig: "LFO Stereo Mode" => [Phase, Spin]
#   param: "Spin", orig: "Spin", value: 0.000000, min: 0.000000, max: 0.500000
#   param: "Phase", orig: "Phase", value: 180.000000, min: 0.000000, max: 360.000000
#   param: "Offset", orig: "Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "LFO Amount", orig: "LFO Amount", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Filter On/Off", orig: "Filter On/Off" => [Off, On]
#   param: "Mid Freq", orig: "Mid Freq", value: 0.508950, min: 0.000000, max: 1.000000
#   param: "Width", orig: "Width", value: 4.000000, min: 0.500000, max: 9.000000
# Q param: "MIDI Frequency", orig: "MIDI Frequency" => [Off, On]
# Q param: "MIDI Mode", orig: "MIDI Mode" => [Last, Low]
#   param: "PB Range", orig: "PB Range", value: 5.000000, min: 0.000000, max: 24.000000
# Q param: "Note Off", orig: "Note Off" => [Off, On]
#   param: "Off Decay", orig: "Off Decay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Gain", orig: "Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Width", orig: "Width", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Bleed", orig: "Bleed", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Dry Wet", orig: "Dry Wet", value: 0.500000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: DrumBuss, Device: Drum Buss, Display: Drum Buss - 14
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Compressor On", orig: "Compressor On" => [Off, On]
#   param: "Drive", orig: "Drive", value: 0.200000, min: 0.000000, max: 1.000000
# Q param: "Drive Type", orig: "Drive Type" => [Soft, Medium, Hard]
#   param: "Crunch", orig: "Crunch", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Damping Freq", orig: "Damping Freq", value: 0.789495, min: 0.000000, max: 1.000000
#   param: "Transients", orig: "Transients", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Boom Freq", orig: "Boom Freq", value: 0.464974, min: 0.000000, max: 1.000000
#   param: "Boom Amt", orig: "Boom Amt", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Boom Decay", orig: "Boom Decay", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Boom Audition", orig: "Boom Audition" => [Off, On]
#   param: "Trim", orig: "Trim", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Output Gain", orig: "Output Gain", value: 0.924942, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Tube, Device: Dynamic Tube, Display: Dynamic Tube - 10
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Drive", orig: "Drive", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "Output", orig: "Output", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "Bias", orig: "Bias", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Envelope", orig: "Envelope", value: 0.000000, min: -3.000000, max: 3.000000
#   param: "Attack", orig: "Attack", value: 0.268622, min: 0.000000, max: 1.000000
#   param: "Release", orig: "Release", value: 0.486154, min: 0.000000, max: 1.000000
#   param: "Tone", orig: "Tone", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "Tube Type", orig: "Tube Type" => [A, B, C]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Erosion, Device: Erosion, Display: Erosion - 5
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Mode", orig: "Mode" => [Noise, Wide Noise, Sine]
#   param: "Frequency", orig: "Frequency", value: 0.708194, min: 0.000000, max: 1.000000
#   param: "Amount", orig: "Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Width", orig: "Width", value: 0.341303, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Gate, Device: Gate, Display: Gate - 18
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Threshold", orig: "Threshold", value: 0.550000, min: 0.000000, max: 1.000000
#   param: "Attack", orig: "Attack", value: 3.500000, min: 0.020000, max: 150.000000
#   param: "Hold", orig: "Hold", value: 0.314852, min: 0.000000, max: 1.000000
#   param: "Release", orig: "Release", value: 0.486047, min: 0.000000, max: 1.000000
#   param: "Return", orig: "Return", value: 3.000000, min: 0.000000, max: 24.000000
#   param: "Floor", orig: "Floor", value: -40.000000, min: -75.000000, max: 0.000000
# Q param: "S/C Listen", orig: "S/C Listen" => [Off, On]
# Q param: "FlipMode", orig: "FlipMode" => [Normal, Flip]
# Q param: "LookAhead", orig: "LookAhead" => [0 ms, 1.5 ms, 10 ms]
# Q param: "S/C On", orig: "S/C On" => [Off, On]
#   param: "S/C Gain", orig: "S/C Gain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "S/C Mix", orig: "S/C Mix", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "S/C EQ Type", orig: "S/C EQ Type" => [Low Shelf, Bell, High Shelf, Low pass, Peak, High pass]
# Q param: "S/C EQ On", orig: "S/C EQ On" => [Off, On]
#   param: "S/C EQ Freq", orig: "S/C EQ Freq", value: 0.305268, min: 0.000000, max: 1.000000
#   param: "S/C EQ Gain", orig: "S/C EQ Gain", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "S/C EQ Q", orig: "S/C EQ Q", value: 0.408567, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Limiter, Device: Limiter, Display: Limiter - 13
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Input Gain", orig: "Input Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Ceiling", orig: "Ceiling", value: 0.970144, min: 0.000000, max: 1.000000
#   param: "Release", orig: "Release", value: 0.730311, min: 0.000000, max: 1.000000
# Q param: "Auto", orig: "Auto" => [Off, On]
#   param: "Link", orig: "Link", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "M/S Link", orig: "M/S Link", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Lookahead", orig: "Lookahead" => [1.5 ms, 3 ms, 6 ms]
# Q param: "Routing", orig: "Routing" => [L/R, M/S]
# Q param: "Mode", orig: "Mode" => [Standard, Soft Clip, True Peak]
# Q param: "Maximize On", orig: "Maximize On" => [Off, On]
#   param: "Threshold", orig: "Threshold", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Output", orig: "Output", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Looper, Device: Looper, Display: Looper - 9
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "State", orig: "State" => [Stop, Record, Play, Overdub]
#   param: "Feedback", orig: "Feedback", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Reverse", orig: "Reverse" => [Off, On]
# Q param: "Monitor", orig: "Monitor" => [Always, Never, Rec/OVR, Rec/OVR/Stop]
#   param: "Speed", orig: "Speed", value: 0.000000, min: -36.000000, max: 36.000000
# Q param: "Quantization", orig: "Quantization" => [Global, None, 8 Bars, 4 Bars, 2 Bars, 1 Bar, 1/2, 1/2T, 1/4, 1/4T, 1/8, 1/8T, 1/16, 1/16T, 1/32]
# Q param: "Song Control", orig: "Song Control" => [None, Start Song, Start & Stop Song]
# Q param: "Tempo Control", orig: "Tempo Control" => [None, Follow song tempo, Set & Follow song tempo]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: MultibandDynamics, Device: Multiband Dynamics, Display: Multiband Dynamics - 38
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Low-Mid Crossover", orig: "Low-Mid Crossover", value: 2.079181, min: 1.477121, max: 3.477121
#   param: "Mid-High Crossover", orig: "Mid-High Crossover", value: 3.397940, min: 2.477121, max: 4.176091
# Q param: "Soft Knee On/Off", orig: "Soft Knee On/Off" => [Off, On]
# Q param: "Peak/RMS Mode", orig: "Peak/RMS Mode" => [RMS, Peak]
#   param: "Master Output", orig: "Master Output", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Amount", orig: "Amount", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Time Scaling", orig: "Time Scaling", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Output Gain (Low)", orig: "Output Gain (Low)", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Output Gain (Mid)", orig: "Output Gain (Mid)", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Output Gain (High)", orig: "Output Gain (High)", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Input Gain (Low)", orig: "Input Gain (Low)", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Input Gain (Mid)", orig: "Input Gain (Mid)", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Input Gain (High)", orig: "Input Gain (High)", value: 0.000000, min: -24.000000, max: 24.000000
# Q param: "Band Activator (Low)", orig: "Band Activator (Low)" => [Off, On]
# Q param: "Band Activator (Mid)", orig: "Band Activator (Mid)" => [Off, On]
# Q param: "Band Activator (High)", orig: "Band Activator (High)" => [Off, On]
#   param: "Above Threshold (Low)", orig: "Above Threshold (Low)", value: -20.000000, min: -80.000000, max: 0.000000
#   param: "Above Threshold (Mid)", orig: "Above Threshold (Mid)", value: -20.000000, min: -80.000000, max: 0.000000
#   param: "Above Threshold (High)", orig: "Above Threshold (High)", value: -20.000000, min: -80.000000, max: 0.000000
#   param: "Below Threshold (Low)", orig: "Below Threshold (Low)", value: -60.000000, min: -80.000000, max: 0.000000
#   param: "Below Threshold (Mid)", orig: "Below Threshold (Mid)", value: -60.000000, min: -80.000000, max: 0.000000
#   param: "Below Threshold (High)", orig: "Below Threshold (High)", value: -60.000000, min: -80.000000, max: 0.000000
#   param: "Above Ratio (Low)", orig: "Above Ratio (Low)", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Above Ratio (Mid)", orig: "Above Ratio (Mid)", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Above Ratio (High)", orig: "Above Ratio (High)", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Below Ratio (Low)", orig: "Below Ratio (Low)", value: 0.000000, min: -3.000000, max: 1.000000
#   param: "Below Ratio (Mid)", orig: "Below Ratio (Mid)", value: 0.000000, min: -3.000000, max: 1.000000
#   param: "Below Ratio (High)", orig: "Below Ratio (High)", value: 0.000000, min: -3.000000, max: 1.000000
#   param: "Attack Time (Low)", orig: "Attack Time (Low)", value: 1.698970, min: -1.000000, max: 3.698970
#   param: "Attack Time (Mid)", orig: "Attack Time (Mid)", value: 1.000000, min: -1.000000, max: 3.698970
#   param: "Attack Time (High)", orig: "Attack Time (High)", value: 0.698970, min: -1.000000, max: 3.698970
#   param: "Release Time (Low)", orig: "Release Time (Low)", value: 2.477121, min: -1.000000, max: 3.698970
#   param: "Release Time (Mid)", orig: "Release Time (Mid)", value: 2.301030, min: -1.000000, max: 3.698970
#   param: "Release Time (High)", orig: "Release Time (High)", value: 2.000000, min: -1.000000, max: 3.698970
# Q param: "S/C On", orig: "S/C On" => [Off, On]
#   param: "S/C Gain", orig: "S/C Gain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "S/C Mix", orig: "S/C Mix", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Pedal, Device: Pedal, Display: Pedal - 10
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Type", orig: "Type" => [Overdrive, Distortion, Fuzz]
#   param: "Gain", orig: "Gain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Output", orig: "Output", value: 0.000000, min: -20.000000, max: 20.000000
#   param: "Bass", orig: "Bass", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Mid", orig: "Mid", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Treble", orig: "Treble", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "Mid Freq", orig: "Mid Freq" => [Low, Mid, High]
# Q param: "Sub", orig: "Sub" => [Off, On]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Roar, Device: Roar, Display: Roar - 87
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Drive", orig: "Drive", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Tone Amt", orig: "Tone Amt", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Tone Freq", orig: "Tone Freq", value: 0.251930, min: 0.000000, max: 1.000000
# Q param: "Color On", orig: "Color On" => [Off, On]
#   param: "Blend", orig: "Blend", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Low Mid X-Over", orig: "Low Mid X-Over", value: 0.417025, min: 0.000000, max: 1.000000
#   param: "Mid High X-Over", orig: "Mid High X-Over", value: 0.511707, min: 0.000000, max: 1.000000
# Q param: "Stage 1 On", orig: "Stage 1 On" => [Off, On]
# Q param: "Shaper 1 On", orig: "Shaper 1 On" => [Off, On]
# Q param: "Shaper 1 Type", orig: "Shaper 1 Type" => [Soft Sine, Digital Clip, Bit Crusher, Diode Clipper, Tube Preamp, Half Wave Rectifier, Full Wave Rectifier, Polynomial, Fractal, Tri Fold, Noise Injection, Shards]
#   param: "Shaper 1 Amt", orig: "Shaper 1 Amt", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Shaper 1 Bias", orig: "Shaper 1 Bias", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Shaper 1 Level", orig: "Shaper 1 Level", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Flt 1 On", orig: "Flt 1 On" => [Off, On]
# Q param: "Flt 1 Type", orig: "Flt 1 Type" => [LP, BP, HP, Notch, Peak, Morph, Comb, Resampling]
#   param: "Flt 1 Freq", orig: "Flt 1 Freq", value: 0.967697, min: 0.000000, max: 1.000000
#   param: "Flt 1 Res", orig: "Flt 1 Res", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Flt 1 Morph", orig: "Flt 1 Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Flt 1 Peak", orig: "Flt 1 Peak", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Flt 1 Pre On", orig: "Flt 1 Pre On" => [Off, On]
# Q param: "Stage 2 On", orig: "Stage 2 On" => [Off, On]
# Q param: "Shaper 2 On", orig: "Shaper 2 On" => [Off, On]
# Q param: "Shaper 2 Type", orig: "Shaper 2 Type" => [Soft Sine, Digital Clip, Bit Crusher, Diode Clipper, Tube Preamp, Half Wave Rectifier, Full Wave Rectifier, Polynomial, Fractal, Tri Fold, Noise Injection, Shards]
#   param: "Shaper 2 Amt", orig: "Shaper 2 Amt", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Shaper 2 Bias", orig: "Shaper 2 Bias", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Shaper 2 Level", orig: "Shaper 2 Level", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Flt 2 On", orig: "Flt 2 On" => [Off, On]
# Q param: "Flt 2 Type", orig: "Flt 2 Type" => [LP, BP, HP, Notch, Peak, Morph, Comb, Resampling]
#   param: "Flt 2 Freq", orig: "Flt 2 Freq", value: 0.967697, min: 0.000000, max: 1.000000
#   param: "Flt 2 Res", orig: "Flt 2 Res", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Flt 2 Morph", orig: "Flt 2 Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Flt 2 Peak", orig: "Flt 2 Peak", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Flt 2 Pre On", orig: "Flt 2 Pre On" => [Off, On]
# Q param: "Stage 3 On", orig: "Stage 3 On" => [Off, On]
# Q param: "Shaper 3 On", orig: "Shaper 3 On" => [Off, On]
# Q param: "Shaper 3 Type", orig: "Shaper 3 Type" => [Soft Sine, Digital Clip, Bit Crusher, Diode Clipper, Tube Preamp, Half Wave Rectifier, Full Wave Rectifier, Polynomial, Fractal, Tri Fold, Noise Injection, Shards]
#   param: "Shaper 3 Amt", orig: "Shaper 3 Amt", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Shaper 3 Bias", orig: "Shaper 3 Bias", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Shaper 3 Level", orig: "Shaper 3 Level", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Flt 3 On", orig: "Flt 3 On" => [Off, On]
# Q param: "Flt 3 Type", orig: "Flt 3 Type" => [LP, BP, HP, Notch, Peak, Morph, Comb, Resampling]
#   param: "Flt 3 Freq", orig: "Flt 3 Freq", value: 0.967697, min: 0.000000, max: 1.000000
#   param: "Flt 3 Res", orig: "Flt 3 Res", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Flt 3 Morph", orig: "Flt 3 Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Flt 3 Peak", orig: "Flt 3 Peak", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Flt 3 Pre On", orig: "Flt 3 Pre On" => [Off, On]
#   param: "Fb Amt", orig: "Fb Amt", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Fb Time Mode", orig: "Fb Time Mode" => [Time, Synced, Triplet, Dotted, Note]
#   param: "Fb Time", orig: "Fb Time", value: 0.430767, min: 0.000000, max: 1.000000
#   param: "Fb Synced", orig: "Fb Synced", value: -4.000000, min: -7.000000, max: 0.000000
#   param: "Fb Note", orig: "Fb Note", value: 33.000000, min: 12.000000, max: 84.000000
#   param: "Fb Freq", orig: "Fb Freq", value: 0.508950, min: 0.000000, max: 1.000000
#   param: "Fb Width", orig: "Fb Width", value: 0.882353, min: 0.000000, max: 1.000000
# Q param: "Fb Inv On", orig: "Fb Inv On" => [Off, On]
# Q param: "Fb Gate On", orig: "Fb Gate On" => [Off, On]
# Q param: "LFO 1 Rate Mode", orig: "LFO 1 Rate Mode" => [Free, Synced, Triplet, Dotted, Sixteenth]
#   param: "LFO 1 Rate", orig: "LFO 1 Rate", value: 0.666667, min: 0.000000, max: 1.000000
#   param: "LFO 1 Synced Rate", orig: "LFO 1 Synced Rate", value: 0.000000, min: -6.000000, max: 3.000000
#   param: "LFO 1 16th", orig: "LFO 1 16th", value: 8.000000, min: 1.000000, max: 64.000000
# Q param: "LFO 1 Wave", orig: "LFO 1 Wave" => [Sine, Triangle, Square, Ramp Up, Ramp Down]
#   param: "LFO 1 Morph", orig: "LFO 1 Morph", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Smooth", orig: "LFO 1 Smooth", value: 0.406724, min: 0.000000, max: 1.000000
# Q param: "LFO 2 Rate Mode", orig: "LFO 2 Rate Mode" => [Free, Synced, Triplet, Dotted, Sixteenth]
#   param: "LFO 2 Rate", orig: "LFO 2 Rate", value: 0.666667, min: 0.000000, max: 1.000000
#   param: "LFO 2 Synced Rate", orig: "LFO 2 Synced Rate", value: 0.000000, min: -6.000000, max: 3.000000
#   param: "LFO 2 16th", orig: "LFO 2 16th", value: 8.000000, min: 1.000000, max: 64.000000
# Q param: "LFO 2 Wave", orig: "LFO 2 Wave" => [Sine, Triangle, Square, Ramp Up, Ramp Down]
#   param: "LFO 2 Morph", orig: "LFO 2 Morph", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Smooth", orig: "LFO 2 Smooth", value: 0.406724, min: 0.000000, max: 1.000000
#   param: "Env Gain", orig: "Env Gain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env Attack", orig: "Env Attack", value: 0.250841, min: 0.000000, max: 1.000000
#   param: "Env Release", orig: "Env Release", value: 0.349232, min: 0.000000, max: 1.000000
#   param: "Env Thresh", orig: "Env Thresh", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env Freq", orig: "Env Freq", value: 0.508950, min: 0.000000, max: 1.000000
#   param: "Env Width", orig: "Env Width", value: 0.882353, min: 0.000000, max: 1.000000
# Q param: "Noise Rate Mode", orig: "Noise Rate Mode" => [Free, Synced, Triplet, Dotted, Sixteenth]
#   param: "Noise Rate", orig: "Noise Rate", value: 0.666667, min: 0.000000, max: 1.000000
#   param: "Noise Synced Rate", orig: "Noise Synced Rate", value: -2.000000, min: -6.000000, max: 3.000000
#   param: "Noise 16th", orig: "Noise 16th", value: 4.000000, min: 1.000000, max: 64.000000
# Q param: "Noise Type", orig: "Noise Type" => [Simplex, Wander, Sample & Hold, Brown]
#   param: "Noise Smooth", orig: "Noise Smooth", value: 0.406724, min: 0.000000, max: 1.000000
#   param: "Global Mod Amt", orig: "Global Mod Amt", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Comp Amt", orig: "Comp Amt", value: 0.250000, min: 0.000000, max: 1.000000
# Q param: "Comp Hp On", orig: "Comp Hp On" => [Off, On]
#   param: "Output", orig: "Output", value: 0.800000, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Saturator, Device: Saturator, Display: Saturator - 19
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Drive", orig: "Drive", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Pre Dc Filter", orig: "Pre Dc Filter" => [Off, On]
# Q param: "Type", orig: "Type" => [Analog Clip, Soft Sine, Bass Shaper, Medium Curve, Hard Curve, Sinoid Fold, Digital Clip, Waveshaper]
# Q param: "Color On", orig: "Color On" => [Off, On]
#   param: "Color Amt Low", orig: "Color Amt Low", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Color Freq", orig: "Color Freq", value: 0.545825, min: 0.000000, max: 1.000000
#   param: "Color Width", orig: "Color Width", value: 0.300000, min: 0.000000, max: 1.000000
#   param: "Color Amt Hi", orig: "Color Amt Hi", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Post Clip Mode", orig: "Post Clip Mode" => [No Clip, Soft Clip, Hard Clip]
#   param: "Output", orig: "Output", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Threshold", orig: "Threshold", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "WS Drive", orig: "WS Drive", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "WS Linearity", orig: "WS Linearity", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "WS Curve", orig: "WS Curve", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "WS Damp", orig: "WS Damp", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "WS Period", orig: "WS Period", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "WS Depth", orig: "WS Depth", value: 0.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Transmute, Device: Spectral Resonator, Display: Spectral Resonator - 17
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Glide", orig: "Glide", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Freq. Hz", orig: "Freq. Hz", value: 0.472340, min: 0.000000, max: 1.000000
#   param: "Note", orig: "Note", value: 45.000000, min: 0.000000, max: 96.000000
#   param: "Shift", orig: "Shift", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Stretch", orig: "Stretch", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Decay", orig: "Decay", value: 0.222738, min: 0.000000, max: 1.000000
#   param: "HF Damp", orig: "HF Damp", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LF Damp", orig: "LF Damp", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Mod Rate", orig: "Mod Rate", value: 0.500841, min: 0.000000, max: 1.000000
#   param: "Pitch Mod", orig: "Pitch Mod", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Harmonics", orig: "Harmonics", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Unison", orig: "Unison", value: 0.000000, min: 0.000000, max: 3.000000
#   param: "Unison Amount", orig: "Unison Amount", value: 0.562341, min: 0.000000, max: 1.000000
#   param: "Input Send Gain", orig: "Input Send Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Dry Wet", orig: "Dry Wet", value: 1.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Spectral, Device: Spectral Time, Display: Spectral Time - 27
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "On", orig: "On" => [Off, On]
# Q param: "Frozen", orig: "Frozen" => [Off, On]
# Q param: "Unit", orig: "Unit" => [Milliseconds, ModulationBeat]
#   param: "Sync Interval", orig: "Sync Interval", value: 6.000000, min: 0.000000, max: 21.000000
#   param: "S.Rate ms", orig: "S.Rate ms", value: 0.363667, min: 0.000000, max: 1.000000
# Q param: "Mode", orig: "Mode" => [Manual, Retrigger]
# Q param: "Retrigger Mode", orig: "Retrigger Mode" => [Onsets, Sync]
# Q param: "Fade Type", orig: "Fade Type" => [Crossfade, Envelope]
#   param: "Fade In", orig: "Fade In", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "XFade %", orig: "XFade %", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fade Out", orig: "Fade Out", value: 0.126076, min: 0.000000, max: 1.000000
#   param: "Sensitivity", orig: "Sensitivity", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Delay On", orig: "Delay On" => [Off, On]
#   param: "Delay Time Seconds", orig: "Delay Time Seconds", value: 0.468849, min: 0.000000, max: 1.000000
# Q param: "Delay Dly. Unit", orig: "Delay Dly. Unit" => [Time, Notes, 16th, 16th Triplet, 16th Dotted]
#   param: "Delay Time Sixteenths", orig: "Delay Time Sixteenths", value: 3.000000, min: 1.000000, max: 16.000000
#   param: "Delay Time Divisions", orig: "Delay Time Divisions", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "Delay Feedback", orig: "Delay Feedback", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Delay Tilt", orig: "Delay Tilt", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Delay Spray", orig: "Delay Spray", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Delay Mask", orig: "Delay Mask", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Delay Stereo Spread", orig: "Delay Stereo Spread", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Delay Frequency Shift", orig: "Delay Frequency Shift", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Delay Mix", orig: "Delay Mix", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Input Send Gain", orig: "Input Send Gain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Dry Wet", orig: "Dry Wet", value: 0.500000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: StereoGain, Device: Utility, Display: Utility - 12
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Left Inv", orig: "Left Inv" => [Off, On]
# Q param: "Right Inv", orig: "Right Inv" => [Off, On]
# Q param: "Channel Mode", orig: "Channel Mode" => [Left, Stereo, Right, Swap]
#   param: "Stereo Width", orig: "Stereo Width", value: 1.000000, min: 0.000000, max: 2.000000
# Q param: "Mono", orig: "Mono" => [Off, On]
# Q param: "Bass Mono", orig: "Bass Mono" => [Off, On]
#   param: "Bass Freq", orig: "Bass Freq", value: 0.380211, min: 0.000000, max: 1.000000
#   param: "Balance", orig: "Balance", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Gain", orig: "Gain", value: 0.000000, min: -1.000000, max: 1.000000
# Q param: "Mute", orig: "Mute" => [Off, On]
# Q param: "DC Filter", orig: "DC Filter" => [Off, On]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#=======================================================================
# Class: Vinyl, Device: Vinyl Distortion, Display: Vinyl Distortion - 14
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Tracing On", orig: "Tracing On" => [Off, On]
#   param: "Tracing Drive", orig: "Tracing Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Tracing Freq.", orig: "Tracing Freq.", value: 0.444426, min: 0.000000, max: 1.000000
#   param: "Tracing Width", orig: "Tracing Width", value: 0.341983, min: 0.000000, max: 1.000000
# Q param: "Pinch On", orig: "Pinch On" => [Off, On]
#   param: "Pinch Drive", orig: "Pinch Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pinch Freq.", orig: "Pinch Freq.", value: 0.851265, min: 0.000000, max: 1.000000
#   param: "Pinch Width", orig: "Pinch Width", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Global Drive", orig: "Global Drive", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Pinch Soft On", orig: "Pinch Soft On" => [Soft, Hard]
# Q param: "Pinch Mono On", orig: "Pinch Mono On" => [Stereo, Mono]
#   param: "Crackle Density", orig: "Crackle Density", value: 10.000000, min: 0.000000, max: 50.000000
#   param: "Crackle Volume", orig: "Crackle Volume", value: 0.000000, min: 0.000000, max: 1.000000
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
</pre>
