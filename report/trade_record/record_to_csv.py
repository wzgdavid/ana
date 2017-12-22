'''
把原始交易记录（shzq.html和zxjt.html）里的平仓记录的数据转成csv
'''
from lxml import etree
import pandas as pd

#with open('zxjt.html', 'r') as file:
with open('shzq.html', 'r') as file:
    html = file.read()


html = etree.HTML(html)
html = etree.ElementTree(html)

#print(html)

pc = html.xpath('//table[@id="tabOffset"]')[0] # 平仓记录的table
pc = etree.ElementTree(pc)
'''
每条交易有两条记录
 billclr1  是开仓
 billclr2  平仓
'''

billclr1s = pc.xpath('//tr[@class="billclr1"]')
billclr2s = pc.xpath('//tr[@class="billclr2"]')

rows = []
for b1, b2 in zip(billclr1s, billclr2s):
    b1 = etree.ElementTree(b1)
    b2 = etree.ElementTree(b2)
    # 交易所
    jys = b1.xpath('//td[1]/span/text()')[0]
    # 合约
    heyue = b1.xpath('//td[2]/span/text()')[0]
    #print(heyue)
    # 手数
    ss = b1.xpath('//td[3]/span/text()')[0]
    #print(ss)
    # 开仓日期
    date1 = b1.xpath('//td[4]/span/text()')[0]
    #print(date1)

    # 开仓方向
    td5 = b1.xpath('//td[5]/span/text()')
    buy = td5[0] if td5 else None
    td6 = b1.xpath('//td[6]/span/text()')
    sell = td6[0] if td6 else None
    # 开仓方向fx
    fx = 'buy' if buy else 'sell'
    # 开仓价格
    kcprice = buy if buy else sell
    

    # 平仓日期
    date2 = b2.xpath('//td[4]/span/text()')[0]

    td5 = b2.xpath('//td[5]/span/text()')
    buy = td5[0] if td5 else None
    td6 = b2.xpath('//td[6]/span/text()')
    sell = td6[0] if td6 else None
    # 平仓价格
    pcprice = buy if buy else sell
    # 平仓盈亏
    winloss = b2.xpath('//td[7]/span/text()')[0]

    row = jys,heyue,ss,date1,fx,kcprice,date2,pcprice,winloss
    rows.append(row)

columns = ['交易所','合约','手数','开仓日期','开仓方向','开仓价格','平仓日期','平仓价格','逐笔平仓盈亏']
data = pd.DataFrame(rows,columns=columns)
#data.to_csv('tracd_record.csv', mode='a')
