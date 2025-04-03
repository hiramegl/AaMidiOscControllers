from .Dev import Dev

class Collision(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
      'Bank0 | nGR0Off | Mallet Noise Color'                                                                                                                                                                        ,
      #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMB0Off | Device On           | Preset Prev        | Mallet On/Off        | Noise On/Off         | Retrigger'         ,
      'Bank0 | nMB1Off | Preset Save         | Preset Next        | -                    | -                    | Structure'                                                                     ,
      #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank0 | nMR0Off | Mallet Volume       | Noise Volume       | Noise Freq < Env     | Noise Filter Type    | Mallet Volume < Key       | Mallet Volume < Vel       | Noise Volume < Key     | Noise Volume < Vel'     ,
      'Bank0 | nMR1Off | Mallet Stiffness    | Noise Filter Freq  | Noise Attack         | Noise Sustain        | Mallet Stiffness < Key    | Mallet Stiffness < Vel    | Noise Freq < Key       | Noise Freq < Vel'       ,
      'Bank0 | nMR2Off | Mallet Noise Amount | Noise Filter Q     | Noise Decay          | Noise Release        | Mallet Noise Amount < Key | Mallet Noise Amount < Vel | Voices                 | Volume'                 ,
      #=====================================================================================================================================================================================================================
      'Bank1 | nGR0Off | -                   | -                  | -                    | -                    | Res 1 Pitch Env. Time'         ,
      'Bank1 | nGR1Off | Res 1 Decay < Key   | Res 1 Decay < Vel  | Res 1 Material < Key | Res 1 Material < Vel | Res 1 Tune < Key          | Res 1 Pan < Key           | Res 1 Pitch Env. < Vel | Res 1 Inharmonics < Vel',
      'Bank1 | nGR2Off | Res 1 Radius < Key  | Res 1 Radius < Vel | Res 1 Opening < Vel'                      ,
      #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMB0Off | Res 1 On/Off'                                                                                                                                                                                     ,
      #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank1 | nMR0Off | Res 1 Type          | Res 1 Quality      | Res 1 Hit            | Res 1 Off Decay      | Res 1 Tune                | Res 1 Pan                 | Res 1 Radius'                                    ,
      'Bank1 | nMR1Off | Res 1 Decay         | Res 1 Material     | Res 1 Hit < Random   | Res 1 Listening L    | Res 1 Fine Tune           | Res 1 Bleed               | Res 1 Opening'                                   ,
      'Bank1 | nMR2Off | Res 1 Brightness    | Res 1 Inharmonics  | Res 1 Ratio          | Res 1 Listening R    | Res 1 Pitch Env.          | Res 1 Volume'                                                                ,
      #=====================================================================================================================================================================================================================
      'Bank2 | nGR0Off | -                   | -                  | -                    | -                    | Res 2 Pitch Env. Time'                                                                                   ,
      'Bank2 | nGR1Off | Res 2 Decay < Key   | Res 2 Decay < Vel  | Res 2 Material < Key | Res 2 Material < Vel | Res 2 Tune < Key          | Res 2 Pan < Key           | Res 2 Pitch Env. < Vel | Res 2 Inharmonics < Vel',
      'Bank2 | nGR2Off | Res 2 Radius < Key  | Res 2 Radius < Vel | Res 2 Opening < Vel'                                                                                                                                   ,
      #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMB0Off | Res 2 On/Off'                                                                                                                                                                            ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank2 | nMR0Off | Res 2 Type          | Res 2 Quality      | Res 2 Hit            | Res 2 Off Decay      | Res 2 Tune                | Res 2 Pan                 | Res 2 Radius'      ,
      'Bank2 | nMR1Off | Res 2 Decay         | Res 2 Material     | Res 2 Hit < Random   | Res 2 Listening L    | Res 2 Fine Tune           | Res 2 Bleed               | Res 2 Opening'     ,
      'Bank2 | nMR2Off | Res 2 Brightness    | Res 2 Inharmonics  | Res 2 Ratio          | Res 2 Listening R    | Res 2 Pitch Env.          | Res 2 Volume'                             ,
      #====================================================================================================================================================================================================================
      'Bank3 | nGR0Off | PB Dest A           | PB Amt A           | PB Range             | Note PB Range        | MW Dest A                 | MW Amt A                  | MW Dest B             | MW Amt B'          ,
      'Bank3 | nGR1Off | Press Dest A        | Press Amt A        | Press Dest B         | Press Amt B          | Slide Dest A              | Slide Amt A               | Slide Dest B          | Slide Amt B'       ,
      #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMB0Off | LFO 1 On/Off        | LFO 1 Sync         | LFO 1 Retrigger      | -                    | LFO 2 On/Off              | LFO 2 Sync                | LFO 2 Retrigger'                                                                                                                                                                                           ,
      #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      'Bank3 | nMR0Off | LFO 1 Shape         | LFO 1 Offset       | LFO 1 Rate           | LFO 1 Depth          | LFO 2 Shape               | LFO 2 Offset              | LFO 2 Rate            | LFO 2 Depth',
      'Bank3 | nMR1Off | LFO 1 Dest A        | LFO 1 Amt A        | LFO 1 Sync Rate      | -                    | LFO 2 Dest A              | LFO 2 Amt A               | LFO 2 Sync Rate',
      'Bank3 | nMR2Off | LFO 1 Dest B        | LFO 1 Amt B        | LFO 1 Rate < Key     | LFO 1 Depth < Vel    | LFO 2 Dest B              | LFO 2 Amt B               | LFO 2 Rate < Key      | LFO 2 Depth < Vel ' ,
    ]
    self.reg('Collision')
    self.parse_cfg()

