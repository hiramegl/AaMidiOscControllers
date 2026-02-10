import Live

# MIDI Effects
from .devs.MidiPitcher           import MidiPitcher
from .devs.MidiVelocity          import MidiVelocity
from .devs.MidiArpeggiator       import MidiArpeggiator

# AUDIO Effects
from .devs.Vocoder               import Vocoder
from .devs.Overdrive             import Overdrive
from .devs.BeatRepeat            import BeatRepeat
from .devs.Compressor2           import Compressor2
from .devs.Resonator             import Resonator
from .devs.AutoPan               import AutoPan
from .devs.Echo                  import Echo
from .devs.EchoOut               import EchoOut
from .devs.Delay                 import Delay
from .devs.FilterDelay           import FilterDelay
from .devs.GrainDelay            import GrainDelay
from .devs.Chorus2               import Chorus2
from .devs.PhaserNew             import PhaserNew
from .devs.Transmute             import Transmute
from .devs.Reverb                import Reverb
from .devs.Eq8                   import Eq8
from .devs.FilterEQ3             import FilterEQ3
from .devs.Redux2                import Redux2
from .devs.VolumeStepper         import VolumeStepper

# Instruments
from .devs.DrumGroupDevice       import DrumGroupDevice
from .devs.InstrumentGroupDevice import InstrumentGroupDevice
from .devs.UltraAnalog           import UltraAnalog
from .devs.Collision             import Collision
from .devs.LoungeLizard          import LoungeLizard
from .devs.Operator              import Operator
from .devs.MultiSampler          import MultiSampler
from .devs.OriginalSimpler       import OriginalSimpler
from .devs.StringStudio          import StringStudio
from .devs.InstrumentVector      import InstrumentVector
from .devs.Drift                 import Drift
from .devs.InstrumentMeld        import InstrumentMeld

# MAX Instruments
from .devs.AaOsc                 import AaOsc

# Stub
from .devs.Stub                  import Stub

