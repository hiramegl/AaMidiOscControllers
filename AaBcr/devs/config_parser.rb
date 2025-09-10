require 'fileutils';
require 'yaml'

FileUtils.mkdir_p("doc")

# parsing methods ******************************************
def get_name(psDev)
  hNames = {
    'Vocoder'              => 'Vocoder',                # Bank 0
    'Overdrive'            => 'Overdrive',
    'Eq8'                  => 'EQ-8',
    'BeatRepeat'           => 'Beat Repeat',            # Bank 1
    'Resonator'            => 'Resonators',
    'AutoPan'              => 'Auto Pan',               # Bank 2
    'Echo'                 => 'Echo',
    'Delay'                => 'Delay',                  # Bank 3
    'FilterDelay'          => 'Filter Delay',
    'Chorus2'              => 'Chorus<br/>Ensemble',
    'PhaserNew'            => 'Phaser<br/>Flanger',     # Bank 4
    'Transmute'            => 'Spectral<br/>Resonator',
    'Reverb'               => 'Reverb',                 # Bank 5
    'Compressor2'          => 'Compressor',
    'FilterEQ3'            => 'EQ-3',
    'Redux2'               => 'Redux',
    'MidiPitcher'          => 'Pitcher',                # Bank 0 (for all insruments)
    'MidiVelocity'         => 'Velocity',
    'MidiArpeggiator'      => 'Arpeggiator',
    'UltraAnalog'          => 'Analog',
    'Collision'            => 'Collision',
    'Drift'                => 'Drift',
    'LoungeLizard'         => 'Electric',
    'InstrumentMeld'       => 'Meld',
    'Operator'             => 'Operator',
    'MultiSampler'         => 'Sampler',
    'OriginalSimpler'      => 'Simpler',
    'StringStudio'         => 'Tension',
    'InstrumentVector'     => 'Wavetable',
    'InstrumentGroupDevice'=> 'InstGroup',
    'DrumGroupDevice'      => 'DrumGroup',
  }
  hNames[psDev]
end

def get_style(psParam)
  {
    /Device On/   => ' device-on',
    /Preset Save/ => ' preset-save',
    /Preset Prev/ => ' preset-prev',
    /Preset Next/ => ' preset-next',
    /Dry.?Wet/    => ' dry-wet',
    /^\+/         => ' extra',
    /^-$/         => ' empty',
    /./           => '',
  }.map { |reStyle, sStyle|
    psParam =~ reStyle ? sStyle : nil
  }.compact.first
end

def get_param(psParam, psDev)
  {
    /Device On/   => "⏻ #{get_name(psDev)}",
    /^\+/         => psParam[1..-1],
    /Preset Save/ => 'Preset 💾',
    /Preset Prev/ => 'Preset ⬆︎',
    /Preset Next/ => 'Preset ⬇︎',
    /^-$/         => '&nbsp;',
    /./           => psParam,
  }.map { |rePatt, sParam|
    psParam =~ rePatt ? sParam : nil
  }.compact.first
end

def parse_params(paPrms, psDev)
  paPrms.
    map { |sParam|
      sStyle = get_style(sParam)
      sParam = get_param(sParam, psDev)
      "<td class='#{psDev}#{sStyle}'>#{sParam}</td>"
    }
end

def parse_line(psLine, psDev)
  psLine =~ /'(.*)'/
  sCfgLine = $1.strip
  aCfg = sCfgLine.split(/\s*\|\s*/)
  sBank = aCfg[0][-1]
  sGrp  = aCfg[1][1..3]
  aPrms = aCfg[2..-1]

  # parse sGrp
  sType = sGrp[0] == 'G' ? 'Group'  : 'Main'
  sCtrl = sGrp[1] == 'B' ? 'Button' : 'Rotary'
  sRow  = sGrp[2]

  [
    sBank.to_i,
    sType,
    sCtrl,
    sRow,
    parse_params(aPrms, psDev),
    aPrms.length
  ]
