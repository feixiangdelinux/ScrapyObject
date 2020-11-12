import datetime
import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from urllib.request import urlopen

from apscheduler.schedulers.blocking import BlockingScheduler
from numpy import *


def sendmail(title, message):
    """
    发送邮件
    :param title:
    :param message:
    :return:
    """
    # 连接发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    smtp.login('957493412@qq.com', 'pdtsanllybzwbdgg')
    # 编写HTML类型的邮件正文
    msg = MIMEText('<html><h1>' + str(message) + '</h1><html>', 'html', 'utf-8')
    msg['Subject'] = Header(title, 'utf-8')
    smtp.sendmail('957493412@qq.com', '1421760774@qq.com', msg.as_string())
    smtp.quit()


def remindsix(currentprice, allprice):
    """
    和以前的100次价格中最低的价格进行比较如果比最低的价格还低就提醒
    :param currentprice:
    :param allprice:
    :return:
    """
    if currentprice <= min(allprice):
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        sendmail('当前价格最低', '当前价格:' + currentprice + '  最低价格:' + str(min(allPrice)) + '  最高价格:' + str(
            max(allPrice)) + '  平均价格:' + str(round(mean(allPrice), 2)) + '  ' + ts)


def saveprice(price):
    """
    保存当前价格
    :param price:
    :return:
    """
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    if len(allPrice) == 0:
        allPrice.append(float(price))
        print('当前价格' + price + '  ' + ts)
    else:
        print('当前价格:' + price + '  最低价格:' + str(min(allPrice)) + '  最高价格:' + str(max(allPrice)) + '  平均价格:' + str(
            round(mean(allPrice), 2)) + '  ' + ts)
        remindsix(float(price), allPrice)
        if len(allPrice) >= 100:
            allPrice.remove(0)
        allPrice.append(float(price))
    jsonstr = json.dumps(allPrice, ensure_ascii=False)
    with open("D:/BtcPrice.txt", "w") as f:
        f.write(jsonstr)


def func():
    url = 'https://api.coinbase.com/v2/prices/ETH-USD/buy'
    svalue = json.loads(urlopen(url).read().decode())
    saveprice(svalue['data']['amount'])


def dojob():
    scheduler = BlockingScheduler()
    scheduler.add_job(func, 'interval', seconds=900, id='test_job1')
    scheduler.start()


f = open('D:/BtcPrice.txt')
st = f.read()
allPrice = json.loads(st)
dojob()
