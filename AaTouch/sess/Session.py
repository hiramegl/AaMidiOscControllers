import Live

from AaTouch.Base import Base

from .Zoom   import Zoom
from .Clips  import Clips
from .Sends  import Sends
from .Tracks import Tracks

class Session(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # mode change
    self.m_sGridMode  = 'CLIPS'         # 'CLIPS', 'SENDS'
    self.m_sTrackMode = 'BASIC'         # 'BASIC', 'EXTRA'
    self.m_sCellMode  = 'FIRE'          # 'SELECT', 'FIRE'
    self.m_sFireMode  = 'FIRE N FOLLOW' # 'ONLY FIRE', 'FIRE N FOLLOW'
    self.connect()

    phObj['oSess'] = self

    Zoom  (phCfg, phObj)
    Clips (phCfg, phObj)
    Sends (phCfg, phObj)
    Tracks(phCfg, phObj)

  # ********************************************************

  def connect(self):
    self.reg_idx_cb('session/mode', 2, self.on_mode)
    self.reg_idx_cb('session/fire', 2, self.on_fire)
    self.reg_idx_cb('session/faders', 4, self.on_faders)
    self.send_msg('/session/fire/0', 1)
    self.send_msg('/session/fire/1', 1)

  def disconnect(self):
    self.obj('oZoom'  ).disconnect()
    self.obj('oClips' ).disconnect()
    self.obj('oSends' ).disconnect()
    self.obj('oTracks').disconnect()

    self.send_msg('/session/mode/0', 0)
    self.send_msg('/session/mode/1', 0)
    self.send_msg('/session/fire/0', 0)
    self.send_msg('/session/fire/1', 0)

  # ********************************************************

  def on_mode(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    nValue = plMsg[2]

    if nIdx == 0: # grid mode toggle
      sGridMode = 'CLIPS' if nValue < 0.5 else 'SENDS'

      if self.m_sGridMode == 'CLIPS': # old mode 'CLIPS'
        self.obj('oClips').set_visible(False)
      elif self.m_sGridMode == 'SENDS': # old mode 'SENDS'
        self.obj('oClips').set_visible(True)

      self.m_sGridMode = sGridMode # new mode
      self.alert('GRID MODE: %s' % (sGridMode))

    else: # track mode toggle
      sTrackMode = 'BASIC' if nValue < 0.5 else 'EXTRA'

      if self.m_sTrackMode == 'BASIC': # old mode 'BASIC'
        self.obj('oTracks').set_cmd1_visible(False)
      elif self.m_sTrackMode == 'EXTRA': # old mode 'EXTRA'
        self.obj('oTracks').set_cmd1_visible(True)

      self.m_sTrackMode = sTrackMode # new mode
      self.alert('TRACK MODE: %s' % (sTrackMode))

  def on_fire(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    nValue = plMsg[2]

    if nIdx == 0: # clip fire mode toggle, Select Only or Fire
      self.m_sCellMode = 'SELECT' if nValue < 0.5 else 'FIRE'
      self.alert('CELL MODE: %s' % (self.m_sCellMode))

    else: # nIdx == 1 # fire mode toggle, Fire Only or Follow
      self.m_sFireMode = 'ONLY FIRE' if nValue < 0.5 else 'FIRE N FOLLOW'
      self.alert('FIRE MODE: %s' % (self.m_sFireMode))

  def on_faders(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])

    nTrackOffset = self.state().track_offset() + (nIdx * 8)
    if self.is_track_available(nTrackOffset) == False:
      self.alert('Unavailable track-span')

    oAaBcf = self.get_faders_or_none()
    if oAaBcf == None:
      self.alert('No BCF controller found!')
      return

    oAaBcf.move_to_track_offset(nTrackOffset)
    self.alert('New faders offset: %d' % (nTrackOffset))

  # ********************************************************

  def get_faders_or_none(self):
    lCtrlInsts = Live.Application.get_application().control_surfaces
    for oCtrlInst in lCtrlInsts:
      sCtrlName = oCtrlInst.__class__.__name__
      if sCtrlName == 'AaBcf':
        return oCtrlInst

    return None

  # ********************************************************

  def get_grid_mode(self):
    return self.m_sGridMode

  def get_cell_mode(self):
    return self.m_sCellMode

  def get_fire_mode(self):
    return self.m_sFireMode

