from .Dev import Dev

class OriginalSimpler(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | Sample Selector       | -                      | -                     | Fade In            | Fade Out               | Transpose             | Vol < Vel         | Volume',
      ##------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On             | Preset Prev            | S Loop On             | +Retrigger         | +Reverse               | +Crop                 | +Warp             | +Warp As',
      'Bank0 | nMB1Off | Preset Save           | Preset Next            | Snap                  | Trigger Mode       | +Clear Slices          | -                     | +Warp Half        | +Warp Double',
      #------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | +Playback Mode        | +Gain                  | S Start               | S Loop Length      | S Length               | S Loop Fade           | +Voices           | +Warp Mode',
      'Bank0 | nMR1Off | +Beats Gran Res       | +Beats Trans Loop Mode | +Beats Trans Envelope | +Tones Grain Size  | +Texture Grain Size    | +Texture Flux         | +Start Marker Pos | +End Marker Pos',
      'Bank0 | nMR2Off | +Complex Pro Formants | +Complex Pro Envelope  | +Slicing Style        | +Slicing Sensivity | +Slicing Beat Division | +Slicing Region Count | +Start Marker Res | +End Marker Res',
      ##=========================================================================================================================================
      'Bank1 | nMB0Off | Fe On',
      'Bank1 | nMB1Off | F On | Filter Slope   | Filter Circuit - BP/NO/Morph',
      #---------------------------------------------------------
      'Bank1 | nMR0Off | Fe < Env              | Fe Attack              | Fe Decay              | Fe Sustain         | Fe Release             | Fe Mode               | Fe Loop           | -',
      'Bank1 | nMR1Off | Fe Retrig             | Fe A Slope             | Fe D Slope            | Fe R Slope         | Fe R < Vel             | Fe Init               | Fe Peak           | Fe End',
      'Bank1 | nMR2Off | Filter Type           | Filter Circuit - LP/HP | Filter Freq           | Filter Res         | Filter Drive           | Filter Morph          | Filt < Vel        | Filt < Key',
      ##=========================================================================================================================================
      'Bank2 | nMB0Off | L Retrig',
      'Bank2 | nMB1Off | L On',
      #---------------------------------------------------------
      'Bank2 | nMR0Off | L Attack              | L R < Key              | L Offset              | Vol < LFO          | Pitch < LFO            | Pan < LFO             | Filt < LFO        | -',
      'Bank2 | nMR1Off | L Wave                | L Rate                 | L Sync                | L Sync Rate',
      'Bank2 | nMR2Off | Ve Attack             | Ve Decay               | Ve Sustain            | Ve Release         | Ve Mode                | Ve Loop               | Ve Retrig         | -',
      ##=========================================================================================================================================
      'Bank3 | nMB0Off | Pe On',
      #---------------------------------------------------------
      'Bank3 | nMR0Off | Pe < Env              | Pe Attack              | Pe Decay              | Pe Sustain         | Pe Release             | Pe Mode               | Pe Loop           | -',
      'Bank3 | nMR1Off | Pe Retrig             | Pe A Slope             | Pe D Slope            | Pe R Slope         | Pe R < Vel             | Pe Init               | Pe Peak           | Pe End',
      'Bank3 | nMR2Off | Pan                   | Pan < Rnd              | Glide Mode            | Spread             | Detune                 | Glide Time',
    ]
    self.reg('OriginalSimpler')
    self.parse_cfg()

  def customize_param(self, phParamCfg):
    sName = phParamCfg['sName']
    if sName  == 'Start Marker Pos':
      phParamCfg['nPos']   = 0
    if sName  == 'Start Marker Res':
      phParamCfg['nRes'] = 0 # 0: Coarse, 1: Medium, 2: Fine
    elif sName  == 'End Marker Pos':
      phParamCfg['nPos']   = 0
    elif sName  == 'End Marker Res':
      phParamCfg['nRes'] = 0 # 0: Coarse, 1: Medium, 2: Fine

  def get_extra_param_tx_value(self, phParamCfg):
    sName   = phParamCfg['sName']
    oSample = self.m_oDev.sample

    if sName == 'Retrigger':
      return int(self.m_oDev.retrigger * 127)
    elif (sName == 'Reverse' or
      sName == 'Clear Slices' or
      sName == 'Crop'):
      return 127 # Commands always ON
    elif sName == 'Warp':
      if oSample != None:
        return int(oSample.warping * 127)
    elif sName == 'Warp As':
      return int(self.m_oDev.can_warp_as * 127)
    elif sName == 'Warp Half':
      return int(self.m_oDev.can_warp_half * 127)
    elif sName == 'Warp Double':
      return int(self.m_oDev.can_warp_double * 127)

    elif sName == 'Playback Mode':
      return int(self.m_oDev.playback_mode * 10)
    elif sName == 'Gain':
      if oSample != None:
        return int(oSample.gain * 127.0)
    elif sName == 'Voices':
      lVoices = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 32]
      return int(lVoices.index(self.m_oDev.voices) * 9)
    elif sName == 'Warp Mode':
      if oSample != None:
        return int(oSample.warp_mode * 10)

    elif sName == 'Beats Gran Res':
      if oSample != None:
        return int(oSample.beats_granulation_resolution * 10)
    elif sName == 'Beats Trans Loop Mode':
      if oSample != None:
        return int(oSample.beats_transient_loop_mode * 10)
    elif sName == 'Beats Trans Envelope':
      if oSample != None:
        return int((float(oSample.beats_transient_envelope) / 100.0) * 127.0)
    elif sName == 'Tones Grain Size':
      if oSample != None:
        return int(((oSample.tones_grain_size - 12.0) / 88.0) * 127.0)
    elif sName == 'Texture Grain Size':
      if oSample != None:
        return int(((oSample.texture_grain_size - 2.0) / 261.0) * 127.0)
    elif sName == 'Texture Flux':
      if oSample != None:
        return int((float(oSample.texture_flux) / 100.0) * 127.0)

    elif sName == 'Complex Pro Formants':
      if oSample != None:
        return int((float(oSample.complex_pro_formants) / 100.0) * 127.0)
    elif sName == 'Complex Pro Envelope':
      if oSample != None:
        return int(((oSample.complex_pro_envelope - 8.0) / 248.0) * 127.0)
    elif sName == 'Slicing Style':
      if oSample != None:
        return int(oSample.slicing_style * 10)
    elif sName == 'Slicing Sensivity':
      if oSample != None:
        return int(oSample.slicing_sensitivity * 127.0)
    elif sName == 'Slicing Beat Division':
      if oSample != None:
        return int(oSample.slicing_beat_division * 12)
    elif sName == 'Slicing Region Counter':
      if oSample != None:
        return int(((oSample.slicing_region_count - 2.0) / 62.0) * 127.0)

    elif sName == 'Start Marker Pos':
      if oSample != None:
        return int((float(oSample.start_marker) / float(oSample.length)) * 127.0)
    elif sName == 'Start Marker Res':
      if oSample != None:
        return int(phParamCfg['nRes'] * 10)
    elif sName == 'End Marker Pos':
      if oSample != None:
        return int((float(oSample.end_marker) / float(oSample.length)) * 127.0)
    elif sName == 'End Marker Res':
      if oSample != None:
        return int(phParamCfg['nRes'] * 10)

    return 0

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName    = phParamCfg['sName']
    oSample  = self.m_oDev.sample
    nValue1  = float(pnValue) / 127.0 # float: 0 .. 1.0
    nValue12 = int(pnValue / 10)      # int:   0 .. 12

    if sName == 'Retrigger':
      self.m_oDev.retrigger = (pnValue == 127)
    elif sName == 'Reverse':
      self.m_oDev.reverse()
      self.tx_param_msg('Reverse', 127)
    elif sName == 'Crop':
      if oSample != None:
        self.m_oDev.crop()
        self.tx_param_msg('Crop', 127)
        self.get_param_config('Start Marker Pos')['nPos'] = 0
        self.get_param_config('End Marker Pos'  )['nPos'] = oSample.length
        self.tx_param_msg('Start Marker Pos', 0)
        self.tx_param_msg('End Marker Pos', 127)
    elif sName == 'Clear Slices':
      if oSample != None:
        oSample.clear_slices()
      self.tx_param_msg('Clear Slices', 127)
    elif sName == 'Warp':
      if oSample != None:
        oSample.warping = (pnValue == 127)
      self.tx_param_msg('Warp', 127)
    elif sName == 'Warp As':
      if self.m_oDev.can_warp_as:
        self.m_oDev.warp_as(self.m_oDev.guess_playback_length())
      self.tx_param_msg('Warp As',     127)
      self.tx_param_msg('Warp Half',   127 * self.m_oDev.can_warp_half)
      self.tx_param_msg('Warp Double', 127 * self.m_oDev.can_warp_double)
    elif sName == 'Warp Half':
      if self.m_oDev.can_warp_half:
        self.m_oDev.warp_half()
      self.tx_param_msg('Warp Half',   127)
      self.tx_param_msg('Warp As',     127 * self.m_oDev.can_warp_as)
      self.tx_param_msg('Warp Double', 127 * self.m_oDev.can_warp_double)
    elif sName == 'Warp Double':
      if self.m_oDev.can_warp_double:
        self.m_oDev.warp_double()
      self.tx_param_msg('Warp Double', 127)
      self.tx_param_msg('Warp As',     127 * self.m_oDev.can_warp_as)
      self.tx_param_msg('Warp Half',   127 * self.m_oDev.can_warp_half)

    elif sName == 'Playback Mode':
      if nValue12 > 2: nValue12 = 2
      self.m_oDev.playback_mode = nValue12
    elif sName == 'Gain':
      if oSample != None and pnValue != 0:
        oSample.gain = nValue1
    elif sName == 'Voices':
      lVoices = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 32]
      self.m_oDev.voices = lVoices[int(pnValue / 9)]
    elif sName == 'Warp Mode':
      if oSample != None:
        if nValue12 > 6: nValue12 = 6
        oSample.warp_mode = nValue12

    elif sName == 'Beats Gran Res':
      if oSample != None:
        if nValue12 > 6: nValue12 = 6
        oSample.beats_granulation_resolution = nValue12
    elif sName == 'Beats Trans Loop Mode':
      if oSample != None:
        if nValue12 > 3: nValue12 = 3
        oSample.beats_transient_loop_mode = nValue12
    elif sName == 'Beats Trans Envelope':
      if oSample != None:
        oSample.beats_transient_envelope = nValue1 * 100.0
    elif sName == 'Tones Grain Size':
      if oSample != None:
        oSample.tones_grain_size = nValue1 * 88.0 + 12.0
    elif sName == 'Texture Grain Size':
      if oSample != None:
        oSample.texture_grain_size = nValue1 * 261.0 + 2.0
    elif sName == 'Texture Flux':
      if oSample != None:
        oSample.texture_flux = nValue1 * 100.0

    elif sName == 'Complex Pro Formants':
      if oSample != None:
        oSample.complex_pro_formants = nValue1 * 100.0
    elif sName == 'Complex Pro Envelope':
      if oSample != None:
        oSample.complex_pro_envelope = nValue1 * 248.0 + 8.0
    elif sName == 'Slicing Style':
      if oSample != None:
        if nValue12 > 3: nValue12 = 3
        oSample.slicing_style = nValue12
    elif sName == 'Slicing Sensivity':
      if oSample != None:
        oSample.slicing_sensitivity = nValue1
    elif sName == 'Slicing Beat Division':
      if oSample != None:
        oSample.slicing_beat_division = int(pnValue / 12)
    elif sName == 'Slicing Region Count':
      if oSample != None:
        oSample.slicing_region_count = int(nValue1 * 62.0 + 2.0)

    elif sName == 'Start Marker Pos':
      if oSample != None:
        self.on_marker_pos_rx_value('Start Marker', phParamCfg, pnValue)
    elif sName == 'Start Marker Res':
      if oSample != None:
        if nValue12 > 2: nValue12 = 2 # 0, 1, 2
        self.on_marker_res_rx_value('Start Marker', phParamCfg, nValue12)
    elif sName == 'End Marker Pos':
      if oSample != None:
        self.on_marker_pos_rx_value('End Marker', phParamCfg, pnValue)
    elif sName == 'End Marker Res':
      if oSample != None:
        if nValue12 > 2: nValue12 = 2 # 0, 1, 2
        self.on_marker_res_rx_value('End Marker', phParamCfg, nValue12)

  def on_marker_pos_rx_value(self, psType, phParamCfg, pnValue):
    oSample = self.m_oDev.sample
    if oSample == None: return

    sPosParam = '%s Pos' % (psType)
    sResParam = '%s Res' % (psType)
    nRes      = self.get_param_config(sResParam)['nRes'] # 0, 1, 2

    nDiv0 = float(oSample.length) / 127.0 # in samples (float)

    if nRes == 0: # coarse
      nPos = int(pnValue * nDiv0)         # in samples
      phParamCfg['nPos'] = nPos

    elif nRes == 1: # medium
      nDiv1 = nDiv0 / 64.0                # in samples (float)
      if nDiv1 < 1.0: nDiv1 = 1.0
      nOffs = float(pnValue - 64) * nDiv1 # in samples (float) [-X , ..., +X)
      nPos  = int(phParamCfg['nPos'] + int(nOffs))

    elif nRes == 2: # fine
      nDiv2 = (nDiv0 / 64.0) / 64.0       # in samples (float)
      if nDiv2 < 1.0: nDiv2 = 1.0
      nOffs = float(pnValue - 64) * nDiv2 # in samples (float) [-X , ..., +X)
      nPos  = int(phParamCfg['nPos'] + int(nOffs))

    if psType == 'Start Marker':
      if nPos >= 0 and nPos < oSample.end_marker:
        oSample.start_marker = nPos
        self.alert('START MARKER: %d' % (nPos))
        return
    else:
      if nPos > oSample.start_marker and nPos <= oSample.length:
        oSample.end_marker = nPos
        self.alert('END MARKER: %d' % (nPos))
        return

    self.alert('%s OUT OF RANGE' % (psType.upper()))

  def on_marker_res_rx_value(self, psType, phParamCfg, pnRes):
    oSample = self.m_oDev.sample
    if oSample == None: return
    if pnRes == phParamCfg['nRes']: return

    phParamCfg['nRes'] = pnRes # 0, 1, 2
    aResName = ['COARSE', 'MEDIUM', 'FINE']
    self.alert('%s RESOLUTION: %s' % (psType.upper(), aResName[pnRes]))

    nPos = oSample.start_marker if psType == 'Start Marker' else oSample.end_marker

    sPosParam = '%s Pos' % (psType)
    if pnRes == 0:   # coarse
      nValue = int((float(nPos) / float(oSample.length)) * 127.0)
      self.tx_param_msg(sPosParam, nValue)

    elif pnRes == 1: # medium
      self.get_param_config(sPosParam)['nPos'] = nPos
      self.tx_param_msg(sPosParam, 64)

    elif pnRes == 2: # fine
      self.get_param_config(sPosParam)['nPos'] = nPos
      self.tx_param_msg(sPosParam, 64)

