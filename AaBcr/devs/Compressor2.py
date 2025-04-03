from .Dev import Dev

class Compressor2(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Auto Release On/Off | Makeup'         ,
      'Bank0 | nGB1Off | Env Mode            | LookAhead'      ,
      'Bank0 | nGB2Off | S/C On              | S/C EQ On'      ,
      'Bank0 | nGB3Off | S/C Listen          | Expansion Ratio',
      #---------------------------------------------------------
      'Bank0 | nGR0Off | Threshold           | Output Gain'    ,
      'Bank0 | nGR1Off | S/C Gain            | S/C Mix'        ,
      'Bank0 | nGR2Off | S/C EQ Type         | S/C EQ Freq'    ,
      'Bank0 | nGR3Off | S/C EQ Gain         | S/C EQ Q'       ,
      #---------------------------------------------------------
      'Bank0 | nMB0Off | Device On           | Preset Prev'    ,
      'Bank0 | nMB1Off | Preset Save         | Preset Next'    ,
      #---------------------------------------------------------
      'Bank0 | nMR0Off | Ratio               | Knee'           ,
      'Bank0 | nMR1Off | Attack              | Model'          ,
      'Bank0 | nMR2Off | Release             | Dry/Wet'        ,
    ]
    self.reg('Compressor2')
    self.parse_cfg()

#-----------------------------------------------------------------------
# Class: Compressor2, Device: Compressor, Display: Compressor
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Threshold", orig: "Threshold", value: 0.850000, min: 0.000000, max: 1.000000
#   param: "Ratio", orig: "Ratio", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Expansion Ratio", orig: "Expansion Ratio", value: 1.150000, min: 1.000000, max: 2.000000
#   param: "Attack", orig: "Attack", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "Release", orig: "Release", value: 0.156993, min: 0.000000, max: 1.000000
# Q param: "Auto Release On/Off", orig: "Auto Release On/Off" => [Off, On]
#   param: "Output Gain", orig: "Output Gain", value: 0.000000, min: -36.000000, max: 36.000000
# Q param: "Makeup", orig: "Makeup" => [Off, On]
#   param: "Dry/Wet", orig: "Dry/Wet", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Model", orig: "Model" => [Peak, RMS, Expand]
# Q param: "Env Mode", orig: "Env Mode" => [Lin, Log]
#   param: "Knee", orig: "Knee", value: 6.000000, min: 0.000000, max: 18.000000
# Q param: "LookAhead", orig: "LookAhead" => [0 ms, 1 ms, 10 ms]
# Q param: "S/C Listen", orig: "S/C Listen" => [Off, On]
# Q param: "S/C On", orig: "S/C On" => [Off, On]
#   param: "S/C Gain", orig: "S/C Gain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "S/C Mix", orig: "S/C Mix", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "S/C EQ Type", orig: "S/C EQ Type" => [Low Shelf, Bell, High Shelf, Low pass, Peak, High pass]
# Q param: "S/C EQ On", orig: "S/C EQ On" => [Off, On]
#   param: "S/C EQ Freq", orig: "S/C EQ Freq", value: 0.157826, min: 0.000000, max: 1.000000
#   param: "S/C EQ Gain", orig: "S/C EQ Gain", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "S/C EQ Q", orig: "S/C EQ Q", value: 0.408567, min: 0.000000, max: 1.000000
