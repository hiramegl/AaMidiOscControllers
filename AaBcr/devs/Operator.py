from .Dev import Dev

class Operator(Dev):
  def __init__(self, phCfg, phObj):
    Dev.__init__(self, phCfg, phObj)
    self.m_lCfg = [
       'Bank0 | nGR0Off | Algorithm   | PB Range               | Time < Key   | Panorama    | Pan < Key   | Pan < Rnd'                                   ,
       'Bank0 | nGR1Off | Pe Amount   | Spread                 | Transpose    | Pe Loop     | Pe Retrig   | Pe A Slope      | Pe D Slope   | Pe R Slope' ,
       'Bank0 | nGR2Off | Pe Attack   | Pe Decay               | Pe Release   | Pe R < Vel  | Pe Init     | Pe Peak         | Pe Sustain'                ,
       'Bank0 | nGR3Off | Pe Mode     | Pe End                 | Pe Amt A     | Pe Amt B    | Pe Dst B    | Glide Time'                                  ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank0 | nMB0Off | Device On   | Preset Prev            | Osc-A On     | A Fix On_   | Pe On       | LFO < Pe        | Glide On'                  ,
       'Bank0 | nMB1Off | Preset Save | Preset Next            | Osc-A Retrig | A Quantize  | Osc-A < Pe  | Osc-B < Pe      | Osc-C < Pe   | Osc-D < Pe' ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank0 | nMR0Off | A Coarse    | A Fine                 | Osc-A Level  | Ae Loop     | Ae Retrig   | A Freq<Vel      | Osc-A Wave   | Time'       ,
       'Bank0 | nMR1Off | A Fix Freq  | A Fix Freq Mul         | Ae Attack    | Ae Decay    | Ae Release  | Ae R < Vel      | Osc-A Feedb  | Tone'       ,
       'Bank0 | nMR2Off | Ae Mode     | Osc-A Lev < Key        | Ae Init      | Ae Peak     | Ae Sustain  | Osc-A Lev < Vel | Osc-A Phase  | Volume'     ,
       #==================================================================================================================================================
       'Bank1 | nMB0Off | Osc-B On    | B Fix On_              | Osc-B Retrig | B Quantize'                                                              ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank1 | nMR0Off | B Coarse    | B Fine                 | Osc-B Level  | Be Loop     | Be Retrig   | B Freq<Vel      | Osc-B Wave   | -'          ,
       'Bank1 | nMR1Off | B Fix Freq  | B Fix Freq Mul         | Be Attack    | Be Decay    | Be Release  | Be R < Vel      | Osc-B Feedb  | -'          ,
       'Bank1 | nMR2Off | Be Mode     | Osc-B Lev < Key        | Be Init      | Be Peak     | Be Sustain  | Osc-B Lev < Vel | Osc-B Phase  | -'          ,
       #==================================================================================================================================================
       'Bank2 | nMB0Off | Osc-C On    | C Fix On_              | Osc-C Retrig | C Quantize'                                                              ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank2 | nMR0Off | C Coarse    | C Fine                 | Osc-C Level  | Ce Loop     | Ce Retrig   | C Freq<Vel      | Osc-C Wave   | -'          ,
       'Bank2 | nMR1Off | C Fix Freq  | C Fix Freq Mul         | Ce Attack    | Ce Decay    | Ce Release  | Ce R < Vel      | Osc-C Feedb  | -'          ,
       'Bank2 | nMR2Off | Ce Mode     | Osc-C Lev < Key        | Ce Init      | Ce Peak     | Ce Sustain  | Osc-C Lev < Vel | Osc-C Phase  | -'          ,
       #==================================================================================================================================================
       'Bank3 | nMB0Off | Osc-D On    | D Fix On_              | Osc-D Retrig | D Quantize'                                                              ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank3 | nMR0Off | D Coarse    | D Fine                 | Osc-D Level  | De Loop     | De Retrig   | D Freq<Vel      | Osc-D Wave   | -'          ,
       'Bank3 | nMR1Off | D Fix Freq  | D Fix Freq Mul         | De Attack    | De Decay    | De Release  | De R < Vel      | Osc-D Feedb  | -'          ,
       'Bank3 | nMR2Off | De Mode     | Osc-D Lev < Key        | De Init      | De Peak     | De Sustain  | Osc-D Lev < Vel | Osc-D Phase  | -'          ,
       #==================================================================================================================================================
       'Bank4 | nGR0Off | Fe A Slope  | Fe D Slope             | Fe R Slope'                                                                             ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank4 | nGR0Off | Filter Type | Filter Circuit - LP/HP | Filter Freq  | Filter Res  | Filter Drive | Fe Loop        | Fe Retrig'                 ,
       'Bank4 | nGR1Off | Fe Attack   | Fe Decay               | Fe Release   | Fe R < Vel  | Fe Init      | Fe Peak        | Fe Sustain   | Fe Amount  ',
       'Bank4 | nGR2Off | Fe Mode     | Fe End                 | Filter Morph | Filt < Vel  | Filt < Key   | Shaper Type    | Shaper Drive | Shaper Mix' ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank4 | nMB0Off | LFO On      | LFO Retrigger          | Osc-A < LFO  | Osc-B < LFO | Osc-C < LFO | Osc-D < LFO'                                 ,
       'Bank4 | nMB1Off | Filter On   | Filter Slope           | Filt < LFO   | Filter Circuit - BP/NO/Morph'                                            ,
       #--------------------------------------------------------------------------------------------------------------------------------------------------
       'Bank4 | nMR0Off | LFO Type    | LFO Range              | LFO Rate     | LFO Sync    | LFO Amt     | Le Loop         | Le Retrig    | -'          ,
       'Bank4 | nMR1Off | Le Attack   | Le Decay               | Le Release   | Le R < Vel  | Le Init     | Le Peak         | Le Sustain   | -'          ,
       'Bank4 | nMR2Off | Le Mode     | Le End                 | LFO Amt A    | LFO Amt B   | LFO Dst B   | LFO R < K       | LFO < Vel    | -'          ,
    ]
    self.reg('Operator')
    self.parse_cfg()

