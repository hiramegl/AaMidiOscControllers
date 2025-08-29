from .Base import Base

class Root(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    phObj['oRoot'] = self

    self.connect()

  # ********************************************************

  def connect(self):
    self.reg_cb('root_panel' , self.on_root)
    self.reg_cb('clip/focus', self.on_focus)

  # ********************************************************

  def on_root(self, plSegs, plMsg):
    nValue = plMsg[2] # 0 => Seq, 1 => Session

    if nValue == 0:
      self.state().set_view_mode('SEQ')
      self.obj('oSeq').highlight_session()
    else:
      self.state().set_view_mode('SESS')
      self.obj('oClips').highlight_session()

  def on_focus(self, plSegs, plMsg):
    nColOff = self.sel_track_idx_abs()
    nRowOff = self.sel_scene_idx_abs()
    self.state().set_clip_offsets(nColOff, nRowOff)

