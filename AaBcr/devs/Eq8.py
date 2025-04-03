import time

from .Dev import Dev

class Eq8(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | 1 Filter On A   | 2 Filter On A   | Adaptive Q   | +Sync Extra',
      #----------------------------------------------------------------------------------
      'Bank0 | nGR0Off | 1 Filter Type A | 2 Filter Type A'                             ,
      #----------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On       | Preset Prev     | +1 Auto Inc  | +2 Auto Inc',
      'Bank0 | nMB1Off | Preset Save     | Preset Next     | +1 Auto Dec  | +2 Auto Dec',
      #----------------------------------------------------------------------------------
      'Bank0 | nMR0Off | 1 Frequency A   | 2 Frequency A   | +Center Freq | +Auto Time' ,
      'Bank0 | nMR1Off | 1 Gain A        | 2 Gain A        | +Bandwidth   | Scale'      ,
      'Bank0 | nMR2Off | 1 Resonance A   | 2 Resonance A   | +Resonance   | Output Gain',
    ]
    self.m_bBusy   = False # flag to prevent changing synchronous parameters
    self.m_lAutoOn = []
    self.reg('Eq8')
    self.parse_cfg()

  def customize_param(self, phParamCfg):
    sName = phParamCfg['sName']
    if (sName == 'Center Freq' or
      sName  == 'Resonance'):
      phParamCfg['nValue'] = 0.5
    elif sName  == 'Bandwidth':
      phParamCfg['nValue'] = 0.6
    elif sName  == 'Auto Time':
      phParamCfg['nValue'] = 10 # bars
    else:
      # All auto params set to OFF when starting
      phParamCfg['nStart'] = 0 # start time
      phParamCfg['nDelta'] = 0 # delta time
      phParamCfg['nTgt'  ] = 0 # target value
      phParamCfg['sCmp'  ] = 0 # limit comparison: ">=", "<="

  def sync_dev(self, pnBankChn):
    Dev.sync_dev(self, pnBankChn)
    self.add_to_sync_devs() # register in auto params

  def get_extra_param_tx_value(self, phParamCfg):
    sName = phParamCfg['sName']
    if (sName == 'Center Freq' or
      sName  == 'Bandwidth'    or
      sName  == 'Resonance'):
      self.update_freq_values()
      return int(phParamCfg['nValue'] * 127.0)
    elif sName == 'Auto Time':
      return int(phParamCfg['nValue'])
    else:
      return 127 if sName in self.m_lAutoOn else 0

  def handle_rx_msg_extra_cmd(self, phParamCfg, pnValue):
    sName = phParamCfg['sName']
    if sName == 'Center Freq':
      phParamCfg['nValue'] = float(pnValue) / 127.0
      self.update_freq_values()
    elif sName == 'Bandwidth':
      phParamCfg['nValue'] = float(pnValue) / 127.0
      self.update_freq_values()
    elif sName == 'Resonance':
      nValue = float(pnValue) / 127.0
      phParamCfg['nValue'] = nValue
      self.set_param_value('1 Resonance A', nValue)
      self.set_param_value('2 Resonance A', nValue)
    elif sName == 'Sync Extra':
      nFreqLo = self.get_param_value('1 Frequency A')
      nFreqHi = self.get_param_value('2 Frequency A')
      nResnLo = self.get_param_value('1 Resonance A')
      nResnHi = self.get_param_value('2 Resonance A')

      nBandwidth = nFreqHi - nFreqLo
      nCenterFrq = (nBandwidth / 2.0) + nFreqLo
      nResonance = (nResnLo + nResnHi) / 2.0

      hBandwidth = self.get_param_config('Bandwidth')
      hBandwidth['nValue'] = nBandwidth
      hCenterFrq = self.get_param_config('Center Freq')
      hCenterFrq['nValue'] = nCenterFrq
      hResonance = self.get_param_config('Resonance')
      hResonance['nValue'] = nResonance

      self.obj('oComm').send_bundle([
        self.to_physical_msg(hBandwidth['tAddr'], nBandwidth * 127.0),
        self.to_physical_msg(hCenterFrq['tAddr'], nCenterFrq * 127.0),
        self.to_physical_msg(hResonance['tAddr'], nResonance * 127.0),
      ])
    elif sName == 'Auto Time':
      phParamCfg['nValue'] = pnValue
      self.update_auto_delta()
      self.alert('> EQ8 AUTO-VEL: %d [bars]' % (pnValue))
    else:
      if pnValue == 127:
        phParamCfg['nStart'] = time.time()
        self.m_lAutoOn.append(sName)
        self.dlog('-> Adding "%s" to auto params' % (sName))

        # if the opposite parameter is on then turn it off
        hOpposites = {
          '1 Auto Inc' : '1 Auto Dec',
          '1 Auto Dec' : '1 Auto Inc',
          '2 Auto Inc' : '2 Auto Dec',
          '2 Auto Dec' : '2 Auto Inc',
        }
        sOpposite = hOpposites[sName]
        if sOpposite in self.m_lAutoOn:
          self.m_lAutoOn.remove(sOpposite)
          self.tx_param_msg(sOpposite, 0) # Turn it Off

        self.update_auto_delta()
      else:
        self.m_lAutoOn.remove(sName)
        self.dlog('-> Removing "%s" from auto params' % (sName))

  def update_freq_values(self):
    nCenterFreq = self.get_param_config('Center Freq')['nValue']
    nBandwidth  = self.get_param_config('Bandwidth'  )['nValue']
    nHalfwidth  = nBandwidth / 2.0
    nFreqLo = nCenterFreq - nHalfwidth
    nFreqHi = nCenterFreq + nHalfwidth
    nFreqLo = 0.0 if nFreqLo < 0.0 else nFreqLo
    nFreqHi = 1.0 if nFreqHi > 1.0 else nFreqHi
    self.set_param_value('1 Frequency A', nFreqLo)
    self.set_param_value('2 Frequency A', nFreqHi)

  def update_auto_delta(self):
    self.m_bBusy = True

    self.dlog('-> Auto updating delta ...')
    hAutoTime = self.get_param_config('Auto Time')
    nAutoTime = hAutoTime['nValue']
    nAutoTime = 0.5 if nAutoTime == 0 else nAutoTime

    nTempo    = self.song().tempo     # in BPM
    nBarSpan  = (60.0 / nTempo) * 4.0 # bar span  [in seconds]
    nTimeSpan = nAutoTime * nBarSpan  # time span [in seconds]
    self.dlog('-> tempo: %3.2f [BPM], timespan: %3.2f [sec]' % (nTempo, nTimeSpan))

    for sParam in self.m_lAutoOn:
      if sParam == '1 Auto Inc':
        nCur = self.get_param_value('1 Frequency A')
        nTgt = self.get_param_value('2 Frequency A')
        sCmp = '<=' # less or equal than target
        sCmd = 'LOW FREQ INC'
      elif sParam == '1 Auto Dec':
        nCur = self.get_param_value('1 Frequency A')
        nTgt = 0.0
        sCmp = '>=' # greater or equal than target
        sCmd = 'LOW FREQ DEC'
      elif sParam == '2 Auto Inc':
        nCur = self.get_param_value('2 Frequency A')
        nTgt = 1.0
        sCmp = '<=' # less or equal than target
        sCmd = 'HIGH FREQ INC'
      elif sParam == '2 Auto Dec':
        nCur = self.get_param_value('2 Frequency A')
        nTgt = self.get_param_value('1 Frequency A')
        sCmp = '>=' # greater or equal than target
        sCmd = 'HIGH FREQ DEC'

      hAuto = self.get_param_config(sParam)
      # divide with 10.0 since update executes every 100 ms (~ish)
      nDelta = ((nTgt - nCur) / nTimeSpan) / 10.0
      hAuto['nDelta'] = nDelta
      hAuto['nTgt']   = nTgt
      hAuto['sCmp']   = sCmp

      self.dlog ('> AUTO %s (%3.2f -> %3.2f) in %3.2f [s] => %3.1f [bars]' % (sCmd, nCur, nTgt, nTimeSpan, nAutoTime))
      self.alert('> AUTO %s (%3.2f -> %3.2f) in %3.2f [s] => %3.1f [bars]' % (sCmd, nCur, nTgt, nTimeSpan, nAutoTime))

    self.m_bBusy = False

  def update_sync_params(self):
    if (self.m_bBusy == True):
      return # busy updating delta

    nAutoOn = len(self.m_lAutoOn)
    if nAutoOn == 0:
      return # no auto param is On, nothing else to do here


    # check case when freq 1 is increased and freq 2 is decreased
    if '1 Auto Inc' in self.m_lAutoOn and '2 Auto Dec' in self.m_lAutoOn:
      nFreqLo = self.get_param_value('1 Frequency A')
      nFreqHi = self.get_param_value('2 Frequency A')

      if nFreqHi - nFreqLo <= 0.005:
        # stop both frequencies
        self.tx_param_msg(self.m_lAutoOn[0], 0)
        self.tx_param_msg(self.m_lAutoOn[1], 0)
        self.m_lAutoOn.clear()
        return

    lAutoOn = self.m_lAutoOn[:] # creates a copy to iterate
    for sAuto in lAutoOn:
      hAuto = self.get_param_config(sAuto)
      sAuto = hAuto['sName']
      self.dlog('-> Auto param: %s' % (hAuto['sName']))

      if sAuto in ['1 Auto Inc', '1 Auto Dec']:
        sParam = '1 Frequency A'
      else:
        sParam = '2 Frequency A'

      hParam = self.get_param_config(sParam)
      nCur   = hParam['oParam'].value
      nTgt   = hAuto['nTgt']
      nDelta = hAuto['nDelta']
      sCmp   = hAuto['sCmp']
      nValue = nCur + nDelta

      self.dlog('-> "%s", Curr: %3.2f, Tgt: %3.2f, nDelta: %1.5f, nValue: %3.2f' % (sParam, nCur, nTgt, nDelta, nValue))

      if sCmp == '<=':
        bCmp = (nValue <= nTgt)
      else:
        bCmp = (nValue >= nTgt)

      if bCmp: # comparison = true -> limit not reached!
        self.dlog('-> Setting param value: %3.2f' % (nValue))
        self.set_param_value(sParam, nValue)
      else:
        self.dlog('-> Stopping autoupdate, param value: %3.2f' % (nTgt))
        # parameter has reached the limit!
        self.set_param_value(sParam, nTgt)
        self.tx_param_msg(sAuto, 0) # turn off auto button
        self.m_lAutoOn.remove(sAuto)
        nTimeSpan = time.time() - hAuto['nStart']
        self.alert('Eq8: "%s" done in %3.2f [sec]' % (sAuto, nTimeSpan))

