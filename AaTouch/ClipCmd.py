import Live

from AaTouch.Base import Base

class ClipCmd(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lClipCmd = ['CLIP/DEV', 'CLIP DUPL']
    self.m_bFollow  = self.song().view.follow_song
    if self.m_bFollow:
      self.send_msg('/sess/follow', 1)
    self.connect()

    phObj['oClipCmd'] = self

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'clip/cmd', 2, self.on_cmd)
    self.reg_cb('sess/follow', self.on_follow)

  def disconnect(self):
    if self.m_bFollow:
      self.send_msg('/sess/follow', 0)

  # ********************************************************

  def on_cmd(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    sCmd   = self.m_lClipCmd[nIdx]

    self.send_msg(sAddr, 0) # turn off button, is a command!
    if sCmd == 'CLIP/DEV':
      # available: Browser, Arranger, Session, Detail, Detail/Clip, Detail/DeviceChain
      oView = Live.Application.get_application().view
      oView.show_view ('Detail')
      oView.focus_view('Detail')
      if (oView.is_view_visible('Detail/Clip')):
        oView.show_view ('Detail/DeviceChain')
        oView.focus_view('Detail/DeviceChain')
      else:
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')

    elif sCmd == 'CLIP DUPL':
      nSelSceneIdxAbs = self.sel_scene_idx_abs()
      oScene          = self.get_scene(nSelSceneIdxAbs + 1)
      oSelTrack       = self.sel_track()
      oSelTrack.duplicate_clip_slot(nSelSceneIdxAbs)
      self.sel_scene(oScene)
      self.alert('> DUPLICATED CLIP at track "%s", scene: %d' %
        (oSelTrack.name, nSelSceneIdxAbs))

  def on_follow(self, plSegs, plMsg):
    nValue = plMsg[2]
    self.m_bFollow = (nValue > 0.5)
    self.song().view.follow_song = self.m_bFollow
    sCmd = 'FOLLOW ON' if nValue > 0.5 else 'FOLLOW OFF'
    self.alert(sCmd)

