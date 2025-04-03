#!/bin/sh

# ******************************************************************************
# This script starts the Open Stage Control server which is used as a bridge
# between the GUI interface of AaTouch and Ableton Live.
#
# Parameters:
# -p 8080              -> http port where the Open Source Control server
#                         will be available to open in a web browser
# -s 127.0.0.1:2726    -> address and port where the OSC messages will be sent
#                         (i.e., where Ableton Live will be listening to)
# -l "./AaTouch.json"  -> path of the AaTouch GUI session file
# -o 2727              -> OSC input port for the Open Stage Control server
#                         (i.e., where Ableton Live will be sending from)
# -d                   -> debug (log received OSC messages in the console)
# -n                   -> disable default GUI
#
# More options at: http://osc.ammd.net/getting-started/
# ******************************************************************************

# configuration
HTTP_PORT=8080
OSC_RX_PORT=2727
OSC_TX_ADDR=127.0.0.1
OSC_TX_PORT=2726

# command
node index.js \
   -l "./AaTouch.json" \
   -p $HTTP_PORT \
   -o $OSC_RX_PORT \
   -s $OSC_TX_ADDR:$OSC_TX_PORT \
   --no-qrcode \
   -n \
   -d