end

def parse_text(psText, psDev)
  aBanks = []

  psText =~ /self\.m_lCfg = \[(.*?)\]/m
  $1.strip.each_line { |sLine|
    sLine.strip!
    next if sLine[0] == '#' # ignore comments
    nBank, sType, sCtrl, sRow, aPrms, nStrips = parse_line(
      sLine,
      psDev)

    aBanks[nBank] = {nStrips: 0} unless aBanks[nBank]
    hBank = aBanks[nBank]
    hBank[sType] = {} unless hBank[sType]
    hType = hBank[sType]
    hType[sCtrl] = {} unless hType[sCtrl]
    hCtrl = hType[sCtrl]
    hCtrl[sRow] = aPrms

    hBank[:nStrips] = nStrips if nStrips > hBank[:nStrips]
  }

  aBanks # return the array of banks
end

# main parsing loop ****************************************

hCfgs = {}

puts('Scanning instruments')
Dir.glob("*.py").
  sort.
  each { |sPath|
  next if sPath =~ /.rb$|.html$/; # do not scan theses files
  sText = File.read(sPath);

  if sText =~/from \.Dev import Dev/
    puts("  - '#{sPath}'")
    sPath.slice!('.py') # remove extension
    aBanks = parse_text(sText, sPath)
    hCfgs[sPath] = aBanks
  end
}

# util methods *********************************************

def new_empty_bank
  sDefault = '<td class="empty"></td>'
  {
    'Group' => {
      'Button' => {
        '0' => Array.new(8, sDefault),
        '1' => Array.new(8, sDefault),
        '2' => Array.new(8, sDefault),
        '3' => Array.new(8, sDefault),
      },
      'Rotary' => {
        '0' => Array.new(8, sDefault),
        '1' => Array.new(8, sDefault),
        '2' => Array.new(8, sDefault),
        '3' => Array.new(8, sDefault),
      }
    },
    'Main' => {
      'Button' => {
        '0' => Array.new(8, sDefault),
        '1' => Array.new(8, sDefault),
      },
      'Rotary' => {
        '0' => Array.new(8, sDefault),
        '1' => Array.new(8, sDefault),
        '2' => Array.new(8, sDefault),
      }
    },
  }
end


# effects banks ********************************************

puts('> Grouping Audio Effects')
hFxBanks  = {}
nBank     = 0
nOffset   = 0
[
  'Vocoder'    , # => 3, # Bank 0
  'Overdrive'  , # => 1,
  'Eq8'        , # => 4,
  'BeatRepeat' , # => 2, # Bank 1
  'Resonator'  , # => 6,
  'AutoPan'    , # => 2, # Bank 2
  'Echo'       , # => 6,
  'Delay'      , # => 2, # Bank 3
  'FilterDelay', # => 4,
  'Chorus2'    , # => 2,
  'PhaserNew'  , # => 4, # Bank 4
  'Transmute'  , # => 4,
  'Reverb'     , # => 3, # Bank 5
  'Compressor2', # => 2,
  'FilterEQ3'  , # => 1,
  'Redux2'     , # => 1,
].each { |sEffect|
  hFxBanks[nBank] = new_empty_bank unless hFxBanks[nBank]
  hFxCfg = hCfgs[sEffect][0] # audio effects have only one bank always, bank[0]

  nStrips = hFxCfg.delete(:nStrips) # extract number of strips
  puts("  - #{sEffect} [#{nStrips}]")

  hFxCfg.each { |sType, hType|
    hType.each { |sCtrl, hCtrl|
      hCtrl.each { |sRow, aRow|
        aRow.each_index { |nStrip|
          hFxBanks[nBank][sType][sCtrl][sRow][nOffset + nStrip] = aRow[nStrip]
        }
      }
    }
  }

  nOffset += nStrips
  if nOffset >= 8
    nBank += 1
    nOffset = 0
  end
}
#puts(hFxBanks.to_yaml)

