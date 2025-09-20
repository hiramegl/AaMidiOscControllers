from .Dev import Dev

class Transmute(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB1Off | Quantize    | Use Scale'                                  ,
      #-----------------------------------------------------------------------------
      'Bank0 | nGR0Off | Freq. Hz    | Transpose     | Glide     | Unison Amount'  ,
      'Bank0 | nGR1Off | Transp Scale'                                             ,
      #-----------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev'                                ,
      'Bank0 | nMB1Off | Preset Save | Preset Next'                                ,
      #-----------------------------------------------------------------------------
      'Bank0 | nMR0Off | Note        | Decay         | Mod Rate  | Input Send Gain',
      'Bank0 | nMR1Off | Stretch     | HF Damp       | Pitch Mod | Unison'         ,
      'Bank0 | nMR2Off | Shift       | LF Damp       | Harmonics | Dry Wet'        ,
    ]
    self.reg('Transmute')
    self.parse_cfg()

# Class: Transmute, Device: Spectral Resonator, Display: Spectral Resonator
# Q param: "Device On", orig: "Device On" => [Off, On]

#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Stretch", orig: "Stretch", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Shift", orig: "Shift", value: 0.500000, min: 0.000000, max: 1.000000

#   param: "Decay", orig: "Decay", value: 0.222738, min: 0.000000, max: 1.000000
#   param: "HF Damp", orig: "HF Damp", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LF Damp", orig: "LF Damp", value: 0.000000, min: 0.000000, max: 1.000000

#   param: "Mod Rate", orig: "Mod Rate", value: 0.500841, min: 0.000000, max: 1.000000
#   param: "Pitch Mod", orig: "Pitch Mod", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Harmonics", orig: "Harmonics", value: 1.000000, min: 0.000000, max: 1.000000

#   param: "Input Send Gain", orig: "Input Send Gain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Unison", orig: "Unison", value: 0.000000, min: 0.000000, max: 3.000000
#   param: "Dry Wet", orig: "Dry Wet", value: 1.000000, min: 0.000000, max: 1.000000

#   param: "Freq. Hz", orig: "Freq. Hz", value: 0.472340, min: 0.000000, max: 1.000000
#   param: "Unison Amount", orig: "Unison Amount", value: 0.562341, min: 0.000000, max: 1.000000
#   param: "Glide", orig: "Glide", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Note", orig: "Note", value: 45.000000, min: 0.000000, max: 96.000000


