from .Dev import Dev

class Vocoder(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Precise/Retro'                                                   ,
      #------------------------------------------------------------------------------------
      'Bank0 | nGR0Off | Lower Filter Band     | Upper Filter Band     | Filter Bandwidth',
      'Bank0 | nGR1Off | Gate Threshold        | Output Level'                            ,
      'Bank0 | nGR2Off | Upper Pitch Detection | Lower Pitch Detection | Noise Rate'      ,
      'Bank0 | nGR3Off | Oscillator Pitch      | Oscillator Waveform   | Noise Crackle'   ,
      #------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On             | Preset Prev           | Enhance'         ,
      'Bank0 | nMB1Off | Preset Save           | Preset Next           | Unvoiced Speed'  ,
      #------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Unvoiced Level        | Envelope Depth        | Mono/Stereo'     ,
      'Bank0 | nMR1Off | Unvoiced Sensitivity  | Attack Time           | Formant Shift'   ,
      'Bank0 | nMR2Off | Ext. In Gain          | Release Time          | Dry/Wet'         ,
    ]
    self.reg('Vocoder')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Vocoder, Device: Vocoder, Display: Vocoder
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Lower Filter Band", orig: "Lower Filter Band", value: 1.903090, min: 1.301030, max: 3.301030
#   param: "Upper Filter Band", orig: "Upper Filter Band", value: 4.079181, min: 2.301030, max: 4.255272
#   param: "Formant Shift", orig: "Formant Shift", value: 0.000000, min: -36.000000, max: 36.000000
#   param: "Filter Bandwidth", orig: "Filter Bandwidth", value: 1.000000, min: 0.100000, max: 2.000000
# Q param: "Precise/Retro", orig: "Precise/Retro" => [Off, On]
#   param: "Gate Threshold", orig: "Gate Threshold", value: -60.000000, min: -60.000000, max: 12.000000
#   param: "Output Level", orig: "Output Level", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Attack Time", orig: "Attack Time", value: 0.000000, min: 0.000000, max: 3.000000
#   param: "Release Time", orig: "Release Time", value: 2.176091, min: 1.000000, max: 4.477121
#   param: "Unvoiced Sensitivity", orig: "Unvoiced Sensitivity", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Unvoiced Speed", orig: "Unvoiced Speed" => [Fast, Slow]
#   param: "Unvoiced Level", orig: "Unvoiced Level", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Enhance", orig: "Enhance" => [Off, On]
# Q param: "Mono/Stereo", orig: "Mono/Stereo" => [Mono, Stereo, L/R]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Envelope Depth", orig: "Envelope Depth", value: 1.000000, min: 0.000000, max: 2.000000
#   param: "Noise Rate", orig: "Noise Rate", value: 4.301030, min: 2.000000, max: 4.301030
#   param: "Noise Crackle", orig: "Noise Crackle", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Lower Pitch Detection", orig: "Lower Pitch Detection", value: 1.903090, min: 1.477121, max: 2.477121
#   param: "Upper Pitch Detection", orig: "Upper Pitch Detection", value: 2.698970, min: 2.477121, max: 3.477121
#   param: "Oscillator Pitch", orig: "Oscillator Pitch", value: 0.000000, min: -36.000000, max: 36.000000
# Q param: "Oscillator Waveform", orig: "Oscillator Waveform" => [Saw, Pulse10, Pulse25, Pulse48]
#   param: "Ext. In Gain", orig: "Ext. In Gain", value: 0.400000, min: 0.000000, max: 1.000000

