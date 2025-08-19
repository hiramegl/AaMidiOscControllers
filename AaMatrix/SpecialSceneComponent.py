import Live

from _Framework.SceneComponent import SceneComponent
from _Framework.SubjectSlot    import subject_slot

class SpecialSceneComponent(SceneComponent):
  __module__ = __name__

  def __init__(self, num_slots, tracks_to_use_callback, *a, **k):
    super(SpecialSceneComponent, self).__init__(num_slots, tracks_to_use_callback, *a, **k)
    self.m_oSelButton = None
    self.set_no_scene_value('Unav.Off')

  def disconnect(self):
    SceneComponent.disconnect(self)
    self.m_oSelButton = None

  # ******************************************************

  def set_select_control(self, poControl):
    if poControl != self.m_oSelButton:
      self.m_oSelButton = poControl
      self._on_select_value.subject = poControl
      self.update()

  @subject_slot(u'value')
  def _on_select_value(self, value):
    if self.is_enabled():
      self._do_select_scene(self._scene)

  # ******************************************************

  def update(self):
    super(SpecialSceneComponent, self).update()
    if self._allow_updates and self.m_oSelButton != None:
      if self._scene != None and self.is_enabled():
        if self.song().view.selected_scene == self._scene:
          self.m_oSelButton.turn_on()
        else:
          self.m_oSelButton.turn_off()
      else:
        self.m_oSelButton.turn_off()

