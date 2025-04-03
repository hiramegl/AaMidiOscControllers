from .Dev import Dev

class LoungeLizard(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | M Force | Noise Pitch | Noise Decay | Noise < Key | F Tine < Key | P Distance | KB Stretch | PB Range',
      #---------------------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev | Pickup Model',
      'Bank0 | nMB1Off | Preset Save | Preset Next',
      #---------------------------------------------------------
      'Bank0 | nMR0Off | M Stiffness   | Noise Amount  | F Tine Vol   | F Tone Vol   | P Symmetry | Note PB Range | Volume      | Voices',
      'Bank0 | nMR1Off | M Stiff < Vel | M Stiff < Key | F Tine Color | F Tine Decay | Damp Tone  | Damp Balance  | Damp Amount | Semitone',
      'Bank0 | nMR2Off | M Force < Vel | M Force < Key | F Release    | F Tone Decay | P Amp In   | P Amp Out     | P Amp < Key | Detune',
    ]
    self.reg('LoungeLizard')
    self.parse_cfg()

#=======================================================================
# Class: LoungeLizard, Device: Electric, Display: Electric
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Voices", orig: "Voices" => [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
#   param: "PB Range", orig: "PB Range", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Note PB Range", orig: "Note PB Range", value: 0.000000, min: 0.000000, max: 48.000000
#   param: "Volume", orig: "Volume", value: 0.704789, min: 0.000000, max: 1.000000
#   param: "Semitone", orig: "Semitone", value: 12.000000, min: 0.000000, max: 24.000000
#   param: "Detune", orig: "Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "KB Stretch", orig: "KB Stretch", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "M Stiffness", orig: "M Stiffness", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "M Stiff < Key", orig: "M Stiff < Key", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "M Stiff < Vel", orig: "M Stiff < Vel", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "M Force", orig: "M Force", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "M Force < Key", orig: "M Force < Key", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "M Force < Vel", orig: "M Force < Vel", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Pitch", orig: "Noise Pitch", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Decay", orig: "Noise Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Amount", orig: "Noise Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise < Key", orig: "Noise < Key", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Release", orig: "F Release", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Tine Decay", orig: "F Tine Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Tine Vol", orig: "F Tine Vol", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Tine < Key", orig: "F Tine < Key", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Tine Color", orig: "F Tine Color", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Tone Decay", orig: "F Tone Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "F Tone Vol", orig: "F Tone Vol", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "P Symmetry", orig: "P Symmetry", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "P Distance", orig: "P Distance", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Pickup Model", orig: "Pickup Model" => [R, W]
#   param: "P Amp In", orig: "P Amp In", value: 0.420000, min: 0.000000, max: 1.000000
#   param: "P Amp Out", orig: "P Amp Out", value: 0.420000, min: 0.000000, max: 1.000000
#   param: "P Amp < Key", orig: "P Amp < Key", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Damp Tone", orig: "Damp Tone", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Damp Amount", orig: "Damp Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Damp Balance", orig: "Damp Balance", value: 0.500000, min: 0.000000, max: 1.000000