class Router():
  def __init__(self, phCfg, phObj):
    # refs
    self.m_hCfg = phCfg
    self.m_hObj = phObj

    # state
    self.m_hDevs      = {} # devices supported by this script
    self.m_hRoutes    = {} # devices routes
    self.m_lDevProcs  = [] # device processors for current track
    self.m_lSyncDevs  = [] # devices that have synchronous tasks
    self.m_nCurrBank  = 0  # current bank  to bind
    self.m_nCurrStrip = 0  # current strip to bind

    phObj['oRouter'] = self
    MidiPitcher          (phCfg, phObj)
    MidiVelocity         (phCfg, phObj)
    MidiArpeggiator      (phCfg, phObj)
    Vocoder              (phCfg, phObj)
    Overdrive            (phCfg, phObj)
    BeatRepeat           (phCfg, phObj)
    Compressor2          (phCfg, phObj)
    Resonator            (phCfg, phObj)
    AutoPan              (phCfg, phObj)
    Echo                 (phCfg, phObj)
    EchoOut              (phCfg, phObj)
    Delay                (phCfg, phObj)
    FilterDelay          (phCfg, phObj)
    GrainDelay           (phCfg, phObj)
    Chorus2              (phCfg, phObj)
    PhaserNew            (phCfg, phObj)
    Transmute            (phCfg, phObj)
    Reverb               (phCfg, phObj)
    Eq8                  (phCfg, phObj)
    FilterEQ3            (phCfg, phObj)
    Redux2               (phCfg, phObj)
    VolumeStepper        (phCfg, phObj)
    DrumGroupDevice      (phCfg, phObj)
    InstrumentGroupDevice(phCfg, phObj)
    UltraAnalog          (phCfg, phObj)
    Collision            (phCfg, phObj)
    LoungeLizard         (phCfg, phObj)
    Operator             (phCfg, phObj)
    MultiSampler         (phCfg, phObj)
    OriginalSimpler      (phCfg, phObj)
    StringStudio         (phCfg, phObj)
    InstrumentVector     (phCfg, phObj)
    Drift                (phCfg, phObj)
    InstrumentMeld       (phCfg, phObj)
    AaOsc                (phCfg, phObj)
    Stub                 (phCfg, phObj)
    self.log('-> Finished registering all devices')

  def reg(self, psClass, psName, poDev):
    self.m_hDevs['%s-%s' % (psClass, psName)] = poDev

  def add_sync_dev(self, poDev):
    if poDev in self.m_lSyncDevs:
      return # prevent from adding device more than once
    self.m_lSyncDevs.append(poDev)

  # ********************************************************

  def bind_track_devs(self, poTrack, plRootIds):
    if poTrack == None:
      self.log('-> No track to bind the router to')
      return

    sTrack = poTrack.name
    if len(poTrack.devices) == 0:
      self.log('-> Track "%s" has no devices' % (sTrack))
      return

    for oDev in poTrack.devices:
      sQualName  = '%s-%s' % (oDev.class_name, oDev.name)
      sQualAll   = '%s-x'  % (oDev.class_name)

      sName = None
      if sQualName in self.m_hDevs:
        sName = sQualName
      elif sQualAll in self.m_hDevs:
        sName = sQualAll

      if sName != None:
        self.add_routes_for_dev(sTrack, oDev, sName, plRootIds)
      else:
        if self.cfg('bUnknown'):
          self.dump_device(oDev)

  def add_routes_for_dev(self, psTrack, poDev, psDevName, plRootIds):
    oDevProc = self.m_hDevs[psDevName]
    nBanks   = oDevProc.get_banks()
    nStrips  = oDevProc.get_strips()

    if self.m_nCurrStrip + nStrips > self.cfg('nStrips'):
      nStubStrips = self.cfg('nStrips') - self.m_nCurrStrip
      if nStubStrips > 0:
        # use the 'Stub' device for ignored strips
        oStubDev = self.m_hDevs['Stub-x']
        self.dlog('=====> Binding Stub Processor, bank id: %d, start strip: %d, strips: %d' %
          (self.m_nCurrBank, self.m_nCurrStrip, nStubStrips))
        for nStripIdx in range(nStubStrips):
          for nRootId in plRootIds:
            tKey = (
              0xB0 | self.m_nCurrBank,
              nRootId + nStripIdx + self.m_nCurrStrip
            )
            self.m_hRoutes[tKey] = oStubDev
            self.dlog('    -> key: %02X % 3d' % (tKey[0], tKey[1]))
        oStubDev.add_offsets(self.m_nCurrBank, self.m_nCurrStrip, nStubStrips, plRootIds)
        if (oStubDev in self.m_lDevProcs) == False:
          self.m_lDevProcs.append(oStubDev)

      # advance to the next bank and reset strip index
      self.m_nCurrBank += 1
      self.m_nCurrStrip = 0

    if self.m_nCurrBank + nBanks > self.cfg('nBanks'):
      self.log('-> Run out of banks to bind!')
      return

    self.dlog('=====> Binding Device Processor "%s", banks: %d strips: %d' % (oDevProc.get_qual_name(), nBanks, nStrips))

    oDevProc.bind_dev(poDev, psTrack, psDevName)
    oDevProc.set_offsets(self.m_nCurrBank, self.m_nCurrStrip)
    self.m_lDevProcs.append(oDevProc)

    # create routes to use the Device Processor
    self.dlog('=====> Router: adding physical routes for "%s"' % (psDevName))
    for nBankIdx in range(nBanks):
      for nStripIdx in range(nStrips):
        self.dlog('-> Router: "%s", strip: %d' % (oDevProc.get_qual_name(), nStripIdx))
        for nRootId in plRootIds:
          tKey = (
            0xB0 |   (nBankIdx  + self.m_nCurrBank),
            nRootId + nStripIdx + self.m_nCurrStrip
          )
          self.m_hRoutes[tKey] = oDevProc
          self.dlog('-> Router: Physical route [0x%02X %3d] -> "%s"' % (tKey[0], tKey[1], oDevProc.get_qual_name()))

    if nBanks > 1:
      self.m_nCurrBank += nBanks # advance current bank
    self.m_nCurrStrip += nStrips # advance current strip

  def dump_device(self, poDev):
    sClass   = poDev.class_name
    sDevice  = poDev.name
    sDisplay = poDev.class_display_name
    self.log('========================================================================')
    self.log('> Class: %s, Device: %s, Display: %s' % (sClass, sDevice, sDisplay))

    #object_methods = [method_name for method_name in dir(poDev) if callable(getattr(poDev, method_name))]
    #for name in object_methods:
    #  self.log('----> Name: "%s"' % (name))

    # dump params
    aParams = poDev.parameters
    for oParam in aParams:
      sParam = oParam.name
      sOrig  = oParam.original_name
      if (oParam.is_quantized):
        aValues = []
        for oValue in oParam.value_items:
          aValues.append(str(oValue))
        self.log('> Q param: "%s", orig: "%s" => [%s]' % (sParam, sOrig, ', '.join(aValues)))
      else:
        tLog = (sParam, sOrig, oParam.value, oParam.min, oParam.max)
        self.log('>   param: "%s", orig: "%s", value: %f, min: %f, max: %f' % tLog)

    # dump chains
    if poDev.can_have_chains:
      for oChain in poDev.chains:
        self.dlog('------------------------------------------------------------------------')
        self.dlog('-> Chain "%s"' % (oChain.name))
        for oChainDev in oChain.devices:
          self.dlog('-> Chain Device "%s"' % (oChainDev.class_name))
          self.dump_device(oChainDev)

    # dump drum pad
    self.dlog('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    if poDev.can_have_drum_pads:
      for oDrumPad in poDev.drum_pads:
        if len(oDrumPad.chains) == 0: continue
        nNote = oDrumPad.note
        self.dlog('........................................................................')
        self.dlog('-> note: %s, chains: %d' % (str(nNote), len(oDrumPad.chains)))
        for oChain in oDrumPad.chains:
          self.dlog('-> Chain: %s' % (oChain.name))
          for oChainDev in oChain.devices:
            self.dlog('-> Chain Device "%s"' % (oChainDev.class_name))
            self.dump_device(oChainDev)

  def unbind_track_devs(self):
    self.m_hRoutes.clear()
    for oDevProc in self.m_lDevProcs:
      oDevProc.unbind_dev()
    self.m_lDevProcs.clear()
    self.m_lSyncDevs.clear()
    self.m_nCurrBank  = 0
    self.m_nCurrStrip = 0

  # ********************************************************

  def sync_track_devs(self, pnBankChn):
    if len(self.m_lDevProcs) == 0:
      self.log('-> Track has no devices, nothing to sync')
      return False # no devices to sync!

    self.dlog('-> Router: Syncing bank %d' % (pnBankChn))
    for oDevProc in self.m_lDevProcs:
      oDevProc.sync_dev(pnBankChn)
    return True # there were devices to sync

  # ********************************************************

  def route(self, ptKey, pnValue):
    if ptKey in self.m_hRoutes:
      self.m_hRoutes[ptKey].handle_rx_msg(ptKey[0] & 0x0F, ptKey[1], pnValue)
    else:
      self.log('-> Route not found for [0x%02X %3d] -> %d' % (ptKey[0], ptKey[1], pnValue))

  # ********************************************************

  def update_sync_devs(self):
    for oDev in self.m_lSyncDevs:
      oDev.update_sync_params()

  # ********************************************************

  def cfg(self, psKey):
    return self.m_hCfg[psKey]

  def obj(self, psKey):
    return self.m_hObj[psKey]

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def dlog(self, psMessage):
    if self.cfg('bDebug'):
      self.log(psMessage)