#=======================================================================
# Class: OriginalSimpler, Device: Simpler, Display: Simpler
#   param: "Sample Selector", orig: "Sample Selector", value: 0.000000, min: 0.000000, max: 127.000000
#   param: "Fade In", orig: "Fade In", value: 0.036840, min: 0.000000, max: 1.000000
#   param: "Fade Out", orig: "Fade Out", value: 0.036840, min: 0.000000, max: 1.000000
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Vol < Vel", orig: "Vol < Vel", value: 0.350000, min: 0.000000, max: 1.000000
#   param: "Volume", orig: "Volume", value: -12.000000, min: -36.000000, max: 36.000000
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "S Loop On", orig: "S Loop On" => [Off, On]
# Q param: "Snap", orig: "Snap" => [Off, On]
# +Retrigger
# Q param: "Trigger Mode", orig: "Trigger Mode" => [Trigger, Gate]
# +Reverse
# +Clear Slices
# +Crop
# +Warp
# +Warp Half
# +Warp As
# +Warp Double
# +Playback Mode
# + Gain
#   param: "S Start", orig: "S Start", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "S Loop Length", orig: "S Loop Length", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "S Length", orig: "S Length", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "S Loop Fade", orig: "S Loop Fade", value: 0.000000, min: 0.000000, max: 1.000000
# +Voices
# +Warp Mode
# Q param: "Fe On", orig: "Fe On" => [Off, On]
# Q param: "F On", orig: "F On" => [Off, On]
# Q param: "Filter Slope", orig: "Filter Slope" => [12 dB, 24 dB]
# Q param: "Filter Circuit - BP/NO/Morph", orig: "Filter Circuit - BP/NO/Morph" => [Clean, OSR]
#   param: "Fe < Env", orig: "Fe < Env", value: 0.000000, min: -72.000000, max: 72.000000
#   param: "Fe Attack", orig: "Fe Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fe Decay", orig: "Fe Decay", value: 0.581428, min: 0.000000, max: 1.000000
#   param: "Fe Sustain", orig: "Fe Sustain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fe Release", orig: "Fe Release", value: 0.355571, min: 0.000000, max: 1.000000
# Q param: "Fe Mode", orig: "Fe Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Fe Loop", orig: "Fe Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Fe Retrig", orig: "Fe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Fe A Slope", orig: "Fe A Slope", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Fe D Slope", orig: "Fe D Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Fe R Slope", orig: "Fe R Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Fe R < Vel", orig: "Fe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Fe Init", orig: "Fe Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fe Peak", orig: "Fe Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Fe End", orig: "Fe End", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Filter Type", orig: "Filter Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter Circuit - LP/HP", orig: "Filter Circuit - LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter Freq", orig: "Filter Freq", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Filter Res", orig: "Filter Res", value: 0.000000, min: 0.000000, max: 1.250000
#   param: "Filter Drive", orig: "Filter Drive", value: 0.000000, min: 0.000000, max: 24.000000
#   param: "Filter Morph", orig: "Filter Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filt < Vel", orig: "Filt < Vel", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filt < Key", orig: "Filt < Key", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "L Retrig", orig: "L Retrig" => [Off, On]
# Q param: "L On", orig: "L On" => [Off, On]
#   param: "L Attack", orig: "L Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L R < Key", orig: "L R < Key", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "L Offset", orig: "L Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "Vol < LFO", orig: "Vol < LFO", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pitch < LFO", orig: "Pitch < LFO", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pan < LFO", orig: "Pan < LFO", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filt < LFO", orig: "Filt < LFO", value: 0.000000, min: 0.000000, max: 24.000000
# Q param: "L Wave", orig: "L Wave" => [Sine, Square, Triangle, Saw Down, Saw Up, Random]
# Q param: "L Sync", orig: "L Sync" => [Free, Sync]
#   param: "L Rate", orig: "L Rate", value: 0.575188, min: 0.000000, max: 1.000000
#   param: "L Sync Rate", orig: "L Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "Ve Attack", orig: "Ve Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ve Decay", orig: "Ve Decay", value: 0.581428, min: 0.000000, max: 1.000000
#   param: "Ve Sustain", orig: "Ve Sustain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ve Release", orig: "Ve Release", value: 0.355571, min: 0.000000, max: 1.000000
# Q param: "Ve Mode", orig: "Ve Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Ve Loop", orig: "Ve Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Ve Retrig", orig: "Ve Retrig", value: 3.000000, min: 0.000000, max: 14.000000
# Q param: "Pe On", orig: "Pe On" => [Off, On]
#   param: "Pe < Env", orig: "Pe < Env", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Pe Attack", orig: "Pe Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pe Decay", orig: "Pe Decay", value: 0.581428, min: 0.000000, max: 1.000000
#   param: "Pe Sustain", orig: "Pe Sustain", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pe Release", orig: "Pe Release", value: 0.355571, min: 0.000000, max: 1.000000
# Q param: "Pe Mode", orig: "Pe Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Pe Loop", orig: "Pe Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Pe Retrig", orig: "Pe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Pe A Slope", orig: "Pe A Slope", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pe D Slope", orig: "Pe D Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Pe R Slope", orig: "Pe R Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Pe R < Vel", orig: "Pe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Pe Init", orig: "Pe Init", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pe Peak", orig: "Pe Peak", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Pe End", orig: "Pe End", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pan", orig: "Pan", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pan < Rnd", orig: "Pan < Rnd", value: 0.000000, min: 0.000000, max: 1.000000
# Q param: "Glide Mode", orig: "Glide Mode" => [Off, Portamento, Glide]
#   param: "Spread", orig: "Spread", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "Detune", orig: "Detune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "Glide Time", orig: "Glide Time", value: 0.539794, min: 0.000000, max: 1.000000

