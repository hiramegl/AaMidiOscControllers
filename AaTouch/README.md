# Ableton Live OSC controller for touchscreen

Client is a Raspberry-Pi with a touchscreen unit.

Touchscreen dimensions: 1366 x 768 pixels - 15.6"

## Features

* Script in MacBook folder to detect IP addresses of MacBook and Raspberry-Pi
  and start scripts
* Script in MacBook folder to start the Open Stage Control session

## Sequencer mode features:
* 32 bits x 12 notes piano roll grid (8 beats = 2 bars, every beat = 4 bits)
* Update GUI when notes change
* update correctly bits when loop start changes (it should be shifted left-right)
* move notes in Live and update GUI
* Region selection indicators / BIT CMD Operator
* zoom map
* len & vel selection
* scale selection (chromatic & extended)
* Loop
  - Roll 1/8, 1/4 -> Loop Button
* Clip tools:
  - Follow toggle
* Shift notes: left, right, up and down
* Note selection (chromatic)
  - Master note selection (chromatic)
* BitOp
* Note selection (with scale)
  - Master note selection (with scale)
* Grid handle scales and roots
* Bit Commands:
  - All: Mute Solo VelRst Del
  - Sel: Mute Solo VelRst Del
* Shift Commands:
  - All: Left Right Down Up
  - Sel: Left Right Down Up
* Fact & Chop Commands:
  - All: Div Mul 2 3
  - Sel: Div Mul 2 3
* Rhythms
* Sel Clip play
* Sel Track Stop
* Sel Track Mute
* Sel Track Solo
* BitOp Cmd:
  Mul, Div, Chop2, Chop3
* Clip Navigation
* Chords
* Transpose
* Warp
* Crop
* Roll: beat and half beat
* Clip tools:
  * Loop toggle, loop dupl, clip dupl
  * CLIP/DEV toggle, LOOP/ENV toggle
* Bit Encoders Modes:
  * Time shift
  * Len
  * Vel
  * Reset
* Bit Encoders
* Master Encoder
* Encoder Modes
* sel track sends

## Session mode features:
* Clips mode: 32 tracks x 8 scenes
* Zoom map
* Sends mode
* grid   mode: SELECT / FIRE
* launch mode: FIRE / FIRE & SELECT
* clips listeners
* when adding/removing tracks
* when adding/removing scenes
  * stop
  * mute
  * solo
  * monitoring
  * arm
  * select
  * pan reset
  * A/B cross
  * vol 0 dB
  * vol -inf dB
  * sends off
  * select
* Volumes
* Loop Extra
* Coarse detune + reset
* Fine detune + reset
* Audio gain
* reset detunes & gain
* Audio gain selected clip listener
* Faders picker
* Sync volumes (fix track listeners for volumes)

