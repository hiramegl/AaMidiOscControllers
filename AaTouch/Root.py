from .Base import Base

class Root(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    phObj['oRoot'] = self

    self.connect()

  # ********************************************************

  def connect(self):
    self.reg_cb('view_toggle', self.on_view_toggle)
    self.reg_cb('clip/focus' , self.on_focus)
    self.reg_cb('bring_sel'  , self.on_bring_sel)
    self.toggle_view(True) # seq visible

  # ********************************************************

  def on_view_toggle(self, plSegs, plMsg):
    if self.state().view_mode() == 'SESS':
      self.state().set_view_mode('SEQ')
      self.obj('oSeq').highlight_session()
      self.toggle_view(True) # seq visible

    else: # view mode == 'SEQ'
      self.state().set_view_mode('SESS')
      self.obj('oClips').highlight_session()
      self.toggle_view(False) # sess visible

  def toggle_view(self, pbSeqVisible):
    sValue = '-1' if pbSeqVisible else '1'
    self.send_msg(
      '/EDIT',
      ['sess_view', '{"css":"z-index:%s"}' % (sValue)])

  def on_focus(self, plSegs, plMsg):
    nColOff = self.sel_track_idx_abs()
    nRowOff = self.sel_scene_idx_abs()
    self.state().set_clip_offsets(nColOff, nRowOff)

  def on_bring_sel(self, plSegs, plMsg):
    nColOff = self.state().col_offset()
    nRowOff = self.state().row_offset()
    oTrack  = self.get_track(nColOff)
    oScene  = self.get_scene(nRowOff)
    self.sel_track(oTrack)
    self.sel_scene(oScene)

