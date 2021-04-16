import json
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from urllib.request import urlopen

from apscheduler.schedulers.blocking import BlockingScheduler


def send_mail(message):
    """
    发送邮件
    :param message:
    :return:
    """
    # 连接发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    smtp.login('2160946606@qq.com', 'jkpzdgrrlgyseccd')
    # 编写HTML类型的邮件正文
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header('低价提醒', 'utf-8')
    smtp.sendmail('2160946606@qq.com', '957493412@qq.com', msg.as_string())
    smtp.quit()


def remind_one(lis):
    """
    如果当前价格达到最低则发送邮件提示投资者
    :param lis:
    :return:
    """
    grade_down_data(lis)
    temp_str = ''
    for i in lis:
        print(i['symbol'])
        temp_str += i['symbol'] + "    " + str(i['current_price']) + "\n"
    if len(lis) > 0:
        send_mail(temp_str)


def grade_down_data(cybermoney_list):
    """
    根据24小时的成交额对数据进行降序处理
    :param cybermoney_list:
    :return:
    """
    n = len(cybermoney_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if cybermoney_list[j]['total_volume'] < cybermoney_list[j + 1]['total_volume']:
                cybermoney_list[j], cybermoney_list[j + 1] = cybermoney_list[j + 1], cybermoney_list[j]


def data_processing(lis):
    """
    对数据进行处理
    :param lis:
    :return:
    """
    final_data = []
    for i in lis:
        if i['current_price'] < i['low_24h']:
            final_data.append(i)
    remind_one(final_data)


def get_price():
    """
    获取当前时间虚拟货币价格
    :return:
    """
    ss = int(round(time.time() * 1000))
    url = 'https://py.btc126.com/json/markets.json?t=' + str(ss)
    print(url)
    # 获取虚拟货币价格
    cybermoney_list = json.loads(urlopen(url).read().decode())
    # 按24小时的成交额进行排序
    grade_down_data(cybermoney_list)
    # 选取成交额最高的前50支
    excellent_list = cybermoney_list[:20]
    for i in excellent_list[::-1]:
        if i['symbol'] == 'usdt' or i['symbol'] == 'usdc' or i['symbol'] == 'busd' or i['symbol'] == 'dai' or i['symbol'] == 'husd':
            excellent_list.remove(i)
    for i in excellent_list:
        print(i['symbol'] + '    ' + str(i['price_change_percentage_24h']))
    # 进行判断
    data_processing(excellent_list)


def dojob():
    """
    定时任务,每900秒执行一次get_price()
    :return:
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(get_price, 'interval', seconds=300, id='test_job1')
    scheduler.start()


if __name__ == '__main__':
    get_price()
    dojob()