aMidiFx = [
  'MidiPitcher'    , # => 2, # Bank 0
  'MidiVelocity'   , # => 3,
  'MidiArpeggiator', # => 3,
]

hInstruments = {
  'UltraAnalog'          => 'Analog',
  'Collision'            => 'Collision',
  'Drift'                => 'Drift',
  'LoungeLizard'         => 'Electric',
  'InstrumentMeld'       => 'Meld',
  'Operator'             => 'Operator',
  'MultiSampler'         => 'Sampler',
  'OriginalSimpler'      => 'Simpler',
  'StringStudio'         => 'Tension',
  'InstrumentVector'     => 'Wavetabl',
  'InstrumentGroupDevice'=> 'InstGrp',
  'DrumGroupDevice'      => 'DrumGrp',
}

# instruments banks ****************************************

puts('> Grouping MIDI Effects and Instruments')
hInsBanks = {}
hInstruments.each { |sInstrument, sDisplayName|
  puts("  - #{sInstrument} [#{sDisplayName}]")
  hInsBanks[sInstrument] = [] unless hInsBanks[sInstrument]
  aSrcInstr = hCfgs    [sInstrument]
  aDstInstr = hInsBanks[sInstrument]
  nBank     = 0
  nOffset   = 0

  # add midi effects in the first bank
  aMidiFx.each { |sEffect|
    aDstInstr[nBank] = new_empty_bank unless aDstInstr[nBank]
    hDstBank = aDstInstr[0]

    hMidiCfg = hCfgs[sEffect][0] # midi effects have only one bank always, bank[0]
    nStrips = hMidiCfg[:nStrips] # extract number of strips
    #puts("> #{sEffect} [#{nStrips}]")

    hMidiCfg.each { |sType, hType|
      next if sType == :nStrips
      hType.each { |sCtrl, hCtrl|
        hCtrl.each { |sRow, aRow|
          aRow.each_index { |nStrip|
            hDstBank[sType][sCtrl][sRow][nOffset + nStrip] = aRow[nStrip]
          }
        }
      }
    }

    nOffset += nStrips
    if nOffset >= 8
      nBank += 1
      nOffset = 0
    end
  }

  # add the instrument banks in the following banks
  aSrcInstr.each { |hSrcBank|
    nStrips  = hSrcBank.delete(:nStrips) # extract number of strips
    aDstInstr[nBank] = new_empty_bank unless aDstInstr[nBank]
    hDstBank = aDstInstr[nBank]

    hSrcBank.each { |sType, hType|
      hType.each { |sCtrl, hCtrl|
        hCtrl.each { |sRow, aRow|
          aRow.each_index { |nStrip|
            hDstBank[sType][sCtrl][sRow][nOffset + nStrip] = aRow[nStrip]
          }
        }
      }
    }

    nOffset += nStrips
    if nOffset >= 8
      nBank += 1
      nOffset = 0
    end
  }
}
#puts(hInsBanks.to_yaml)

aAudioFxViews = [
  %w(Vocoder Overdrive Eq8),
  %w(BeatRepeat Resonator),
  %w(AutoPan Echo),
  %w(Delay FilterDelay Chorus2),
  %w(PhaserNew Transmute),
  %w(Reverb Compressor2 FilterEQ3 Redux2),
]

aMidiFxViews = [
  %w(MidiPitcher MidiVelocity MidiArpeggiator),
]

aInstrViews = [
  %w(UltraAnalog),
  %w(Collision),
  %w(Drift),
  %w(LoungeLizard),
  %w(InstrumentMeld),
  %w(Operator),
  %w(MultiSampler),
  %w(OriginalSimpler),
  %w(StringStudio),
  %w(InstrumentVector),
]

# rendering html *******************************************

puts('> Rendering html')

