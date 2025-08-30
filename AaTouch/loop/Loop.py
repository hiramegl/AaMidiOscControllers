import math
import Live

from AaTouch.Base import Base

from .Roll import Roll

class Loop(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    # state
    self.m_lLoopLen = ['1', '2', '4', '8', '16', '32']
    self.m_lLoopExt = [
      'LOOP TOGGLE', 'LOOP DUPL', 'LOOP/ENV',
    ]
    self.m_bLpEnvToggle = True
    self.connect()
    self.update()

    phObj['oLoop'] = self

    Roll(phCfg, phObj)

  # ********************************************************

  def connect(self):
    self.comm().reg_indexed_rx_cb(
      'loop/len', 6, self.on_len)
    self.comm().reg_indexed_rx_cb(
      'loop/cmd/sta', 2, self.on_cmd)
    self.comm().reg_indexed_rx_cb(
      'loop/cmd/mid', 2, self.on_cmd)
    self.comm().reg_indexed_rx_cb(
      'loop/cmd/end', 2, self.on_cmd)
    self.comm().reg_indexed_rx_cb(
      'loop/ext', 3, self.on_ext)
    self.send_msg(
      '/EDIT',
      ['loop/len/2', '{"colorStroke":"#ffffff","lineWidth":5}'])

  def disconnect(self):
    self.send_msg('/loop/ext/0', 0) # loop-toggle
    self.obj('oRoll').disconnect()
    self.send_msg(
      '/EDIT',
      ['loop/len/2', '{"colorStroke":"","lineWidth":1}'])

  # ********************************************************

  def update(self):
    oClip = self.state().get_clip_or_none()
    if oClip == None:
      nValue = 0
    else:
      nValue = 1 if oClip.looping else 0
    self.send_msg('/loop/ext/0', nValue) # loop-toggle

  # ********************************************************

  def on_len(self, plSegs, plMsg):
    oClip = self.state().get_clip_or_none()
    if oClip == None: return

    self.obj('oRoll').toggle_off()
    nIdx = int(plSegs[3])
    sCmd = self.m_lLoopLen[nIdx]
    nLen = float(sCmd)

    nPlayPos  = oClip.playing_position
    nCurrBar  = (math.floor(math.floor(nPlayPos)/ 4.0)) * 4.0
    nCurrBeat = math.floor(nPlayPos)
    nNewStart = nCurrBar

    if nLen < 4.0:
      # when using beat loop (1 or 2 beats)
      # set the start offset to current beat
      nNewStart += (nCurrBeat - nCurrBar)
    nNewEnd = nNewStart + nLen
    #self.log('Play pos: %.5f, curr bar: %.1f, curr beat: %.1f, start: %.5f, end: %.5f' %
    #  (nPlayPos, nCurrBar, nCurrBeat, nNewStart, nNewEnd))

    oClip.looping = True

    nOldStart = oClip.loop_start
    nOldEnd   = oClip.loop_end

    if nNewStart >= nOldEnd:
      oClip.loop_end   = nNewEnd
      oClip.loop_start = nNewStart
    else:
      oClip.loop_start = nNewStart
      oClip.loop_end   = nNewEnd

    oClip.position = nNewStart

    self.send_msg('/loop/ext/0', 1) # loop-toggle ON
    self.alert('LOOP LEN: %s BEATS, [%.2f, .%2f]' %
      (sCmd, nNewStart, nNewEnd))

  def on_cmd(self, plSegs, plMsg):
    oClip = self.state().get_clip_or_none()
    if oClip == None: return

    self.obj('oRoll').toggle_off()
    sType =     plSegs[3]
    nIdx  = int(plSegs[4])

    bLooping = oClip.looping
    if bLooping == False: return

    nLoopStart = oClip.loop_start
    nLoopEnd   = oClip.loop_end
    nLoopLen   = nLoopEnd - nLoopStart

    if   sType == 'sta':
      if nIdx == 0:
        oClip.loop_start = nLoopStart + (nLoopLen / 2.0)
      else:
        if nLoopStart <= 0.0: return
        oClip.loop_start = nLoopStart - nLoopLen

    elif sType == 'mid':
      if nIdx == 0:
        oClip.loop_start = nLoopStart + (nLoopLen / 4.0)
        oClip.loop_end   = nLoopEnd   - (nLoopLen / 4.0)
      else:
        if nLoopStart <= 0.0: return
        oClip.loop_start = nLoopStart - (nLoopLen / 2.0)
        oClip.loop_end   = nLoopEnd   + (nLoopLen / 2.0)

    elif sType == 'end':
      if nIdx == 0:
        oClip.loop_end = nLoopEnd - (nLoopLen / 2.0)
      else:
        oClip.loop_end   = nLoopEnd + nLoopLen
        # update end marker on loop extension (if necessary)
        if oClip.end_marker < oClip.loop_end:
          oClip.end_marker = oClip.loop_end

  def on_ext(self, plSegs, plMsg):
    nIdx   = int(plSegs[3])
    sAddr  = plMsg[0]
    nValue = plMsg[2]
    sCmd   = self.m_lLoopExt[nIdx]
    oClip  = self.state().get_clip_or_none()

    if sCmd == 'LOOP TOGGLE':
      if nValue < 0.5:
        self.obj('oRoll').toggle_off()
        if oClip != None:
          oClip.looping = False
          self.alert('LOOP OFF')
        else:
          self.alert('NO CLIP, LOOP unavailable')

      else:
        if oClip != None:
          oClip.looping = True
          self.alert('LOOP ON')
        else:
          self.alert('NO CLIP, LOOP unavailable')
      self.obj('oSelected').update_warp()

    elif sCmd == 'LOOP DUPL':
      self.send_msg(sAddr, 0) # turn off, is a command!
      oClip = self.state().get_midi_clip_or_none()
      if oClip != None:
        oClip.duplicate_loop()
        self.alert('MIDI LOOP DUPLICATED')
      else:
        self.alert('NO MIDI CLIP. Loop duplicated unavailable')

    elif sCmd == 'LOOP/ENV':
      self.send_msg(sAddr, 0) # turn off, is a command!
      oView = Live.Application.get_application().view
      oView.show_view('Detail')
      oView.focus_view('Detail')
      oView.show_view('Detail/Clip')
      oView.focus_view('Detail/Clip')
      if self.m_bLpEnvToggle:
        oClip.view.hide_envelope()
        oClip.view.show_loop()
        self.alert('SHOWING LOOP')
      else:
        oClip.view.show_envelope()
        self.alert('SHOWING ENVELOPE')
      self.m_bLpEnvToggle = not self.m_bLpEnvToggle

  # ********************************************************

  def toggle_loop(self, pnValue):
    self.send_msg('/loop/ext/0', pnValue) # loop-toggle

