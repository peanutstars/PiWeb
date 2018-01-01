#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import requests

try:
    from lib.psDebug import DBG, ERR
except:
    ERR = print
    DBG = print

# stock_info = '''({
#     shcode: '095700',
#     hname: '제넥신',
#     stype: '2',
#     price: {price: '46250', updown: 'up', mark: '▲'},
#     pchange: {price: '600', updown: 'up'},
#     pchgrate: {rate: '+1.31％', updown: 'up'},
#     askedPrice: {str: '호가', otPriceMsg: '0'},
#     totalvolume: {volume: '117568', rate: '118%'},
#     totalvalue: '5391',
#     timeInfo: {
#     date: '06.05', time: '', msg: '장종료'
#     },
#     chart: [{src: 'http://chart.finance.daum.net/time3/real/095700-290157.png?date=201706052245'},
#     {src: 'http://chart.finance.daum.net/candle3/095700-290157.png?date=201706052245'},
#     {src: 'http://chart.finance.daum.net/time3/3month/095700-290157.png?date=201706052245'},
#     {src: 'http://chart.finance.daum.net/time3/year/095700-290157.png?date=201706052245'},
#     {src: 'http://chart.finance.daum.net/time3/3year/095700-290157.png?date=201706052245'}],
#     preprice: '45650',
#     open: {price: '45650', updown: 'keep'},
#     high: {price: '46600', updown: 'up'},
#     low: {price: '45150', updown: 'down'},
#     highlimit: '59300',
#     lowlimit: '32000',
#     high52wk: '69200',
#     low52wk: '35300',
#     foreignRate: {rate: '3.87%', prerate: '-0.01%'},
#     mainstockvol: {volume: '8256', rank: '27'},
#     theme: {themecd: '352010', themename: '생물공학', fthemename: '생물공학', pchgrate: '+2.03%', updown: 'up'},
#     end: {}
# })'''


class CacaoStock:
    class Error(Exception):
        pass
    class StockItem:
        def __init__(self, code, name, price, updown, volume):
            self.code = code
            self.name = name
            self.price = int(price)
            self.vector = 1 if updown == 'up' else -1
            self.volume = int(volume)
        def toString(self):
            return '# %s %-13s %6d %3d %10d' % (self.code, self.name, self.price, self.vector, self.volume)

    @classmethod
    def query(cls, code):
        url = 'http://finance.daum.net/item/ajax/checkprice.daum?code=%s' % code
        data = None
        try:
            DBG('Request@%s' % url)
            r = requests.get(url, data=data)
        except requests.exceptions.ConnectionError as e:
            raise CacaoStock.Error('Connection Error : %s' % str(e))
        if r.status_code == 200:
            return r.text
        raise CacaoStock.Error('HTTP Error Code : %d' % r.status_code)

    @classmethod
    def getObject(cls, strJs):
        jstr = re.sub('([{,: ])(\w+)([},:])','\\1\"\\2\"\\3', strJs)
        # XXX Needs to check which is json or not.
        obj = eval(jstr)
        return CacaoStock.StockItem(obj['shcode'], obj['hname'],
                            obj['price']['price'], obj['price']['updown'],
                            obj['totalvolume']['volume'])

    @classmethod
    def getStock(cls, code):
        try:
            stock = CacaoStock.getObject(CacaoStock.query(code))
        except CacaoStock.Error as e:
            ERR('Query Error, %s' % str(e))
            return None
        # stock.toString()
        return stock


if __name__ == '__main__':
    for code in ['095700', '002390', '066570', '000660']:
        CacaoStock.getStock(code)