#-----------------------------------------------------------------------
# Class: Eq8, Device: EQ Eight, Display: EQ Eight
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Adaptive Q", orig: "Adaptive Q" => [Off, On]
#   param: "Scale", orig: "Scale", value: 1.000000, min: -2.000000, max: 2.000000
#   param: "Output Gain", orig: "Output Gain", value: 0.000000, min: -12.000000, max: 12.000000
# Q param: "1 Filter On A", orig: "1 Filter On A" => [Off, On]
# Q param: "1 Filter Type A", orig: "1 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "1 Frequency A", orig: "1 Frequency A", value: 0.200000, min: 0.000000, max: 1.000000
#   param: "1 Gain A", orig: "1 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "1 Resonance A", orig: "1 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "2 Filter On A", orig: "2 Filter On A" => [Off, On]
# Q param: "2 Filter Type A", orig: "2 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "2 Frequency A", orig: "2 Frequency A", value: 0.800000, min: 0.000000, max: 1.000000
#   param: "2 Gain A", orig: "2 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "2 Resonance A", orig: "2 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "1 Filter On B", orig: "1 Filter On B" => [Off, On]
# Q param: "1 Filter Type B", orig: "1 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "1 Frequency B", orig: "1 Frequency B", value: 0.180127, min: 0.000000, max: 1.000000
#   param: "1 Gain B", orig: "1 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "1 Resonance B", orig: "1 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "2 Filter On B", orig: "2 Filter On B" => [Off, On]
# Q param: "2 Filter Type B", orig: "2 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "2 Frequency B", orig: "2 Frequency B", value: 0.389248, min: 0.000000, max: 1.000000
#   param: "2 Gain B", orig: "2 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "2 Resonance B", orig: "2 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "3 Filter On A", orig: "3 Filter On A" => [Off, On]
# Q param: "3 Filter Type A", orig: "3 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "3 Frequency A", orig: "3 Frequency A", value: 0.598368, min: 0.000000, max: 1.000000
#   param: "3 Gain A", orig: "3 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "3 Resonance A", orig: "3 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "3 Filter On B", orig: "3 Filter On B" => [Off, On]
# Q param: "3 Filter Type B", orig: "3 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "3 Frequency B", orig: "3 Frequency B", value: 0.299184, min: 0.000000, max: 1.000000
#   param: "3 Gain B", orig: "3 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "3 Resonance B", orig: "3 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "4 Filter On A", orig: "4 Filter On A" => [Off, On]
# Q param: "4 Filter Type A", orig: "4 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "4 Frequency A", orig: "4 Frequency A", value: 0.807489, min: 0.000000, max: 1.000000
#   param: "4 Gain A", orig: "4 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "4 Resonance A", orig: "4 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "4 Filter On B", orig: "4 Filter On B" => [Off, On]
# Q param: "4 Filter Type B", orig: "4 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "4 Frequency B", orig: "4 Frequency B", value: 0.508305, min: 0.000000, max: 1.000000
#   param: "4 Gain B", orig: "4 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "4 Resonance B", orig: "4 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "5 Filter On A", orig: "5 Filter On A" => [Off, On]
# Q param: "5 Filter Type A", orig: "5 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "5 Frequency A", orig: "5 Frequency A", value: 0.299184, min: 0.000000, max: 1.000000
#   param: "5 Gain A", orig: "5 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "5 Resonance A", orig: "5 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "5 Filter On B", orig: "5 Filter On B" => [Off, On]
# Q param: "5 Filter Type B", orig: "5 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "5 Frequency B", orig: "5 Frequency B", value: 0.688432, min: 0.000000, max: 1.000000
#   param: "5 Gain B", orig: "5 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "5 Resonance B", orig: "5 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "6 Filter On A", orig: "6 Filter On A" => [Off, On]
# Q param: "6 Filter Type A", orig: "6 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "6 Frequency A", orig: "6 Frequency A", value: 0.897553, min: 0.000000, max: 1.000000
#   param: "6 Gain A", orig: "6 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "6 Resonance A", orig: "6 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "6 Filter On B", orig: "6 Filter On B" => [Off, On]
# Q param: "6 Filter Type B", orig: "6 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "6 Frequency B", orig: "6 Frequency B", value: 0.897553, min: 0.000000, max: 1.000000
#   param: "6 Gain B", orig: "6 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "6 Resonance B", orig: "6 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "7 Filter On A", orig: "7 Filter On A" => [Off, On]
# Q param: "7 Filter Type A", orig: "7 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "7 Frequency A", orig: "7 Frequency A", value: 0.807489, min: 0.000000, max: 1.000000
#   param: "7 Gain A", orig: "7 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "7 Resonance A", orig: "7 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "7 Filter On B", orig: "7 Filter On B" => [Off, On]
# Q param: "7 Filter Type B", orig: "7 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "7 Frequency B", orig: "7 Frequency B", value: 0.807489, min: 0.000000, max: 1.000000
#   param: "7 Gain B", orig: "7 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "7 Resonance B", orig: "7 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "8 Filter On A", orig: "8 Filter On A" => [Off, On]
# Q param: "8 Filter Type A", orig: "8 Filter Type A" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "8 Frequency A", orig: "8 Frequency A", value: 0.973926, min: 0.000000, max: 1.000000
#   param: "8 Gain A", orig: "8 Gain A", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "8 Resonance A", orig: "8 Resonance A", value: 0.376666, min: 0.000000, max: 1.000000
# Q param: "8 Filter On B", orig: "8 Filter On B" => [Off, On]
# Q param: "8 Filter Type B", orig: "8 Filter Type B" => [High Pass 48dB, High Pass 12dB, Low Shelf, Bell, Notch, High Shelf, Low Pass 12dB, Low Pass 48dB]
#   param: "8 Frequency B", orig: "8 Frequency B", value: 0.973926, min: 0.000000, max: 1.000000
#   param: "8 Gain B", orig: "8 Gain B", value: 0.000000, min: -15.000000, max: 15.000000
#   param: "8 Resonance B", orig: "8 Resonance B", value: 0.376666, min: 0.000000, max: 1.000000
