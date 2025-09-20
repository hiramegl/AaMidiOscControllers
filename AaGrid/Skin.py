from _Framework.Skin          import Skin
from _Framework.ButtonElement import Color

BLACK       = Color(0)
GREEN       = Color(1)
GREEN_BLINK = Color(2)
RED         = Color(3)
RED_BLINK   = Color(4)
AMBER       = Color(5)
AMBER_BLINK = Color(6)

BOTTOM_OFF  = Color(0)
BOTTOM_ON   = Color(1)

SIDE_OFF    = Color(0)
SIDE_ON     = Color(1)

class Colors:
  class DefaultButton:
    On       = BLACK
    Off      = BLACK
    Disabled = BLACK

  class Nav:
    On  = BOTTOM_ON
    Off = BOTTOM_OFF

  class Bottom:
    On  = BOTTOM_ON
    Off = BOTTOM_OFF

  class Side:
    On  = SIDE_ON
    Off = SIDE_OFF

  class Loop:
    class ShiftSize: # Row1
      On  = RED
      Off = AMBER

    class SongStart: # Row2
      On  = AMBER
      Off = BLACK
    class SongEnd:
      On  = GREEN
      Off = BLACK
    class LoopStart:
      On  = AMBER
      Off = BLACK
    class LoopEnd:
      On  = GREEN
      Off = BLACK

    class Shift:     # Row3
      On  = GREEN
      Off = BLACK
    class LoopShSta:
      On  = AMBER
      Off = BLACK
    class LoopShMid:
      On  = RED
      Off = BLACK
    class LoopShEnd:
      On  = GREEN
      Off = BLACK

    class Roll:      # Row4
      On  = GREEN
      Off = BLACK
    class Roll14:
      On  = AMBER
      Off = BLACK

    class Roll18:    # Row5
      On  = RED
      Off = BLACK

    class LoopCmd:   # Row6
      On  = GREEN
      Off = BLACK
    class ClipCmd:
      On  = RED
      Off = BLACK
    class Legato:
      On  = GREEN
      Off = BLACK
    class Warp:
      On  = AMBER
      Off = BLACK
    class Crop:
      On  = RED
      Off = BLACK

    class Tempo:      # Row7
      On  = AMBER
      Off = RED

    class TempoDec:   # Row8
      On  = RED
      Off = BLACK
    class TempoInc:
      On  = GREEN
      Off = RED

  class Tune:
    class TunCoaNeg:  # Row 1-6
      On  = RED
      Off = BLACK
    class TunCoaPos:
      On  = GREEN
      Off = BLACK

    class TunFinNeg:  # Row 7
      On  = AMBER
      Off = BLACK
    class TunFinPos:
      On  = GREEN
      Off = BLACK

    class Gain:       # Row 8
      On  = RED
      Off = BLACK

def make_skin():
  return Skin(Colors)

