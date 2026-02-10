import re

from .Dev import Dev

class VolumeStepper(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_bAddPanel = False # Do not add panel commands (Preset Save, etc.)
    self.m_lCfg = [
      'Bank0 | nGB0Off | SyncBeats | +xSpan1   | +xSpan16  | +xSpanMul2 | +xSpanDiv2',
      'Bank0 | nGB1Off | -         | Span1     | Span16    | SpanMul2   | SpanDiv2'  ,
      'Bank0 | nGB2Off | -         | Vol1On    | Vol2On    | Vol3On     | Vol4On'    ,
      'Bank0 | nGB3Off | -         | Vol1Off   | Vol2Off   | Vol3Off    | Vol4Off'   ,
      #-------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On | +xVol1On  | +xVol2On  | +xVol3On   | +xVol4On'  ,
      'Bank0 | nMB1Off | -         | +xVol1Off | +xVol2Off | +xVol3Off  | +xVol4Off' ,
      #-------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Beat      | Vol1      | Vol2      | Vol3       | Vol4'      ,
      'Bank0 | nMR1Off | Span',
      'Bank0 | nMR2Off | Start',
    ]
    self.reg('MxDeviceAudioEffect', 'VolumeStepper')
    self.parse_cfg()

  def get_extra_param_tx_value(self, phParamCfg):
    sName = phParamCfg['sName']

    if sName == 'xSpan16':
      self.set_param_value('Span',  '15.0') # select span  = 16 bits
      self.set_param_value('Start', '0.0' ) # select start = bit 1

    # all buttons should return "ON" value
    return 127

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName = phParamCfg['sName']
    self.tx_param_msg(sName, 127) # turn button ON again

    if sName == 'xSpan1':
      self.set_param_value('Span', '0.0')

    elif sName == 'xSpan16':
      self.set_param_value('Span', '15.0')

    elif sName == 'xSpanMul2':
      nOldSpan = self.get_param_value('Span') + 1.0
      nNewSpan = int((nOldSpan * 2.0) - 1.0)
      if nNewSpan > 15:
        self.alert('Invalid span')
        return
      self.set_param_value('Span', str(float(nNewSpan)))

    elif sName == 'xSpanDiv2':
      nOldSpan = self.get_param_value('Span') + 1.0
      nNewSpan = int((nOldSpan / 2.0) - 1.0)
      if nNewSpan < 0:
        self.alert('Invalid span %f' % (nNewSpan))
        return
      self.set_param_value('Span', str(nNewSpan))

    else:
      lMatch = re.search("xVol(\\d)(.*)", sName)
      sIdx   = lMatch[1]
      sType  = lMatch[2]
      sVal   = '127.0' if sType == 'On' else '0.0'
      sParam = 'Vol%s' % (sIdx)
      self.set_param_value(sParam, sVal)

#=======================================================================
# Class: MxDeviceAudioEffect, Device: VolumeStepper, Display: Max Audio Effect
# Q param: "Beat", orig: "Beat" => [1, 2, 3, 4]
# Q param: "SyncBeats", orig: "SyncBeats" => [off, on]
# Q param: "Span1", orig: "Span1" => [off, on]
# Q param: "Span16", orig: "Span16" => [off, on]
# Q param: "SpanDiv2", orig: "SpanDiv2" => [off, on]
# Q param: "SpanMul2", orig: "SpanMul2" => [off, on]
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Vol1Off", orig: "Vol1Off" => [off, on]
# Q param: "Vol1On", orig: "Vol1On" => [off, on]
# Q param: "Vol2Off", orig: "Vol2Off" => [off, on]
# Q param: "Vol2On", orig: "Vol2On" => [off, on]
# Q param: "Vol3Off", orig: "Vol3Off" => [off, on]
# Q param: "Vol3On", orig: "Vol3On" => [off, on]
# Q param: "Vol4Off", orig: "Vol4Off" => [off, on]
# Q param: "Vol4On", orig: "Vol4On" => [off, on]
# Q param: "Mul2", orig: "Mul2" => [1, 2, 4, 8, 16]
# Q param: "Free", orig: "Free" => [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# Q param: "Start", orig: "Start" => [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#   param: "Vol1", orig: "Vol1", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Vol2", orig: "Vol2", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Vol3", orig: "Vol3", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Vol4", orig: "Vol4", value: 0.000000, min: 0.000000, max: 127.000000

# BCR Tx [0xB0  65 127] -> "Device On"
# BCR Tx [0xB0  81   0] -> "Beat"
# BCR Tx [0xB0  89   0] -> "Span"
# BCR Tx [0xB0  42 127] -> "Span1"
# BCR Tx [0xB0  43 127] -> "Span16"
# BCR Tx [0xB0  45 127] -> "SpanDiv2"
# BCR Tx [0xB0  44 127] -> "SpanMul2"
# BCR Tx [0xB0  97   0] -> "Start"
# BCR Tx [0xB0  33 127] -> "SyncBeats"
# BCR Tx [0xB0  82 127] -> "Vol1"
# BCR Tx [0xB0  58 127] -> "Vol1Off"
# BCR Tx [0xB0   2 127] -> "Vol1On"
# BCR Tx [0xB0  83 127] -> "Vol2"
# BCR Tx [0xB0  59 127] -> "Vol2Off"
# BCR Tx [0xB0   3 127] -> "Vol2On"
# BCR Tx [0xB0  84 127] -> "Vol3"
# BCR Tx [0xB0  60 127] -> "Vol3Off"
# BCR Tx [0xB0   4 127] -> "Vol3On"
# BCR Tx [0xB0  85 127] -> "Vol4"
# BCR Tx [0xB0  61 127] -> "Vol4Off"
# BCR Tx [0xB0   5 127] -> "Vol4On"
# BCR Tx [0xB0  34 127] -> "xSpan1"
# BCR Tx [0xB0  35 127] -> "xSpan16"
# BCR Tx [0xB0  36 127] -> "xSpanMul2"
# BCR Tx [0xB0  37 127] -> "xSpanDiv2"
# BCR Tx [0xB0  66 127] -> "xVol1On"
# BCR Tx [0xB0  67 127] -> "xVol2On"
# BCR Tx [0xB0  68 127] -> "xVol3On"
# BCR Tx [0xB0  69 127] -> "xVol4On"
# BCR Tx [0xB0  74 127] -> "xVol1Off"
# BCR Tx [0xB0  75 127] -> "xVol2Off"
# BCR Tx [0xB0  76 127] -> "xVol3Off"
# BCR Tx [0xB0  77 127] -> "xVol4Off"

