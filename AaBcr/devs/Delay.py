from .Dev import Dev

class Delay(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | L Sync      | R Sync'      ,
      'Bank0 | nGB1Off | Filter On'                 ,
      'Bank0 | nGB2Off | Link'                      ,
      'Bank0 | nGB3Off | Freeze      | Ping Pong'   ,
      #----------------------------------------------
      'Bank0 | nGR0Off | L Time      | R Time'      ,
      'Bank0 | nGR1Off | Filter Freq | Filter Width',
      'Bank0 | nGR2Off | Mod Freq    | Filter < Mod',
      'Bank0 | nGR3Off | Dly < Mod   | Delay Mode'  ,
      #----------------------------------------------
      'Bank0 | nMB0Off | Device On   | Preset Prev' ,
      'Bank0 | nMB1Off | Preset Save | Preset Next' ,
      #----------------------------------------------
      'Bank0 | nMR0Off | L 16th      | R 16th'      ,
      'Bank0 | nMR1Off | L Offset    | R Offset'    ,
      'Bank0 | nMR2Off | Feedback    | Dry/Wet'     ,
    ]
    self.reg('Delay')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Delay, Device: Delay, Display: Delay
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Delay Mode", orig: "Delay Mode" => [Repitch, Fade, Jump]
# Q param: "Link", orig: "Link" => [Off, On]
# Q param: "Ping Pong", orig: "Ping Pong" => [Off, On]
# Q param: "L Sync", orig: "L Sync" => [Off, On]
# Q param: "R Sync", orig: "R Sync" => [Off, On]
#   param: "L Time", orig: "L Time", value: 0.595385, min: 0.000000, max: 1.000000
#   param: "R Time", orig: "R Time", value: 0.595385, min: 0.000000, max: 1.000000
# Q param: "L 16th", orig: "L 16th" => [1, 2, 3, 4, 5, 6, 8, 16]
# Q param: "R 16th", orig: "R 16th" => [1, 2, 3, 4, 5, 6, 8, 16]
#   param: "L Offset", orig: "L Offset", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "R Offset", orig: "R Offset", value: 0.581927, min: 0.000000, max: 1.000000
#   param: "Feedback", orig: "Feedback", value: 0.551181, min: 0.000000, max: 1.000000
# Q param: "Freeze", orig: "Freeze" => [Off, On]
# Q param: "Filter On", orig: "Filter On" => [Off, On]
#   param: "Filter Freq", orig: "Filter Freq", value: 0.508950, min: 0.000000, max: 1.000000
#   param: "Filter Width", orig: "Filter Width", value: 0.882353, min: 0.000000, max: 1.000000
#   param: "Mod Freq", orig: "Mod Freq", value: 0.471666, min: 0.000000, max: 1.000000
#   param: "Dly < Mod", orig: "Dly < Mod", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter < Mod", orig: "Filter < Mod", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Dry/Wet", orig: "Dry/Wet", value: 0.771654, min: 0.000000, max: 1.000000