sScript = <<__FUN__
function on_view(pnGroup) {
  for (var i = 0; i < 14; i++) {
    var oEl = document.getElementById('group-' + i)
    oEl.style.display = (i == pnGroup) ? 'block' : 'none';
  }

  var oMainEl = document.getElementById('main-group')
  oMainEl.setAttribute('data-group', pnGroup)
}

function on_bank(pnGroup, pnBank) {
  for (var i = 0; i < 6; i++) {
    var oEl = document.getElementById('bank-' + pnGroup + '-' + i)
    if (oEl == null) continue;

    oEl.style.display = (i == pnBank) ? 'block' : 'none';
    if (i != pnBank) continue;

    var oHeaderEl = document.getElementById('header-group-' + pnGroup)
    var newHeader = oHeaderEl.innerText.replace(/ \\/ \\d+$/, ` / ${pnBank}`)
    oHeaderEl.innerHTML = newHeader
    oHeaderEl.setAttribute('data-bank', pnBank)

    var oFooterEl = document.getElementById('footer-group-' + pnGroup)
    oFooterEl.innerHTML = newHeader
  }
}

function on_bank_image() {
  var oMainEl = document.getElementById('main-group')
  var sGroup  = oMainEl.getAttribute('data-group')

  var oHeaderEl = document.getElementById('header-group-' + sGroup)
  var sBank     = oHeaderEl.getAttribute('data-bank')

  var oBankImgEl = document.getElementById(`bank-img-${sGroup}-${sBank}`)
  var sDisplay   = oBankImgEl.style.display
  oBankImgEl.style.display = (sDisplay == 'none') ? 'flex' : 'none';
}
__FUN__

aHtml = ['<html>'];
aHtml << '<head>';
aHtml << '<style>';
aHtml << 'body   {font-family: monospace; font-size: 12px; background-color: #333366}';
aHtml << 'table  {border-spacing: 0px}';
aHtml << 'td     {border-radius: 10px; font-weight: bold; font-size: 22px; height: 60px; width: 250px; border: solid 1px; text-align: center;}';
aHtml << 'button {border-radius: 10px; font-weight: bold; font-size: 22px; height: 60px; width: 130px;}';

aHtml << '.Effects               {background-color: #666666; color: white;}';
aHtml << '.Group-header          {background-color: #cccccc; height: 10px;}';
aHtml << '.Main-header           {background-color: #cccccc; height: 10px;}';
aHtml << '.header                {border: 0px; width: 200px}';

aHtml << '.device-on             {background-color: #6666cc !important; color: #ff8c00 !important;}';
aHtml << '.preset-save           {background-color: #db7093 !important; color: #ffcc00 !important;}';
aHtml << '.preset-prev           {background-color: #db7093 !important; color: #00ccff !important;}';
aHtml << '.preset-next           {background-color: #db7093 !important; color: #00ffcc !important;}';
aHtml << '.extra                 {                                      color: #ffffff !important; font-style: italic; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;}';
aHtml << '.dry-wet               {background-color: #99ff99 !important; color: #339933 !important; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 2px 0 #000, 1px 1px 0 #000;}';
aHtml << '.empty                 {background-color: #999999 !important; color: #ffffff !important;}';

aHtml << '.Vocoder               {background-color: #cc9999}';
aHtml << '.Overdrive             {background-color: #cc6666}';
aHtml << '.Eq8                   {background-color: #cc3333}';
aHtml << '.BeatRepeat            {background-color: #99cc99}';
aHtml << '.Resonator             {background-color: #33cc33}';
aHtml << '.AutoPan               {background-color: #ccccff}';
aHtml << '.Echo                  {background-color: #9999ff}';
aHtml << '.Delay                 {background-color: #cc9999}';
aHtml << '.FilterDelay           {background-color: #cc6666}';
aHtml << '.Chorus2               {background-color: #cc3333}';
aHtml << '.PhaserNew             {background-color: #99cc99}';
aHtml << '.Transmute             {background-color: #33cc33;}';
aHtml << '.Reverb                {background-color: #9999ff}';
aHtml << '.Compressor2           {background-color: #9999cc}';
aHtml << '.FilterEQ3             {background-color: #6666cc;}';
aHtml << '.Redux2                {background-color: #3333cc}';

