LAUNCHPAD MINI MK3 - COLOR BUTTONS
=======================

MIDI MAPPING:
Channel 1 (MIDI 0)
11 -> 98 (NOTE ON, NOTE OFF)

    1    2    3    4    5    6    7    8
  +---------------------------------------+
  | 91   92   93   94   95   96   97   98 |        ^ v < > Session Drums Keys User
  +---------------------------------------+------+
8 | 81   82   83   84   85   86   87   88 |  89  |
7 | 71   72   73   74   75   76   77   78 |  79  |
6 | 61   62   63   64   65   66   67   68 |  69  |
5 | 51   52   53   54   55   56   57   58 |  59  |
4 | 41   42   43   44   45   46   47   48 |  49  |
3 | 31   32   33   34   35   36   37   38 |  39  |
2 | 21   22   23   24   25   26   27   28 |  29  |
1 | 11   12   13   14   15   16   17   18 |  19  |
  +---------------------------------------+------+

===================================================

     1            2            3            4            5            6            7            8
   +--------------------------------------------------------------------------------------------------------+--------------+
   |  SESS UP      SESS DW      SESS LEFT    SESS RIGHT   COL 1        COL 2        COL 3        COL 4      |              |
   +--------------------------------------------------------------------------------------------------------+--------------+
 8 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | ROW 1        |
 7 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | ROW 2        |
 6 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | ROW 3        |
 5 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | ROW 4        |
 4 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SENDS        |
 3 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | TRACK        |
 2 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SELECT CLIP  |
 1 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | FIRE CLP/SCN |
   +--------------------------------------------------------------------------------------------------------+--------------+

AaMatrix (ControlSurface)
+ Registers the buttons and forwards events to the selector

Selector
+ selector routes the event to the selected module

LOGICAL SESSION SIZE = 32 x 32  -> (8 buttons x 4 columns) X (8 buttons x 4 rows)
PHYSICAL PAD SIZE    = 8  x 8   buttons

TRACK buttons:
1. STOP
2. MUTE
3. SOLO
4. ARM
5. INPUT (MONITOR)
6. DECK (CROSSFADER)
7. SENDS OFF
8. SELECT TRACK

FIRE MODE has 2 submodes:
1. FIRE CLIPS
2. FIRE SCENES

NOTE! Make sure the Scene buttons have colors in Ableton Live UI
