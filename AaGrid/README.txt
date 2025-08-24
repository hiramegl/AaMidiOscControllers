APC MINI - MIDI MAPPING
=======================

Channel 1 (MIDI 0)
0 -> 98 (NOTE ON, NOTE OFF)
VALUE = 127

    1    2    3    4    5    6    7    8
  +---------------------------------------+------+
8 | 56   57   58   59   60   61   62   63 |  82  | MIDI NOTE
7 | 48   49   40   51   52   53   54   55 |  83  | MIDI NOTE
6 | 40   41   42   43   44   45   46   47 |  84  | MIDI NOTE
5 | 32   33   34   35   36   37   38   39 |  85  | MIDI NOTE
4 | 24   25   26   27   28   29   30   31 |  86  | MIDI NOTE
3 | 16   17   18   19   20   21   22   23 |  87  | MIDI NOTE
2 | 8    9    10   11   12   13   14   15 |  88  | MIDI NOTE
1 | 0    1    2    3    4    5    6    7  |  89  | MIDI NOTE
  +---------------------------------------+------+
  | 64   65   66   67   68   69   70   71 |  98  | MIDI NOTE
  +---------------------------------------+------+
  | 48   49   50   51   52   53   54   55 |  56  | MIDI CONTROL
  +---------------------------------------+------+

0 shift amount
1 ss se ls le
2 sh ls lm le - lptg
3 roll  roll 1/4
4 roll 1/8
5 2lp 2cl Legato Warp WarpMode Crop - Fllw
6 Tempo - Tempo Rst
7 Tempo Inc/Dec
- Mode

0-5 coarse tune - Rst
6   fine tune   - Rst
1   gain
- Mode

To implement: Quantize, Metro