#=======================================================================
# Class: Collision, Device: Collision, Display: Collision
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Structure", orig: "Structure" => [1 > 2, 1 + 2]
#   param: "PB Range", orig: "PB Range", value: 5.000000, min: 0.000000, max: 24.000000
# Q param: "Voices", orig: "Voices" => [Mono, 2, 4, 6, 8, 10, 12, 14, 16]
# Q param: "Retrigger", orig: "Retrigger" => [Off, On]
#   param: "Volume", orig: "Volume", value: 0.704789, min: 0.000000, max: 1.000000
#   param: "Note PB Range", orig: "Note PB Range", value: 48.000000, min: 0.000000, max: 48.000000
# Q param: "Mallet On/Off", orig: "Mallet On/Off" => [Off, On]
#   param: "Mallet Volume", orig: "Mallet Volume", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Mallet Volume < Vel", orig: "Mallet Volume < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Mallet Volume < Key", orig: "Mallet Volume < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Mallet Stiffness", orig: "Mallet Stiffness", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Mallet Stiffness < Vel", orig: "Mallet Stiffness < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Mallet Stiffness < Key", orig: "Mallet Stiffness < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Mallet Noise Amount", orig: "Mallet Noise Amount", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Mallet Noise Amount < Vel", orig: "Mallet Noise Amount < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Mallet Noise Amount < Key", orig: "Mallet Noise Amount < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Mallet Noise Color", orig: "Mallet Noise Color", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Noise On/Off", orig: "Noise On/Off" => [Off, On]
#   param: "Noise Volume", orig: "Noise Volume", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Volume < Vel", orig: "Noise Volume < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Noise Volume < Key", orig: "Noise Volume < Key", value: 0.000000, min: -2.000000, max: 2.000000
# Q param: "Noise Filter Type", orig: "Noise Filter Type" => [LP, HP, BP, LP+HP]
#   param: "Noise Filter Freq", orig: "Noise Filter Freq", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Noise Freq < Vel", orig: "Noise Freq < Vel", value: 0.000000, min: -8.000000, max: 8.000000
#   param: "Noise Freq < Key", orig: "Noise Freq < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Noise Freq < Env", orig: "Noise Freq < Env", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Noise Filter Q", orig: "Noise Filter Q", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Noise Attack", orig: "Noise Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Noise Decay", orig: "Noise Decay", value: 0.200000, min: 0.000000, max: 1.000000
#   param: "Noise Sustain", orig: "Noise Sustain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Noise Release", orig: "Noise Release", value: 0.200000, min: 0.000000, max: 1.000000
# Q param: "Res 1 On/Off", orig: "Res 1 On/Off" => [Off, On]
# Q param: "Res 1 Type", orig: "Res 1 Type" => [Beam, Marimba, String, Membrane, Plate, Pipe, Tube]
# Q param: "Res 1 Quality", orig: "Res 1 Quality" => [Eco, Low, Med, High]
#   param: "Res 1 Tune", orig: "Res 1 Tune", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Res 1 Fine Tune", orig: "Res 1 Fine Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "Res 1 Tune < Key", orig: "Res 1 Tune < Key", value: 1.000000, min: -2.000000, max: 2.000000
#   param: "Res 1 Pitch Env.", orig: "Res 1 Pitch Env.", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 1 Pitch Env. < Vel", orig: "Res 1 Pitch Env. < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 1 Pitch Env. Time", orig: "Res 1 Pitch Env. Time", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 1 Decay", orig: "Res 1 Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 1 Decay < Vel", orig: "Res 1 Decay < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 1 Decay < Key", orig: "Res 1 Decay < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Res 1 Off Decay", orig: "Res 1 Off Decay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 1 Material", orig: "Res 1 Material", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 1 Material < Vel", orig: "Res 1 Material < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 1 Material < Key", orig: "Res 1 Material < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Res 1 Radius", orig: "Res 1 Radius", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 1 Radius < Vel", orig: "Res 1 Radius < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 1 Radius < Key", orig: "Res 1 Radius < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Res 1 Ratio", orig: "Res 1 Ratio", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 1 Brightness", orig: "Res 1 Brightness", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 1 Bleed", orig: "Res 1 Bleed", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 1 Inharmonics", orig: "Res 1 Inharmonics", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 1 Inharmonics < Vel", orig: "Res 1 Inharmonics < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 1 Opening", orig: "Res 1 Opening", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Res 1 Opening < Vel", orig: "Res 1 Opening < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 1 Hit", orig: "Res 1 Hit", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 1 Hit < Random", orig: "Res 1 Hit < Random", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 1 Listening L", orig: "Res 1 Listening L", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Res 1 Listening R", orig: "Res 1 Listening R", value: 0.900000, min: 0.000000, max: 1.000000
#   param: "Res 1 Pan", orig: "Res 1 Pan", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 1 Pan < Key", orig: "Res 1 Pan < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 1 Volume", orig: "Res 1 Volume", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "Res 2 On/Off", orig: "Res 2 On/Off" => [Off, On]
# Q param: "Res 2 Type", orig: "Res 2 Type" => [Beam, Marimba, String, Membrane, Plate, Pipe, Tube]
# Q param: "Res 2 Quality", orig: "Res 2 Quality" => [Eco, Low, Med, High]
#   param: "Res 2 Tune", orig: "Res 2 Tune", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Res 2 Fine Tune", orig: "Res 2 Fine Tune", value: 0.000000, min: -50.000000, max: 50.000000
#   param: "Res 2 Tune < Key", orig: "Res 2 Tune < Key", value: 1.000000, min: -2.000000, max: 2.000000
#   param: "Res 2 Pitch Env.", orig: "Res 2 Pitch Env.", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 2 Pitch Env. < Vel", orig: "Res 2 Pitch Env. < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 2 Pitch Env. Time", orig: "Res 2 Pitch Env. Time", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 2 Decay", orig: "Res 2 Decay", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 2 Decay < Vel", orig: "Res 2 Decay < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 2 Decay < Key", orig: "Res 2 Decay < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Res 2 Off Decay", orig: "Res 2 Off Decay", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 2 Material", orig: "Res 2 Material", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 2 Material < Vel", orig: "Res 2 Material < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 2 Material < Key", orig: "Res 2 Material < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Res 2 Radius", orig: "Res 2 Radius", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 2 Radius < Vel", orig: "Res 2 Radius < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 2 Radius < Key", orig: "Res 2 Radius < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "Res 2 Ratio", orig: "Res 2 Ratio", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 2 Brightness", orig: "Res 2 Brightness", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 2 Bleed", orig: "Res 2 Bleed", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 2 Inharmonics", orig: "Res 2 Inharmonics", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 2 Inharmonics < Vel", orig: "Res 2 Inharmonics < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 2 Opening", orig: "Res 2 Opening", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Res 2 Opening < Vel", orig: "Res 2 Opening < Vel", value: 0.000000, min: -5.000000, max: 5.000000
#   param: "Res 2 Hit", orig: "Res 2 Hit", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "Res 2 Hit < Random", orig: "Res 2 Hit < Random", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Res 2 Listening L", orig: "Res 2 Listening L", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Res 2 Listening R", orig: "Res 2 Listening R", value: 0.900000, min: 0.000000, max: 1.000000
#   param: "Res 2 Pan", orig: "Res 2 Pan", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 2 Pan < Key", orig: "Res 2 Pan < Key", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Res 2 Volume", orig: "Res 2 Volume", value: 0.500000, min: 0.000000, max: 1.000000
# Q param: "LFO 1 On/Off", orig: "LFO 1 On/Off" => [Off, On]
# Q param: "LFO 1 Shape", orig: "LFO 1 Shape" => [Sine, Square, Triangle, SawUp, SawDown, Sample & Hold, Random Ramp]
# Q param: "LFO 1 Retrigger", orig: "LFO 1 Retrigger" => [Off, On]
# Q param: "LFO 1 Sync", orig: "LFO 1 Sync" => [Free, Sync]
#   param: "LFO 1 Rate", orig: "LFO 1 Rate", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Sync Rate", orig: "LFO 1 Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "LFO 1 Rate < Key", orig: "LFO 1 Rate < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "LFO 1 Offset", orig: "LFO 1 Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "LFO 1 Depth", orig: "LFO 1 Depth", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 1 Depth < Vel", orig: "LFO 1 Depth < Vel", value: 0.000000, min: -5.000000, max: 5.000000
# Q param: "LFO 1 Dest A", orig: "LFO 1 Dest A" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 2 Rate, LFO 2 Depth]
#   param: "LFO 1 Amt A", orig: "LFO 1 Amt A", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "LFO 1 Dest B", orig: "LFO 1 Dest B" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 2 Rate, LFO 2 Depth]
#   param: "LFO 1 Amt B", orig: "LFO 1 Amt B", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "LFO 2 On/Off", orig: "LFO 2 On/Off" => [Off, On]
# Q param: "LFO 2 Shape", orig: "LFO 2 Shape" => [Sine, Square, Triangle, SawUp, SawDown, Sample & Hold, Random Ramp]
# Q param: "LFO 2 Retrigger", orig: "LFO 2 Retrigger" => [Off, On]
# Q param: "LFO 2 Sync", orig: "LFO 2 Sync" => [Free, Sync]
#   param: "LFO 2 Rate", orig: "LFO 2 Rate", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Sync Rate", orig: "LFO 2 Sync Rate", value: 4.000000, min: 0.000000, max: 21.000000
#   param: "LFO 2 Rate < Key", orig: "LFO 2 Rate < Key", value: 0.000000, min: -2.000000, max: 2.000000
#   param: "LFO 2 Offset", orig: "LFO 2 Offset", value: 0.000000, min: 0.000000, max: 360.000000
#   param: "LFO 2 Depth", orig: "LFO 2 Depth", value: 0.500000, min: 0.000000, max: 1.000000
#   param: "LFO 2 Depth < Vel", orig: "LFO 2 Depth < Vel", value: 0.000000, min: -5.000000, max: 5.000000
# Q param: "LFO 2 Dest A", orig: "LFO 2 Dest A" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate]
#   param: "LFO 2 Amt A", orig: "LFO 2 Amt A", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "LFO 2 Dest B", orig: "LFO 2 Dest B" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate]
#   param: "LFO 2 Amt B", orig: "LFO 2 Amt B", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "PB Dest A", orig: "PB Dest A" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "PB Amt A", orig: "PB Amt A", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "MW Dest A", orig: "MW Dest A" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "MW Amt A", orig: "MW Amt A", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "MW Dest B", orig: "MW Dest B" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "MW Amt B", orig: "MW Amt B", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "Press Dest A", orig: "Press Dest A" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "Press Amt A", orig: "Press Amt A", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "Press Dest B", orig: "Press Dest B" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "Press Amt B", orig: "Press Amt B", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "Slide Dest A", orig: "Slide Dest A" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "Slide Amt A", orig: "Slide Amt A", value: 2.500000, min: -5.000000, max: 5.000000
# Q param: "Slide Dest B", orig: "Slide Dest B" => [No Destination, Mallet Stiffness, Noise Freq, Noise Volume, Res 1 Pitch, Res 1 Hit, Res 1 Pan, Res 1 Pipe Opening, Res 2 Input, Res 2 Pitch, Res 2 Hit, Res 2 Pan, Res 2 Pipe Opening, Volume, LFO 1 Rate, LFO 1 Depth, LFO 2 Rate, LFO 2 Depth]
#   param: "Slide Amt B", orig: "Slide Amt B", value: 2.500000, min: -5.000000, max: 5.000000
