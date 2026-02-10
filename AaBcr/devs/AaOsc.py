from .Dev import Dev

class AaOsc(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | Release',
      #---------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev',
      'Bank0 | nMB1Off | Preset Save | Preset Next',
      #---------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Time        | CrDuty | AmShape | AmFreq   | FmShape   | FmAmpHiF | FmFreq   | Attack ',
      'Bank0 | nMR1Off | Freq        | CrAmp  | AmDuty  | AmHiFreq | FmDuty    | FmAmpLoF | FmHiFreq | Decay  ',
      'Bank0 | nMR2Off | CrShape     | CrFreq | AmAmp   | AmLoFreq | FmAmpFreq | Sustain  | FmLoFreq | Gain   ',
    ]

    self.reg('MxDeviceInstrument', 'AaOsc')
    self.parse_cfg()

#=======================================================================
# Class: MxDeviceInstrument, Device: AaOsc, Display: Max Instrument
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "AmAmp", orig: "AmAmp", value: 0.338583, min: 0.000000, max: 1.000000
#   param: "AmDuty", orig: "AmDuty", value: 0.501102, min: 0.010000, max: 1.000000
# Q param: "AmFreq", orig: "AmFreq" => [, ]
#   param: "AmHiFreq", orig: "AmHiFreq", value: 6.000000, min: 0.000000, max: 127.000000
#   param: "AmLoFreq", orig: "AmLoFreq", value: 121.000000, min: 0.000000, max: 127.000000
# Q param: "AmShape", orig: "AmShape" => [, , , ]
#   param: "Attack", orig: "Attack", value: 9340.416992, min: 0.000000, max: 20000.000000
#   param: "CrAmp", orig: "CrAmp", value: 1.057480, min: 0.100000, max: 2.000000
#   param: "CrDuty", orig: "CrDuty", value: 0.500000, min: 0.010000, max: 0.500000
#   param: "CrFreq", orig: "CrFreq", value: 62.000000, min: 0.000000, max: 127.000000
# Q param: "CrShape", orig: "CrShape" => [, , ]
#   param: "Decay", orig: "Decay", value: 40644.558594, min: 1.000000, max: 60000.000000
# Q param: "FmAmpFreq", orig: "FmAmpFreq" => [, ]
#   param: "FmAmpHiF", orig: "FmAmpHiF", value: 25.000000, min: 0.000000, max: 127.000000
#   param: "FmAmpLoF", orig: "FmAmpLoF", value: 57.000000, min: 0.000000, max: 127.000000
#   param: "FmDuty", orig: "FmDuty", value: 0.508898, min: 0.010000, max: 1.000000
# Q param: "FmFreq", orig: "FmFreq" => [, ]
#   param: "FmHiFreq", orig: "FmHiFreq", value: 26.000000, min: 0.000000, max: 127.000000
#   param: "FmLoFreq", orig: "FmLoFreq", value: 113.000000, min: 0.000000, max: 127.000000
# Q param: "FmShape", orig: "FmShape" => [, , , ]
# Q param: "Freq", orig: "FreqSel" => [, ]
#   param: "Gain", orig: "Gain", value: 0.000000, min: -70.000000, max: 6.000000
#   param: "Release", orig: "Release", value: 47175.042969, min: 1.000000, max: 60000.000000
#   param: "Sustain", orig: "Sustain", value: 69.291336, min: 0.000000, max: 100.000000
# Q param: "Time", orig: "TimeSel" => [, ]