aHtml << '.MidiPitcher           {background-color: #cc9999}';
aHtml << '.MidiVelocity          {background-color: #cc6666}';
aHtml << '.MidiArpeggiator       {background-color: #cc3333}';

aHtml << '.UltraAnalog           {background-color: #CE8179}';
aHtml << '.Collision             {background-color: #DCA382}';
aHtml << '.Drift                 {background-color: #D1C788}';
aHtml << '.LoungeLizard          {background-color: #8FB98C}';
aHtml << '.InstrumentMeld        {background-color: #869DB2}';
aHtml << '.Operator              {background-color: #A6829F}';
aHtml << '.MultiSampler          {background-color: #D499AB}';
aHtml << '.OriginalSimpler       {background-color: #E3C495}';
aHtml << '.StringStudio          {background-color: #E3E2C3}';
aHtml << '.InstrumentVector      {background-color: #A2C0A9}';
aHtml << '.InstrumentGroupDevice {background-color: #819BAF}';
aHtml << '.DrumGroupDevice       {background-color: #7C7098}';

aHtml << '.views                 {background-color: #3BA9E0;}';
aHtml << '.views-container       {#3BA9E0; height: 1000px; width: 1630px; overflow-y: scroll}';
aHtml << '.dev-image             {height: 250px;}';

aHtml << '.bank-image-container  {background-color: #333333; position: absolute; top: 130px; left: 5px; width: 2035px; height: 260px; display: flex; justify-content: center; align-items: center;}';
aHtml << '.bank-image            {height: 260px; max-width: 1270px;}';

aHtml << '</style>';
aHtml << '<script type="text/javascript">';
aHtml << sScript;
aHtml << '</script>';
aHtml << '</head>';
aHtml << '<body>';

# bank group buttons ***************************************
aMenu = ["<button class='Effects' onclick='on_view(0)' id='main-group' data-group='0'>EFFECTS</button>"];
nIdx = 1
hInstruments.each { |sInstrument, sDisplayName|
  aMenu << "<button class='#{sInstrument}' onclick='on_view(#{nIdx})'>#{sDisplayName}</button>"
  nIdx += 1
}
aMenu << "<button class='views' onclick='on_view(13)'>Views</button>";
aHtml << aMenu.join("\n");
aHtml << "<br/>";

def get_bank_image(pnGroup, pnBank, paViews, pnSpace)
  aDiv = ["<div id='bank-img-#{pnGroup}-#{pnBank}' class='bank-image-container' style='display: none;'>"]
  aDiv << "<div style='margin: 0 auto;'>"
  aDiv << paViews.collect { |sView|
    "<img src='#{sView}.png' class='bank-image'/>"
  }.join("\n<img width='#{pnSpace}px'/>\n")
  aDiv << '</div>'
  aDiv << '</div>'
  return aDiv.join("\n")
end

# effects group buttons ************************************
aHtml << "<div id='group-0' style='display: block'>";
aHtml << "<button class='Effects header' id='header-group-0' data-bank='0'>EFFECTS / 0</button>";
sBanks = hFxBanks.keys.collect { |nBank|
  "<button onclick='on_bank(0, #{nBank})'>BANK #{nBank}</button>"
}.join("\n")
sBanks += "\n<button class='views' onclick='on_bank_image()'>VIEWS</button>"
aHtml << sBanks;
hFxBanks.each { |nBank, hBank|
  sDisplay = (nBank == 0) ? 'block' : 'none';
  aHtml << "<div id='bank-0-#{nBank}' style='display: #{sDisplay}'>";
  aHtml << get_bank_image(0, nBank, aAudioFxViews[nBank], 100);
  hBank.each { |sType, hType|
    aHtml << '<table>';
    hType.each { |sCtrl, hCtrl|
      aHtml << "<tr>";
      aHtml << "<td colspan='8' class='#{sType}-header'></td>";
      aHtml << "</tr>";
      hCtrl.each { |sRow, aRow|
        aHtml << '<tr>';
        aRow.each { |sCell|
          if (sCell == nil)
            aHtml << '<td></td>';
          else
            aHtml << sCell;
          end
        }
        aHtml << '</tr>';
      }
    }
    aHtml << '</table>';
  }
  aHtml << '</div>';
}
aHtml << "<button class='Effects header' id='footer-group-0'>EFFECTS / 0</button>";
aHtml << sBanks;
aHtml << '</div>';