#=======================================================================
# Class: Operator, Device: Operator, Display: Operator
# Q param: "Device On", orig: "Device On" => [Off, On]
# Q param: "Osc-A On", orig: "Osc-A On" => [Off, On]
# Q param: "A Fix On ", orig: "A Fix On " => [Off, On]
# Q param: "Osc-A Retrig", orig: "Osc-A Retrig" => [Off, On]
# Q param: "A Quantize", orig: "A Quantize" => [Off, On]
#   param: "A Coarse", orig: "A Coarse", value: 1.000000, min: 0.000000, max: 48.000000
#   param: "A Fine", orig: "A Fine", value: 0.000000, min: 0.000000, max: 1000.000000
#   param: "Osc-A Level", orig: "Osc-A Level", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ae Loop", orig: "Ae Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Ae Retrig", orig: "Ae Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "A Freq<Vel", orig: "A Freq<Vel", value: 0.000000, min: -100.000000, max: 100.000000
# Q param: "Osc-A Wave", orig: "Osc-A Wave" => [Sine, Sine 4 Bit, Sine 8 Bit, Saw 3, Saw 4, Saw 6, Saw 8, Saw 16, Saw 32, Saw 64, Saw D, Square 3, Square 4, Square 6, Square 8, Square 16, Square 32, Square 64, Square D, Triangle, Noise Looped, Noise White, User]
#   param: "Time", orig: "Time", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "A Fix Freq", orig: "A Fix Freq", value: 0.434588, min: 0.000000, max: 1.000000
#   param: "A Fix Freq Mul", orig: "A Fix Freq Mul", value: 4.000000, min: 0.000000, max: 5.000000
#   param: "Ae Attack", orig: "Ae Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ae Decay", orig: "Ae Decay", value: 0.627858, min: 0.000000, max: 1.000000
#   param: "Ae Release", orig: "Ae Release", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "Ae R < Vel", orig: "Ae R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Osc-A Feedb", orig: "Osc-A Feedb", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "Tone", orig: "Tone", value: 0.700000, min: 0.000000, max: 1.000000
# Q param: "Ae Mode", orig: "Ae Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Osc-A Lev < Key", orig: "Osc-A Lev < Key", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Ae Init", orig: "Ae Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ae Peak", orig: "Ae Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ae Sustain", orig: "Ae Sustain", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Osc-A Lev < Vel", orig: "Osc-A Lev < Vel", value: 50.000000, min: -100.000000, max: 100.000000
#   param: "Osc-A Phase", orig: "Osc-A Phase", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "Volume", orig: "Volume", value: 0.400000, min: 0.000000, max: 1.000000
# Q param: "Osc-B On", orig: "Osc-B On" => [Off, On]
# Q param: "B Fix On ", orig: "B Fix On " => [Off, On]
# Q param: "Osc-B Retrig", orig: "Osc-B Retrig" => [Off, On]
# Q param: "B Quantize", orig: "B Quantize" => [Off, On]
#   param: "B Coarse", orig: "B Coarse", value: 1.000000, min: 0.000000, max: 48.000000
#   param: "B Fine", orig: "B Fine", value: 0.000000, min: 0.000000, max: 1000.000000
#   param: "Osc-B Level", orig: "Osc-B Level", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Be Loop", orig: "Be Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Be Retrig", orig: "Be Retrig", value: 3.000000, min: 0.000000, max: 14.000000
# Q param: "Osc-B Wave", orig: "Osc-B Wave" => [Sine, Sine 4 Bit, Sine 8 Bit, Saw 3, Saw 4, Saw 6, Saw 8, Saw 16, Saw 32, Saw 64, Saw D, Square 3, Square 4, Square 6, Square 8, Square 16, Square 32, Square 64, Square D, Triangle, Noise Looped, Noise White, User]
#   param: "B Fix Freq", orig: "B Fix Freq", value: 0.434588, min: 0.000000, max: 1.000000
#   param: "B Fix Freq Mul", orig: "B Fix Freq Mul", value: 4.000000, min: 0.000000, max: 5.000000
#   param: "Be Attack", orig: "Be Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Be Decay", orig: "Be Decay", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "Be Release", orig: "Be Release", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "Be R < Vel", orig: "Be R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Osc-B Feedb", orig: "Osc-B Feedb", value: 0.000000, min: 0.000000, max: 100.000000
# Q param: "Be Mode", orig: "Be Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Osc-B Lev < Key", orig: "Osc-B Lev < Key", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Be Init", orig: "Be Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Be Peak", orig: "Be Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Be Sustain", orig: "Be Sustain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "Osc-B Lev < Vel", orig: "Osc-B Lev < Vel", value: 50.000000, min: -100.000000, max: 100.000000
#   param: "Osc-B Phase", orig: "Osc-B Phase", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "B Freq<Vel", orig: "B Freq<Vel", value: 0.000000, min: -100.000000, max: 100.000000
# Q param: "Osc-C On", orig: "Osc-C On" => [Off, On]
# Q param: "C Fix On ", orig: "C Fix On " => [Off, On]
# Q param: "Osc-C Retrig", orig: "Osc-C Retrig" => [Off, On]
# Q param: "C Quantize", orig: "C Quantize" => [Off, On]
#   param: "C Coarse", orig: "C Coarse", value: 1.000000, min: 0.000000, max: 48.000000
#   param: "C Fine", orig: "C Fine", value: 0.000000, min: 0.000000, max: 1000.000000
#   param: "Osc-C Level", orig: "Osc-C Level", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ce Loop", orig: "Ce Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Ce Retrig", orig: "Ce Retrig", value: 3.000000, min: 0.000000, max: 14.000000
# Q param: "Osc-C Wave", orig: "Osc-C Wave" => [Sine, Sine 4 Bit, Sine 8 Bit, Saw 3, Saw 4, Saw 6, Saw 8, Saw 16, Saw 32, Saw 64, Saw D, Square 3, Square 4, Square 6, Square 8, Square 16, Square 32, Square 64, Square D, Triangle, Noise Looped, Noise White, User]
#   param: "C Fix Freq", orig: "C Fix Freq", value: 0.434588, min: 0.000000, max: 1.000000
#   param: "C Fix Freq Mul", orig: "C Fix Freq Mul", value: 4.000000, min: 0.000000, max: 5.000000
#   param: "Ce Attack", orig: "Ce Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ce Decay", orig: "Ce Decay", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "Ce Release", orig: "Ce Release", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "Ce R < Vel", orig: "Ce R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Osc-C Feedb", orig: "Osc-C Feedb", value: 0.000000, min: 0.000000, max: 100.000000
# Q param: "Ce Mode", orig: "Ce Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Osc-C Lev < Key", orig: "Osc-C Lev < Key", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Ce Init", orig: "Ce Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Ce Peak", orig: "Ce Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Ce Sustain", orig: "Ce Sustain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "Osc-C Lev < Vel", orig: "Osc-C Lev < Vel", value: 50.000000, min: -100.000000, max: 100.000000
#   param: "Osc-C Phase", orig: "Osc-C Phase", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "C Freq<Vel", orig: "C Freq<Vel", value: 0.000000, min: -100.000000, max: 100.000000
# Q param: "Osc-D On", orig: "Osc-D On" => [Off, On]
# Q param: "D Fix On ", orig: "D Fix On " => [Off, On]
# Q param: "Osc-D Retrig", orig: "Osc-D Retrig" => [Off, On]
# Q param: "D Quantize", orig: "D Quantize" => [Off, On]
#   param: "D Coarse", orig: "D Coarse", value: 1.000000, min: 0.000000, max: 48.000000
#   param: "D Fine", orig: "D Fine", value: 0.000000, min: 0.000000, max: 1000.000000
#   param: "Osc-D Level", orig: "Osc-D Level", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "De Loop", orig: "De Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "De Retrig", orig: "De Retrig", value: 3.000000, min: 0.000000, max: 14.000000
# Q param: "Osc-D Wave", orig: "Osc-D Wave" => [Sine, Sine 4 Bit, Sine 8 Bit, Saw 3, Saw 4, Saw 6, Saw 8, Saw 16, Saw 32, Saw 64, Saw D, Square 3, Square 4, Square 6, Square 8, Square 16, Square 32, Square 64, Square D, Triangle, Noise Looped, Noise White, User]
#   param: "D Fix Freq", orig: "D Fix Freq", value: 0.434588, min: 0.000000, max: 1.000000
#   param: "D Fix Freq Mul", orig: "D Fix Freq Mul", value: 4.000000, min: 0.000000, max: 5.000000
#   param: "De Attack", orig: "De Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "De Decay", orig: "De Decay", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "De Release", orig: "De Release", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "De R < Vel", orig: "De R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Osc-D Feedb", orig: "Osc-D Feedb", value: 0.000000, min: 0.000000, max: 100.000000
# Q param: "De Mode", orig: "De Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Osc-D Lev < Key", orig: "Osc-D Lev < Key", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "De Init", orig: "De Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "De Peak", orig: "De Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "De Sustain", orig: "De Sustain", value: 0.400000, min: 0.000000, max: 1.000000
#   param: "Osc-D Lev < Vel", orig: "Osc-D Lev < Vel", value: 50.000000, min: -100.000000, max: 100.000000
#   param: "Osc-D Phase", orig: "Osc-D Phase", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "D Freq<Vel", orig: "D Freq<Vel", value: 0.000000, min: -100.000000, max: 100.000000
# Q param: "LFO On", orig: "LFO On" => [Off, On]
# Q param: "LFO Retrigger", orig: "LFO Retrigger" => [Off, On]
# Q param: "Osc-A < LFO", orig: "Osc-A < LFO" => [Off, On]
# Q param: "Osc-B < LFO", orig: "Osc-B < LFO" => [Off, On]
# Q param: "Osc-C < LFO", orig: "Osc-C < LFO" => [Off, On]
# Q param: "Osc-D < LFO", orig: "Osc-D < LFO" => [Off, On]
# Q param: "LFO Type", orig: "LFO Type" => [Sine, Square, Triangle, SwUp, SwDown, S&H, Noise]
# Q param: "LFO Range", orig: "LFO Range" => [Low, High, Sync]
#   param: "LFO Rate", orig: "LFO Rate", value: 100.000000, min: 0.000000, max: 127.000000
#   param: "LFO Sync", orig: "LFO Sync", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "LFO Amt", orig: "LFO Amt", value: 0.100000, min: 0.000000, max: 1.000000
#   param: "Le Loop", orig: "Le Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Le Retrig", orig: "Le Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Le Attack", orig: "Le Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Le Decay", orig: "Le Decay", value: 0.581428, min: 0.000000, max: 1.000000
#   param: "Le Release", orig: "Le Release", value: 0.355571, min: 0.000000, max: 1.000000
#   param: "Le R < Vel", orig: "Le R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Le Init", orig: "Le Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Le Peak", orig: "Le Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Le Sustain", orig: "Le Sustain", value: 1.000000, min: 0.000000, max: 1.000000
# Q param: "Le Mode", orig: "Le Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Le End", orig: "Le End", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO Amt A", orig: "LFO Amt A", value: 100.000000, min: -100.000000, max: 100.000000
# Q param: "LFO Dst B", orig: "LFO Dst B" => [Off, OSC Volume A, OSC Volume B, OSC Volume C, OSC Volume D, OSC Crossfade A/C, OSC Crossfade B/D, OSC Feedback, OSC Fixed Frequency, FM Drive, Filter Freq, Filter Q (Legacy), Filter Res, Filter Morph, Filter Drive, Filter Envelope Amount, Shaper Drive, LFO Rate, LFO Amount, Aux Envelope Amount, Volume, Panorama, Tone, Time]
#   param: "LFO Amt B", orig: "LFO Amt B", value: 100.000000, min: -100.000000, max: 100.000000
#   param: "LFO R < K", orig: "LFO R < K", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "LFO < Vel", orig: "LFO < Vel", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Fe Loop", orig: "Fe Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Fe Retrig", orig: "Fe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
# Q param: "Filter On", orig: "Filter On" => [Off, On]
# Q param: "Filter Slope", orig: "Filter Slope" => [12 dB, 24 dB]
# Q param: "Filt < LFO", orig: "Filt < LFO" => [Off, On]
# Q param: "Filter Circuit - BP/NO/Morph", orig: "Filter Circuit - BP/NO/Morph" => [Clean, OSR]
# Q param: "Filter Type", orig: "Filter Type" => [Lowpass, Highpass, Bandpass, Notch, Morph]
# Q param: "Filter Circuit - LP/HP", orig: "Filter Circuit - LP/HP" => [Clean, OSR, MS2, SMP, PRD]
#   param: "Filter Freq", orig: "Filter Freq", value: 0.932621, min: 0.000000, max: 1.000000
#   param: "Filter Res", orig: "Filter Res", value: 0.277778, min: 0.000000, max: 1.250000
#   param: "Fe Amount", orig: "Fe Amount", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Fe A Slope", orig: "Fe A Slope", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Fe D Slope", orig: "Fe D Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Fe R Slope", orig: "Fe R Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Fe Attack", orig: "Fe Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fe Decay", orig: "Fe Decay", value: 0.581428, min: 0.000000, max: 1.000000
#   param: "Fe Release", orig: "Fe Release", value: 0.355571, min: 0.000000, max: 1.000000
#   param: "Fe R < Vel", orig: "Fe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Fe Init", orig: "Fe Init", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Fe Peak", orig: "Fe Peak", value: 1.000000, min: 0.000000, max: 1.000000
#   param: "Fe Sustain", orig: "Fe Sustain", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter Drive", orig: "Filter Drive", value: 0.000000, min: 0.000000, max: 24.000000
# Q param: "Fe Mode", orig: "Fe Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Fe End", orig: "Fe End", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filter Morph", orig: "Filter Morph", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Filt < Vel", orig: "Filt < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Filt < Key", orig: "Filt < Key", value: 100.000000, min: -200.000000, max: 200.000000
# Q param: "Shaper Type", orig: "Shaper Type" => [Off, Soft, Hard, Sine, 4Bit]
#   param: "Shaper Drive", orig: "Shaper Drive", value: 0.000000, min: -12.000000, max: 12.000000
#   param: "Shaper Mix", orig: "Shaper Mix", value: 100.000000, min: 0.000000, max: 100.000000
# Q param: "Pe On", orig: "Pe On" => [Off, On]
# Q param: "LFO < Pe", orig: "LFO < Pe" => [Off, On]
# Q param: "Glide On", orig: "Glide On" => [Off, On]
# Q param: "Osc-A < Pe", orig: "Osc-A < Pe" => [Off, On]
# Q param: "Osc-B < Pe", orig: "Osc-B < Pe" => [Off, On]
# Q param: "Osc-C < Pe", orig: "Osc-C < Pe" => [Off, On]
# Q param: "Osc-D < Pe", orig: "Osc-D < Pe" => [Off, On]
# Q param: "Algorithm", orig: "Algorithm" => [Alg. 1, Alg. 2, Alg. 3, Alg. 4, Alg. 5, Alg. 6, Alg. 7, Alg. 8, Alg. 9, Alg. 10, Alg. 11]
#   param: "PB Range", orig: "PB Range", value: 5.000000, min: 0.000000, max: 24.000000
#   param: "Time < Key", orig: "Time < Key", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Panorama", orig: "Panorama", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pan < Key", orig: "Pan < Key", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "Pan < Rnd", orig: "Pan < Rnd", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "Pe Amount", orig: "Pe Amount", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Spread", orig: "Spread", value: 0.000000, min: 0.000000, max: 100.000000
#   param: "Transpose", orig: "Transpose", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Pe Loop", orig: "Pe Loop", value: 0.539794, min: 0.000000, max: 1.000000
#   param: "Pe Retrig", orig: "Pe Retrig", value: 3.000000, min: 0.000000, max: 14.000000
#   param: "Pe A Slope", orig: "Pe A Slope", value: 0.000000, min: -1.000000, max: 1.000000
#   param: "Pe D Slope", orig: "Pe D Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Pe R Slope", orig: "Pe R Slope", value: 1.000000, min: -1.000000, max: 1.000000
#   param: "Pe Attack", orig: "Pe Attack", value: 0.000000, min: 0.000000, max: 1.000000
#   param: "Pe Decay", orig: "Pe Decay", value: 0.544575, min: 0.000000, max: 1.000000
#   param: "Pe Release", orig: "Pe Release", value: 0.355571, min: 0.000000, max: 1.000000
#   param: "Pe R < Vel", orig: "Pe R < Vel", value: 0.000000, min: -100.000000, max: 100.000000
#   param: "Pe Init", orig: "Pe Init", value: 12.000000, min: -48.000000, max: 48.000000
#   param: "Pe Peak", orig: "Pe Peak", value: 12.000000, min: -48.000000, max: 48.000000
#   param: "Pe Sustain", orig: "Pe Sustain", value: 0.000000, min: -48.000000, max: 48.000000
# Q param: "Pe Mode", orig: "Pe Mode" => [None, Loop, Beat, Sync, Trigger]
#   param: "Pe End", orig: "Pe End", value: 0.000000, min: -48.000000, max: 48.000000
#   param: "Pe Amt A", orig: "Pe Amt A", value: 100.000000, min: -100.000000, max: 100.000000
#   param: "Pe Amt B", orig: "Pe Amt B", value: 100.000000, min: -100.000000, max: 100.000000
# Q param: "Pe Dst B", orig: "Pe Dst B" => [Off, OSC Volume A, OSC Volume B, OSC Volume C, OSC Volume D, OSC Crossfade A/C, OSC Crossfade B/D, OSC Feedback, OSC Fixed Frequency, FM Drive, Filter Freq, Filter Q (Legacy), Filter Res, Filter Morph, Filter Drive, Filter Envelope Amount, Shaper Drive, LFO Rate, LFO Amount, Aux Envelope Amount, Volume, Panorama, Tone, Time]
#   param: "Glide Time", orig: "Glide Time", value: 0.539794, min: 0.000000, max: 1.000000
