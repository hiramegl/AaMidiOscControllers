import Live

from .Dev import Dev

ModulationSource = Live.WavetableDevice.ModulationSource

class InstrumentVector(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lSaveXtra = ['Osc1Class', 'Osc1Index', 'Osc1Effect', 'Osc2Class', 'Osc2Index', 'Osc2Effect', 'PolyVoices', 'UnisonMode', 'UnisonVoices', 'FilterRouting', 'XyzParamMatrix']
    self.m_lCfg = [
      'Bank0 | nGR0Off | Transpose       | Osc 1 Pos            | -                  | -               | Osc 2 Pos      | +UnisonMode       | +UnisonVoices  | Unison Amount    ' ,
      'Bank0 | nGR1Off | -               | -                    | -                  | -               | -              | +XyzParamMatrix   | Time           | Global Mod Amount' , # XyzParamMatrix will appear at the end in presets
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On       | Preset Prev          | Sub On             | Osc 1 On        | Osc 2 On       | +MonoPoly'                                              ,
      'Bank0 | nMB1Off | Preset Save     | Preset Next'                                                                                                                           ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Sub Gain        | +Osc1Class           | Osc 1 Pan          | Osc 1 Transp    | +Osc2Class     | Osc 2 Pan         | Osc 2 Transp   | Volume'            ,
      'Bank0 | nMR1Off | Sub Tone        | +Osc1Index           | Osc 1 Gain         | Osc 1 Detune    | +Osc2Index     | Osc 2 Gain        | Osc 2 Detune   | +PolyVoices'       ,
      'Bank0 | nMR2Off | Sub Transpose   | +Osc1Effect          | Osc 1 Effect 1     | Osc 1 Effect 2  | +Osc2Effect    | Osc 2 Effect 1    | Osc 2 Effect 2 | Glide'             ,
      ##===========================================================================================================================================================================
      'Bank1 | nGR0Off | Env 2 Attack    | Env 2 Decay          | Env 2 Sustain      | Env 2 Release   | Env 3 Attack   | Env 3 Decay       | Env 3 Sustain   | Env 3 Release'    ,
      'Bank1 | nGR1Off | Env 2 A Slope   | Env 2 D Slope        | Env 2 R Slope      | Env 2 Loop Mode | Env 3 A Slope  | Env 3 D Slope     | Env 3 R Slope   | Env 3 Loop Mode'  ,
      'Bank1 | nGR2Off | Env 2 Initial   | Env 2 Peak           | Env 2 Final        | -               | Env 3 Initial  | Env 3 Peak        | Env 3 Final'                        ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMB0Off | Filter 1 On     | Filter 1 BP/NO/Morph | Filter 2 On        | Filter 2 BP/NO/Morph'                                                                      ,
      'Bank1 | nMB1Off | -               | Filter 1 Slope       | -                  | Filter 2 Slope'                                                                            ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | Filter 1 Type   | Filter 1 Res         | Filter 2 Type      | Filter 2 Res    | Amp Attack     | Amp Decay         | Amp Sustain     | Amp Release'      ,
      'Bank1 | nMR1Off | Filter 1 LP/HP  | Filter 1 Drive       | Filter 2 LP/HP     | Filter 2 Drive  | Amp A Slope    | Amp D Slope       | Amp R Slope     | Amp Loop Mode'    ,
      'Bank1 | nMR2Off | Filter 1 Freq   | Filter 1 Morph       | Filter 2 Freq      | Filter 2 Morph  | +FilterRouting'                                                          ,
      #============================================================================================================================================================================
      'Bank2 | nGR0Off | +Tgt01AmpEnv    | +Tgt01Env2           | +Tgt01Env3         | +Tgt01Lfo1      | +Tgt01Lfo2     | +Tgt01MidiVel     | +Tgt01MidiNote     | +Tgt01MidiRand' ,
      'Bank2 | nGR1Off | +Tgt02AmpEnv    | +Tgt02Env2           | +Tgt02Env3         | +Tgt02Lfo1      | +Tgt02Lfo2     | +Tgt02MidiVel     | +Tgt02MidiNote     | +Tgt02MidiRand' ,
      'Bank2 | nGR2Off | +Tgt03AmpEnv    | +Tgt03Env2           | +Tgt03Env3         | +Tgt03Lfo1      | +Tgt03Lfo2     | +Tgt03MidiVel     | +Tgt03MidiNote     | +Tgt03MidiRand' ,
      'Bank2 | nGR3Off | +Tgt04AmpEnv    | +Tgt04Env2           | +Tgt04Env3         | +Tgt04Lfo1      | +Tgt04Lfo2     | +Tgt04MidiVel     | +Tgt04MidiNote     | +Tgt04MidiRand' ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMB0Off | LFO 1 Sync      | LFO 2 Sync'                                                                                                                            ,
      'Bank2 | nMB1Off | LFO 1 Retrigger | LFO 2 Retrigger'                                                                                                                       ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | LFO 1 Shape     | LFO 1 Attack Time    | LFO 1 Rate         | LFO 1 S. Rate   | LFO 2 Shape    | LFO 2 Attack Time | LFO 2 Rate         | LFO 2 S. Rate' ,
      'Bank2 | nMR1Off | LFO 1 Amount    | LFO 1 Shaping        | LFO 1 Phase Offset | -               | LFO 2 Amount   | LFO 2 Shaping     | LFO 2 Phase Offset | -            ' ,
      'Bank2 | nMR2Off | +Tgt00AmpEnv    | +Tgt00Env2           | +Tgt00Env3         | +Tgt00Lfo1      | +Tgt00Lfo2     | +Tgt00MidiVel     | +Tgt00MidiNote     | +Tgt00MidiRand' ,
      #============================================================================================================================================================================
      'Bank3 | nGR0Off | +Tgt08AmpEnv    | +Tgt08Env2           | +Tgt08Env3         | +Tgt08Lfo1      | +Tgt08Lfo2     | +Tgt08MidiVel     | +Tgt08MidiNote     | +Tgt08MidiRand' ,
      'Bank3 | nGR1Off | +Tgt09AmpEnv    | +Tgt09Env2           | +Tgt09Env3         | +Tgt09Lfo1      | +Tgt09Lfo2     | +Tgt09MidiVel     | +Tgt09MidiNote     | +Tgt09MidiRand' ,
      'Bank3 | nGR2Off | +Tgt10AmpEnv    | +Tgt10Env2           | +Tgt10Env3         | +Tgt10Lfo1      | +Tgt10Lfo2     | +Tgt10MidiVel     | +Tgt10MidiNote     | +Tgt10MidiRand',
      'Bank3 | nGR3Off | +Tgt11AmpEnv    | +Tgt11Env2           | +Tgt11Env3         | +Tgt11Lfo1      | +Tgt11Lfo2     | +Tgt11MidiVel     | +Tgt11MidiNote     | +Tgt11MidiRand',
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMR0Off | +Tgt05AmpEnv    | +Tgt05Env2           | +Tgt05Env3         | +Tgt05Lfo1      | +Tgt05Lfo2     | +Tgt05MidiVel     | +Tgt05MidiNote     | +Tgt05MidiRand' ,
      'Bank3 | nMR1Off | +Tgt06AmpEnv    | +Tgt06Env2           | +Tgt06Env3         | +Tgt06Lfo1      | +Tgt06Lfo2     | +Tgt06MidiVel     | +Tgt06MidiNote     | +Tgt06MidiRand' ,
      'Bank3 | nMR2Off | +Tgt07AmpEnv    | +Tgt07Env2           | +Tgt07Env3         | +Tgt07Lfo1      | +Tgt07Lfo2     | +Tgt07MidiVel     | +Tgt07MidiNote     | +Tgt07MidiRand' ,
      #============================================================================================================================================================================
      'Bank4 | nGR0Off | +Tgt15AmpEnv    | +Tgt15Env2           | +Tgt15Env3         | +Tgt15Lfo1      | +Tgt15Lfo2     | +Tgt15MidiVel     | +Tgt15MidiNote     | +Tgt15MidiRand',
      'Bank4 | nGR1Off | +Tgt16AmpEnv    | +Tgt16Env2           | +Tgt16Env3         | +Tgt16Lfo1      | +Tgt16Lfo2     | +Tgt16MidiVel     | +Tgt16MidiNote     | +Tgt16MidiRand',
      'Bank4 | nGR2Off | +Tgt17AmpEnv    | +Tgt17Env2           | +Tgt17Env3         | +Tgt17Lfo1      | +Tgt17Lfo2     | +Tgt17MidiVel     | +Tgt17MidiNote     | +Tgt17MidiRand',
      'Bank4 | nGR3Off | +Tgt18AmpEnv    | +Tgt18Env2           | +Tgt18Env3         | +Tgt18Lfo1      | +Tgt18Lfo2     | +Tgt18MidiVel     | +Tgt18MidiNote     | +Tgt18MidiRand',
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank4 | nMR0Off | +Tgt12AmpEnv    | +Tgt12Env2           | +Tgt12Env3         | +Tgt12Lfo1      | +Tgt12Lfo2     | +Tgt12MidiVel     | +Tgt12MidiNote     | +Tgt12MidiRand',
      'Bank4 | nMR1Off | +Tgt13AmpEnv    | +Tgt13Env2           | +Tgt13Env3         | +Tgt13Lfo1      | +Tgt13Lfo2     | +Tgt13MidiVel     | +Tgt13MidiNote     | +Tgt13MidiRand',
      'Bank4 | nMR2Off | +Tgt14AmpEnv    | +Tgt14Env2           | +Tgt14Env3         | +Tgt14Lfo1      | +Tgt14Lfo2     | +Tgt14MidiVel     | +Tgt14MidiNote     | +Tgt14MidiRand',
    ]
    self.reg('InstrumentVector')
    self.m_hModSrcs = {
      'AmpEnv'  : ModulationSource.amp_envelope,
      'Env2'    : ModulationSource.envelope_2,
      'Env3'    : ModulationSource.envelope_3,
      'Lfo1'    : ModulationSource.lfo_1,
      'Lfo2'    : ModulationSource.lfo_2,
      'MidiVel' : ModulationSource.midi_velocity,
      'MidiNote': ModulationSource.midi_note,
      'MidiPb'  : ModulationSource.midi_pitch_bend,
      'MidiPrs' : ModulationSource.midi_channel_pressure,
      'MidiMod' : ModulationSource.midi_mod_wheel,
      'MidiRand': ModulationSource.midi_random,
    }
    self.m_lModSrcs = [
      ModulationSource.amp_envelope,
      ModulationSource.envelope_2,
      ModulationSource.envelope_3,
      ModulationSource.lfo_1,
      ModulationSource.lfo_2,
      ModulationSource.midi_velocity,
      ModulationSource.midi_note,
      ModulationSource.midi_pitch_bend,
      ModulationSource.midi_channel_pressure,
      ModulationSource.midi_mod_wheel,
      ModulationSource.midi_random,
    ]
    self.parse_cfg()

  def get_extra_param_tx_value(self, phParamCfg):
    sName = phParamCfg['sName']

    if sName == 'Osc1Class':
      return (self.m_oDev.oscillator_1_wavetable_category * 5)
    elif sName == 'Osc1Index':
      return (self.m_oDev.oscillator_1_wavetable_index * 5)
    elif sName == 'Osc1Effect':
      return (self.m_oDev.oscillator_1_effect_mode * 5)
    elif sName == 'Osc2Class':
      return (self.m_oDev.oscillator_2_wavetable_category * 5)
    elif sName == 'Osc2Index':
      return (self.m_oDev.oscillator_2_wavetable_index * 5)
    elif sName == 'Osc2Effect':
      return (self.m_oDev.oscillator_2_effect_mode * 5)
    elif sName == 'MonoPoly':
      return (self.m_oDev.mono_poly * 127)
    elif sName == 'PolyVoices':
      return (self.m_oDev.poly_voices * 5)
    elif sName == 'UnisonMode':
      return (self.m_oDev.unison_mode * 5)
    elif sName == 'UnisonVoices':
      return (self.m_oDev.unison_voice_count * 5) - 10
    elif sName == 'FilterRouting':
      return (self.m_oDev.filter_routing * 5)
    elif sName == 'XyzParamMatrix':
      return 0
    elif sName[:3] == 'Tgt':
      return self.get_tgt_matrix_value(int(sName[3:5]), sName[5:])

  def get_tgt_matrix_value(self, pnIdx, psModName):
    lTgtNames = self.m_oDev.visible_modulation_target_names
    if pnIdx >= len(lTgtNames):
      return 0 # target not available for index pnIdx

    nValue = self.m_oDev.get_modulation_value(pnIdx, self.m_hModSrcs[psModName])
    return int(nValue * 127.0)

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName = phParamCfg['sName']

    nCategories = len(self.m_oDev.oscillator_wavetable_categories)
    if sName == 'Osc1Class':
      nValue = min(int(pnValue / 5), nCategories)
      self.m_oDev.oscillator_1_wavetable_category = nValue
    elif sName == 'Osc1Index':
      nValue = int(pnValue / 5)
      self.m_oDev.oscillator_1_wavetable_index = nValue
    elif sName == 'Osc1Effect':
      nValue = min(int(pnValue / 5), 3)
      self.m_oDev.oscillator_1_effect_mode = nValue
    elif sName == 'Osc2Class':
      nValue = min(int(pnValue / 5), nCategories)
      self.m_oDev.oscillator_2_wavetable_category = nValue
    elif sName == 'Osc2Index':
      nValue = int(pnValue / 5)
      self.m_oDev.oscillator_2_wavetable_index = nValue
    elif sName == 'Osc2Effect':
      nValue = min(int(pnValue / 5), 3)
      self.m_oDev.oscillator_2_effect_mode = nValue
    elif sName == 'MonoPoly':
      nValue = int(pnValue / 127)
      self.m_oDev.mono_poly = nValue
    elif sName == 'PolyVoices':
      nValue = min(int(pnValue / 5), 6)
      self.m_oDev.poly_voices = nValue
    elif sName == 'UnisonMode':
      nValue = min(int(pnValue / 5), 6)
      self.m_oDev.unison_mode = nValue
    elif sName == 'UnisonVoices':
      nValue = min(int(pnValue / 5), 6) + 2
      self.m_oDev.unison_voice_count = nValue
    elif sName == 'FilterRouting':
      nValue = min(int(pnValue / 5), 2)
      self.m_oDev.filter_routing = nValue
    elif sName == 'XyzParamMatrix':
      nValue = 0.0 # dummy value
    elif sName[:3] == 'Tgt':
      nValue = self.set_tgt_matrix_value(int(sName[3:5]), sName[5:], pnValue)
      if nValue == None:
        return

    self.alert('Track: %s, Dev: %s, Param: %s -> %d (%f)' %
      (phParamCfg['sTrack'], phParamCfg['sDev'], phParamCfg['sName'], pnValue, nValue))

  def set_tgt_matrix_value(self, pnIdx, psModName, pnValue):
    lTgtNames = self.m_oDev.visible_modulation_target_names
    if pnIdx >= len(lTgtNames):
      self.alert('!Error: target index %d not available in modulation matrix' % pnIdx)
      return None

    nValue = float(pnValue) / 127.0
    self.m_oDev.set_modulation_value(pnIdx, self.m_hModSrcs[psModName], nValue)
    return nValue

  # ********************************************************

  def get_extra_param_value_for_save(self, psParam):
    if psParam == 'Osc1Class':
      return self.m_oDev.oscillator_1_wavetable_category
    elif psParam == 'Osc1Index':
      return self.m_oDev.oscillator_1_wavetable_index
    elif psParam == 'Osc1Effect':
      return self.m_oDev.oscillator_1_effect_mode
    elif psParam == 'Osc2Class':
      return self.m_oDev.oscillator_2_wavetable_category
    elif psParam == 'Osc2Index':
      return self.m_oDev.oscillator_2_wavetable_index
    elif psParam == 'Osc2Effect':
      return self.m_oDev.oscillator_2_effect_mode
    elif psParam == 'MonoPoly':
      return self.m_oDev.mono_poly
    elif psParam == 'PolyVoices':
      return self.m_oDev.poly_voices
    elif psParam == 'UnisonMode':
      return self.m_oDev.unison_mode
    elif psParam == 'UnisonVoices':
      return self.m_oDev.unison_voice_count
    elif psParam == 'FilterRouting':
      return self.m_oDev.filter_routing
    elif psParam == 'XyzParamMatrix':
      return self.get_param_matrix()

  def get_param_matrix(self):
    lTgtNames = self.m_oDev.visible_modulation_target_names
    lTgtRows  = []
    for nIdx in range(len(lTgtNames)):
      lRow = []
      for oModSrc in self.m_lModSrcs:
        lRow.append(str(self.m_oDev.get_modulation_value(nIdx, oModSrc)))
      sTgtName = self.m_oDev.get_modulation_target_parameter_name(nIdx)
      sTgtRow  = '%s=%s' % (sTgtName, '/'.join(lRow))
      lTgtRows.append(sTgtRow)
    return '!'.join(lTgtRows)

  def set_extra_param_value_from_load(self, psParam, poValue):
    if psParam == 'XyzParamMatrix':
      self.set_param_matrix(poValue)
      return

    nValue = int(float(poValue))
    if psParam == 'Osc1Class':
      self.m_oDev.oscillator_1_wavetable_category = nValue
    elif psParam == 'Osc1Index':
      self.m_oDev.oscillator_1_wavetable_index = nValue
    elif psParam == 'Osc1Effect':
      self.m_oDev.oscillator_1_effect_mode = nValue
    elif psParam == 'Osc2Class':
      self.m_oDev.oscillator_2_wavetable_category = nValue
    elif psParam == 'Osc2Index':
      self.m_oDev.oscillator_2_wavetable_index = nValue
    elif psParam == 'Osc2Effect':
      self.m_oDev.oscillator_2_effect_mode = nValue
    elif psParam == 'MonoPoly':
      self.m_oDev.mono_poly = nValue
    elif psParam == 'PolyVoices':
      self.m_oDev.poly_voices = nValue
    elif psParam == 'UnisonMode':
      self.m_oDev.unison_mode = nValue
    elif psParam == 'UnisonVoices':
      self.m_oDev.unison_voice_count = nValue
    elif psParam == 'FilterRouting':
      self.m_oDev.filter_routing = nValue

  def set_param_matrix(self, psMatrix):
    # parse parameters matrix
    hTgtMap  = {}
    lTgtRows = psMatrix.split('!')
    for sTgtRow in lTgtRows:
      lTgtValues = sTgtRow.split('=')
      sTgtName   = lTgtValues[0]
      sValues    = lTgtValues[1]
      lValues    = sValues.split('/')
      hTgtMap[sTgtName] = lValues
    self.dlog('-> Preset uses %d tgt params: %s' %
      (len(hTgtMap.keys()), ','.join(hTgtMap.keys())))

    # get a hash with modulatable parameters
    hParams = {}
    for oParam in self.m_oDev.parameters:
      bMod = self.m_oDev.is_parameter_modulatable(oParam)
      if bMod:
        hParams[oParam.name] = oParam

    # get list of currently visible target parameters
    lTgtNames = self.m_oDev.visible_modulation_target_names
    self.dlog('-> visible tgt names BEFORE adding missing: %d = %s' %
      (len(lTgtNames), ','.join(lTgtNames)))
    lTgtVis   = []
    for nIdx in range(len(lTgtNames)):
      sTgtName = self.m_oDev.get_modulation_target_parameter_name(nIdx)
      lTgtVis.append(sTgtName)

    # add missing target parameters
    for sTgtParam in hTgtMap.keys():
      if (sTgtParam in lTgtVis) == False:
        oParam = hParams[sTgtParam]
        nNewIdx = self.m_oDev.add_parameter_to_modulation_matrix(oParam)
        # set a dummy modulation value to complete addition
        # of the new target parameter
        self.m_oDev.set_modulation_value(
          nNewIdx, ModulationSource.amp_envelope, 1.0)
        self.dlog('-> Added missing tgt param: %s at index %d' %
          (sTgtParam, nNewIdx))

    # fill in the matrix values
    lTgtNames = self.m_oDev.visible_modulation_target_names # update tgt names
    self.dlog('-> visible tgt names AFTER adding missing: %d = %s' %
      (len(lTgtNames), ','.join(lTgtNames)))
    for nIdx in range(len(lTgtNames)):
      sTgtName = self.m_oDev.get_modulation_target_parameter_name(nIdx)
      if sTgtName in hTgtMap:
        lValues = hTgtMap[sTgtName]
        self.log('-> Tgt name "%s" found in preset with values: %s' %
          (sTgtName, '|'.join(lValues)))
        for nValIdx in range(len(self.m_lModSrcs)):
          self.m_oDev.set_modulation_value(
            nIdx, self.m_lModSrcs[nValIdx], float(lValues[nValIdx]))
      else:
        self.log('-> Tgt name "%s" NOT found in preset! Resetting ...' %
          (sTgtName))
        for nValIdx in range(len(self.m_lModSrcs)):
          self.m_oDev.set_modulation_value(
            nIdx, self.m_lModSrcs[nValIdx], 0.0)

#=======================================================================
# Class: InstrumentVector, Device: Wavetable, Display: Wavetable
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Sub On", orig: "Sub On" => [Off, On]
# Q param: "Osc 1 On", orig: "Osc 1 On" => [Off, On]
# Q param: "Osc 2 On", orig: "Osc 2 On" => [Off, On]
#   param: "Sub Gain", orig: "Sub Gain", value: 0.501188, min: 0.000000, max: 1.000000
#   param: "Osc 1 Pan", orig: "Osc 1 Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Gain", orig: "Osc 1 Gain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Effect 1", orig: "Osc 1 Effect 1", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Effect 2", orig: "Osc 1 Effect 2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Transp", orig: "Osc 1 Transp", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Osc 1 Detune", orig: "Osc 1 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 1 Pos", orig: "Osc 1 Pos", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Sub Tone", orig: "Sub Tone", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Pan", orig: "Osc 2 Pan", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Gain", orig: "Osc 2 Gain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Effect 1", orig: "Osc 2 Effect 1", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Effect 2", orig: "Osc 2 Effect 2", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Transp", orig: "Osc 2 Transp", value: 0.000000, min: -24.000000, max: 24.000000
#   param: "Osc 2 Detune", orig: "Osc 2 Detune", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Osc 2 Pos", orig: "Osc 2 Pos", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Sub Transpose", orig: "Sub Transpose" => [0, -1, -2]
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Volume", orig: "Volume", value: 0.595662, min: 0.000000, max: 1.000000
#   param: "Glide", orig: "Glide", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Unison Amount", orig: "Unison Amount", value: 0.300000, min: 0.000000, max: 1.000000
#   param: "Time", orig: "Time", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Global Mod Amount", orig: "Global Mod Amount", value: 0.500000, min: 0.000000, max: 1.000000
#---------------------
# Q param: "Filter 1 On", orig: "Filter 1 On" => [Off, On]
# Q param: "Filter 1 BP/NO/Morph", orig: "Filter 1 BP/NO/Morph" => [Clean, OSR]
# Q param: "Filter 1 Slope", orig: "Filter 1 Slope" => [12, 24]
# Q param: "Filter 2 On", orig: "Filter 2 On" => [Off, On]
# Q param: "Filter 2 BP/NO/Morph", orig: "Filter 2 BP/NO/Morph" => [Clean, OSR]
# Q param: "Filter 2 Slope", orig: "Filter 2 Slope" => [12, 24]
# Q param: "Filter 1 Type", orig: "Filter 1 Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter 1 LP/HP", orig: "Filter 1 LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter 1 Freq", orig: "Filter 1 Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Filter 1 Res", orig: "Filter 1 Res", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 1 Drive", orig: "Filter 1 Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 1 Morph", orig: "Filter 1 Morph", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Filter 2 Type", orig: "Filter 2 Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter 2 LP/HP", orig: "Filter 2 LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter 2 Freq", orig: "Filter 2 Freq", value: 0.000002, min: 0.000000, max: 1.000000
#   param: "Filter 2 Res", orig: "Filter 2 Res", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 2 Drive", orig: "Filter 2 Drive", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter 2 Morph", orig: "Filter 2 Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Amp Attack", orig: "Amp Attack", value: 0.084090, min: 0.000000, max: 1.000000
#   param: "Amp Decay", orig: "Amp Decay", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Amp Sustain", orig: "Amp Sustain", value: 0.707946, min: 0.000000, max: 1.000000
#   param: "Amp Release", orig: "Amp Release", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Amp A Slope", orig: "Amp A Slope", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Amp D Slope", orig: "Amp D Slope", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Amp R Slope", orig: "Amp R Slope", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "Amp Loop Mode", orig: "Amp Loop Mode" => [None, Trigger, Loop]
#---------------------
#   param: "Env 2 Attack", orig: "Env 2 Attack", value: 0.084090, min: 0.000000, max: 1.000000
#   param: "Env 2 Decay", orig: "Env 2 Decay", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 2 Sustain", orig: "Env 2 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 2 Release", orig: "Env 2 Release", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 3 Attack", orig: "Env 3 Attack", value: 0.084090, min: 0.000000, max: 1.000000
#   param: "Env 3 Decay", orig: "Env 3 Decay", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 3 Sustain", orig: "Env 3 Sustain", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 3 Release", orig: "Env 3 Release", value: 0.415927, min: 0.000000, max: 1.000000
#   param: "Env 2 A Slope", orig: "Env 2 A Slope", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 2 D Slope", orig: "Env 2 D Slope", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Env 2 R Slope", orig: "Env 2 R Slope", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "Env 2 Loop Mode", orig: "Env 2 Loop Mode" => [None, Trigger, Loop]
#   param: "Env 3 A Slope", orig: "Env 3 A Slope", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Env 3 D Slope", orig: "Env 3 D Slope", value: 0.750000, min: 0.000000, max: 1.000000
#   param: "Env 3 R Slope", orig: "Env 3 R Slope", value: 0.750000, min: 0.000000, max: 1.000000
# Q param: "Env 3 Loop Mode", orig: "Env 3 Loop Mode" => [None, Trigger, Loop]
#   param: "Env 2 Initial", orig: "Env 2 Initial", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env 2 Peak", orig: "Env 2 Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Env 2 Final", orig: "Env 2 Final", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env 3 Initial", orig: "Env 3 Initial", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Env 3 Peak", orig: "Env 3 Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Env 3 Final", orig: "Env 3 Final", value: 0.000000, min: 0.000000, max: 1.000000
#---------------------
# Q param: "LFO 1 Retrigger", orig: "LFO 1 Retrigger" => [Off, On]
# Q param: "LFO 1 Sync", orig: "LFO 1 Sync" => [Free, Tempo]
# Q param: "LFO 2 Retrigger", orig: "LFO 2 Retrigger" => [Off, On]
# Q param: "LFO 2 Sync", orig: "LFO 2 Sync" => [Free, Tempo]
# Q param: "LFO 1 Shape", orig: "LFO 1 Shape" => [Sine, Triangle, Sawtooth, Rectangle, Noise]
#   param: "LFO 1 Attack Time", orig: "LFO 1 Attack Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Rate", orig: "LFO 1 Rate", value: 0.320789, min: 0.000000, max: 1.000000
#   param: "LFO 1 S. Rate", orig: "LFO 1 S. Rate", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "LFO 1 Amount", orig: "LFO 1 Amount", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Shaping", orig: "LFO 1 Shaping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Phase Offset", orig: "LFO 1 Phase Offset", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "LFO 2 Shape", orig: "LFO 2 Shape" => [Sine, Triangle, Sawtooth, Rectangle, Noise]
#   param: "LFO 2 Attack Time", orig: "LFO 2 Attack Time", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Rate", orig: "LFO 2 Rate", value: 0.320789, min: 0.000000, max: 1.000000
#   param: "LFO 2 S. Rate", orig: "LFO 2 S. Rate", value: 15.000000, min: 0.000000, max: 21.000000
#   param: "LFO 2 Amount", orig: "LFO 2 Amount", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Shaping", orig: "LFO 2 Shaping", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Phase Offset", orig: "LFO 2 Phase Offset", value: 0.000000, min: 0.000000, max: 1.000000
