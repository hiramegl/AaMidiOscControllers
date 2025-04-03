from .Base import Base

class Shift(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lAmounts = [
      '1 bit', '2 bit' , '1 beat',
      '1 bar', '2 bars', '4 bars']
    self.m_lValues = [
       0.25, 0.5,  1,
       4   ,   8, 16]
    self.m_nAmountIdx = 3 # 1 bar (4 beats) (default)
    self.connect()

    phObj['oShift'] = self

  # ********************************************************

  def connect(self):
    self.send_msg('/shift/amount/%d' % (self.m_nAmountIdx), 1.0)
    self.send_msg(
      '/EDIT',
      ['shift/amount/3', '{"colorStroke":"#ffffff","lineWidth":5}'])

    self.reg_idx_cb('shift/amount', 6, self.on_shift_amount)
    self.reg_idx_cb('shift/sh/dir', 2, self.on_shift_dir) # loop shift
    self.reg_idx_cb('shift/ls/dir', 2, self.on_shift_dir) # loop start
    self.reg_idx_cb('shift/le/dir', 2, self.on_shift_dir) # loop end
    self.reg_idx_cb('shift/cs/dir', 2, self.on_shift_dir) # clip start
    self.reg_idx_cb('shift/ce/dir', 2, self.on_shift_dir) # clip end

  def disconnect(self):
    self.send_msg('/shift/amount/%d' % (self.m_nAmountIdx), 0.0)
    self.send_msg(
      '/EDIT',
      ['shift/amount/3', '{"colorStroke":"","lineWidth":1}'])

  # ********************************************************

  def on_shift_amount(self, plSegs, plMsg):
    nIdx = int(plSegs[3])
    if self.m_nAmountIdx == nIdx:
      self.send_msg('/shift/amount/%d' % (self.m_nAmountIdx), 1.0)
    else:
      self.send_msg('/shift/amount/%d' % (self.m_nAmountIdx), 0.0)
      self.m_nAmountIdx = nIdx
    self.alert('Shift Amount: %s' % (self.m_lAmounts[nIdx]))

  def on_shift_dir(self, plSegs, plMsg):
    oClip = self.state().get_clip_or_none()
    if oClip == None: return

    sType  =     plSegs[2]
    nIdx   = int(plSegs[4])
    nFact  = -1.0 if nIdx == 0 else +1.0
    nValue = self.m_lValues[self.m_nAmountIdx]

    if   sType == 'sh':
      if nFact < 0: # shift to left
        if oClip.loop_start - nValue < 0.0:
          self.alert('Error: Loop Start should be > 0')
          return
        # update start first
        oClip.loop_start -= nValue
        oClip.loop_end   -= nValue
      else:         # shift to right
        if oClip.loop_end + nValue > oClip.end_marker:
          self.alert('Error: Loop End should be < Clip End')
          return
        # update end first
        oClip.loop_end   += nValue
        oClip.loop_start += nValue

    elif sType == 'ls':
      if nFact < 0: # shift to left
        if oClip.loop_start - nValue < 0.0:
          self.alert('Error: Loop Start should be > 0')
          return
      else:         # shift to right
        if oClip.loop_start + nValue >= oClip.end_marker:
          self.alert('Error: Loop Start should be < Clip End')
          return
        if oClip.loop_start + nValue >= oClip.loop_end:
          self.alert('Error: Loop Start should be < Loop End')
          return
      oClip.loop_start += (nFact * nValue)

    elif sType == 'le':
      if nFact < 0: # shift to left
        if oClip.loop_end - nValue <= 0.0:
          self.alert('Error: Loop Start should be > 0')
          return
        if oClip.loop_end - nValue <= oClip.loop_start:
          self.alert('Error: Loop End should be > Loop Start')
          return
      else:         # shift to right
        if oClip.loop_end + nValue > oClip.end_marker:
          self.alert('Error: Loop End should be < Clip End')
          return
      oClip.loop_end += (nFact * nValue)

    if sType == 'cs':
      if nFact < 0: # shift to left
        if oClip.start_marker - nValue < 0.0:
          self.alert('Error: Clip Start should be > 0')
          return
      else:         # shift to right
        if oClip.start_marker + nValue >= oClip.end_marker:
          self.alert('Error: Clip Start should be < Clip End')
          return
        if oClip.start_marker + nValue >= oClip.loop_end:
          self.alert('Error: Clip Start should be < Loop End')
          return
      oClip.start_marker += (nFact * nValue)

    elif sType == 'ce':
      if nFact < 0: # shift to left
        if oClip.end_marker - nValue <= oClip.start_marker:
          self.alert('Error: Clip End should be > Clip Start')
          return
      oClip.end_marker += (nFact * nValue)

