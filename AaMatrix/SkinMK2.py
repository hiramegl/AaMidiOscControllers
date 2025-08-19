from _Framework.Skin import Skin
from .ColorsMK2      import Rgb

class Colors:
  class DefaultButton:
    On       = Rgb.GREY
    Off      = Rgb.BLACK
    Disabled = Rgb.BLACK

  class Unav:
    On  = Rgb.BLACK
    Off = Rgb.BLACK

  class Session:
    #scene
    SceneTriggered      = Rgb.GREEN_BLINK
    Scene               = Rgb.GREEN
    NoScene             = Rgb.BLACK

    #clip states
    ClipStarted         = Rgb.GREEN_PULSE
    ClipStopped         = Rgb.RED_THIRD
    ClipRecording       = Rgb.RED_PULSE
    ClipEmpty           = Rgb.BLACK

    #trigs
    ClipTriggeredPlay   = Rgb.GREEN_BLINK
    ClipTriggeredRecord = Rgb.RED_BLINK
    RecordButton        = Rgb.RED_THIRD

    #stop button
    StopClip            = Rgb.RED
    StopClipTriggered   = Rgb.RED_BLINK

    class Nav:
      On  = Rgb.RED
      Off = Rgb.BLACK

    class ColNav:
      On  = Rgb.MINT
      Off = Rgb.WHITE

    class RowNav:
      On  = Rgb.PURPLE
      Off = Rgb.WHITE

    class ModeSends:
      On  = Rgb.PINK
      Off = Rgb.BLACK
    class ModeTrack:
      On  = Rgb.GREEN
      Off = Rgb.BLACK
    class ModeSelect:
      On  = Rgb.BLUE
      Off = Rgb.BLACK
    class ModeFire:
      class Clips:
        On  = Rgb.RED
        Off = Rgb.BLACK
      class Scenes:
        On  = Rgb.GREEN_BLINK
        Off = Rgb.BLACK

    class Send:
      On  = Rgb.RED
      Off = Rgb.YELLOW

    class Stop:
      On  = Rgb.RED
      Off = Rgb.BLACK
    class Mute:
      On  = Rgb.AMBER
      Off = Rgb.BLACK
    class Solo:
      On  = Rgb.BLUE
      Off = Rgb.BLUE_THIRD
    class Arm:
      On  = Rgb.PURPLE
      Off = Rgb.PURPLE_THIRD
    class Monitor:
      On   = Rgb.BLACK
      Off  = Rgb.MINT_THIRD
      In   = Rgb.MINT
      Auto = Rgb.YELLOW
      Unav = Rgb.BLACK
    class Deck:
      On   = Rgb.BLACK
      Off  = Rgb.LIGHT_BLUE_THIRD
      A    = Rgb.ORANGE
      B    = Rgb.LIGHT_BLUE
      Unav  = Rgb.BLACK
    class SendsOff:
      On  = Rgb.RED_HALF
      Off = Rgb.BLACK
    class Select:
      On  = Rgb.LIME
      Off = Rgb.BLACK

def make_skin():
  return Skin(Colors)
