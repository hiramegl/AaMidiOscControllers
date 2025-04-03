from AaTouch.Base import Base

class Patterns(Base):
  def __init__(self, phCfg, phObj):
    Base.__init__(self, phCfg, phObj)

    self.m_lUnav = [
      '          xx        xx          ',
      '          xxx      xxx          ',
      '           xxx    xxx           ',
      '            xxx  xxx            ',
      '             xxxxxx             ',
      '              xxxx              ',
      '              xxxx              ',
      '             xxxxxx             ',
      '            xxx  xxx            ',
      '           xxx    xxx           ',
      '          xxx      xxx          ',
      '          xx        xx          ',
    ]

    self.m_lAdd = [
      '               xx               ',
      '               xx               ',
      '               xx               ',
      '               xx               ',
      '               xx               ',
      '          xxxxxxxxxxxx          ',
      '          xxxxxxxxxxxx          ',
      '               xx               ',
      '               xx               ',
      '               xx               ',
      '               xx               ',
      '               xx               ',
    ]
    phObj['oPatt'] = self

  def send_pattern(self, psType, pnValue):
    if psType == 'unav':
      self.send_patt_bundle(self.m_lUnav, pnValue)
    elif psType == 'add':
      self.send_patt_bundle(self.m_lAdd, pnValue)

  def send_patt_bundle(self, plPattern, pnValue):
    sPatt = ''.join(plPattern)
    lBundle = []
    for nIdx, sChar in enumerate(sPatt):
      if sChar == ' ': continue
      nGridIdx = int(nIdx / 8) % 4
      nRowIdx  = int(nIdx / 32)
      nColIdx  = nIdx % 8
      nBitIdx  = nRowIdx * 8 + nColIdx
      lBundle.append([
        '/seq/grid/%d/%d' % (nGridIdx, nBitIdx),
        pnValue])
    self.send_bundle(lBundle)

