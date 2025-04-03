from .Dev import Dev

class MidiVelocity(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nMB0Off | Device On   | Preset Prev'         ,
      'Bank0 | nMB1Off | Preset Save | Preset Next'         ,
      #------------------------------------------------------
      'Bank0 | nMR0Off | Operation   | Drive      | Out Hi' ,
      'Bank0 | nMR1Off | Mode        | Compand    | Out Low',
      'Bank0 | nMR2Off | Lowest      | Random     | Range'  ,
    ]
    self.reg('MidiVelocity')
    self.parse_cfg()

#=======================================================================
# Class: MidiVelocity, Device: Velocity, Display: Velocity
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Operation", orig: "Operation" => [Velocity, Rel. Vel., Both]
# Q param: "Mode", orig: "Mode" => [Clip, Gate, Fixed]
#   param: "Lowest", orig: "Lowest", value: 1.000000, min: 0.000000, max: 127.000000
#   param: "Drive", orig: "Drive", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Compand", orig: "Compand", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Random", orig: "Random", value: 0.000000, min: 0.000000, max: 64.000000
#   param: "Out Hi", orig: "Out Hi", value: 127.000000, min: 0.000000, max: 127.000000
#   param: "Out Low", orig: "Out Low", value: 1.000000, min: 0.000000, max: 127.000000
#   param: "Range", orig: "Range", value: 127.000000, min: 0.000000, max: 127.000000

