# AaMidiOscControllers

MIDI-OSC controller scripts for Ableton Live 12.

The scripts in AaMidiControllers were not compatible with the new series of MacBook Pro computers
with Max chips. Therefore I developed these new scripts that use a raspberry-pi as a bridge
to convert MIDI to OSC and (controllers -> MacBook) and OSC to MIDI (MacBook -> controllers).

With these scripts you can control 4 different types of MIDI controllers:

1) AaBCF: Behringer BCF2000 B-Control Fader MIDI Control Surface
   * With 8 motorized faders, 16 buttons, 8 encoder-buttons, 4 modes and 16 banks
2) AaBCR: Behringer BCR2000 B-Control Rotary MIDI Control Surface
   * With 32 encoders, 16 buttons, 8 encoder-buttons, 4 modes and 16 banks
3) AaWfd: SubZero MiniControl MIDI-Kontroller
   * With 9 volume faders, 1 channels fader, 9 buttons and 4 banks
4) AaMatrix: Novation Launchpad Mini MK3
   * With 8 x 8 pad, 8 top and 8 side RGB buttons

A new Open Stage Control touch-screen application is also available:

5) AaTouch:
   * 32 x 12 beat grid buttons - MIDI piano roll
   * 32 x 8  (tracks x scenes) for playing clips

With these scripts both the AaMatrix and AaTouch can communicate with the BCF2000 in order to
sync the tracks' faders.

The BCR2000 is programmed to support up to 6 MIDI channels with 56 encoders (32 + 24),
giving you the possibility to change 336 parameters quickly!

# Instructions

Download Open Stage Control from:
* https://openstagecontrol.ammd.net/download/
  * Node.js (5M) -> open-stage-control_1.28.5_node.zip

* Replace css file in "assets" folder (in order to hide buttons numbers)
  * open-stage-control.css

# Starting the MIDI-OSC bridges

1. Use "fix-pi.rb" script in order to look for MacBook and RaspberryPi ip-addresses
   when using a wired ethernet connection (MacBook dongle)

2. Use "run.sh" in order to start the Open-Stage-Control server

Enjoy!

Hiram Galicia - hiramegl@yahoo.com

