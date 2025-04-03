from .Dev import Dev

class Resonator(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Mode        | I On        | II On     | III On      | IV On    | V On'   ,
      #--------------------------------------------------------------------------------------------
      'Bank0 | nGR0Off | Decay       | Color       | Width     | Global Gain'                     ,
      #--------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev | Filter On'                                   ,
      'Bank0 | nMB1Off | Preset Save | Preset Next | Const'                                       ,
      #--------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Frequency   | I Note      | II Pitch  | III Pitch   | IV Pitch | V Pitch',
      'Bank0 | nMR1Off | Filter Type | I Tune      | II Tune   | III Tune    | IV Tune  | V Tune' ,
      'Bank0 | nMR2Off | Dry/Wet     | I Gain      | II Gain   | III Gain    | IV Gain  | V Gain' ,
    ]
    self.reg('Resonator')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Resonator, Device: Resonators, Display: Resonators
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Filter On", orig: "Filter On" => [Off, On]
#   param: "Frequency", orig: "Frequency", value: 0.453696, min: 0.000000, max: 1.000000
# Q param: "Filter Type", orig: "Filter Type" => [low pass, high pass, band pass, notch]
# Q param: "Mode", orig: "Mode" => [Mode B, Mode A]
#   param: "Decay", orig: "Decay", value: 50.000000, min: 0.000000, max: 100.000000
# Q param: "Const", orig: "Const" => [Off, On]
#   param: "Color", orig: "Color", value: 90.000000, min: 0.000000, max: 100.000000
#   param: "Width", orig: "Width", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Global Gain", orig: "Global Gain", value: 0.000000, min: -15.000000, max: 15.000000
# Q param: "I On", orig: "I On" => [Off, On]
#   param: "I Note", orig: "I Note", value: 48.000000, min: 12.000000, max: 84.000000
#   param: "I Tune", orig: "I Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "I Gain", orig: "I Gain", value: 0.850000, min: 0.000000, max: 1.000000
# Q param: "II On", orig: "II On" => [Off, On]
#   param: "II Pitch", orig: "II Pitch", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "II Tune", orig: "II Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "II Gain", orig: "II Gain", value: 0.850000, min: 0.000000, max: 1.000000
# Q param: "III On", orig: "III On" => [Off, On]
#   param: "III Pitch", orig: "III Pitch", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "III Tune", orig: "III Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "III Gain", orig: "III Gain", value: 0.850000, min: 0.000000, max: 1.000000
# Q param: "IV On", orig: "IV On" => [Off, On]
#   param: "IV Pitch", orig: "IV Pitch", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "IV Tune", orig: "IV Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "IV Gain", orig: "IV Gain", value: 0.850000, min: 0.000000, max: 1.000000
# Q param: "V On", orig: "V On" => [Off, On]
#   param: "V Pitch", orig: "V Pitch", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "V Tune", orig: "V Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "V Gain", orig: "V Gain", value: 0.850000, min: 0.000000, max: 1.000000
