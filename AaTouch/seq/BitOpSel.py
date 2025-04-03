from AaTouch.Base import Base

class BitOpSel(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lButOps   = ['DIV', 'MUL', 'CHOP2', 'CHOP3']
    self.m_nButSelOp = 1 # MUL by default
    self.m_lEncOps   = ['LEN', 'VEL', 'SHIFT', 'RESET']
    self.m_nEncSelOp = 2 # SHIFT by default
    self.connect()

    phObj['oBitOpSel'] = self

    self.activate()

  # ********************************************************

  def connect(self):
    self.reg_idx_cb('seq/bit/op_sel' , 4, self.on_op_sel)
    self.reg_idx_cb('seq/bit/enc_sel', 4, self.on_enc_sel)

  def disconnect(self):
    self.deactivate()

  # ********************************************************

  def activate(self):
    self.send_msg('/seq/bit/op_sel/%d'  % (self.m_nButSelOp), 1)
    self.send_msg('/seq/bit/enc_sel/%d' % (self.m_nEncSelOp), 1)

  def deactivate(self):
    self.send_msg('/seq/bit/op_sel/%d'  % (self.m_nButSelOp), 0)
    self.send_msg('/seq/bit/enc_sel/%d' % (self.m_nEncSelOp), 0)

  # ********************************************************

  def on_op_sel(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    if nValue < 0.5:
      if nIdx == self.m_nButSelOp:
        self.alert('OPERATION: %s' % (self.m_lButOps[nIdx]))
        self.send_msg(sAddr, 1) # prevent from turning off
      return

    if nIdx != self.m_nButSelOp:
      self.send_msg('/seq/bit/op_sel/%d' % (self.m_nButSelOp), 0)
      self.m_nButSelOp = nIdx
      self.alert('OPERATION: %s' % (self.m_lButOps[nIdx]))

  def on_enc_sel(self, plSegs, plMsg):
    sAddr  = plMsg[0]
    nIdx   = int(plSegs[4])
    nValue = int(plMsg[2])

    if nValue < 0.5:
      if nIdx == self.m_nEncSelOp:
        self.alert('OPERATION: %s' % (self.m_lEncOps[nIdx]))
        self.send_msg(sAddr, 1) # prevent from turning off
      return

    if nIdx == 3: # RESET
      self.send_msg(sAddr, 0) # prevent from turning on
      self.obj('oBitOp').enc_reset(self.m_lEncOps[self.m_nEncSelOp])
      self.alert('RESET: %s' % (self.m_lEncOps[self.m_nEncSelOp]))
      return

    if nIdx != self.m_nEncSelOp:
      self.send_msg('/seq/bit/enc_sel/%d' % (self.m_nEncSelOp), 0)
      self.m_nEncSelOp = nIdx
      self.alert('OPERATION: %s' % (self.m_lEncOps[nIdx]))

  # ********************************************************

  def get_but_sel_op(self):
    return self.m_lButOps[self.m_nButSelOp]

  def get_enc_sel_op(self):
    return self.m_lEncOps[self.m_nEncSelOp]

