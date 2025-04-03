from .Dev import Dev

class AutoPan(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | LFO Type       | Stereo Mode',
      'Bank0 | nGB1Off | Invert'                      ,
      #------------------------------------------------
      'Bank0 | nGR0Off | Frequency      | Spin'       ,
      'Bank0 | nGR1Off | Width (Random)'              ,
      #------------------------------------------------
      'Bank0 | nMB0Off | Device On      | Preset Prev',
      'Bank0 | nMB1Off | Preset Save    | Preset Next',
      #------------------------------------------------
      'Bank0 | nMR0Off | Amount         | Sync Rate'  ,
      'Bank0 | nMR1Off | Phase          | Shape'      ,
      'Bank0 | nMR2Off | Offset         | Waveform'   ,
    ]
    self.reg('AutoPan')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: AutoPan, Device: Auto Pan, Display: Auto Pan
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "LFO Type", orig: "LFO Type" => [Frequency, Beats]
#   param: "Amount", orig: "Amount", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Frequency", orig: "Frequency", value: 0.399669, min: 0.000000, max: 1.000000
#   param: "Sync Rate", orig: "Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "Phase", orig: "Phase", value: 180.000000, min: 0.000000, max: 360.000000
#   param: "Spin", orig: "Spin", value: 0.000000, min: 0.000000, max: 0.500000
# Q param: "Stereo Mode", orig: "Stereo Mode" => [Phase, Spin]
#   param: "Offset", orig: "Offset", value: 0.000000, min: 0.000000, max: 360.000000
# Q param: "Waveform", orig: "Waveform" => [Sine, Triangle, SawDown, S&H Width]
#   param: "Shape", orig: "Shape", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Width (Random)", orig: "Width (Random)", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Invert", orig: "Invert" => [Normal, Inverted]
