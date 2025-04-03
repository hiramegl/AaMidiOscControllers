from .Dev import Dev

class FilterDelay(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | 1 Input On    | 1 Filter On    | -            | 1 Delay Mode',
      'Bank0 | nGB1Off | 2 Input On    | 2 Filter On    | -            | 2 Delay Mode',
      'Bank0 | nGB2Off | 3 Input On    | 3 Filter On    | -            | 3 Delay Mode',
      #--------------------------------------------------------------------------------
      'Bank0 | nGR0Off | 1 Feedback    | 1 Pan          | 1 Volume     | 1 Time Delay',
      'Bank0 | nGR1Off | 2 Feedback    | 2 Pan          | 2 Volume     | 2 Time Delay',
      'Bank0 | nGR2Off | 3 Feedback    | 3 Pan          | 3 Volume     | 3 Time Delay',
      'Bank0 | nGR3Off | Dry'                                                         ,
      #--------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On     | Preset Prev'                                 ,
      'Bank0 | nMB1Off | Preset Save   | Preset Next'                                 ,
      #--------------------------------------------------------------------------------
      'Bank0 | nMR0Off | 1 Filter Freq | 1 Filter Width | 1 Beat Delay | 1 Beat Swing',
      'Bank0 | nMR1Off | 2 Filter Freq | 2 Filter Width | 2 Beat Delay | 2 Beat Swing',
      'Bank0 | nMR2Off | 3 Filter Freq | 3 Filter Width | 3 Beat Delay | 3 Beat Swing',
    ]
    self.reg('FilterDelay')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: FilterDelay, Device: Filter Delay, Display: Filter Delay
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "1 Input On", orig: "1 Input On" => [Off, On]
# Q param: "1 Filter On", orig: "1 Filter On" => [Off, On]
#   param: "1 Filter Freq", orig: "1 Filter Freq", value: 0.449322, min: 0.000000, max: 1.000000
#   param: "1 Filter Width", orig: "1 Filter Width", value: 4.000000, min: 0.500000, max: 9.000000
# Q param: "1 Delay Mode", orig: "1 Delay Mode" => [Off, On]
# Q param: "1 Beat Delay", orig: "1 Beat Delay" => [1, 2, 3, 4, 5, 6, 8, 16]
#   param: "1 Beat Swing", orig: "1 Beat Swing", value: 0.000000, min: -0.333000, max: 0.333000
#   param: "1 Time Delay", orig: "1 Time Delay", value: 10.000000, min: 1.000000, max: 999.000000
#   param: "1 Feedback", orig: "1 Feedback", value: 0.210000, min: 0.000000, max: 1.000000
#   param: "1 Pan", orig: "1 Pan", value: -1.000000, min: -1.000000, max: 1.000000
#   param: "1 Volume", orig: "1 Volume", value: 0.950000, min: 0.000000, max: 1.000000
# Q param: "2 Input On", orig: "2 Input On" => [Off, On]
# Q param: "2 Filter On", orig: "2 Filter On" => [Off, On]
#   param: "2 Filter Freq", orig: "2 Filter Freq", value: 0.372912, min: 0.000000, max: 1.000000
#   param: "2 Filter Width", orig: "2 Filter Width", value: 4.000000, min: 0.500000, max: 9.000000
# Q param: "2 Delay Mode", orig: "2 Delay Mode" => [Off, On]
# Q param: "2 Beat Delay", orig: "2 Beat Delay" => [1, 2, 3, 4, 5, 6, 8, 16]
#   param: "2 Beat Swing", orig: "2 Beat Swing", value: 0.000000, min: -0.333000, max: 0.333000
#   param: "2 Time Delay", orig: "2 Time Delay", value: 10.000000, min: 1.000000, max: 999.000000
#   param: "2 Feedback", orig: "2 Feedback", value: 0.460000, min: 0.000000, max: 1.000000
#   param: "2 Pan", orig: "2 Pan", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "2 Volume", orig: "2 Volume", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "3 Input On", orig: "3 Input On" => [Off, On]
# Q param: "3 Filter On", orig: "3 Filter On" => [Off, On]
#   param: "3 Filter Freq", orig: "3 Filter Freq", value: 0.494414, min: 0.000000, max: 1.000000
#   param: "3 Filter Width", orig: "3 Filter Width", value: 4.000000, min: 0.500000, max: 9.000000
# Q param: "3 Delay Mode", orig: "3 Delay Mode" => [Off, On]
# Q param: "3 Beat Delay", orig: "3 Beat Delay" => [1, 2, 3, 4, 5, 6, 8, 16]
#   param: "3 Beat Swing", orig: "3 Beat Swing", value: 0.000000, min: -0.333000, max: 0.333000
#   param: "3 Time Delay", orig: "3 Time Delay", value: 10.000000, min: 1.000000, max: 999.000000
#   param: "3 Feedback", orig: "3 Feedback", value: 0.240000, min: 0.000000, max: 1.000000
#   param: "3 Pan", orig: "3 Pan", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "3 Volume", orig: "3 Volume", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Dry", orig: "Dry", value: 0.874942, min: 0.000000, max: 1.000000

