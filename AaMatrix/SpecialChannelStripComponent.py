import time
import Live

from _Framework.ChannelStripComponent import ChannelStripComponent
from .ConfigurableButtonElement       import ConfigurableButtonElement

def release_control(control):
  if control != None:
    control.release_parameter()

class SpecialChannelStripComponent(ChannelStripComponent):
  empty_color = 'Unav.Off'

  def __init__(self):
    ChannelStripComponent.__init__(self)
    self.m_oStopControl  = None
    self.m_oInputControl = None
    self.m_oDeckControl  = None
    self.m_oSendsControl = None

    self.m_oSend1Button  = None
    self.m_oSend2Button  = None
    self.m_oSend3Button  = None
    self.m_oSend4Button  = None
    self.m_oSend5Button  = None
    self.m_oSend6Button  = None
    self.m_oSend7Button  = None
    self.m_oSend8Button  = None

    def make_control_slot(name):
      return self.register_slot(None, getattr(self, u'_%s_value' % name), u'value')

    self._stop_button_slot  = make_control_slot(u'stop')
    self._input_button_slot = make_control_slot(u'input')
    self._deck_button_slot  = make_control_slot(u'deck')
    self._sends_button_slot = make_control_slot(u'sends')

  def disconnect(self):
    oTrack = self.get_track_or_none()

    # remove track parameters listeners
    if oTrack != None:
      oMixDev = oTrack.mixer_device
      lSends  = oMixDev.sends
      if len(lSends) > 0 and lSends[0].value_has_listener(self._on_send1_changed):
        lSends[0].remove_value_listener(self._on_send1_changed)
      if len(lSends) > 1 and lSends[1].value_has_listener(self._on_send2_changed):
        lSends[1].remove_value_listener(self._on_send2_changed)
      if len(lSends) > 2 and lSends[2].value_has_listener(self._on_send3_changed):
        lSends[2].remove_value_listener(self._on_send3_changed)
      if len(lSends) > 3 and lSends[3].value_has_listener(self._on_send4_changed):
        lSends[3].remove_value_listener(self._on_send4_changed)
      if len(lSends) > 4 and lSends[4].value_has_listener(self._on_send5_changed):
        lSends[4].remove_value_listener(self._on_send5_changed)
      if len(lSends) > 5 and lSends[5].value_has_listener(self._on_send6_changed):
        lSends[5].remove_value_listener(self._on_send6_changed)
      if len(lSends) > 6 and lSends[6].value_has_listener(self._on_send7_changed):
        lSends[6].remove_value_listener(self._on_send7_changed)
      if len(lSends) > 7 and lSends[7].value_has_listener(self._on_send8_changed):
        lSends[7].remove_value_listener(self._on_send8_changed)

    # remove buttons listeners
    if self.m_oSend1Button != None:
      self.m_oSend1Button.remove_value_listener(self._on_send1_value)
      self.m_oSend1Button = None
    if self.m_oSend2Button != None:
      self.m_oSend2Button.remove_value_listener(self._on_send2_value)
      self.m_oSend2Button = None
    if self.m_oSend3Button != None:
      self.m_oSend3Button.remove_value_listener(self._on_send3_value)
      self.m_oSend3Button = None
    if self.m_oSend4Button != None:
      self.m_oSend4Button.remove_value_listener(self._on_send4_value)
      self.m_oSend4Button = None
    if self.m_oSend5Button != None:
      self.m_oSend5Button.remove_value_listener(self._on_send5_value)
      self.m_oSend5Button = None
    if self.m_oSend6Button != None:
      self.m_oSend6Button.remove_value_listener(self._on_send6_value)
      self.m_oSend6Button = None
    if self.m_oSend7Button != None:
      self.m_oSend7Button.remove_value_listener(self._on_send7_value)
      self.m_oSend7Button = None
    if self.m_oSend8Button != None:
      self.m_oSend8Button.remove_value_listener(self._on_send8_value)
      self.m_oSend8Button = None
    ChannelStripComponent.disconnect(self)

  def set_track(self, poTrack):
    assert ((poTrack == None) or isinstance(poTrack, Live.Track.Track))
    if (poTrack != self._track):
      oTrack = self.get_track_or_none()
      if oTrack != None: # it has to be a track not a return!
        oMixDev = self._track.mixer_device
        lSends  = oMixDev.sends
        if len(lSends) > 0 and lSends[0].value_has_listener(self._on_send1_changed):
          lSends[0].remove_value_listener(self._on_send1_changed)
        if len(lSends) > 1 and lSends[1].value_has_listener(self._on_send2_changed):
          lSends[1].remove_value_listener(self._on_send2_changed)
        if len(lSends) > 2 and lSends[2].value_has_listener(self._on_send3_changed):
          lSends[2].remove_value_listener(self._on_send3_changed)
        if len(lSends) > 3 and lSends[3].value_has_listener(self._on_send4_changed):
          lSends[3].remove_value_listener(self._on_send4_changed)
        if len(lSends) > 4 and lSends[4].value_has_listener(self._on_send5_changed):
          lSends[4].remove_value_listener(self._on_send5_changed)
        if len(lSends) > 5 and lSends[5].value_has_listener(self._on_send6_changed):
          lSends[5].remove_value_listener(self._on_send6_changed)
        if len(lSends) > 6 and lSends[6].value_has_listener(self._on_send7_changed):
          lSends[6].remove_value_listener(self._on_send7_changed)
        if len(lSends) > 7 and lSends[7].value_has_listener(self._on_send8_changed):
          lSends[7].remove_value_listener(self._on_send8_changed)
      ChannelStripComponent.set_track(self, poTrack)
    else:
      self.update()

  def set_send_controls(self, poSend1Control, poSend2Control, poSend3Control, poSend4Control, poSend5Control, poSend6Control, poSend7Control, poSend8Control):
    assert ((poSend1Control == None) or isinstance(poSend1Control, ConfigurableButtonElement))
    assert ((poSend2Control == None) or isinstance(poSend2Control, ConfigurableButtonElement))
    assert ((poSend3Control == None) or isinstance(poSend3Control, ConfigurableButtonElement))
    assert ((poSend4Control == None) or isinstance(poSend4Control, ConfigurableButtonElement))
    assert ((poSend5Control == None) or isinstance(poSend5Control, ConfigurableButtonElement))
    assert ((poSend6Control == None) or isinstance(poSend6Control, ConfigurableButtonElement))
    assert ((poSend7Control == None) or isinstance(poSend7Control, ConfigurableButtonElement))
    assert ((poSend8Control == None) or isinstance(poSend8Control, ConfigurableButtonElement))
    if poSend1Control != self.m_oSend1Button:
      if self.m_oSend1Button != None:
        self.m_oSend1Button.remove_value_listener(self._on_send1_value)
      self.m_oSend1Button = poSend1Control
      if self.m_oSend1Button != None:
        self.m_oSend1Button.add_value_listener(self._on_send1_value)
    if poSend2Control != self.m_oSend2Button:
      if self.m_oSend2Button != None:
        self.m_oSend2Button.remove_value_listener(self._on_send2_value)
      self.m_oSend2Button = poSend2Control
      if self.m_oSend2Button != None:
        self.m_oSend2Button.add_value_listener(self._on_send2_value)
    if poSend3Control != self.m_oSend3Button:
      if self.m_oSend3Button != None:
        self.m_oSend3Button.remove_value_listener(self._on_send3_value)
      self.m_oSend3Button = poSend3Control
      if self.m_oSend3Button != None:
        self.m_oSend3Button.add_value_listener(self._on_send3_value)
    if poSend4Control != self.m_oSend4Button:
      if self.m_oSend4Button != None:
        self.m_oSend4Button.remove_value_listener(self._on_send4_value)
      self.m_oSend4Button = poSend4Control
      if self.m_oSend4Button != None:
        self.m_oSend4Button.add_value_listener(self._on_send4_value)
    if poSend5Control != self.m_oSend5Button:
      if self.m_oSend5Button != None:
        self.m_oSend5Button.remove_value_listener(self._on_send5_value)
      self.m_oSend5Button = poSend5Control
      if self.m_oSend5Button != None:
        self.m_oSend5Button.add_value_listener(self._on_send5_value)
    if poSend6Control != self.m_oSend6Button:
      if self.m_oSend6Button != None:
        self.m_oSend6Button.remove_value_listener(self._on_send6_value)
      self.m_oSend6Button = poSend6Control
      if self.m_oSend6Button != None:
        self.m_oSend6Button.add_value_listener(self._on_send6_value)
    if poSend7Control != self.m_oSend7Button:
      if self.m_oSend7Button != None:
        self.m_oSend7Button.remove_value_listener(self._on_send7_value)
      self.m_oSend7Button = poSend7Control
      if self.m_oSend7Button != None:
        self.m_oSend7Button.add_value_listener(self._on_send7_value)
    if poSend8Control != self.m_oSend8Button:
      if self.m_oSend8Button != None:
        self.m_oSend8Button.remove_value_listener(self._on_send8_value)
      self.m_oSend8Button = poSend8Control
      if self.m_oSend8Button != None:
        self.m_oSend8Button.add_value_listener(self._on_send8_value)
    self.update()

  def update(self):
    ChannelStripComponent.update(self)
    if self._allow_updates:
      if self.is_enabled():
        oTrack = self.get_track_or_none()
        if oTrack != None:
          oMixDev = self._track.mixer_device
          aSends  = oMixDev.sends
          if len(aSends) > 0:
            if not aSends[0].value_has_listener(self._on_send1_changed):
              aSends[0].add_value_listener(self._on_send1_changed)
            self._on_send1_changed()
          elif self.m_oSend1Button != None:
            self.m_oSend1Button.turn_off()
          if len(aSends) > 1:
            if not aSends[1].value_has_listener(self._on_send2_changed):
              aSends[1].add_value_listener(self._on_send2_changed)
            self._on_send2_changed()
          elif self.m_oSend2Button != None:
            self.m_oSend2Button.turn_off()
          if len(aSends) > 2:
            if not aSends[2].value_has_listener(self._on_send3_changed):
              aSends[2].add_value_listener(self._on_send3_changed)
            self._on_send3_changed()
          elif self.m_oSend3Button != None:
            self.m_oSend3Button.turn_off()
          if len(aSends) > 3:
            if not aSends[3].value_has_listener(self._on_send4_changed):
              aSends[3].add_value_listener(self._on_send4_changed)
            self._on_send4_changed()
          elif self.m_oSend4Button != None:
            self.m_oSend4Button.turn_off()
          if len(aSends) > 4:
            if not aSends[4].value_has_listener(self._on_send5_changed):
              aSends[4].add_value_listener(self._on_send5_changed)
            self._on_send5_changed()
          elif self.m_oSend5Button != None:
            self.m_oSend5Button.turn_off()
          if len(aSends) > 5:
            if not aSends[5].value_has_listener(self._on_send6_changed):
              aSends[5].add_value_listener(self._on_send6_changed)
            self._on_send6_changed()
          elif self.m_oSend6Button != None:
            self.m_oSend6Button.turn_off()
          if len(aSends) > 6:
            if not aSends[6].value_has_listener(self._on_send7_changed):
              aSends[6].add_value_listener(self._on_send7_changed)
            self._on_send7_changed()
          elif self.m_oSend7Button != None:
            self.m_oSend7Button.turn_off()
          if len(aSends) > 7:
            if not aSends[7].value_has_listener(self._on_send8_changed):
              aSends[7].add_value_listener(self._on_send8_changed)
            self._on_send8_changed()
          elif self.m_oSend8Button != None:
            self.m_oSend8Button.turn_off()
        else:
          if self._solo_button != None:
            self._solo_button.reset()
          if self.m_oSend1Button != None:
            self.m_oSend1Button.reset()
          if self.m_oSend2Button != None:
            self.m_oSend2Button.reset()
          if self.m_oSend3Button != None:
            self.m_oSend3Button.reset()
          if self.m_oSend4Button != None:
            self.m_oSend4Button.reset()
          if self.m_oSend5Button != None:
            self.m_oSend5Button.reset()
          if self.m_oSend6Button != None:
            self.m_oSend6Button.reset()
          if self.m_oSend7Button != None:
            self.m_oSend7Button.reset()
          if self.m_oSend8Button != None:
            self.m_oSend8Button.reset()

        self._on_send1_changed()
        self._on_send2_changed()
        self._on_send3_changed()
        self._on_send4_changed()
        self._on_send5_changed()
        self._on_send6_changed()
        self._on_send7_changed()
        self._on_send8_changed()

  # LISTENERS **********************************************

  def on_sel_track_change(self):
    self._on_stop_changed()  # depends on track
    self._on_input_changed() # depends on track

  # TRACK STOP *********************************************

  def set_stop_button(self, poControl):
    if poControl != self.m_oStopControl:
      release_control(self.m_oStopControl)
      self.m_oStopControl = poControl
      self._stop_button_slot.subject = poControl
      self._on_stop_changed()

  def _stop_value(self, pnValue):
    assert self.m_oStopControl != None
    assert isinstance(pnValue, int)
    oTrack = self.get_track_or_none(self.m_oStopControl, 0)
    if (oTrack == None):
      self.m_oStopControl.turn_off()
      return None
    oTrack.stop_all_clips()
    self.m_oStopControl.turn_on()

  def _on_stop_changed(self):
    if (self.m_oStopControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oStopControl, 0)
    if oTrack == None:
      self.m_oStopControl.turn_off()
      return None
    self.m_oStopControl.turn_on()

  # INPUT SELECT *******************************************

  def set_input_control(self, poControl):
    if poControl != self.m_oInputControl:
      release_control(self.m_oInputControl)
      self.m_oInputControl = poControl
      self._input_button_slot.subject = poControl
      self._on_input_changed()

  def _input_value(self, pnValue):
    assert self.m_oInputControl != None
    assert isinstance(pnValue, int)
    if pnValue == 0: return
    oTrack = self.get_track_or_none(self.m_oInputControl, 0)
    if (oTrack == None):
      self.m_oInputControl.turn_on()
      self.m_oInputControl.set_light('Session.Monitor.Unav')
      return None
    nMonitor = (oTrack.current_monitoring_state + 1) % 3
    oTrack.current_monitoring_state = nMonitor
    self.m_oInputControl.turn_on()
    lColors = ['In', 'Auto', 'Off']
    self.m_oInputControl.set_light('Session.Monitor.%s' % (lColors[nMonitor]))

  def _on_input_changed(self):
    if (self.m_oInputControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oInputControl, 0)
    if oTrack == None:
      self.m_oInputControl.turn_on()
      self.m_oInputControl.set_light('Session.Monitor.Unav')
      return None
    nMonitor = oTrack.current_monitoring_state
    self.m_oInputControl.turn_on()
    lColors = ['In', 'Auto', 'Off']
    self.m_oInputControl.set_light('Session.Monitor.%s' % (lColors[nMonitor]))

  # DECK (CROSSFADE) ***************************************

  def set_deck_control(self, poControl):
    if poControl != self.m_oDeckControl:
      release_control(self.m_oDeckControl)
      self.m_oDeckControl = poControl
      self._deck_button_slot.subject = poControl
      self._on_deck_changed()

  def _deck_value(self, pnValue):
    assert self.m_oDeckControl != None
    assert isinstance(pnValue, int)
    if pnValue == 0: return
    oTrack = self.get_track_or_none(self.m_oDeckControl, 0)
    if (oTrack == None):
      self.m_oDeckControl.turn_on()
      self.m_oDeckControl.set_light('Session.Deck.Unav')
      return None
    nMonitor = (oTrack.mixer_device.crossfade_assign - 1) % 3
    oTrack.mixer_device.crossfade_assign = nMonitor
    self.m_oDeckControl.turn_on()
    lColors = ['A', 'Off', 'B']
    self.m_oDeckControl.set_light('Session.Deck.%s' % (lColors[nMonitor]))

  def _on_deck_changed(self):
    if (self.m_oDeckControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oDeckControl, 0)
    if oTrack == None:
      self.m_oDeckControl.turn_on()
      self.m_oDeckControl.set_light('Session.Deck.Unav')
      return None
    nDeck = oTrack.mixer_device.crossfade_assign
    self.m_oDeckControl.turn_on()
    lColors = ['A', 'Off', 'B']
    self.m_oDeckControl.set_light('Session.Deck.%s' % (lColors[nDeck]))

  # SENDS OFF **********************************************

  def set_sends_control(self, poControl):
    if poControl != self.m_oSendsControl:
      release_control(self.m_oSendsControl)
      self.m_oSendsControl = poControl
      self._sends_button_slot.subject = poControl
      self._on_sends_changed()

  def _sends_value(self, pnValue):
    assert self.m_oSendsControl != None
    assert isinstance(pnValue, int)
    if pnValue == 0: return
    oTrack = self.get_track_or_none(self.m_oSendsControl, 0)
    if (oTrack == None):
      self.m_oSendsControl.turn_off()
      return None
    oMixDev = oTrack.mixer_device
    lSends  = oMixDev.sends
    for oSend in lSends:
      oSend.value = 0.0
    self.m_oSendsControl.turn_on()

  def _on_sends_changed(self):
    if (self.m_oSendsControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oSendsControl, 0)
    if oTrack == None:
      self.m_oSendsControl.turn_off()
      return None
    self.m_oSendsControl.turn_on()

  # ********************************************************

  def _on_send1_value(self, pnValue):
    self._handle_send_value(pnValue, 0)

  def _on_send2_value(self, pnValue):
    self._handle_send_value(pnValue, 1)

  def _on_send3_value(self, pnValue):
    self._handle_send_value(pnValue, 2)

  def _on_send4_value(self, pnValue):
    self._handle_send_value(pnValue, 3)

  def _on_send5_value(self, pnValue):
    self._handle_send_value(pnValue, 4)

  def _on_send6_value(self, pnValue):
    self._handle_send_value(pnValue, 5)

  def _on_send7_value(self, pnValue):
    self._handle_send_value(pnValue, 6)

  def _on_send8_value(self, pnValue):
    self._handle_send_value(pnValue, 7)

  def _handle_send_value(self, pnValue, pnIdx):
    assert (pnValue in range(128))
    if (self.is_enabled() and (self._track != None) and (pnValue == 127)):
      lSends = self._track.mixer_device.sends
      if pnIdx >= len(lSends):
        return
      oSend = lSends[pnIdx]
      if oSend.is_enabled:
        if oSend.value < 0.5:
          oSend.value = 1.0
        else:
          oSend.value = 0.0

  def _on_send1_changed(self):
    self._handle_send_changed(0, self.m_oSend1Button)

  def _on_send2_changed(self):
    self._handle_send_changed(1, self.m_oSend2Button)

  def _on_send3_changed(self):
    self._handle_send_changed(2, self.m_oSend3Button)

  def _on_send4_changed(self):
    self._handle_send_changed(3, self.m_oSend4Button)

  def _on_send5_changed(self):
    self._handle_send_changed(4, self.m_oSend5Button)

  def _on_send6_changed(self):
    self._handle_send_changed(5, self.m_oSend6Button)

  def _on_send7_changed(self):
    self._handle_send_changed(6, self.m_oSend7Button)

  def _on_send8_changed(self):
    self._handle_send_changed(7, self.m_oSend8Button)

  def _handle_send_changed(self, pnIdx, poBut):
    if (self._track != None):
      lSends = self._track.mixer_device.sends
      if (self.is_enabled() and (poBut != None)):
        if pnIdx >= len(lSends):
          return
        if (lSends[pnIdx].value > 0.5):
          poBut.turn_on()
        else:
          poBut.turn_off()
    else:
      if (self.is_enabled() and poBut != None):
        poBut.set_light('Unav.Off')

  # ********************************************************

  def tracks(self):
    return self.song().tracks # visible_tracks

  def get_track_or_none(self, poControl = None, pnResetValue = None):
    if (not self.is_enabled()):
      # disabled! nothing else to do!
      return self.send_reset_value(poControl, pnResetValue)

    if (self._track == None):
      # no track! nothing else to do!
      return self.send_reset_value(poControl, pnResetValue)

    if (self._track == self.song().master_track):
      # is master track, nothing else to do!
      return self.send_reset_value(poControl, pnResetValue)

    if (not self._track in self.tracks()):
      # is a return track, nothing else to do!
      return self.send_reset_value(poControl, pnResetValue)

    return self._track

  def send_reset_value(self, poControl, pnResetValue):
    if (poControl != None):
      poControl.send_value(pnResetValue)
    return None

  # ********************************************************

  def log(self, psMsg):
    Live.Base.log(psMsg)
