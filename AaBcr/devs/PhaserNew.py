from .Dev import Dev

class PhaserNew(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB1Off | Spin Enabled'                                        ,
      'Bank0 | nGB2Off | Env Enabled'                                         ,
      'Bank0 | nGB3Off | Mod Sync 2'                                          ,
      #------------------------------------------------------------------------
      'Bank0 | nGR0Off | Flange Time | Doubler Time'                          ,
      'Bank0 | nGR1Off | Mod Wave    | Duty Cycle  | Mod Phase  | Spin'       ,
      'Bank0 | nGR2Off | Env Amount  | Env Attack  | Env Release'             ,
      'Bank0 | nGR3Off | Lfo Blend   | Mod Rate 2  | Mod Freq 2 | Safe Freq'  ,
      #------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev | Mod Sync'                ,
      'Bank0 | nMB1Off | Preset Save | Preset Next | FB Inv'                  ,
      #------------------------------------------------------------------------
      'Bank0 | nMR0Off | Mode        | Notches     | Mod Freq   | Output Gain',
      'Bank0 | nMR1Off | Center Freq | Spread      | Mod Blend  | Warmth'     ,
      'Bank0 | nMR2Off | Mod Rate    | Amount      | Feedback   | Dry/Wet'    ,
    ]
    self.reg('PhaserNew')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: PhaserNew, Device: Phaser-Flanger, Display: Phaser-Flanger

# Q param: "Spin Enabled", orig: "Spin Enabled" => [Off, On]
# Q param: "Mod Wave", orig: "Mod Wave" => [Sine, Triangle, Triangle Analog, Triangle 8, Triangle 16, Saw Up, Saw Down, Rectangle, Random, Random S&H]
#   param: "Duty Cycle", orig: "Duty Cycle", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Mod Phase", orig: "Mod Phase", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Spin", orig: "Spin", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Env Enabled", orig: "Env Enabled" => [Off, On]
#   param: "Env Amount", orig: "Env Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env Attack", orig: "Env Attack", value: 0.197324, min: 0.000000, max: 1.000000
#   param: "Env Release", orig: "Env Release", value: 0.499875, min: 0.000000, max: 1.000000
# Q param: "Mod Sync 2", orig: "Mod Sync 2" => [Off, On]
#   param: "Lfo Blend", orig: "Lfo Blend", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Mod Freq 2", orig: "Mod Freq 2", value: 0.361191, min: 0.000000, max: 1.000000
#   param: "Mod Rate 2", orig: "Mod Rate 2", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "Safe Freq", orig: "Safe Freq", value: 0.468308, min: 0.000000, max: 1.000000
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Amount", orig: "Amount", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Mod Sync", orig: "Mod Sync" => [Off, On]
#   param: "Mod Rate", orig: "Mod Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "Mod Freq", orig: "Mod Freq", value: 0.361191, min: 0.000000, max: 1.000000
# Q param: "Mode", orig: "Mode" => [Phaser, Flanger, Doubler]
#   param: "Notches", orig: "Notches", value: 4.000000, min: 1.000000, max: 42.000000
#   param: "Flange Time", orig: "Flange Time", value: 0.607528, min: 0.000000, max: 1.000000
#   param: "Doubler Time", orig: "Doubler Time", value: 0.688020, min: 0.000000, max: 1.000000
#   param: "Mod Blend", orig: "Mod Blend", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Center Freq", orig: "Center Freq", value: 0.476824, min: 0.000000, max: 1.000000
#   param: "Spread", orig: "Spread", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Feedback", orig: "Feedback", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Warmth", orig: "Warmth", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "FB Inv", orig: "FB Inv" => [Off, On]
#   param: "Output Gain", orig: "Output Gain", value: 0.707107, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000

