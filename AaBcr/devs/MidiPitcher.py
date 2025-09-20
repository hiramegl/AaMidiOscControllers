from .Dev import Dev

class MidiPitcher(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Use Current Scale'                            ,
      'Bank0 | nGB1Off | +Pitch Reset     | +Pitch Scale Degrees Reset', # + = extra
      'Bank0 | nGB2Off | +Step Down       | +Step Up'                  , # + = extra
      'Bank0 | nGB3Off | +Step Down Scale | +Step Up Scale'            , # + = extra
      #-----------------------------------------------------------------
      'Bank0 | nGR0Off | Mode'                                         ,
      #-----------------------------------------------------------------
      'Bank0 | nMB0Off | Device On        | Preset Prev'               ,
      'Bank0 | nMB1Off | Preset Save      | Preset Next'               ,
      #-----------------------------------------------------------------
      'Bank0 | nMR0Off | Pitch            | Pitch Scale Degrees'       ,
      'Bank0 | nMR1Off | Step Width       | Step Width Scale Degrees'  ,
      'Bank0 | nMR2Off | Lowest           | Range'                     ,
    ]
    self.reg('MidiPitcher')
    self.parse_cfg()

  def customize_param(self, phParamCfg):
    if phParamCfg['sName'] == 'Pitch':
      # Pitch has a min of -128 and a max of 128 and the
      # span is too wide for the midi span 0~127
      phParamCfg['nMin'] = -64
      phParamCfg['nMax'] =  63

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName = phParamCfg['sName']
    if sName == 'Pitch Reset':
      self.reset_param_value('Pitch')
    elif sName == 'Pitch Scale Degrees Reset':
      self.reset_param_value('Pitch Scale Degrees')
    elif sName == 'Step Down':
      nStep = self.get_param_value('Step Width')
      self.add_to_param_value('Pitch', -nStep)
    elif sName == 'Step Up':
      nStep = self.get_param_value('Step Width')
      self.add_to_param_value('Pitch', +nStep)
    elif sName == 'Step Down Scale':
      nStep = self.get_param_value('Step Width Scale Degrees')
      self.add_to_param_value('Pitch Scale Degrees', -nStep)
    elif sName == 'Step Up Scale':
      nStep = self.get_param_value('Step Width Scale Degrees')
      self.add_to_param_value('Pitch Scale Degrees', +nStep)

#-----------------------------------------------------------------------
# Class: MidiPitcher, Device: Pitch, Display: Pitch
# Q param: "Device On", orig: "Device On" => [Off, On]
#   param: "Pitch", orig: "Pitch", value: 0.000000, min: -128.000000, max: 128.000000
#   param: "Pitch Scale Degrees", orig: "Pitch Scale Degrees", value: 0.000000, min: -30.000000, max: 30.000000
#   param: "Lowest", orig: "Lowest", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Range", orig: "Range", value: 127.000000, min: 0.000000, max: 127.000000
# Q param: "Mode", orig: "Mode" => [Block, Fold, Limit]
# Q param: "Use Song Scale", orig: "Use Song Scale" => [Off, On]
#   param: "Step Width", orig: "Step Width", value: 12.000000, min: 1.000000, max: 48.000000
#   param: "Step Width Scale Degrees", orig: "Step Width Scale Degrees", value: 7.000000, min: 1.000000, max: 30.000000