# instruments group buttons ********************************
nInst = 1;
hInsBanks.each { |sInstrument, aBanks|
  aHtml << "<div id='group-#{nInst}' style='display: none'>";
  aHtml << "<button class='#{sInstrument} header' id='header-group-#{nInst}' data-bank='0'>#{hInstruments[sInstrument]} / 0</button>";
  sBanks = Range.new(0, aBanks.length - 1).collect { |nIdx|
    "<button onclick='on_bank(#{nInst}, #{nIdx})'>BANK #{nIdx}</button>";
  }.join("\n")
  sBanks += "\n<button class='views' onclick='on_bank_image()'>VIEWS</button>"
  aHtml << sBanks;
  nBank = 0
  aBanks.each { |hBank|
    sDisplay = (nBank == 0) ? 'block' : 'none';
    aHtml << "<div id='bank-#{nInst}-#{nBank}' style='display: #{sDisplay}'>";
    aHtml << get_bank_image(nInst, nBank, aMidiFx + [sInstrument], 0);
    hBank.each { |sType, hType|
      aHtml << '<table>';
      hType.each { |sCtrl, hCtrl|
        aHtml << "<tr>";
        aHtml << "<td colspan='8' class='#{sType}-header'></td>";
        aHtml << "</tr>";
        hCtrl.each { |sRow, aRow|
          aHtml << '<tr>';
          aRow.each { |sCell|
            if (sCell == nil)
              aHtml << '<td></td>';
            else
              aHtml << sCell;
            end
          }
          aHtml << '</tr>';
        }
      }
      aHtml << '</table>';
    }
    nBank += 1;
    aHtml << '</div>';
  }
  aHtml << "<button class='#{sInstrument} header' id='footer-group-#{nInst}'>#{hInstruments[sInstrument]} / 0</button>";
  aHtml << sBanks;
  aHtml << '</div>';
  nInst += 1;
}

aHtml << "<div id='group-13' style='display: none'>";
aHtml << "<div class='views views-container'>"

aHtml << "<h1>Audio Effects (per bank)</h1>"
aAudioFxViews.each { |aRow|
  aRow.each { |sDev|
    aHtml << "<img class='dev-image' src='#{sDev}.png'/>"
  }
  aHtml << '<br/>'
}

aHtml << '<hr/>'
aHtml << "<h1>MIDI Effects (per bank)</h1>"
aMidiFxViews.each { |aRow|
  aRow.each { |sDev|
    aHtml << "<img class='dev-image' src='#{sDev}.png'/>"
  }
  aHtml << '<br/>'
}

aHtml << '<hr/>'
aHtml << "<h1>Instruments</h1>"
aInstrViews.each { |aRow|
  aRow.each { |sDev|
    aHtml << "<img class='dev-image' src='#{sDev}.png'/>"
  }
  aHtml << '<br/>'
}
aHtml << "</div>"
aHtml << '</div>';

# closing section ******************************************
aHtml << aMenu;
aHtml << '</body>';
aHtml << '</html>';

oFile = File.new("doc/banks.html", "wt");
oFile.puts(aHtml.join("\n"))

puts('> Done!')

