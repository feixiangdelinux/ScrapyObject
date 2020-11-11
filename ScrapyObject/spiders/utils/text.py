import datetime
import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from urllib.request import urlopen

from apscheduler.schedulers.blocking import BlockingScheduler


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
    # 发送消息
    if currentprice <= min(allprice):
        print('当前价格最低' + str(currentprice))
        sendmail('当前价格最低', currentprice)


def saveprice(price):
    """
    保存当前价格
    :param price:
    :return:
    """
    if len(allPrice) == 0:
        allPrice.append(float(price))
    else:
        remindsix(float(price), allPrice)
        if len(allPrice) >= 100:
            allPrice.remove(0)
        allPrice.append(float(price))
    jsonstr = json.dumps(allPrice, ensure_ascii=False)
    with open("D:/BtcPrice.txt", "w") as f:
        f.write(jsonstr)


def func():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print(ts)
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
