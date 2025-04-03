from .Dev import Dev

class MidiArpeggiator(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGB0Off | Velocity On    | Vel. Retrigger | Use Current Scale',
      #-----------------------------------------------------------------------
      'Bank0 | nGR0Off | Retrigger Mode | Repeats'                           ,
      'Bank0 | nGR1Off | Velocity Decay | Velocity Target'                   ,
      'Bank0 | nGR2Off | Tranpose Key   | Tranpose Mode'                     ,
      #-----------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On      | Preset Prev    | Hold On'          ,
      'Bank0 | nMB1Off | Preset Save    | Preset Next    | Sync On'          ,
      #-----------------------------------------------------------------------
      'Bank0 | nMR0Off | Style          | Offset         | Groove'           ,
      'Bank0 | nMR1Off | Free Rate      | Synced Rate    | Transp. Dist.'    ,
      'Bank0 | nMR2Off | Transp. Steps  | Gate           | Ret. Interval'    ,
    ]
    self.reg('MidiArpeggiator')
    self.parse_cfg()

#=======================================================================
# Class: MidiArpeggiator, Device: Arpeggiator, Display: Arpeggiator
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Velocity On", orig: "Velocity On" => [Off, On]
# Q param: "Vel. Retrigger", orig: "Vel. Retrigger" => [Off, On]
# Q param: "Use Current Scale", orig: "Use Current Scale" => [Off, On]
# Q param: "Retrigger Mode", orig: "Retrigger Mode" => [Off, Note, Beat]
#   param: "Repeats", orig: "Repeats", value: 0.000000, min: 0.000000, max: 16.000000
#   param: "Velocity Decay", orig: "Velocity Decay", value: 0.529359, min: 0.000000, max: 1.000000
#   param: "Velocity Target", orig: "Velocity Target", value: 64.000000, min: 0.000000, max: 127.000000
# Q param: "Tranpose Mode", orig: "Tranpose Mode" => [Chromatic, Major, Minor, Dorian, Mixolydian, Lydian, Phrygian, Locrian, Whole Tone, Half-whole Dim., Whole-half Dim., Minor Blues, Minor Pentatonic, Major Pentatonic, Harmonic Minor, Harmonic Major, Dorian #4, Phrygian Dominant, Melodic Minor, Lydian Augmented, Lydian Dominant, Super Locrian, 8-Tone Spanish, Bhairav, Hungarian Minor, Hirajoshi, In-Sen, Iwato, Kumoi, Pelog Selisir, Pelog Tembung, Messiaen 3, Messiaen 4, Messiaen 5, Messiaen 6, Messiaen 7]
# Q param: "Tranpose Key", orig: "Tranpose Key" => [C, C♯, D, D♯, E, F, F♯, G, G♯, A, A♯, B]
# Q param: "Hold On", orig: "Hold On" => [Off, On]
# Q param: "Sync On", orig: "Sync On" => [Off, On]
# Q param: "Style", orig: "Style" => [Up, Down, UpDown, DownUp, Up & Down, Down & Up, Converge, Diverge, Con & Diverge, Pinky Up, Pinky UpDown, Thumb Up, Thumb UpDown, Play Order, Chord Trigger, Random, Random Other, Random Once]
#   param: "Offset", orig: "Offset", value: 0.000000, min: -8.000000, max: 8.000000
# Q param: "Groove", orig: "Groove" => [Straight, Swing 8, Swing 16, Swing 32]
#   param: "Free Rate", orig: "Free Rate", value: 0.150515, min: 0.000000, max: 1.000000
#   param: "Synced Rate", orig: "Synced Rate", value: 8.000000, min: 0.000000, max: 13.000000
#   param: "Transp. Dist.", orig: "Transp. Dist.", value: 12.000000, min: -24.000000, max: 24.000000
#   param: "Transp. Steps", orig: "Transp. Steps", value: 0.000000, min: 0.000000, max: 8.000000
#   param: "Gate", orig: "Gate", value: 50.000000, min: 1.000000, max: 200.000000
#   param: "Ret. Interval", orig: "Ret. Interval", value: 8.000000, min: 0.000000, max: 14.000000

